# -*- coding: utf-8 -*-
"""
Created on Fri May  1 13:57:12 2026

@author: 
    Group 17, 3/2568, Project 1/2
    Natthira Sannok,  Suwannee Pitram, Warisara Promwicharn;
    Project Advisor: Dr. Evgenii Kaptsov,
    Suranaree University of Technology
"""

import customtkinter as ctk

class AboutDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("About DNG Converter")
        self.geometry("400x250")
        self.resizable(False, False)

        # center relative to parent
        self.transient(parent)

        label = ctk.CTkLabel(self, text=(
                "SCI19 3912 Project 1/2, Group 17 (2568/3)\n\n"
                '"State complexity, two-way NFAs, and graph languages"\n\n'
                "Natthira Sannok\n"
                "Suwannee Pitram\n"
                "Warisara Promwicharn\n\n"
                "Project Advisor: Dr. Evgenii Kaptsov"
            ),
            justify="center")
        
        label.pack(pady=20)

        btn = ctk.CTkButton(self, text="OK", command=self.on_ok)
        btn.pack(pady=10)

        # make modal
        self.grab_set()
        self.wait_window()

    def on_ok(self):
        self.destroy()