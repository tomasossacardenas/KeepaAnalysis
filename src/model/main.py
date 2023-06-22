import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))# Get the current directory of main.py
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))# Get the parent directory by going one level up
sys.path.append(parent_dir)# Append the parent directory to sys.path
import json
import pandas
import csv
import tkinter as tk
import customtkinter
from ui.home import App
from ui.ManageScrappers import ToplevelWindow

#"precio sugerido de vta":"precio sugerido de vta", "precio tienda":"precio tienda", "costo logistico":"costo logistico", "utilidad":"utilidad", "roi":"roi", "inventario":"inventario"
ALS=json.loads('''{
    "upc":"upc", 
    "price":"price", 
    "availability":"availability", 
    "sku":"sku", 
    "title":"title"}'''
)
KEEPA=json.loads('''{
  "Title": "Title",
  "Sales Rank: Current": "Sales Rank: Current",
  "Sales Rank: 90 days avg.": "Sales Rank: 90 days avg.",
  "Sales Rank: Drops last 30 days": "Sales Rank: Drops last 30 days",
  "Sales Rank: Drops last 90 days": "Sales Rank: Drops last 90 days",
  "Sales Rank: Drops last 180 days": "Sales Rank: Drops last 180 days",
  "Reviews: Rating": "Reviews: Rating",
  "Reviews: Review Count - 90 days avg.": "Reviews: Review Count - 90 days avg.",
  "Buy Box: Current": "Buy Box: Current",
  "Buy Box: 90 days avg.": "Buy Box: 90 days avg.",
  "Amazon: Current": "Amazon: Current",
  "Amazon: 90 days avg.": "Amazon: 90 days avg.",
  "Amazon: Stock": "Amazon: Stock",
  "New: Current": "New: Current",
  "New: 90 days avg.": "New: 90 days avg.",
  "New, 3rd Party FBA: Current": "New, 3rd Party FBA: Current",
  "New, 3rd Party FBA: 90 days avg.": "New, 3rd Party FBA: 90 days avg.",
  "FBA Fees:": "FBA Fees:",
  "Referral Fee %": "Referral Fee %",
  "Referral Fee based on current Buy Box price": "Referral Fee based on current Buy Box price",
  "New, 3rd Party FBM: Current": "New, 3rd Party FBM: Current",
  "New, 3rd Party FBM: 90 days avg.": "New, 3rd Party FBM: 90 days avg.",
  "List Price: Current": "List Price: Current",
  "List Price: 90 days avg.": "List Price: 90 days avg.",
  "eBay New: 90 days avg.": "eBay New: 90 days avg.",
  "New Offer Count: Current": "New Offer Count: Current",
  "New Offer Count: 30 days avg.": "New Offer Count: 30 days avg.",
  "New Offer Count: 90 days avg.": "New Offer Count: 90 days avg.",
  "New Offer Count: 180 days avg.": "New Offer Count: 180 days avg.",
  "Tracking since": "Tracking since",
  "Listed since": "Listed since",
  "URL: Amazon": "URL: Amazon",
  "ASIN": "ASIN",
  "Product Codes: EAN": "Product Codes: EAN",
  "upc": "upc",
  "Parent ASIN": "Parent ASIN",
  "Variation ASINs": "Variation ASINs",
  "Manufacturer": "Manufacturer",
  "Brand": "Brand",
  "Product Group": "Product Group",
  "Model": "Model",
  "Variation Attributes": "Variation Attributes",
  "Color": "Color",
  "Size": "Size",
  "Author": "Author",
  "Contributors": "Contributors",
  "Number of Items": "Number of Items",
  "Number of Pages": "Number of Pages",
  "Publication Date": "Publication Date",
  "Package: Weight (g)": "Package: Weight (g)",
  "Adult Product": "Adult Product"
}'''
)

