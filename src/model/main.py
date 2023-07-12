import json
import re
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))# Get the current directory of main.py
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))# Get the parent directory by going one level up
sys.path.append(parent_dir)# Append the parent directory to sys.path
import pandas
import csv
import tkinter as tk
import numpy as np
from model.Scrapper import Scrapper

#ARRAY OF SCRAPPERS
array_scrappers=[]
#ARRAY WITH THE ORDER TO GET THE PRECIO SUGERIDO
array_preciosugeridoventa=['New, 3rd Party FBA: 90 days avg.','Buy Box: 90 days avg.','List Price: 90 days avg.','New, 3rd Party FBM: 90 days avg.','Amazon: 90 days avg.','New: 90 days avg.','New, 3rd Party FBA: Current','Buy Box: Current','List Price: Current','New, 3rd Party FBM: Current','Amazon: Current','New: Current']

def createScrapper(name, columns=None, column_upc=None, exe_path=None, results_analysis=None, base_files_analysis=None):
    found=searchScrapper(name)
    if found == False:
        scrapper = Scrapper(name, columns, column_upc, exe_path, results_analysis, base_files_analysis)
        array_scrappers.append(scrapper)
        save_scrappers_array()
        return
    else:
        return False

def deleteScrapper(name):
    for scrapper in array_scrappers:
        if scrapper._name == name:
            array_scrappers.remove(scrapper)
            save_scrappers_array()
            return
    return False
def searchScrapper(name):
    for scrapper in array_scrappers:
        if scrapper._name == name:
            return scrapper
    return False

def editScrapper(name, new_name=None, new_columns=None, new_column_upc=None, new_exe_path=None, new_results_analysis=None, new_base_files_analysis=None):
    for scrapper in array_scrappers:
        if scrapper._name == name:
            if new_name is not None:
                scrapper._name = new_name
            if new_columns is not None:
                scrapper._columns = new_columns
            if new_column_upc is not None:
                scrapper._column_upc = new_column_upc
            if new_exe_path is not None:
                scrapper._exe_path = new_exe_path
            if new_results_analysis is not None:
                scrapper._results_analysis = new_results_analysis
            if new_base_files_analysis is not None:
                scrapper._base_files_analysis = new_base_files_analysis
            save_scrappers_array()
            return

    return False
    

def excelToPandas(path):   
    return pandas.read_excel(path)

def csvToPandas(path, sep):
    #THE CLIENT SHOULD HAVE AN OPTION TO CHANGE DE DELIMETER OF THE FILE IF IT IS DIFFERENT IN THE FILE THAN ;
    return pandas.read_csv(path , sep=sep)

def cleanEmptyUpc(df, columnName):
    if columnName in df.columns:
        df = df.dropna(subset=[columnName])
        # Reset the index of the DataFrame
        df = df.reset_index(drop=True)
    else:
        print(f"Column '{columnName}' does not exist in the DataFrame, columns of the df are: ", df.columns)
    return df

def mergeAndSaveDataframes(scrapper_df, scrapperColumnName, keepa_df,keepaColumnName):
    print("Combinando archivos, Columnas del scrapper CSV:", scrapper_df.columns)#Show the columns of the scrapper in case there is a mistake.
    scrapper_df[scrapperColumnName] = scrapper_df[scrapperColumnName].astype(str).str.split('.').str[0].str.zfill(13)
    keepa_df[keepaColumnName] = keepa_df[keepaColumnName].astype(str).str.split('.').str[0].str.zfill(13)
    
    # Merge the dataframes based on the "upc" column
    merged_df = pandas.merge(scrapper_df, keepa_df, left_on=scrapperColumnName, right_on=keepaColumnName, how="inner")

    return merged_df

def save_scrappers_array():
    with open('scrappers_data.json', 'w') as file:
        json.dump(array_scrappers, file, default=lambda o: o.__dict__)

# Function to load the scrappers_array from the JSON file
def load_scrappers_array():
    #print('loading scrappers')
    try:
        with open("scrappers_data.json", "r") as file:
            loaded_data = json.load(file)
    except FileNotFoundError:
        return []

    array_scrappers = []
    for scrapper_data in loaded_data:
        name = scrapper_data['_name']
        columns = scrapper_data['_columns']
        column_upc = scrapper_data['_column_upc']
        exe_path = scrapper_data['_exe_path']
        results_analysis = scrapper_data['_results_analysis']
        base_files_analysis = scrapper_data['_base_files_analysis']
        
        scrapper = Scrapper(name, columns, column_upc, exe_path, results_analysis, base_files_analysis)
        array_scrappers.append(scrapper)
        #print('scrapper appended')
    
    return array_scrappers

#Function to find the first column non empty to get the precio sugerido de venta
def find_first_non_empty(row):
    for column in array_preciosugeridoventa:
        if pandas.notnull(row[column]):
            return row[column]
    return np.nan

