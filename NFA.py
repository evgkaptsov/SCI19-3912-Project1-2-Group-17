# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 18:05:29 2026

@author: CCS
"""
import json

# for now we will use a code 
# stub (draft) for a finite automata

class NFA:
    def __init__(self, Q, q0, Sigma, F, delta):
        self.Q = Q                  # list of states
        self.q0 = q0                # start state
        self.Sigma = Sigma          # alphabet
        self.F = F                  # accepting states
        self.delta = delta          # transition table

    def __repr__(self):
        return (f"NFA(Q={self.Q}, q0={self.q0}, "
                f"Sigma={self.Sigma}, F={self.F})")
    
    def save_to_file(self, filename):
        symbols = self.Sigma + ["eps"]
        raw_delta = []

        for q in self.Q:
            for s in symbols:
                states = self.delta.get((q, s), set())
                raw_delta.append(list(states))

        data = {
            "Q": self.Q,
            "q0": self.q0,
            "Sigma": self.Sigma,
            "F": self.F,
            "delta": raw_delta
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)