def excelToPandas(path):
    keepa = pandas.read_excel("C:/Users/tomas/Desktop/KeepaAnalysis/files/KeepaAls.xlsx")
    scrapper = pandas.read_csv("C:/Users/tomas/Desktop/KeepaAnalysis/files/scrapperAls.csv")
    scrapper.to_excel("./files/scrapperAls.xlsx", index=False)
    
    keepa=keepa.astype(str)
    scrapper=scrapper.astype(str)

    print("keepa shape:", keepa.shape)
    print("scrapper shape:", scrapper.shape)

    # merging the files
    '''
    f3 = keepa[[KEEPA["Title"], KEEPA["Sales Rank: Current"], KEEPA["Sales Rank: 90 days avg."], KEEPA["Sales Rank: Drops last 30 days"], KEEPA["Sales Rank: Drops last 90 days"], KEEPA["Sales Rank: Drops last 180 days"], KEEPA["Reviews: Rating"], KEEPA["Reviews: Review Count - 90 days avg."], KEEPA["Buy Box: Current"], KEEPA["Buy Box: 90 days avg."], KEEPA["Amazon: Current"], KEEPA["Amazon: 90 days avg."], KEEPA["Amazon: Stock"], KEEPA["New: Current"], KEEPA["New: 90 days avg."], KEEPA["New, 3rd Party FBA: Current"], KEEPA["New, 3rd Party FBA: 90 days avg."], KEEPA["FBA Fees:"], KEEPA["Referral Fee %"], KEEPA["Referral Fee based on current Buy Box price"], KEEPA["New, 3rd Party FBM: Current"], KEEPA["New, 3rd Party FBM: 90 days avg."], KEEPA["List Price: Current"], KEEPA["List Price: 90 days avg."], KEEPA["eBay New: 90 days avg."], KEEPA["New Offer Count: Current"], KEEPA["New Offer Count: 30 days avg."], KEEPA["New Offer Count: 90 days avg."], KEEPA["New Offer Count: 180 days avg."], KEEPA["Tracking since"], KEEPA["Listed since"], KEEPA["URL: Amazon"], KEEPA["ASIN"], KEEPA["Product Codes: EAN"], KEEPA["upc"], KEEPA["Parent ASIN"], KEEPA["Variation ASINs"], KEEPA["Manufacturer"], KEEPA["Brand"], KEEPA["Product Group"], KEEPA["Model"], KEEPA["Variation Attributes"], KEEPA["Color"], KEEPA["Size"], KEEPA["Author"], KEEPA["Contributors"], KEEPA["Number of Items"], KEEPA["Number of Pages"], KEEPA["Publication Date"], KEEPA["Package: Weight (g)"], KEEPA["Adult Product"]]
        ].merge(scrapper[[ALS["upc"], ALS["price"], ALS["availability"], ALS["sku"] , ALS["title"]]], 
                                        on = "upc", 
                                        how = "left")
    '''
    merged_df = scrapper.merge(keepa, on="upc")
        
    merged_df.to_excel("./files/result.xlsx", index=False)
    
    # creating a new file
    #f3.to_excel("Results.xlsx", index = False)

#change upc column in keepa
def changeExcelColumnName(filename, currentName, newName):
    df = pandas.read_excel(filename)

    # Get the current column names
    column_names = df.columns.tolist()

    try:
        column_index = column_names.index(currentName)
        # Update the desired column name
        column_names[column_index] = newName

        # Assign the updated column names back to the DataFrame
        df.columns = column_names

        # Save the DataFrame back to the Excel file
        df.to_excel(filename, index=False)
    except Exception as e:
        print(e)
        print("the column "+currentName+"was not found in "+filename)

#change upc column in scrapper
def changeCsvColumnName(filename, currentName, newName):
    # Read the CSV file and store the data in a list
    rows = []
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Get the header row
    header_row = rows[0]

    try:
        # Find the index of the old column name
        column_index = header_row.index(currentName)

        # Update the column name
        header_row[column_index] = newName

        # Write the updated data back to the CSV file
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
    except Exception as e:
        print(e)
        print(print("the column "+currentName+"was not found in "+filename))


#FIRST THING CHANGE THE COLUMN IN KEEPA AND SCRAPPER EXCEL TO UPC TO HAVE THE SAME NAME THAN IN SCRAPPER FILE
#changeExcelColumnName("C:/Users/tomas/Desktop/KeepaAnalysis/files/KeepaAls.xlsx", "Product Codes: UPC", "upc")
#changeCsvColumnName("C:/Users/tomas/Desktop/KeepaAnalysis/files/scrapperAls.csv", ALS["upc"], "upc")
#excelToPandas("")

#UI MANAGEMENT
def productCodeChanged(app, productCode: str):
    app.KeepaColumnName.configure(textvariable=tk.StringVar(app, "Product Codes: " + productCode))
    app.scrapperColumnName.configure(textvariable=tk.StringVar(app, productCode.lower()))
    print("in main")


        
if __name__=="__main__":
    app=App()
    app.productCodeChanged = lambda productCode: productCodeChanged(app, productCode)
    app.mainloop()