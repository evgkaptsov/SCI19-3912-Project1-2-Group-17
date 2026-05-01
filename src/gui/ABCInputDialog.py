# -*- coding: utf-8 -*-
"""
Created on Fri May  1 18:18:53 2026

@author: 
    Group 17, 3/2568, Project 1/2
    Natthira Sannok,  Suwannee Pitram, Warisara Promwicharn;
    Project Advisor: Dr. Evgenii Kaptsov,
    Suranaree University of Technology
"""

import customtkinter as ctk

class ABCInputDialog(ctk.CTkToplevel):
    
    def __init__(self, parent, sigma):
        super().__init__(parent)

        self.title("Input")
        self.geometry("420x200")
        self.resizable(False, False)

        self.result = None

        self.transient(parent)

        # message
        msg = f"Please, use only symbols from the FA alphabet:\n{sigma}"
        label = ctk.CTkLabel(self, text=msg, wraplength=380, justify="center")
        label.pack(pady=15, padx=10)

        # input field
        self.entry = ctk.CTkEntry(self, width=300)
        self.entry.pack(pady=5)
        self.entry.focus()

        # buttons
        frame = ctk.CTkFrame(self)
        frame.pack(pady=15)

        ok_btn = ctk.CTkButton(frame, text="OK", command=self.on_ok)
        ok_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(frame, text="Cancel", command=self.on_cancel)
        cancel_btn.pack(side="left", padx=10)

        # modal
        self.grab_set()
        self.wait_window()

    def on_ok(self):
        self.result = self.entry.get()
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()