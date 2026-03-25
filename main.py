# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 17:55:39 2026

@author: Group 17
"""

from NFA import NFA
from FAFactory import FAFactory
from pathlib import Path



def main():
    # your code here
    BASE_DIR = Path(__file__).resolve().parent
    file_path = BASE_DIR / "data" / "NFA01.json"
    
    nfa = FAFactory.from_file(file_path)
    print(nfa)
    
    file_path = BASE_DIR / "data" / "NFA01a.json"
    nfa.save_to_file(file_path)
    
    print("Done.")


if __name__ == "__main__":
    main()
