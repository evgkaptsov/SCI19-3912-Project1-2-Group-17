# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 18:05:29 2026

@author: CCS
"""
import json
import string
from graphviz import Source


class DFA:
    def __init__(self, Q, q0, Sigma, F, delta):
        self.Q = Q                  # list of states
        self.q0 = q0                # start state
        self.Sigma = Sigma          # alphabet
        self.F = F                  # accepting states
        self.delta = delta          # transition table
        self.type = "DFA"

    def __repr__(self):
        def fmt_state(s):
            return "{" + ", ".join(sorted(s)) + "}"

        lines = []
        lines.append(f"{self.type}(")
        lines.append(f"  Q={{ {', '.join(fmt_state(s) for s in self.Q)} }},")
        lines.append(f"  q0={fmt_state(self.q0)},")
        lines.append(f"  Sigma={self.Sigma},")
        lines.append(f"  F={{ {', '.join(fmt_state(s) for s in self.F)} }},")
        lines.append("  delta={")

        for (state, a), target in self.delta.items():
            lines.append(f"    ({fmt_state(state)}, '{
                         a}') -> {fmt_state(target)}")

        lines.append("  }")
        lines.append(")")
        return "\n".join(lines)

    def save_to_dot(self, filename):

        # assign names: stateA, stateB, ...
        names = {}
        letters = list(string.ascii_uppercase)

        for i, q in enumerate(self.Q):
            if i < len(letters):
                names[q] = f"state{letters[i]}"
            else:
                names[q] = f"state{i}"   # fallback if many states

        with open(filename, "w", encoding="utf-8") as f:
            f.write("digraph DFA {\n")
            f.write("    rankdir=LR;\n")

            # accepting states
            f.write("    node [shape = doublecircle]; ")
            for q in self.F:
                f.write(f"{names[q]} ")
            f.write(";\n")

            # normal states
            f.write("    node [shape = circle];\n")

            # start arrow
            f.write("    start [shape=point];\n")
            f.write(f"    start -> {names[self.q0]};\n")

            # transitions
            for (q, a), t in self.delta.items():
                f.write(
                    f'    {names[q]} -> {names[t]} [label="{a}"];\n'
                )

            f.write("}\n")

    def render_dot_to_png(self, dot_file, output_file="output", view=False):
        src = Source.from_file(dot_file)
        src.render(output_file, format="png", view=view)

# for now we will use a code
# stub (draft) for a finite automata


class NFA(DFA):

    def __init__(self, Q, q0, Sigma, F, delta):
        super().__init__(Q, q0, Sigma, F, delta)
        self.type = "NFA"

    def find_all_paths(self, qq, a):
        result = set()
        for q in qq:
            result |= self.delta.get((q, a), set())
        return result

    def epsilon_closure_of_set(self, qq):
        EE = set()
        for q in qq:
            E = self.epsilon_closure(q)
            EE |= E      # union
        return EE

    def epsilon_closure(self, q):
        stack = [q]
        closure = {q}
        while stack:
            state = stack.pop()
            for nxt in self.delta.get((state, "eps"), set()):
                if nxt not in closure:
                    closure.add(nxt)
                    stack.append(nxt)
        return closure

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

    # def save_to_dot(self, filename):
    #     with open(filename, "w", encoding="utf-8") as f:
    #         f.write("digraph NFA {\n")
    #         f.write("    rankdir=LR;\n")

    #         # accepting states
    #         f.write("    node [shape = doublecircle]; ")
    #         for q in self.F:
    #             f.write(f"{q} ")
    #         f.write(";\n")

    #         # normal states
    #         f.write("    node [shape = circle];\n")

    #         # start arrow
    #         f.write(f"    start [shape=point];\n")
    #         f.write(f"    start -> {self.q0};\n")

    #         # transitions
    #         symbols = self.Sigma + ["eps"]
    #         for q in self.Q:
    #             for s in symbols:
    #                 targets = self.delta.get((q, s), set())
    #                 for t in targets:
    #                     label = "ε" if s == "eps" else s
    #                     f.write(f'    {q} -> {t} [label="{label}"];\n')

    #         f.write("}\n")