def fillPriorities(merged_df): 
    priorities_df=merged_df
    #CONVERT THE NEW OFFERS IN BLANK TO THE NUMBER 0
    priorities_df['New Offer Count: Current'] = priorities_df['New Offer Count: Current'].fillna(0)
    priorities_df['New Offer Count: Current'] = np.nan_to_num(priorities_df['New Offer Count: Current'], nan=0)
    
    #CREATE HE COLUMN PRIORITY WITH BLANK FIELDS
    priorities_df.loc[:, 'priority'] = pandas.NA
#FOR THE NEW OFFERS=0
    priorities_df.loc[(priorities_df['New Offer Count: Current']==0)&(priorities_df['Sales Rank: 90 days avg.'] >= 0) & (priorities_df['Sales Rank: 90 days avg.'] < 500000) & (priorities_df['roi'] >= 1), 'priority'] = '1.1'
    priorities_df.loc[(priorities_df['New Offer Count: Current']==0)&(priorities_df['Sales Rank: 90 days avg.'] >= 0) & (priorities_df['Sales Rank: 90 days avg.'] < 500000) & (priorities_df['roi'] >= 0.5) & (priorities_df['roi'] < 1), 'priority'] = '1.2'
    priorities_df.loc[(priorities_df['New Offer Count: Current']==0)&(priorities_df['Sales Rank: 90 days avg.'] >= 0) & (priorities_df['Sales Rank: 90 days avg.'] < 500000) & (priorities_df['roi'] >= 0.25) & (priorities_df['roi'] < 0.5), 'priority'] = '1.3'
    # Apply the priority values based on the additional conditions
    priorities_df.loc[(priorities_df['New Offer Count: Current']==0)&(priorities_df['Sales Rank: 90 days avg.'] >= 500000) & (priorities_df['Sales Rank: 90 days avg.'] < 1000000) & (priorities_df['roi'] > 1), 'priority'] = '2.1'
    priorities_df.loc[(priorities_df['New Offer Count: Current']==0)&(priorities_df['Sales Rank: 90 days avg.'] >= 500000) & (priorities_df['Sales Rank: 90 days avg.'] < 1000000) & (priorities_df['roi'] >= 0.5) & (priorities_df['roi'] < 1), 'priority'] = '2.2'
    priorities_df.loc[(priorities_df['New Offer Count: Current']==0)&(priorities_df['Sales Rank: 90 days avg.'] >= 500000) & (priorities_df['Sales Rank: 90 days avg.'] < 1000000) & (priorities_df['roi'] >= 0.25) & (priorities_df['roi'] < 0.5), 'priority'] = '2.3'

    priorities_df.loc[(priorities_df['New Offer Count: Current']==0)&(priorities_df['Sales Rank: 90 days avg.'] >= 1000000) & (priorities_df['Sales Rank: 90 days avg.'] < 4400000) & (priorities_df['roi'] > 1), 'priority'] = '3.1'
    priorities_df.loc[(priorities_df['New Offer Count: Current']==0)&(priorities_df['Sales Rank: 90 days avg.'] >= 1000000) & (priorities_df['Sales Rank: 90 days avg.'] < 4400000) & (priorities_df['roi'] >= 0.5) & (priorities_df['roi'] < 1), 'priority'] = '3.2'
    priorities_df.loc[(priorities_df['New Offer Count: Current']==0)&(priorities_df['Sales Rank: 90 days avg.'] >= 1000000) & (priorities_df['Sales Rank: 90 days avg.'] < 4400000) & (priorities_df['roi'] >= 0.25) & (priorities_df['roi'] < 0.5), 'priority'] = '3.3'
#FOR THE NEW OFFERS >0
    priorities_df.loc[(priorities_df['New Offer Count: Current']>0)&(priorities_df['Sales Rank: 90 days avg.'] >= 0) & (priorities_df['Sales Rank: 90 days avg.'] < 500000) & (priorities_df['roi'] >= 1), 'priority'] = '4.1'
    priorities_df.loc[(priorities_df['New Offer Count: Current']>0)&(priorities_df['Sales Rank: 90 days avg.'] >= 0) & (priorities_df['Sales Rank: 90 days avg.'] < 500000) & (priorities_df['roi'] >= 0.5) & (priorities_df['roi'] < 1), 'priority'] = '4.2'
    priorities_df.loc[(priorities_df['New Offer Count: Current']>0)&(priorities_df['Sales Rank: 90 days avg.'] >= 0) & (priorities_df['Sales Rank: 90 days avg.'] < 500000) & (priorities_df['roi'] >= 0.25) & (priorities_df['roi'] < 0.5), 'priority'] = '4.3'
    # Apply the priority values based on the additional conditions
    priorities_df.loc[(priorities_df['New Offer Count: Current']>0)&(priorities_df['Sales Rank: 90 days avg.'] >= 500000) & (priorities_df['Sales Rank: 90 days avg.'] < 1000000) & (priorities_df['roi'] > 1), 'priority'] = '5.1'
    priorities_df.loc[(priorities_df['New Offer Count: Current']>0)&(priorities_df['Sales Rank: 90 days avg.'] >= 500000) & (priorities_df['Sales Rank: 90 days avg.'] < 1000000) & (priorities_df['roi'] >= 0.5) & (priorities_df['roi'] < 1), 'priority'] = '5.2'
    priorities_df.loc[(priorities_df['New Offer Count: Current']>0)&(priorities_df['Sales Rank: 90 days avg.'] >= 500000) & (priorities_df['Sales Rank: 90 days avg.'] < 1000000) & (priorities_df['roi'] >= 0.25) & (priorities_df['roi'] < 0.5), 'priority'] = '5.3'

    priorities_df.loc[(priorities_df['New Offer Count: Current']>0)&(priorities_df['Sales Rank: 90 days avg.'] >= 1000000) & (priorities_df['Sales Rank: 90 days avg.'] < 4400000) & (priorities_df['roi'] > 1), 'priority'] = '6.1'
    priorities_df.loc[(priorities_df['New Offer Count: Current']>0)&(priorities_df['Sales Rank: 90 days avg.'] >= 1000000) & (priorities_df['Sales Rank: 90 days avg.'] < 4400000) & (priorities_df['roi'] >= 0.5) & (priorities_df['roi'] < 1), 'priority'] = '6.2'
    priorities_df.loc[(priorities_df['New Offer Count: Current']>0)&(priorities_df['Sales Rank: 90 days avg.'] >= 1000000) & (priorities_df['Sales Rank: 90 days avg.'] < 4400000) & (priorities_df['roi'] >= 0.25) & (priorities_df['roi'] < 0.5), 'priority'] = '6.3'

    return priorities_df

