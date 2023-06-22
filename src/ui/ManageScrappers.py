import customtkinter
import tkinter as tk

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("800x500")
        self.title("Manage Scrappers")
        
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.left_frame = customtkinter.CTkFrame(self, corner_radius=0,fg_color="#242424") 
        self.left_frame.pack_configure(row=0, column=0, rowspan=6, sticky="nsew")
        self.left_frame.grid_rowconfigure(6, weight=1)

        self.name_label = customtkinter.CTkLabel(self.left_frame, text="Scrapper Name", font=customtkinter.CTkFont(size=14), anchor="w")
        self.name_label.grid(row=1, column=0, padx=20, pady=(20, 10))
        self.name= customtkinter.CTkEntry(self.left_frame, placeholder_text="Scrapper Name")
        self.name.grid(row=2,column=0, padx=20, pady=(0, 0))

        self.right_frame = customtkinter.CTkFrame(self, corner_radius=0,fg_color="#242424") 
        self.right_frame.grid(row=0, column=1, rowspan=6, sticky="nsew")
        self.right_frame.grid_rowconfigure(6, weight=1)

        self.columns_label = customtkinter.CTkLabel(self.left_frame, text="Scrapper Columns", font=customtkinter.CTkFont(size=14), anchor="w")
        self.columns_label.grid(row=1, column=1, padx=20, pady=(20, 10))
        self.columns= customtkinter.CTkEntry(self.left_frame, placeholder_text="[column1,column2..]")
        self.columns.grid(row=2,column=1, padx=20, pady=(0, 0))


