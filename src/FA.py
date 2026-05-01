# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 18:05:29 2026

@author: 
    Group 17, 3/2568, Project 1/2
    Natthira Sannok,  Suwannee Pitram, Warisara Promwicharn;
    Project Advisor: Dr. Evgenii Kaptsov,
    Suranaree University of Technology
"""
import json
import string
from collections import defaultdict
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

        print("Saving to dot-file:", filename)
        
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

    def render_dot_to_png(self, dot_file_path, output_file="output", view=False):
        print("Loading description from dot-file:", dot_file_path)
        src = Source.from_file(dot_file_path)
        src.render(output_file, format="png", view=view)




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





class TwoWayNFA(NFA):

    def __init__(self, Q, q0, Sigma, F, delta):
        """
        delta[(q, a)] = set of (p, dir) where dir ∈ {"L", "R"}
        """
        super().__init__(Q, q0, Sigma, F, delta)
        self.type = "TwoNFA"

        # extend alphabet with markers
        self.left_marker = "⊢"
        self.right_marker = "⊣"
        self.Sigma_ext = [self.left_marker] + Sigma + [self.right_marker]

    # WARNING: this method wansn't tested properly!
    def find_all_paths(self, qq, a):
        """
        Return set of (state, direction)
        """
        result = set()
        for q in qq:
            result |= self.delta.get((q, a), set())
        return result

    # WARNING: this method wansn't tested properly!
    def move(self, qq, a, position, length):
        """
        Perform one 2-way move from a set of states.

        position: current head position
        length: length of input (including markers)

        Returns:
            set of (next_state, next_position)
        """
        result = set()

        for q in qq:
            for (p, d) in self.delta.get((q, a), set()):
                if d == "R":
                    new_pos = position + 1
                elif d == "L":
                    new_pos = position - 1
                else:
                    continue

                # boundary check
                if 0 <= new_pos < length:
                    result.add((p, new_pos))

        return result

    def __repr__(self):
        lines = []
        lines.append("TwoNFA(")
        lines.append(f"  Q={self.Q},")
        lines.append(f"  q0={self.q0},")
        lines.append(f"  Sigma={self.Sigma},")
        lines.append(f"  Sigma_ext={self.Sigma_ext},")
        lines.append(f"  F={self.F},")
        lines.append("  delta={")

        for (q, a), targets in self.delta.items():
            for (p, d) in targets:
                lines.append(f"    ({q}, '{a}') -> ({p}, {d})")

        lines.append("  }")
        lines.append(")")
        return "\n".join(lines)
    

    def save_to_dot(self, filename):
        # marker replacement (Graphviz-safe)
        symbol_map = {
            "⊢": "|-",
            "⊣": "-|"
        }
    
        # assign readable names
        names = {}
        letters = list(string.ascii_uppercase)
    
        for i, q in enumerate(self.Q):
            if i < len(letters):
                names[q] = f"{letters[i]}"
            else:
                names[q] = f"{i}"
    
        print("Saving to dot-file:", filename)
    
        # --- group transitions ---
        grouped = defaultdict(list)
    
        for (q, a), targets in self.delta.items():
            a_print = symbol_map.get(a, a)
    
            for (p, d) in targets:
                label = f"{a_print},{d}"
                grouped[(q, p)].append(label)
    
        with open(filename, "w", encoding="utf-8") as f:
            f.write("digraph TwoNFA {\n")
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
    
            # --- merged transitions ---
            for (q, p), labels in grouped.items():
                labels = sorted(set(labels))   # remove duplicates + stable order
    
                # vertical layout (top → bottom)
                label_str = "\\n".join(labels)
    
                f.write(
                    f'    {names[q]} -> {names[p]} [label="{label_str}"];\n'
                )
    
            f.write("}\n")