def setOperationsColumns(merged_df):
    #Find precio sugerido de Venta with the function
    merged_df['precio Sugerido de Venta'] = merged_df.apply(find_first_non_empty, axis=1)
    
    #Set the columns to format to be ready for operations
    merged_df['precio Sugerido de Venta']=merged_df['precio Sugerido de Venta'].astype(float)
    merged_df['Referral Fee %']=merged_df['Referral Fee %'].astype(float)
    merged_df['FBA Fees:']=merged_df['FBA Fees:'].astype(float)

    if merged_df['price'].dtype != object:  # Check if 'price' column is not already of string data type
        merged_df['price'] = merged_df['price'].astype(str)  # Convert 'price' column to string data type

    merged_df['price']=merged_df['price'].apply(lambda x: re.sub(r'[^0-9.]', '', str(x))).str.replace(',', '.').astype(float) #Scrapper sometimes the price is 49.99 or 49,99

    # Create columns in the DataFrame
    merged_df['costo logistico'] = (merged_df['Referral Fee %']*merged_df['precio Sugerido de Venta'])+10+ merged_df['FBA Fees:']
    merged_df['costo logistico']=merged_df['costo logistico'].astype(float)

    #Look the utilidad column because price column name must always be the same in scrappers
    merged_df['utilidad'] = merged_df['precio Sugerido de Venta']-merged_df['price']-merged_df['costo logistico'] 
    merged_df['utilidad']=merged_df['utilidad'].astype(float)
    merged_df['roi'] = merged_df['utilidad']/(10+merged_df['price'])
    merged_df['roi']=merged_df['roi'].astype(float)

    return merged_df

def reorderColumns(merged_df, scrapperColumns):
    columns_array=scrapperColumns.split(",") #Lo que el usuario digita es los nombres de las columnas separados con comas
    print("Reordenando Columnas, columns array", columns_array)
    keepaOrder=['precio Sugerido de Venta','costo logistico', 
       'utilidad', 'roi', 'Title','ASIN','Sales Rank: Current', 
       'Sales Rank: 90 days avg.',
       'Sales Rank: Drops last 30 days', 'Sales Rank: Drops last 90 days',
       'Sales Rank: Drops last 180 days', 'Reviews: Rating',
       'Reviews: Review Count - 90 days avg.', 'Buy Box: Current',
       'Buy Box: 90 days avg.', 'Amazon: Current', 'Amazon: 90 days avg.',
       'Amazon: Stock', 'New: Current', 'New: 90 days avg.',
       'New, 3rd Party FBA: Current', 'New, 3rd Party FBA: 90 days avg.',
       'FBA Fees:', 'Referral Fee %',
       'Referral Fee based on current Buy Box price',
       'New, 3rd Party FBM: Current', 'New, 3rd Party FBM: 90 days avg.',
       'List Price: Current', 'List Price: 90 days avg.',
       'eBay New: 90 days avg.', 'New Offer Count: Current',
       'New Offer Count: 30 days avg.', 'New Offer Count: 90 days avg.',
       'New Offer Count: 180 days avg.', 'Tracking since', 'Listed since',
       'URL: Amazon', 'ASIN', 'Product Codes: EAN', 'Product Codes: UPC',
       'Parent ASIN', 'Variation ASINs', 'Manufacturer', 'Brand',
       'Product Group', 'Model', 'Variation Attributes', 'Color', 'Size',
       'Author', 'Contributors', 'Number of Items', 'Number of Pages',
       'Publication Date', 'Package: Weight (g)', 'Adult Product' ]
    newOrder=columns_array+keepaOrder #Primero aparece las columnas del scrapper luego las de keepa
    merged_df=merged_df[newOrder]
    return merged_df

def createExcel(dataframe, path):
    dataframe.to_excel(path)