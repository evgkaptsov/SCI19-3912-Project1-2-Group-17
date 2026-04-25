# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 17:35:13 2026

@author: CCS
"""

import json
from FA import NFA


class FAFactory:
    @staticmethod
    def from_file(filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        Q = data["Q"]
        q0 = data["q0"]
        Sigma = data["Sigma"]
        F = data["F"]
        raw_delta = data["delta"]
        
        print(">>>>>>>> {Sigma}")

        # convert delta to a dict: (state, symbol) -> set(states)
        symbols = Sigma + ["eps"]
        delta = {}

        idx = 0
        for q in Q:
            for s in symbols:
                cell = raw_delta[idx]
                idx += 1

                # แก้กรณี "1," -> "1"
                states = set(x.strip(",") for x in cell if x)

                delta[(q, s)] = states

        return NFA(Q, q0, Sigma, F, delta)
    
    