# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 17:55:39 2026

@author: Group 17
"""

from NFA_to_DFA_coverter import NFA2DFAConverter
from FAFactory import FAFactory
from pathlib import Path
from GraphLangGen import GraphLanguageGenerator


def NFA_test():
    fileName = "jsonNFA5"
    # your code here
    BASE_DIR = Path(__file__).resolve().parent.parent
    file_path = BASE_DIR / "data" / f"{fileName}.json"
    
    nfa = FAFactory.from_file(file_path)
    print(nfa)
    
    
    cvt = NFA2DFAConverter()
    dfa = cvt.convertNFA2DFA(nfa)
    print("Result:", dfa)
    
    dot_file_path = BASE_DIR / "data" / f"{fileName}.dot"
    dfa.save_to_dot(dot_file_path)
    
    png_file_path = BASE_DIR / "data" / f"{fileName}"
    
    dfa.render_dot_to_png(dot_file_path, png_file_path, view=False)
    
    
    graphLangGen = GraphLanguageGenerator(nfa)
    graphLang = graphLangGen.generate_graphs()
    graphLangGen.renderGraphAlphabet(graphLang, BASE_DIR / "data", fileName)
    
    input = "bcabbcabbccbcb"
    graphLangGen.renderGraphString(graphLang, input, BASE_DIR / "data" / f"{fileName}_{input}")
    
    
def TwoNFA_test():
    fileName = "json2NFA1"
    # your code here
    BASE_DIR = Path(__file__).resolve().parent.parent
    file_path = BASE_DIR / "data" / f"{fileName}.json"
    
    print("Loading", file_path)
    
    nfa2 = FAFactory.from_file_2way(file_path)
    print(nfa2)
    
    dot_file_path = BASE_DIR / "data" / f"{fileName}.dot"
    nfa2.save_to_dot(dot_file_path)
    
    png_file_path = BASE_DIR / "data" / f"{fileName}"
    
    nfa2.render_dot_to_png(dot_file_path, png_file_path, view=True)


def main():
    
    TwoNFA_test()
    
    print("Done.")


if __name__ == "__main__":
    main()
