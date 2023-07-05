import tkinter as tk
from tkinter import messagebox
import customtkinter
import sys
from os.path import dirname, abspath
import traceback

# Add the root directory to the system path
root_dir = dirname(dirname(abspath(__file__)))
sys.path.append(root_dir)

# Now you can import `main.py` from `model` package
from model import main



customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.toplevel_window = None

        main.array_scrappers=main.load_scrappers_array()
        # configure window
        self.title("Products Analysis")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0,weight=0)
        self.grid_rowconfigure((1, 2, 3, 4, 5, 6), weight=1)

        # Create top bar frame
        self.top_bar_frame = customtkinter.CTkFrame(self, fg_color="#191919")
        self.top_bar_frame.grid(row=0, column=0, columnspan=2, padx=(0,0), pady=(0,0), sticky="ew")

        # Add buttons to the top bar
        self.home_button = customtkinter.CTkButton(master=self.top_bar_frame, text="Home", command=self.show_home_frame, fg_color="transparent", corner_radius=0)
        self.home_button.grid(row=0, column=0, sticky="nsew")

        self.add_scrapper_button = customtkinter.CTkButton(master=self.top_bar_frame, text="Add Scrapper", command=self.show_add_scrapper_frame, fg_color="transparent", corner_radius=0)
        self.add_scrapper_button.grid(row=0, column=1, sticky="nsew")

        self.edit_scrapper_button = customtkinter.CTkButton(master=self.top_bar_frame, text="Edit Scrapper", command=self.show_edit_scrapper_frame, fg_color="transparent", corner_radius=0)
        self.edit_scrapper_button.grid(row=0, column=2, sticky="nsew")

        # Create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="#242424")
        self.home_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.home_frame.grid_rowconfigure(0, weight=1)
        self.home_frame.grid_columnconfigure(0, weight=1)

        # Create addScrapper frame
        self.add_scrapper_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="#242424")
        self.add_scrapper_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.add_scrapper_frame.grid_rowconfigure(0, weight=1)
        self.add_scrapper_frame.grid_columnconfigure(0, weight=1)

        # Create editScrapper frame
        self.edit_scrapper_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="#242424")
        self.edit_scrapper_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.edit_scrapper_frame.grid_rowconfigure(0, weight=1)
        self.edit_scrapper_frame.grid_columnconfigure(0, weight=1)

        # Show the home frame initially
        self.show_home_frame()

    def show_home_frame(self):
        self.add_scrapper_frame.grid_forget()  # Hide the addScrapper frame if it's visible
        self.edit_scrapper_frame.grid_forget()

        self.home_frame.grid(row=1, column=0, rowspan=7,columnspan=2, sticky="nsew")
        self.home_frame.grid_columnconfigure(0, weight=0)
        self.home_frame.grid_columnconfigure(1, weight=1)        
        self.home_frame.grid_rowconfigure((0,1,2,3,4,5,6), weight=1)

        #left sidebar
        self.sidebar_frame = customtkinter.CTkFrame(self.home_frame, width=140, corner_radius=10, fg_color="#2b2b2b")
        self.sidebar_frame.grid(row=0, column=0, rowspan=7, sticky="nsew", padx=(0,20), pady=(0,0))
        self.sidebar_frame.grid_rowconfigure(10, weight=1)

        #main (middle) frame
        self.middleHome_frame = customtkinter.CTkFrame(self.home_frame, corner_radius=0,fg_color="#242424") 
        self.middleHome_frame.grid_columnconfigure(1, weight=1)
        self.middleHome_frame.grid_columnconfigure(2, weight=1)
        self.middleHome_frame.grid(row=0, column=1, rowspan=7, sticky="nsew")
        self.middleHome_frame.grid_rowconfigure(10, weight=1)

        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Choose Scrapper", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=20, pady=(20, 10))

        #scrapperOption Menu, falta command para realizar accion
        values = [scrapper._name for scrapper in main.array_scrappers]
        self.scrappers_menu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=values, command=lambda scrapperName: self.scrapperChanged(scrapperName))
        self.scrappers_menu.grid(row=2, column=0, padx=20, pady=(0, 0))

        self.upc_menu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["UPC", "EAN"],command=lambda productCode: self.productCodeChanged(productCode))
        self.upc_menu.grid(row=3, column=0, padx=20, pady=(0, 0))

        #If dropbox is "upc" then is "Product Code: UPC" and if is "ean" is "Product Code: EAN"
        self.KeepaColumnName_label = customtkinter.CTkLabel(self.sidebar_frame, text="Keepa Column Name", font=customtkinter.CTkFont(size=15), anchor="w")
        self.KeepaColumnName_label.grid(row=4, column=0, padx=20, pady=(20, 10))
        self.KeepaColumnName = customtkinter.CTkEntry(self.sidebar_frame, textvariable=tk.StringVar(self,"Product Codes: "+self.upc_menu.get()))
        self.KeepaColumnName.grid(row=5,column=0, padx=20, pady=(0, 0))

        #If dropbox is "upc" then is "Product Code: UPC" and if is "ean" is "Product Code: EAN"
        self.scrapperColumnName_label = customtkinter.CTkLabel(self.sidebar_frame, text="Scrapper Column Name", font=customtkinter.CTkFont(size=15), anchor="w")
        self.scrapperColumnName_label.grid(row=6, column=0, padx=20, pady=(20, 10))
        selected_scrapper = main.searchScrapper(self.scrappers_menu.get())
        scrapper_column_name = selected_scrapper._column_upc if selected_scrapper else ""
        self.scrapperColumnName = customtkinter.CTkEntry(self.sidebar_frame, textvariable=tk.StringVar(self, scrapper_column_name))
        self.scrapperColumnName.grid(row=7,column=0, padx=20, pady=(0, 0))
       
        #Excel Keepa Path
        self.KeepaExcel_label = customtkinter.CTkLabel(self.middleHome_frame, text="Keepa Excel", font=customtkinter.CTkFont(size=15), anchor="w")
        self.KeepaExcel_label.grid(row=1, column=1,padx=5, pady=(20,0), ipadx=5, ipady=5,  sticky="ew")
        self.KeepaExcel_path = customtkinter.CTkEntry(self.middleHome_frame)
        self.KeepaExcel_path.grid(row=2, column=1,padx=5, ipadx=5, ipady=10 ,sticky="ew")

        #CSV Scrapper Path
        self.scrapperExcel_label = customtkinter.CTkLabel(self.middleHome_frame, text="Scrapper CSV", font=customtkinter.CTkFont(size=15), anchor="w")
        self.scrapperExcel_label.grid(row=1, column=2,padx=5,pady=(20, 0), ipadx=5, ipady=5, sticky="ew")
        self.scrapperExcel_path = customtkinter.CTkEntry(self.middleHome_frame)
        self.scrapperExcel_path.grid(row=2, column=2, padx=5,  ipadx=5, ipady=10 ,sticky="ew")
       
        #CSV DELIMETER
        self.delimiterExcel_label = customtkinter.CTkLabel(self.middleHome_frame, text="Delimiter", font=customtkinter.CTkFont(size=15), anchor="w")
        self.delimiterExcel_label.grid(row=1, column=3,padx=5,pady=(20, 0), ipadx=5, ipady=5, sticky="ew")
        self.delimiterExcel = customtkinter.CTkEntry(self.middleHome_frame, placeholder_text="csv separated by")
        self.delimiterExcel.grid(row=2, column=3,padx=5, ipadx=5, ipady=10 ,sticky="ew")

        self.resultsExcel_label = customtkinter.CTkLabel(self.middleHome_frame, text="Results Excel", font=customtkinter.CTkFont(size=15), anchor="w")
        self.resultsExcel_label.grid(row=3, column=1, columnspan=2,padx=5, pady=(20,0), ipadx=5, ipady=5, sticky="ew")
        
        #Excel Results Path
        self.resultsExcel_path = customtkinter.CTkEntry(self.middleHome_frame)
        self.resultsExcel_path.grid(row=4, column=1, columnspan=2, padx=5,  ipadx=5, ipady=10 ,sticky="ew")

        #Button Submit
        self.analyze_button = customtkinter.CTkButton(master=self.middleHome_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Analyze")
        self.analyze_button.grid(row=6, column=1, padx=(20, 20), columnspan=2, pady=(20, 20))
        self.analyze_button.configure(command=self.analyze)

    #Connected to main.py
    def analyze(self):
        self.scrapper=main.searchScrapper(self.scrappers_menu.get())
        self.keepa_path = self.KeepaExcel_path.get()
        self.scrapper_path = self.scrapperExcel_path.get()
        self.delimiter = self.delimiterExcel.get()

        verification=self.verifyEntries()

        if verification is True: #If all required entries are filled
            #FIRST LOAD THE DATAFRAMES
            try:
                keepa_df=main.excelToPandas(self.keepa_path)
            except FileNotFoundError as e:
                messagebox.showerror("Error", f"File not found: {e.filename}")
                return
            except PermissionError as e:
                messagebox.showerror("Error", f"File permission error: {e}")
                return

            try:
                scrapper_df=main.csvToPandas(self.scrapper_path, self.delimiter)
            except FileNotFoundError as e:
                messagebox.showerror("Error", f"File not found: {e.filename}")
                return
            except PermissionError as e:
                messagebox.showerror("Error", f"File permission error: {e}")
                return
            
            #CLEAN EMPTY UPC
            try:
                keepa_df=main.cleanEmptyUpc(keepa_df,self.KeepaColumnName.get())
                scrapper_df=main.cleanEmptyUpc(scrapper_df,self.scrapperColumnName.get())
            except Exception as e:
                messagebox.showerror("Error", f"Something wrong occured cleaning the empty upcs: {e}")
                traceback.print_exc()
                return
            
            #MERGEDATAFRAMES
            try: 
                merged_df=main.mergeAndSaveDataframes(scrapper_df,self.scrapperColumnName.get(),keepa_df,self.KeepaColumnName.get())
            except Exception as e:
                messagebox.showerror("Error", f"Something wrong occured merging data: {e}")
                traceback.print_exc()
                return
            
            #MERGED_DF WITH NEW COLUMNS ADDED AND OPERATIONS DONE
            try:
                merged_df=main.setOperationsColumns(merged_df)
            except Exception as e:
                messagebox.showerror("Error", f"Something wrong occured doing operations: {e}")
                traceback.print_exc()
                return

            #REORDER COLUMNS IN MERGED_dF
            #IT IS NOT ESSENTIAL SO IF ITS NOT POSSIBLE THEN THE PROCESS CONTINUES
            try:
                merged_df=main.reorderColumns(merged_df, self.scrapper._columns)
            except Exception as e:
                messagebox.showwarning("Problem", f"Could not reorder columns but the process will continue: {e}")
                traceback.print_exc()
            
            #Do the prioritization
            try:    
                merged_df=main.fillPriorities(merged_df)
            except Exception as e:
                messagebox.showerror("Error", f"Something wrong occured: {e}")
                traceback.print_exc()
                return

            #Send to excel
            try:    
                main.createExcel(merged_df, self.resultsExcel_path.get())
                messagebox.showinfo("Proceso Satisfactorio", "ya puedes abrir tu excel")
            except PermissionError as e:
                messagebox.showerror("Error", f"File permission error: {e}")
                traceback.print_exc()
                return
            except FileNotFoundError as e:
                messagebox.showerror("Error", f"File not found: {e.filename}")
                traceback.print_exc()
                return
            except Exception as e:
                messagebox.showerror("Error", f"Something wrong occured creating the results excel: {e}")
                traceback.print_exc()
                return

        else:
             messagebox.showerror("Error",verification)
             return
        
        
    def verifyEntries(self):
        if self.KeepaExcel_path.get() == "":
            return "Keepa excel path field is required"
        elif self.scrapperExcel_path.get() == "":
            return "Scrapper excel path field is required"
        elif self.KeepaColumnName.get() == "":
            return "Keepa column name field is required"
        elif self.scrapperColumnName.get() == "":
            return "Scrapper column name field is required"
        elif self.delimiterExcel.get() == "":
            return "Scrapper delimeter field is required"
        elif self.resultsExcel_path.get() == "":
            return "Results Excel path field is required"
        else:
            return True
        
        #WHEN CHOICE CHANGE (UPC OR EAN) LOCAL PROCESS
    def productCodeChanged(self, productCode: str):
        self.KeepaColumnName.configure(textvariable=tk.StringVar(self, "Product Codes: " + productCode))
        #self.scrapperColumnName.configure(textvariable=tk.StringVar(self, productCode.lower()))

        #WHEN Scrapper CHANGE LOCAL PROCESS
    def scrapperChanged(self, scrapperName: str):
        scrapper=main.searchScrapper(scrapperName)
        self.scrapperColumnName.configure(textvariable=tk.StringVar(self, scrapper._column_upc))

        self.KeepaExcel_path.configure(textvariable=tk.StringVar(self, scrapper._base_files_analysis))
        self.scrapperExcel_path.configure(textvariable=tk.StringVar(self, scrapper._base_files_analysis))
        self.resultsExcel_path.configure(textvariable=tk.StringVar(self, scrapper._results_analysis))
        


    def show_add_scrapper_frame(self):
        self.home_frame.grid_forget()  # Hide the home frame if it's visible
        self.edit_scrapper_frame.grid_forget()

        self.add_scrapper_frame.grid(row=1, column=0, rowspan=7,columnspan=2, sticky="nsew")

        self.add_scrapper_frame.grid_rowconfigure((0,1,2,3,4,5,6), weight=0)
        self.add_scrapper_frame.grid_columnconfigure(0, weight=1)
        self.add_scrapper_frame.grid_columnconfigure(1, weight=1)

        self.title_label = customtkinter.CTkLabel(self.add_scrapper_frame, text="Add Scrapper", font=customtkinter.CTkFont(size=40, weight="bold"))
        self.title_label.grid(row=0, column=0,columnspan=2, padx=(20,20), pady=(20,40),sticky="nswe")

        # Name entry
        self.name_label = customtkinter.CTkLabel(self.add_scrapper_frame, text="Name:")
        self.name_label.grid(row=1, column=0, padx=(20,20), pady=(0,0),sticky="w")
        self.name_entry = customtkinter.CTkEntry(self.add_scrapper_frame)
        self.name_entry.grid(row=2, column=0,padx=(20,20), pady=(0,0), sticky="we")

        # Columns entry
        self.columns_label = customtkinter.CTkLabel(self.add_scrapper_frame, text="Columns:")
        self.columns_label.grid(row=3, column=0,padx=(20,20), sticky="w")
        self.columns_entry = customtkinter.CTkEntry(self.add_scrapper_frame)
        self.columns_entry.grid(row=4, column=0, padx=(20,20), pady=(0,0), sticky="we")

        # Column UPC entry
        self.column_upc_label = customtkinter.CTkLabel(self.add_scrapper_frame, text="Column UPC:")
        self.column_upc_label.grid(row=5, column=0,padx=(20,20), sticky="w")
        self.column_upc_entry = customtkinter.CTkEntry(self.add_scrapper_frame)
        self.column_upc_entry.grid(row=6, column=0,padx=(20,20), pady=(0,0), sticky="we")
        
        # EXE Path entry
        self.exe_path_label = customtkinter.CTkLabel(self.add_scrapper_frame, text="EXE Path:")
        self.exe_path_label.grid(row=1, column=1,padx=(20,20), sticky="w")
        self.exe_path_entry = customtkinter.CTkEntry(self.add_scrapper_frame)
        self.exe_path_entry.grid(row=2, column=1, padx=(20,20), pady=(0,0), sticky="we")

        # Results Analysis entry
        self.results_analysis_label = customtkinter.CTkLabel(self.add_scrapper_frame, text="Results Analysis:")
        self.results_analysis_label.grid(row=3, column=1,padx=(20,20), sticky="w")
        self.results_analysis_entry = customtkinter.CTkEntry(self.add_scrapper_frame)
        self.results_analysis_entry.grid(row=4, column=1, padx=(20,20), pady=(0,0), sticky="we")

        # Base Files Analysis entry
        self.base_files_analysis_label = customtkinter.CTkLabel(self.add_scrapper_frame, text="Base Files Analysis:")
        self.base_files_analysis_label.grid(row=5, column=1,padx=(20,20), sticky="w")
        self.base_files_analysis_entry = customtkinter.CTkEntry(self.add_scrapper_frame)
        self.base_files_analysis_entry.grid(row=6, column=1, padx=(20,20), pady=(0,0), sticky="we")

        # Save button
        self.save_button = customtkinter.CTkButton(self.add_scrapper_frame, text="Create", command=self.addScrapper)
        self.save_button.grid(row=7, columnspan=2, pady=(30,30))

    def addScrapper(self):
        name=self.name_entry.get()
        columns=self.columns_entry.get()
        column_upc=self.column_upc_entry.get()
        exe_path=self.exe_path_entry.get()
        results_analysis=self.results_analysis_entry.get()
        base_files_analysis=self.base_files_analysis_entry.get()

        if name == "":
            messagebox.showerror("Error", "Name is required")
        elif column_upc=="":
            messagebox.showerror("Error", "Columns Upc is required")

        result=main.createScrapper(name=name, columns=columns, column_upc=column_upc, exe_path=exe_path,results_analysis=results_analysis,base_files_analysis=base_files_analysis)
        
        if result==False:
            messagebox.showerror("Error", "There is already a scrapper with that name")
        else:
            messagebox.showinfo("Proceso Satisfactorio", "El Scrapper ha sido creado")


    def show_edit_scrapper_frame(self):
        self.home_frame.grid_forget()  # Hide the home frame if it's visible
        self.add_scrapper_frame.grid_forget()  # Hide the addScrapper frame if it's visible

        self.edit_scrapper_frame.grid(row=1, column=0, rowspan=7,columnspan=2, sticky="nsew")

        self.edit_scrapper_frame.grid_rowconfigure((0,1,2,3,4,5,6), weight=0)
        self.edit_scrapper_frame.grid_columnconfigure(0, weight=1)
        self.edit_scrapper_frame.grid_columnconfigure(1, weight=1)

        self.title_label = customtkinter.CTkLabel(self.edit_scrapper_frame, text="Edit Scrapper", font=customtkinter.CTkFont(size=40, weight="bold"))
        self.title_label.grid(row=0, column=0,columnspan=2, padx=(20,20), pady=(20,40),sticky="nswe")


        self.name_label = customtkinter.CTkLabel(self.edit_scrapper_frame, text="Name:")
        self.name_label.grid(row=1, column=0, padx=(20,20), pady=(0,0),sticky="w")
        # Name entry with a frame to put a button and the name entry in the same row
        self.name_frame=customtkinter.CTkFrame(self.edit_scrapper_frame, corner_radius=0, fg_color="transparent") 
        self.name_frame.grid(row=2, column=0,padx=(20,20), pady=(0,0),sticky="we")

        self.name_frame.columnconfigure(0, weight=1)
        self.name_frame.columnconfigure(1, weight=0)
        self.name_frame.rowconfigure((0,1), weight=0)
        self.name_entry = customtkinter.CTkEntry(self.name_frame)
        self.name_entry.grid(row=1, column=0,padx=(0,20), pady=(0,0), sticky="we")
        
        #delete Scrapper
        self.search_button = customtkinter.CTkButton(self.name_frame, text="Search", fg_color="transparent", border_color="white", border_width=1, command=self.fillScrapperInfo)
        self.search_button.grid(row=1, column=1)

        # Columns entry
        self.columns_label = customtkinter.CTkLabel(self.edit_scrapper_frame, text="Columns:")
        self.columns_label.grid(row=3, column=0,padx=(20,20), sticky="w")
        self.columns_entry = customtkinter.CTkEntry(self.edit_scrapper_frame)
        self.columns_entry.grid(row=4, column=0, padx=(20,20), pady=(0,0), sticky="we")

        # Column UPC entry
        self.column_upc_label = customtkinter.CTkLabel(self.edit_scrapper_frame, text="Column UPC:")
        self.column_upc_label.grid(row=5, column=0,padx=(20,20), sticky="w")
        self.column_upc_entry = customtkinter.CTkEntry(self.edit_scrapper_frame)
        self.column_upc_entry.grid(row=6, column=0,padx=(20,20), pady=(0,0), sticky="we")
        
        # EXE Path entry
        self.exe_path_label = customtkinter.CTkLabel(self.edit_scrapper_frame, text="EXE Path:")
        self.exe_path_label.grid(row=1, column=1,padx=(20,20), sticky="w")
        self.exe_path_entry = customtkinter.CTkEntry(self.edit_scrapper_frame)
        self.exe_path_entry.grid(row=2, column=1, padx=(20,20), pady=(0,0), sticky="we")

        # Results Analysis entry
        self.results_analysis_label = customtkinter.CTkLabel(self.edit_scrapper_frame, text="Results Analysis:")
        self.results_analysis_label.grid(row=3, column=1,padx=(20,20), sticky="w")
        self.results_analysis_entry = customtkinter.CTkEntry(self.edit_scrapper_frame)
        self.results_analysis_entry.grid(row=4, column=1, padx=(20,20), pady=(0,0), sticky="we")

        # Base Files Analysis entry
        self.base_files_analysis_label = customtkinter.CTkLabel(self.edit_scrapper_frame, text="Base Files Analysis:")
        self.base_files_analysis_label.grid(row=5, column=1,padx=(20,20), sticky="w")
        self.base_files_analysis_entry = customtkinter.CTkEntry(self.edit_scrapper_frame)
        self.base_files_analysis_entry.grid(row=6, column=1, padx=(20,20), pady=(0,0), sticky="we")

        self.buttons_frame=customtkinter.CTkFrame(self.edit_scrapper_frame, corner_radius=0, fg_color="transparent") 
        self.buttons_frame.grid(row=7, column=0, columnspan=2,padx=(0,20), pady=(30,30),sticky="nsew")
        self.buttons_frame.columnconfigure((0,1), weight=1)

        # Save button
        self.edit_button = customtkinter.CTkButton(self.buttons_frame, text="Edit", command=self.editScrapper)
        self.edit_button.grid(row=0, column=0,ipadx=5, ipady=5, padx=(0,10), sticky="e")

        # Save button
        self.delete_button = customtkinter.CTkButton(self.buttons_frame, text="Delete", fg_color="red", command=self.deleteScrapper)
        self.delete_button.grid(row=0, column=1,ipadx=5, ipady=5,padx=(10,0), sticky="w")

    def fillScrapperInfo(self):
        name=self.name_entry.get()
        if name != "":
            scrapper=main.searchScrapper(name)
            if scrapper != False:
                self.columns_entry.configure(textvariable=tk.StringVar(self, scrapper._columns))
                self.column_upc_entry.configure(textvariable=tk.StringVar(self, scrapper._column_upc))
                self.exe_path_entry.configure(textvariable=tk.StringVar(self, scrapper._exe_path))
                self.results_analysis_entry.configure(textvariable=tk.StringVar(self, scrapper._results_analysis))
                self.base_files_analysis_entry.configure(textvariable=tk.StringVar(self, scrapper._base_files_analysis))            
            else:
                messagebox.showerror("Error", "Scrapper was not found")

        else:
            messagebox.showerror("Error", "The name field is required")
    
    def editScrapper(self):
        name=self.name_entry.get()
        if name != "":
            scrapper=main.searchScrapper(name)
            if scrapper != False:
                columns=self.columns_entry.get()
                column_upc=self.column_upc_entry.get()
                exe_path=self.exe_path_entry.get()
                results_analysis=self.results_analysis_entry.get()
                base_files_analysis=self.base_files_analysis_entry.get()
                result=main.editScrapper(name, new_name=name, new_columns=columns, new_column_upc=column_upc, new_exe_path=exe_path, new_results_analysis=results_analysis, new_base_files_analysis=base_files_analysis)
                if result ==False:
                    messagebox.showerror("Error", "Could not edit the scrapper info")
                else:
                    messagebox.showinfo("Succesful Proces", "El scrapper fue editado")

            else:
                messagebox.showerror("Error", "Scrapper was not found")

        else:
            messagebox.showerror("Error", "The name field is required")
    def deleteScrapper(self):
        name=self.name_entry.get()
        if name != "":
            scrapper=main.searchScrapper(name)
            if scrapper != False:
                result=main.deleteScrapper(name)
                if result==False:
                    messagebox.showerror("Error", "Could not delete the scrapper info")
                else:
                    messagebox.showinfo("Succesful Proces", "El scrapper fue eliminado")

            else:
                messagebox.showerror("Error", "Scrapper was not found")

        else:
            messagebox.showerror("Error", "The name field is required")


        
    


if __name__ == "__main__":
    app = App()
    app.mainloop()
   
