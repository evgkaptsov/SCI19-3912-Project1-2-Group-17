# -*- coding: utf-8 -*-
"""
Created on Fri May  1 16:28:44 2026

@author: CCS
"""

import os
import sys

import customtkinter as ctk
from tkinter import filedialog
import traceback

from gui.AboutDialog import AboutDialog
from gui.ABCInputDialog import ABCInputDialog

from FAFactory import FAFactory
from GraphLangGen import NFAGraphLanguageGenerator
from GraphLangGen import TwoNFAGraphLanguageGenerator
from NFA_to_DFA_coverter import NFA2DFAConverter


def remove_json_ext(filename):
    return filename[:-5]



def global_exception_handler(exc_type, exc_value, exc_traceback):
    # ignore Ctrl+C
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    # short message (what happened)
    short_msg = f"{exc_type.__name__}: {exc_value}"

    # full traceback (details)
    details = "".join(
        traceback.format_exception(exc_type, exc_value, exc_traceback)
    )

    show_error_dialog(short_msg + "\n\n" + details)
    

def show_error_dialog(message):
    dlg = ctk.CTkToplevel()
    dlg.title("Error")
    dlg.geometry("500x300")

    text = ctk.CTkTextbox(dlg)
    text.insert("1.0", message)
    text.configure(state="disabled")
    text.pack(expand=True, fill="both", padx=10, pady=10)

    btn = ctk.CTkButton(dlg, text="OK", command=dlg.destroy)
    btn.pack(pady=5)

    dlg.grab_set()


def safe_call(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            global_exception_handler(*sys.exc_info())
    return wrapper


##############################################
##############################################
class MainWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        sys.excepthook = global_exception_handler
    
        # setuo styles
        # Modes: system (default), light, dark
        # ctk.set_appearance_mode("System")
        ctk.set_appearance_mode("dark")
        # Themes: blue (default), dark-blue, green
        ctk.set_default_color_theme("blue")
        

        self.title("DNG Converter")
        self.geometry("400x300")

        btn_base_y = 0.2
        btn_step = 0.12

        # Use instead of tkinter Button
        button01 = ctk.CTkButton(master=self, text="1NFA to 1DFA",
                                           command=safe_call(self.btn_convert_NFA_to_DFA))
        button01.place(relx=0.5, rely=btn_base_y +
                       0 * btn_step, anchor=ctk.CENTER)

        button02 = ctk.CTkButton(master=self, text="Alphabet for 1NFA",
                                           command=safe_call(self.btn_gen_alphabet_1NFA))
        button02.place(relx=0.5, rely=btn_base_y +
                       1 * btn_step, anchor=ctk.CENTER)

        button03 = ctk.CTkButton(master=self, text="Alphabet for 2NFA",
                                           command=safe_call(self.btn_gen_alphabet_2NFA))
        button03.place(relx=0.5, rely=btn_base_y +
                       2 * btn_step, anchor=ctk.CENTER)

        button04 = ctk.CTkButton(master=self, text="Graph for 1NFA string",
                                           command=safe_call(self.btn_gen_graph_1NFA_str))
        button04.place(relx=0.5, rely=btn_base_y +
                       3 * btn_step, anchor=ctk.CENTER)

        button05 = ctk.CTkButton(master=self, text="Graph for 2NFA string",
                                           command=safe_call(self.btn_gen_graph_2NFA_str))
        button05.place(relx=0.5, rely=btn_base_y +
                       4 * btn_step, anchor=ctk.CENTER)

        buttonAbout = ctk.CTkButton(master=self, text="About",
                                              command=safe_call(self.btn_about))
        buttonAbout.place(relx=0.5, rely=btn_base_y +
                          5 * btn_step, anchor=ctk.CENTER)
        

    def getJSONFileName(self):
        return filedialog.askopenfilename(
            title="Open JSON file", filetypes=[("JSON files", "*.json")]
        )

    def generate_graph_alphabet(self, filename, gen):
        graphLangGen = gen
        graphLang = graphLangGen.generate_graphs()
        graphLangGen.renderGraphAlphabet(
            graphLang,
            os.path.dirname(filename),
            remove_json_ext(os.path.basename(filename))
        )
        print("Generation finished.")

    def btn_convert_NFA_to_DFA(self):
        filename = self.getJSONFileName()
        if filename:

            nfa = FAFactory.from_file(filename)

            cvt = NFA2DFAConverter()
            dfa = cvt.convertNFA2DFA(nfa)
            print("Result:", dfa)

            filename_no_ext = remove_json_ext(filename)
            dot_file_path = f"{filename_no_ext}.dot"

            dfa.save_to_dot(dot_file_path)
            dfa.render_dot_to_png(
                dot_file_path, f"{filename_no_ext}", view=True)

    def btn_gen_alphabet_1NFA(self):
        filename = self.getJSONFileName()
        if filename:
            print("Selected:", filename)
            print("Generating alphabet for 1NFA...")
            nfa = FAFactory.from_file(filename)
            graphLangGen = NFAGraphLanguageGenerator(nfa)
            self.generate_graph_alphabet(filename, graphLangGen)

    def btn_gen_alphabet_2NFA(self):
        filename = self.getJSONFileName()
        if filename:
            print("Selected:", filename)
            print("Generating alphabet for 2NFA...")
            nfa2 = FAFactory.from_file_2way(filename)
            graphLangGen = TwoNFAGraphLanguageGenerator(nfa2)
            self.generate_graph_alphabet(filename, graphLangGen)

    def btn_gen_graph_1NFA_str(self):
        filename = self.getJSONFileName()
        if filename:
            
            nfa = FAFactory.from_file(filename)
            
            inputDlg = ABCInputDialog(self, nfa.Sigma)
            userInput = inputDlg.result
            
            if userInput:
                
                print("Generating graph for 1NFA for '{userInput}'...")
                
                graphLangGen = NFAGraphLanguageGenerator(nfa)
                graphLang = graphLangGen.generate_graphs()
                graphLangGen.renderGraphString(
                    graphLang, 
                    userInput, 
                    remove_json_ext(filename) + f"_{userInput}"
                )
      

    def btn_gen_graph_2NFA_str(self):
        # TODO:
        # implement similar to btn_gen_graph_1NFA_str
        # use from_file_two_way instead of from_file
        # use TwoWayNFAGraphLanguageGenerator instead of NFAGraphLanguageGenerator
        pass
    
      
        
    def btn_about(self):
        AboutDialog(self)
    

