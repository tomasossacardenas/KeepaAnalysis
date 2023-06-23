import tkinter as tk
import customtkinter
import sys
from os.path import dirname, abspath

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
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Footsmart", "Rei", "6pm", "Rockport", "Ascis", "Saucony", "Als","Journeys"])
        self.appearance_mode_optionemenu.grid(row=2, column=0, padx=20, pady=(0, 0))

        self.appearance_mode_optionemenu1 = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["UPC", "EAN"],command=lambda productCode: self.productCodeChanged(productCode))
        self.appearance_mode_optionemenu1.grid(row=3, column=0, padx=20, pady=(0, 0))

        #If dropbox is "upc" then is "Product Code: UPC" and if is "ean" is "Product Code: EAN"
        self.KeepaColumnName_label = customtkinter.CTkLabel(self.sidebar_frame, text="Keepa Column Name", font=customtkinter.CTkFont(size=15), anchor="w")
        self.KeepaColumnName_label.grid(row=4, column=0, padx=20, pady=(20, 10))
        self.KeepaColumnName = customtkinter.CTkEntry(self.sidebar_frame, textvariable=tk.StringVar(self,"Product Codes: "+self.appearance_mode_optionemenu1.get()))
        self.KeepaColumnName.grid(row=5,column=0, padx=20, pady=(0, 0))

        #If dropbox is "upc" then is "Product Code: UPC" and if is "ean" is "Product Code: EAN"
        self.scrapperColumnName_label = customtkinter.CTkLabel(self.sidebar_frame, text="Scrapper Column Name", font=customtkinter.CTkFont(size=15), anchor="w")
        self.scrapperColumnName_label.grid(row=6, column=0, padx=20, pady=(20, 10))
        self.scrapperColumnName = customtkinter.CTkEntry(self.sidebar_frame, textvariable=tk.StringVar(self,self.appearance_mode_optionemenu1.get().lower()))
        self.scrapperColumnName.grid(row=7,column=0, padx=20, pady=(0, 0))
       
        #Excel Keepa Path
        self.KeepaExcel_label = customtkinter.CTkLabel(self.middleHome_frame, text="Keepa Excel", font=customtkinter.CTkFont(size=15), anchor="w")
        self.KeepaExcel_label.grid(row=1, column=1,padx=5, pady=(20,0), ipadx=5, ipady=5,  sticky="ew")
        self.KeepaExcel_path = customtkinter.CTkEntry(self.middleHome_frame, placeholder_text="Path to Keepa Excel")
        self.KeepaExcel_path.grid(row=2, column=1,padx=5, ipadx=5, ipady=10 ,sticky="ew")

        #CSV Scrapper Path
        self.scrapperExcel_label = customtkinter.CTkLabel(self.middleHome_frame, text="Scrapper CSV", font=customtkinter.CTkFont(size=15), anchor="w")
        self.scrapperExcel_label.grid(row=1, column=2,padx=5,pady=(20, 0), ipadx=5, ipady=5, sticky="ew")
        self.scrapperExcel_path = customtkinter.CTkEntry(self.middleHome_frame, placeholder_text="path to Scrapper csv")
        self.scrapperExcel_path.grid(row=2, column=2, padx=5,  ipadx=5, ipady=10 ,sticky="ew")
       
        #CSV DELIMETER
        self.delimiterExcel_label = customtkinter.CTkLabel(self.middleHome_frame, text="Delimiter", font=customtkinter.CTkFont(size=15), anchor="w")
        self.delimiterExcel_label.grid(row=1, column=3,padx=5,pady=(20, 0), ipadx=5, ipady=5, sticky="ew")
        self.delimiterExcel = customtkinter.CTkEntry(self.middleHome_frame, placeholder_text="csv separated by")
        self.delimiterExcel.grid(row=2, column=3,padx=5, ipadx=5, ipady=10 ,sticky="ew")

        self.resultsExcel_label = customtkinter.CTkLabel(self.middleHome_frame, text="Results Excel", font=customtkinter.CTkFont(size=15), anchor="w")
        self.resultsExcel_label.grid(row=3, column=1, columnspan=2,padx=5, pady=(20,0), ipadx=5, ipady=5, sticky="ew")
        
        #Excel Results Path
        self.resultsExcel_path = customtkinter.CTkEntry(self.middleHome_frame, placeholder_text="path to Results in Excel")
        self.resultsExcel_path.grid(row=4, column=1, columnspan=2, padx=5,  ipadx=5, ipady=10 ,sticky="ew")

        #Button Submit
        self.analyze_button = customtkinter.CTkButton(master=self.middleHome_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Analyze")
        self.analyze_button.grid(row=6, column=1, padx=(20, 20), columnspan=2, pady=(20, 20))
        self.analyze_button.configure(command=self.analyze)
        self.information_label = customtkinter.CTkLabel(self.middleHome_frame, text="information", font=customtkinter.CTkFont(size=15), anchor="w", fg_color="red")
        self.information_label.grid(row=7, column=0, columnspan=4,padx=5, pady=(20,0), ipadx=5, ipady=5, sticky="nsew")

    #Connected to main.py
    def analyze(self):
        self.keepa_path = self.KeepaExcel_path.get()
        self.scrapper_path = self.scrapperExcel_path.get()
        self.delimiter = self.delimiterExcel.get()

        main.excelToPandas(self.keepa_path)
        main.csvToPandas(self.scrapper_path, self.delimiter)


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
        columns_label = customtkinter.CTkLabel(self.add_scrapper_frame, text="Columns:")
        columns_label.grid(row=3, column=0,padx=(20,20), sticky="w")
        columns_entry = customtkinter.CTkEntry(self.add_scrapper_frame)
        columns_entry.grid(row=4, column=0, padx=(20,20), pady=(0,0), sticky="we")

        # Column UPC entry
        column_upc_label = customtkinter.CTkLabel(self.add_scrapper_frame, text="Column UPC:")
        column_upc_label.grid(row=5, column=0,padx=(20,20), sticky="w")
        column_upc_entry = customtkinter.CTkEntry(self.add_scrapper_frame)
        column_upc_entry.grid(row=6, column=0,padx=(20,20), pady=(0,0), sticky="we")
        
        # EXE Path entry
        exe_path_label = customtkinter.CTkLabel(self.add_scrapper_frame, text="EXE Path:")
        exe_path_label.grid(row=1, column=1,padx=(20,20), sticky="w")
        exe_path_entry = customtkinter.CTkEntry(self.add_scrapper_frame)
        exe_path_entry.grid(row=2, column=1, padx=(20,20), pady=(0,0), sticky="we")

        # Results Analysis entry
        results_analysis_label = customtkinter.CTkLabel(self.add_scrapper_frame, text="Results Analysis:")
        results_analysis_label.grid(row=3, column=1,padx=(20,20), sticky="w")
        results_analysis_entry = customtkinter.CTkEntry(self.add_scrapper_frame)
        results_analysis_entry.grid(row=4, column=1, padx=(20,20), pady=(0,0), sticky="we")

        # Base Files Analysis entry
        base_files_analysis_label = customtkinter.CTkLabel(self.add_scrapper_frame, text="Base Files Analysis:")
        base_files_analysis_label.grid(row=5, column=1,padx=(20,20), sticky="w")
        base_files_analysis_entry = customtkinter.CTkEntry(self.add_scrapper_frame)
        base_files_analysis_entry.grid(row=6, column=1, padx=(20,20), pady=(0,0), sticky="we")

        # Save button
        save_button = customtkinter.CTkButton(self.add_scrapper_frame, text="Create")
        save_button.grid(row=7, columnspan=2, pady=(30,30))

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
        #Search Scrapper
        delete_button = customtkinter.CTkButton(self.name_frame, text="Search", fg_color="transparent", border_color="white", border_width=1)
        delete_button.grid(row=1, column=1)

        # Columns entry
        columns_label = customtkinter.CTkLabel(self.edit_scrapper_frame, text="Columns:")
        columns_label.grid(row=3, column=0,padx=(20,20), sticky="w")
        columns_entry = customtkinter.CTkEntry(self.edit_scrapper_frame)
        columns_entry.grid(row=4, column=0, padx=(20,20), pady=(0,0), sticky="we")

        # Column UPC entry
        column_upc_label = customtkinter.CTkLabel(self.edit_scrapper_frame, text="Column UPC:")
        column_upc_label.grid(row=5, column=0,padx=(20,20), sticky="w")
        column_upc_entry = customtkinter.CTkEntry(self.edit_scrapper_frame)
        column_upc_entry.grid(row=6, column=0,padx=(20,20), pady=(0,0), sticky="we")
        
        # EXE Path entry
        exe_path_label = customtkinter.CTkLabel(self.edit_scrapper_frame, text="EXE Path:")
        exe_path_label.grid(row=1, column=1,padx=(20,20), sticky="w")
        exe_path_entry = customtkinter.CTkEntry(self.edit_scrapper_frame)
        exe_path_entry.grid(row=2, column=1, padx=(20,20), pady=(0,0), sticky="we")

        # Results Analysis entry
        results_analysis_label = customtkinter.CTkLabel(self.edit_scrapper_frame, text="Results Analysis:")
        results_analysis_label.grid(row=3, column=1,padx=(20,20), sticky="w")
        results_analysis_entry = customtkinter.CTkEntry(self.edit_scrapper_frame)
        results_analysis_entry.grid(row=4, column=1, padx=(20,20), pady=(0,0), sticky="we")

        # Base Files Analysis entry
        base_files_analysis_label = customtkinter.CTkLabel(self.edit_scrapper_frame, text="Base Files Analysis:")
        base_files_analysis_label.grid(row=5, column=1,padx=(20,20), sticky="w")
        base_files_analysis_entry = customtkinter.CTkEntry(self.edit_scrapper_frame)
        base_files_analysis_entry.grid(row=6, column=1, padx=(20,20), pady=(0,0), sticky="we")

        self.buttons_frame=customtkinter.CTkFrame(self.edit_scrapper_frame, corner_radius=0, fg_color="transparent") 
        self.buttons_frame.grid(row=7, column=0, columnspan=2,padx=(0,20), pady=(30,30),sticky="nsew")
        self.buttons_frame.columnconfigure((0,1), weight=1)

        # Save button
        edit_button = customtkinter.CTkButton(self.buttons_frame, text="Edit")
        edit_button.grid(row=0, column=0,ipadx=5, ipady=5, padx=(0,10), sticky="e")

        # Save button
        delete_button = customtkinter.CTkButton(self.buttons_frame, text="Delete", fg_color="red")
        delete_button.grid(row=0, column=1,ipadx=5, ipady=5,padx=(10,0), sticky="w")
    
    #WHEN CHOICE CHANGE (UPC OR EAN)
    def productCodeChanged(self, productCode: str):
        self.KeepaColumnName.configure(textvariable=tk.StringVar(self, "Product Codes: " + productCode))
        self.scrapperColumnName.configure(textvariable=tk.StringVar(self, productCode.lower()))

if __name__ == "__main__":
    app = App()
    app.mainloop()
   
