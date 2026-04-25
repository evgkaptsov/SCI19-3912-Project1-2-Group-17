# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 17:14:24 2026

@author: CCS
"""

from graphviz import Digraph, Source
from collections import defaultdict, deque


class GraphLanguageGenerator:

    START_SYMBOL = "start"
    FINAL_SYMBOL = "final"

    def __init__(self, nfa):
        self.nfa = nfa

    def getExtendedAlphabet(self):
        return [
            GraphLanguageGenerator.START_SYMBOL,
            *self.nfa.Sigma,
            GraphLanguageGenerator.FINAL_SYMBOL
        ]

    def renderGraphAlphabet(self, graphLang, path, baseFileName):
        for s in self.getExtendedAlphabet():
            graplang_png_file_path = path / (f"{baseFileName}_graplang_" + s)
            self.render_graph(graphLang, s, graplang_png_file_path)


    def renderGraphString(self, graphLang, s, fileName, view=True):
        # --- validate ---
        for c in s:
            if c not in self.nfa.Sigma:
                raise ValueError(f"Symbol '{c}' not in alphabet {self.nfa.Sigma}")
    
        sequence = [(GraphLanguageGenerator.START_SYMBOL, graphLang[GraphLanguageGenerator.START_SYMBOL])]
        sequence += [(c, graphLang[c]) for c in s]
        sequence.append((GraphLanguageGenerator.FINAL_SYMBOL, graphLang[GraphLanguageGenerator.FINAL_SYMBOL]))
    
        merged = {"nodes": {}, "edges": []}
    
        states = list(self.nfa.Q)
        n = len(states)
    
        dx = 1.25
        h = 1.0
        label_y = 0.5
    
        y_pos = {str(i+1): -i * h for i in range(n)}
    
        node_map_prev = {}
        counter = 0
        x_offset = 0.0
    
        leftmost_nodes = set()
        rightmost_nodes = set()
    
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
    
            node_map_prev = {
                str(i): node_map_curr[f"R{i}"]
                for i in range(1, n+1)
            }
    
            x_offset += dx
    
        # -------- PATH SEARCH --------
        adj = defaultdict(list)
        for src, dst, _ in merged["edges"]:
            adj[src].append(dst)
    
        parent = {}
        found_target = None
    
        queue = deque(leftmost_nodes)
        visited = set(leftmost_nodes)
    
        while queue:
            u = queue.popleft()
            if u in rightmost_nodes:
                found_target = u
                break
            for v in adj[u]:
                if v not in visited:
                    visited.add(v)
                    parent[v] = u
                    queue.append(v)
    
        path_edges = set()
        if found_target is not None:
            v = found_target
            while v in parent:
                u = parent[v]
                path_edges.add((u, v))
                v = u
    
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

        G[GraphLanguageGenerator.START_SYMBOL] = graph_start

        # --- final graph ---
        graph_final = create_base_graph()

        for q in nfa.F:
            k = states.index(q) + 1
            graph_final["edges"].append((f"l{k}", f"R{k}", {"label": ""}))

        G[GraphLanguageGenerator.FINAL_SYMBOL] = graph_final

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
