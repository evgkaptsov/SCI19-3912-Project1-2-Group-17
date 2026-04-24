# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 17:14:24 2026

@author: CCS
"""

from graphviz import Digraph

class GraphLanguageGenerator:

    def __init__(self):
        pass


    def generate_graphs(self, nfa):
        """
        Generate graph descriptions for each symbol in the alphabet.
        Each graph is represented as a dictionary with nodes and edges,
        suitable for rendering with Graphviz.
        """
        G = {}
    
        h = 1.0  # vertical spacing
        x_left = 0.0
        x_right = 2.0  # horizontal offset
    
        n = len(nfa.Q)
        states = list(nfa.Q)
    
        for s in nfa.Sigma:
            graph = {
                "nodes": {},   # node_id -> attributes
                "edges": []    # list of (src, dst, attributes)
            }
    
            # Create nodes
            for i, q in enumerate(states, start=1):
                y = -h * (i - 1)
    
                l_i = f"l{i}"
                r_i = f"R{i}"
    
                # Left nodes
                graph["nodes"][l_i] = {
                    "label": l_i,
                    "pos": f"{x_left},{y}!",
                    "shape": "circle"
                }
    
                # Right nodes
                graph["nodes"][r_i] = {
                    "label": r_i,
                    "pos": f"{x_right},{y}!",
                    "shape": "circle"
                }
    
            # Create edges
            for (q_i, sym), targets in nfa.delta.items():
                if sym != s:
                    continue
    
                i = states.index(q_i) + 1
                for q_j in targets:
                    j = states.index(q_j) + 1
    
                    src = f"l{i}"
                    dst = f"R{j}"
    
                    graph["edges"].append((src, dst, {"label": "" }))
                    

    
            G[s] = graph
    
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
