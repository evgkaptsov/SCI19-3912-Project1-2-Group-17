# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 17:55:39 2026

@author: Group 17
"""

from NFA_to_DFA_coverter import NFA2DFAConverter
from FAFactory import FAFactory
from pathlib import Path



def main():
    
    fileName = "jsonNFA2"
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
    
    png_file_path = BASE_DIR / "data" / f"{fileName}.png"
    
    
    dfa.render_dot_to_png(dot_file_path, png_file_path, view=True)
    
    print("Done.")


if __name__ == "__main__":
    main()
