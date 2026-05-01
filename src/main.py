# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 17:55:39 2026

@author: Group 17
"""

from pathlib import Path
from NFA_to_DFA_coverter import NFA2DFAConverter
from FAFactory import FAFactory
from pathlib import Path
from GraphLangGen import NFAGraphLanguageGenerator
from GraphLangGen import TwoNFAGraphLanguageGenerator
from gui.AboutDialog import AboutDialog



import customtkinter
from tkinter import filedialog


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
    
    
    graphLangGen = NFAGraphLanguageGenerator(nfa)
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
    
    nfa2.render_dot_to_png(dot_file_path, png_file_path, view=False)
    
    graphLangGen = TwoNFAGraphLanguageGenerator(nfa2)
    graphLang = graphLangGen.generate_graphs()
    graphLangGen.renderGraphAlphabet(graphLang, BASE_DIR / "data", fileName)
    
    input = "abbbabb"
    graphLangGen.renderGraphString(graphLang, input, BASE_DIR / "data" / f"{fileName}_{input}")


def main():
    
    # TwoNFA_test()
    
    
    customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


    app = customtkinter.CTk()  # create CTk window like you do with the Tk window
    app.geometry("800x600")
    app.title("DNG Converter")
    
    def btn_convert_NFA_2_DFA():
        filename = filedialog.askopenfilename(
            title="Open JSON file", filetypes=[("JSON files", "*.json")]
        )
        
        if filename:
            print("Selected:", filename)
            nfa2 = FAFactory.from_file_2way(filename)
            print(nfa2)
        else:
            print("Cancelled")
    
            
    def btn_gen_alphabet_1NFA():
        filename = filedialog.askopenfilename(
            title="Open JSON file", filetypes=[("JSON files", "*.json")]
        )
        
        if filename:
            print("Selected:", filename)
            print("Generating alphabet for 1NFA...")
            nfa2 = FAFactory.from_file_2way(filename)
            graphLangGen = TwoNFAGraphLanguageGenerator(nfa2)
            graphLang = graphLangGen.generate_graphs()
            p = Path(filename)
            graphLangGen.renderGraphAlphabet(
                graphLang, 
                p.parent, 
                p.name
            )
            
            
            print(nfa2)
        else:
            print("Cancelled")
        
    def btn_about():
        AboutDialog(app)
    
    
    # Use instead of tkinter Button
    button01 = customtkinter.CTkButton(master=app, text="NFA to DFA", command=btn_convert_NFA_2_DFA)
    button01.place(relx=0.5, rely=0.25, anchor=customtkinter.CENTER)
    
    button02 = customtkinter.CTkButton(master=app, text="Alphabet for 1NFA", command=btn_gen_alphabet_1NFA)
    button02.place(relx=0.5, rely=0.35, anchor=customtkinter.CENTER)
    
    buttonAbout = customtkinter.CTkButton(master=app, text="About", command=btn_about)
    buttonAbout.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
    
    app.mainloop()    
    
    
    print("Done.")


if __name__ == "__main__":
    main()
