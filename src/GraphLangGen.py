# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 17:14:24 2026

@author: 
    Group 17, 3/2568, Project 1/2
    Natthira Sannok,  Suwannee Pitram, Warisara Promwicharn;
    Project Advisor: Dr. Evgenii Kaptsov,
    Suranaree University of Technology
"""

from pathlib import Path


from graphviz import Digraph, Source
from collections import defaultdict, deque


class NFAGraphLanguageGenerator:

    START_SYMBOL = "start"
    FINAL_SYMBOL = "final"

    def __init__(self, nfa):
        self.nfa = nfa

    def getExtendedAlphabet(self):
        return [
            NFAGraphLanguageGenerator.START_SYMBOL,
            *self.nfa.Sigma,
            NFAGraphLanguageGenerator.FINAL_SYMBOL
        ]

    def renderGraphAlphabet(self, graphLang, path, baseFileName):
        for s in self.getExtendedAlphabet():
            graplang_png_file_path = Path(path) / (f"{baseFileName}_graphlang_" + s)
            self.render_graph(graphLang, s, graplang_png_file_path)

    def renderGraphString(self, graphLang, s, fileName, view=True):
        # --- validate ---
        for c in s:
            if c not in self.nfa.Sigma:
                raise ValueError(f"Symbol '{c}' not in alphabet {self.nfa.Sigma}")
    
        # --- sequence ---
        sequence = [(NFAGraphLanguageGenerator.START_SYMBOL, graphLang[NFAGraphLanguageGenerator.START_SYMBOL])]
        sequence += [(c, graphLang[c]) for c in s]
        sequence.append((NFAGraphLanguageGenerator.FINAL_SYMBOL, graphLang[NFAGraphLanguageGenerator.FINAL_SYMBOL]))
    
        merged = {"nodes": {}, "edges": []}
    
        states = list(self.nfa.Q)
        n = len(states)
    
        # --- geometry ---
        dx = 1.25
        h = 1.0
        label_y = 0.5
    
        y_pos = {str(i+1): -i * h for i in range(n)}
    
        node_map_prev = {}
        counter = 0
        x_offset = 0.0
    
        leftmost_nodes = set()
        rightmost_nodes = set()
    
        # --- build graph ---
        for block_idx, (sym, g) in enumerate(sequence):
            node_map_curr = {}
    
            # label
            label_node = f"label_{counter}"
            counter += 1
            merged["nodes"][label_node] = {
                "label": sym,
                "pos": f"{x_offset + dx/2},{label_y}!",
                "shape": "none"
            }
    
            for i in range(1, n+1):
                key = str(i)
    
                # LEFT
                if key in node_map_prev:
                    node_map_curr[f"l{i}"] = node_map_prev[key]
                else:
                    nid = f"n{counter}"
                    counter += 1
                    node_map_curr[f"l{i}"] = nid
                    merged["nodes"][nid] = {
                        "label": key,
                        "pos": f"{x_offset},{y_pos[key]}!",
                        "shape": "circle"
                    }
                    if block_idx == 0:
                        leftmost_nodes.add(nid)
    
                # RIGHT
                nid = f"n{counter}"
                counter += 1
                node_map_curr[f"R{i}"] = nid
                merged["nodes"][nid] = {
                    "label": key,
                    "pos": f"{x_offset + dx},{y_pos[key]}!",
                    "shape": "circle"
                }
    
                if block_idx == len(sequence) - 1:
                    rightmost_nodes.add(nid)
    
            # edges
            for src, dst, attrs in g["edges"]:
                merged["edges"].append((
                    node_map_curr[src],
                    node_map_curr[dst],
                    attrs
                ))
    
            # glue
            node_map_prev = {
                str(i): node_map_curr[f"R{i}"]
                for i in range(1, n+1)
            }
    
            x_offset += dx
    
        # -------- ALL PATHS DETECTION --------
        adj = defaultdict(list)
        rev_adj = defaultdict(list)
    
        for src, dst, _ in merged["edges"]:
            adj[src].append(dst)
            rev_adj[dst].append(src)
    
        # reachable from leftmost
        reachable = set(leftmost_nodes)
        queue = deque(leftmost_nodes)
    
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if v not in reachable:
                    reachable.add(v)
                    queue.append(v)
    
        # can reach rightmost
        can_reach = set(rightmost_nodes)
        queue = deque(rightmost_nodes)
    
        while queue:
            u = queue.popleft()
            for v in rev_adj[u]:
                if v not in can_reach:
                    can_reach.add(v)
                    queue.append(v)
    
        # edges on valid paths
        path_edges = set()
        for src, dst, _ in merged["edges"]:
            if src in reachable and dst in can_reach:
                path_edges.add((src, dst))
    
        # -------- DOT --------
        lines = []
        lines.append("digraph G {")
        lines.append("    graph [layout=neato];")
        lines.append("    node [shape=circle];")
    
        for nid, attrs in merged["nodes"].items():
            lines.append(
                f'    {nid} [label="{attrs["label"]}", pos="{attrs["pos"]}", shape={attrs["shape"]}];'
            )
    
        for src, dst, attrs in merged["edges"]:
            label = attrs.get("label", "")
    
            if (src, dst) in path_edges:
                lines.append(
                    f'    {src} -> {dst} [label="{label}", penwidth=3, style=solid];'
                )
            else:
                lines.append(
                    f'    {src} -> {dst} [label="{label}", style=dashed];'
                )
    
        lines.append("}")
    
        Source("\n".join(lines)).render(fileName, format="png", view=view)
    

    def generate_graphs(self):
        """
        Generate graph descriptions for each symbol in the alphabet.
        """
        G = {}

        h = 1.0
        x_left = 0.0
        x_right = 2.0

        # n = len(nfa.Q)
        nfa = self.nfa
        states = list(nfa.Q)

        # helper to create empty graph with nodes
        def create_base_graph():
            graph = {"nodes": {}, "edges": []}

            for i, q in enumerate(states, start=1):
                y = -h * (i - 1)

                l_i = f"l{i}"
                r_i = f"R{i}"

                graph["nodes"][l_i] = {
                    "label": l_i,
                    "pos": f"{x_left},{y}!",
                    "shape": "circle"
                }

                graph["nodes"][r_i] = {
                    "label": r_i,
                    "pos": f"{x_right},{y}!",
                    "shape": "circle"
                }

            return graph

        # graphs for symbols
        for s in nfa.Sigma:
            graph = create_base_graph()

            for (q_i, sym), targets in nfa.delta.items():
                if sym != s:
                    continue

                i = states.index(q_i) + 1
                for q_j in targets:
                    j = states.index(q_j) + 1

                    src = f"l{i}"
                    dst = f"R{j}"

                    graph["edges"].append((src, dst, {"label": ""}))

            G[s] = graph

        # --- start graph ---
        graph_start = create_base_graph()

        k = states.index(nfa.q0) + 1
        graph_start["edges"].append((f"l{k}", f"R{k}", {"label": ""}))

        G[NFAGraphLanguageGenerator.START_SYMBOL] = graph_start

        # --- final graph ---
        graph_final = create_base_graph()

        for q in nfa.F:
            k = states.index(q) + 1
            graph_final["edges"].append((f"l{k}", f"R{k}", {"label": ""}))

        G[NFAGraphLanguageGenerator.FINAL_SYMBOL] = graph_final

        return G

    def render_graph(self, G, symbol, filename):
        """
        Render the graph corresponding to a given symbol to a file.
        """
        data = G[symbol]

        dot = Digraph(engine="neato")  # neato respects positions
        dot.attr(overlap="false")

        # Add nodes
        for node_id, attrs in data["nodes"].items():
            dot.node(node_id, **attrs)

        # Add edges
        for src, dst, attrs in data["edges"]:
            dot.edge(src, dst, **attrs)

        # Save and render
        dot.render(filename, format="png", cleanup=True)






#########################################


class TwoNFAGraphLanguageGenerator:

    LEFT_END = "LEnd"
    RIGHT_END = "REnd"

    def __init__(self, nfa):
        self.nfa = nfa

    def getExtendedAlphabet(self):
        return [
            TwoNFAGraphLanguageGenerator.LEFT_END,
            *self.nfa.Sigma,
            TwoNFAGraphLanguageGenerator.RIGHT_END
        ]
    
    def renderGraphAlphabet(self, graphLang, path, baseFileName):
        for s in self.getExtendedAlphabet():
            file_path = Path(path) / f"{baseFileName}_graphlang_{s}"
            self.render_graph(graphLang, s, file_path)
            
    def render_graph(self, G, symbol, filename):
        data = G[symbol]
    
        dot = Digraph(engine="neato")
        dot.attr(overlap="false")
    
        # nodes
        for node_id, attrs in data["nodes"].items():
            dot.node(node_id, **attrs)
    
        # edges
        for src, dst, attrs in data["edges"]:
            dot.edge(src, dst, **attrs)
    
        dot.render(filename, format="png", cleanup=True)

    # --------------------------------------------------
    # GRAPH GENERATION (Sipser–Sakoda correct version)
    # --------------------------------------------------

    def generate_graphs(self):
        G = {}

        nfa = self.nfa
        states = list(nfa.Q)
        #n = len(states)

        h = 1.0
        x_left = 0.0
        x_right = 2.0

        # --- helper ---
        def create_base_graph():
            graph = {"nodes": {}, "edges": []}
            
            # total rows = 2n
            # first n rows: l1..ln / R1..Rn
            # next n rows: L1..Ln / r1..rn
            
            for i in range(1, len(states) + 1):
                # --- upper half (l_i and R_i) ---
                y_top = -h * (i - 1)
            
                graph["nodes"][f"l{i}"] = {
                    "label": f"l{i}",
                    "pos": f"{x_left},{y_top}!",
                    "shape": "circle"
                }
            
                graph["nodes"][f"R{i}"] = {
                    "label": f"R{i}",
                    "pos": f"{x_right},{y_top}!",
                    "shape": "circle"
                }
            
            for i in range(1, len(states) + 1):
                # --- lower half (L_i and r_i) ---
                y_bottom = -h * (len(states) + i - 1)
            
                graph["nodes"][f"L{i}"] = {
                    "label": f"L{i}",
                    "pos": f"{x_left},{y_bottom}!",
                    "shape": "circle"
                }
            
                graph["nodes"][f"r{i}"] = {
                    "label": f"r{i}",
                    "pos": f"{x_right},{y_bottom}!",
                    "shape": "circle"
                }
            
            return graph

        # --------------------------------------------------
        # SYMBOL GRAPHS (a ∈ Σ)
        # --------------------------------------------------
        for a in nfa.Sigma:
            graph = create_base_graph()

            for (q_i, sym), targets in nfa.delta.items():
                if sym != a:
                    continue

                i = states.index(q_i) + 1

                for (q_j, d) in targets:
                    j = states.index(q_j) + 1

                    if d == "R":
                        # l_i -> R_j and L_i -> R_j
                        graph["edges"].append((f"l{i}", f"R{j}", {"label": ""}))
                        graph["edges"].append((f"L{i}", f"R{j}", {"label": ""}))

                    elif d == "L":
                        # l_i -> L_j and r_i -> L_j
                        graph["edges"].append((f"l{i}", f"L{j}", {"label": ""}))
                        graph["edges"].append((f"r{i}", f"L{j}", {"label": ""}))

            G[a] = graph

        # --------------------------------------------------
        # LEFT ENDMARKER
        # --------------------------------------------------
        graph_left = create_base_graph()

        for (q_i, sym), targets in nfa.delta.items():
            if sym != self.LEFT_END:
                continue

            i = states.index(q_i) + 1

            for (q_j, d) in targets:
                if d == "R":
                    j = states.index(q_j) + 1
                    # r_i -> R_j
                    graph_left["edges"].append((f"r{i}", f"R{j}", {"label": ""}))

        # initial states: l_i -> R_i
        for q in [nfa.q0]:   # single initial state assumed
            i = states.index(q) + 1
            graph_left["edges"].append((f"l{i}", f"R{i}", {"label": ""}))

        G[self.LEFT_END] = graph_left

        # --------------------------------------------------
        # RIGHT ENDMARKER
        # --------------------------------------------------
        graph_right = create_base_graph()

        for (q_i, sym), targets in nfa.delta.items():
            if sym != self.RIGHT_END:
                continue

            i = states.index(q_i) + 1

            for (q_j, d) in targets:
                if d == "L":
                    j = states.index(q_j) + 1
                    # l_i -> L_j
                    graph_right["edges"].append((f"l{i}", f"L{j}", {"label": ""}))

        # final states: l_i -> R_i
        for q in nfa.F:
            i = states.index(q) + 1
            graph_right["edges"].append((f"l{i}", f"R{i}", {"label": ""}))

        G[self.RIGHT_END] = graph_right

        return G
    
    def renderGraphString(self, graphLang, s, fileName, view=True):
        # --- validate ---
        for c in s:
            if c not in self.nfa.Sigma:
                raise ValueError(f"Symbol '{c}' not in alphabet {self.nfa.Sigma}")
    
        # --- sequence ---
        sequence = [(self.LEFT_END, graphLang[self.LEFT_END])]
        sequence += [(c, graphLang[c]) for c in s]
        sequence.append((self.RIGHT_END, graphLang[self.RIGHT_END]))
    
        merged = {"nodes": {}, "edges": []}
    
        states = list(self.nfa.Q)
        n = len(states)
    
        dx = 1.5
        h = 1.0
        label_y = 1.0
    
        counter = 0
        x_offset = 0.0
    
        # previous block right boundary
        node_map_prev = {}
    
        leftmost_nodes = set()
        rightmost_nodes = set()
    
        for block_idx, (sym, g) in enumerate(sequence):
            node_map_curr = {}
    
            # --- label ---
            lid = f"label_{counter}"
            counter += 1
            merged["nodes"][lid] = {
                "label": sym,
                "pos": f"{x_offset + dx/2},{label_y}!",
                "shape": "none"
            }
    
            # --- create nodes ---
            for i in range(1, n + 1):
    
                # --- TOP HALF ---
                y_top = -h * (i - 1)
    
                # l_i
                if ("l", i) in node_map_prev:
                    node_map_curr[f"l{i}"] = node_map_prev[("l", i)]
                else:
                    nid = f"n{counter}"; counter += 1
                    node_map_curr[f"l{i}"] = nid
                    merged["nodes"][nid] = {
                        "label": f"l{i}",
                        "pos": f"{x_offset},{y_top}!",
                        "shape": "circle"
                    }
                    if block_idx == 0:
                        leftmost_nodes.add(nid)
    
                # R_i
                nid = f"n{counter}"; counter += 1
                node_map_curr[f"R{i}"] = nid
                merged["nodes"][nid] = {
                    "label": f"R{i}",
                    "pos": f"{x_offset + dx},{y_top}!",
                    "shape": "circle"
                }
    
                if block_idx == len(sequence) - 1:
                    rightmost_nodes.add(nid)
    
            # --- BOTTOM HALF ---
            for i in range(1, n + 1):
                y_bot = -h * (n + i - 1)
    
                # L_i
                if ("L", i) in node_map_prev:
                    node_map_curr[f"L{i}"] = node_map_prev[("L", i)]
                else:
                    nid = f"n{counter}"; counter += 1
                    node_map_curr[f"L{i}"] = nid
                    merged["nodes"][nid] = {
                        "label": f"L{i}",
                        "pos": f"{x_offset},{y_bot}!",
                        "shape": "circle"
                    }
                    if block_idx == 0:
                        leftmost_nodes.add(nid)
    
                # r_i
                nid = f"n{counter}"; counter += 1
                node_map_curr[f"r{i}"] = nid
                merged["nodes"][nid] = {
                    "label": f"r{i}",
                    "pos": f"{x_offset + dx},{y_bot}!",
                    "shape": "circle"
                }
    
                if block_idx == len(sequence) - 1:
                    rightmost_nodes.add(nid)
    
            # --- edges ---
            for src, dst, attrs in g["edges"]:
                merged["edges"].append((
                    node_map_curr[src],
                    node_map_curr[dst],
                    attrs
                ))
    
            # --- GLUING ---
            node_map_prev = {}
    
            for i in range(1, n + 1):
                # R_i → l_i
                node_map_prev[("l", i)] = node_map_curr[f"R{i}"]
    
                # r_i → L_i
                node_map_prev[("L", i)] = node_map_curr[f"r{i}"]
    
            x_offset += dx
    
        # -------- PATH DETECTION --------
        from collections import defaultdict, deque
    
        adj = defaultdict(list)
        rev_adj = defaultdict(list)
    
        for src, dst, _ in merged["edges"]:
            adj[src].append(dst)
            rev_adj[dst].append(src)
    
        reachable = set(leftmost_nodes)
        queue = deque(leftmost_nodes)
    
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if v not in reachable:
                    reachable.add(v)
                    queue.append(v)
    
        can_reach = set(rightmost_nodes)
        queue = deque(rightmost_nodes)
    
        while queue:
            u = queue.popleft()
            for v in rev_adj[u]:
                if v not in can_reach:
                    can_reach.add(v)
                    queue.append(v)
    
        path_edges = set()
        for src, dst, _ in merged["edges"]:
            if src in reachable and dst in can_reach:
                path_edges.add((src, dst))
    
        # -------- DOT --------
        lines = []
        lines.append("digraph G {")
        lines.append("    graph [layout=neato];")
        lines.append("    node [shape=circle];")
    
        for nid, attrs in merged["nodes"].items():
            lines.append(
                f'    {nid} [label="{attrs["label"]}", pos="{attrs["pos"]}", shape={attrs["shape"]}];'
            )
    
        for src, dst, attrs in merged["edges"]:
            if (src, dst) in path_edges:
                lines.append(f'    {src} -> {dst} [penwidth=3];')
            else:
                lines.append(f'    {src} -> {dst} [style=dashed];')
    
        lines.append("}")
    
        Source("\n".join(lines)).render(fileName, format="png", view=view)