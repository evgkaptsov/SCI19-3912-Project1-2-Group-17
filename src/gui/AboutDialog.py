# -*- coding: utf-8 -*-
"""
Created on Fri May  1 13:57:12 2026

@author: CCS
"""

import customtkinter as ctk

class AboutDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("About")
        self.geometry("450x300")
        self.resizable(False, False)

        # center relative to parent
        self.transient(parent)

        label = ctk.CTkLabel(self, text='''\
                             SCI19 3912 Project 1/2, Group 17\n
                             \n
                             State complexity, two-way NFAs, and graph languages
                             \n
                             Natthira Sannok\n
                             Suwannee Pitram\n
                             Warisara Promwicharn\n\n
                             \nProject Advisor: Dr. Evgenii Kaptsov
                             ''',
                             justify="center")
        label.pack(pady=20)

        btn = ctk.CTkButton(self, text="OK", command=self.on_ok)
        btn.pack(pady=10)

        # make modal
        self.grab_set()
        self.wait_window()

    def on_ok(self):
        self.destroy()