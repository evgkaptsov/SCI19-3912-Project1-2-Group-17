# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 17:55:39 2026

@author: Group 17
"""

from NFA_to_DFA_coverter import NFA2DFAConverter
from FAFactory import FAFactory
from pathlib import Path
from GraphLangGen import GraphLanguageGenerator



def main():
    
    fileName = "jsonNFA5"
    # your code here
    BASE_DIR = Path(__file__).resolve().parent
    file_path = BASE_DIR / "data" / f"{fileName}.json"
    
    nfa = FAFactory.from_file(file_path)
    print(nfa)
    
    
    cvt = NFA2DFAConverter()
    dfa = cvt.convertNFA2DFA(nfa)
    print("Result: ", dfa)
    
    dot_file_path = BASE_DIR / "data" / f"{fileName}.dot"
    dfa.save_to_dot(dot_file_path)
    
    png_file_path = BASE_DIR / "data" / f"{fileName}"
    graplang_png_file_path = BASE_DIR / "data" / f"{fileName}_graplang"
    
    
    dfa.render_dot_to_png(dot_file_path, png_file_path, view=False)
    
    
    graphLangGen = GraphLanguageGenerator()
    graphLang = graphLangGen.generate_graphs(nfa)
    graphLangGen.render_graph(graphLang, "c", graplang_png_file_path)
    print(f"Graph language description: {graphLang}")
    
    print("Done.")


if __name__ == "__main__":
    main()
