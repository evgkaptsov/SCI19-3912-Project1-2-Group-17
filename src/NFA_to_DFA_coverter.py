# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 14:50:28 2026

@author: CCS
"""

from FA import DFA


class NFA2DFAConverter:

    def find_new_set(self, nfa, qq, a):
        paths = nfa.find_all_paths(qq, a)
        state_DFA = nfa.epsilon_closure_of_set(paths)
        return frozenset(state_DFA)


    def all_paths(self, nfa, states_DFA, delta):
        stack = list(states_DFA)

        while stack:
            qq = stack.pop()   # frozenset

            for a in nfa.Sigma:
                q_DFA = self.find_new_set(nfa, qq, a)

                # record transition
                delta[(qq, a)] = q_DFA

                if q_DFA not in states_DFA:
                    states_DFA.add(q_DFA)
                    stack.append(q_DFA)

        return states_DFA


    def find_accept_states(self, Q_DFA, F_NFA):
        return {q for q in Q_DFA if any(x in F_NFA for x in q)}


    def convertNFA2DFA(self, nfa):
        states_DFA = set()
        delta = {}

        q0_DFA = frozenset(nfa.epsilon_closure(nfa.q0))
        states_DFA.add(q0_DFA)

        states_DFA = self.all_paths(nfa, states_DFA, delta)

        Q = states_DFA
        q0 = q0_DFA
        Sigma = nfa.Sigma
        F = self.find_accept_states(Q, nfa.F)

        return DFA(Q, q0, Sigma, F, delta)
    
