import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))# Get the current directory of main.py
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))# Get the parent directory by going one level up
sys.path.append(parent_dir)# Append the parent directory to sys.path
import pandas
import csv
import tkinter as tk
import numpy as np

#ARRAY WITH THE ORDER TO GET THE PRECIO SUGERIDO
array_preciosugeridoventa=['New, 3rd Party FBA: 90 days avg.','Buy Box: 90 days avg.','List Price: 90 days avg.','New, 3rd Party FBM: 90 days avg.','Amazon: 90 days avg.','New: 90 days avg.','New, 3rd Party FBA: Current','Buy Box: Current','List Price: Current','New, 3rd Party FBM: Current','Amazon: Current','New: Current']

def excelToPandas(path):   
    return pandas.read_excel(path)

def csvToPandas(path, sep):
    #THE CLIENT SHOULD HAVE AN OPTION TO CHANGE DE DELIMETER OF THE FILE IF IT IS DIFFERENT IN THE FILE THAN ;
    return pandas.read_csv(path , sep=sep)

def cleanEmptyUpc(df, columnName):
    # Drop rows where "upc" column is empty
    df = df.dropna(subset=[columnName])

    # Reset the index of the DataFrame
    df = df.reset_index(drop=True)

    return df
def mergeAndSaveDataframes(scrapper_df, scrapperColumnName, keepa_df,keepaColumnName):
    
    scrapper_df[scrapperColumnName] = scrapper_df[scrapperColumnName].astype(str).str.split('.').str[0].str.zfill(13)
    keepa_df[keepaColumnName] = keepa_df[keepaColumnName].astype(str).str.split('.').str[0].str.zfill(13)
    
    # Merge the dataframes based on the "upc" column
    merged_df = pandas.merge(scrapper_df, keepa_df, left_on=scrapperColumnName, right_on=keepaColumnName, how="inner")

    return merged_df

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
    priorities_df.loc[(priorities_df['New Offer Count: Current']==0)&(priorities_df['Sales Rank: 90 days avg.'] >= 500) & (priorities_df['Sales Rank: 90 days avg.'] < 1000000) & (priorities_df['roi'] > 1), 'priority'] = '2.1'
    priorities_df.loc[(priorities_df['New Offer Count: Current']==0)&(priorities_df['Sales Rank: 90 days avg.'] >= 500) & (priorities_df['Sales Rank: 90 days avg.'] < 1000000) & (priorities_df['roi'] >= 0.5) & (priorities_df['roi'] < 1), 'priority'] = '2.2'
    priorities_df.loc[(priorities_df['New Offer Count: Current']==0)&(priorities_df['Sales Rank: 90 days avg.'] >= 500) & (priorities_df['Sales Rank: 90 days avg.'] < 1000000) & (priorities_df['roi'] >= 0.25) & (priorities_df['roi'] < 0.5), 'priority'] = '2.3'

    priorities_df.loc[(priorities_df['New Offer Count: Current']==0)&(priorities_df['Sales Rank: 90 days avg.'] >= 1000000) & (priorities_df['Sales Rank: 90 days avg.'] < 4400000) & (priorities_df['roi'] > 1), 'priority'] = '3.1'
    priorities_df.loc[(priorities_df['New Offer Count: Current']==0)&(priorities_df['Sales Rank: 90 days avg.'] >= 1000000) & (priorities_df['Sales Rank: 90 days avg.'] < 4400000) & (priorities_df['roi'] >= 0.5) & (priorities_df['roi'] < 1), 'priority'] = '3.2'
    priorities_df.loc[(priorities_df['New Offer Count: Current']==0)&(priorities_df['Sales Rank: 90 days avg.'] >= 1000000) & (priorities_df['Sales Rank: 90 days avg.'] < 4400000) & (priorities_df['roi'] >= 0.25) & (priorities_df['roi'] < 0.5), 'priority'] = '3.3'
#FOR THE NEW OFFERS >0
    priorities_df.loc[(priorities_df['New Offer Count: Current']>0)&(priorities_df['Sales Rank: 90 days avg.'] >= 0) & (priorities_df['Sales Rank: 90 days avg.'] < 500000) & (priorities_df['roi'] >= 1), 'priority'] = '4.1'
    priorities_df.loc[(priorities_df['New Offer Count: Current']>0)&(priorities_df['Sales Rank: 90 days avg.'] >= 0) & (priorities_df['Sales Rank: 90 days avg.'] < 500000) & (priorities_df['roi'] >= 0.5) & (priorities_df['roi'] < 1), 'priority'] = '4.2'
    priorities_df.loc[(priorities_df['New Offer Count: Current']>0)&(priorities_df['Sales Rank: 90 days avg.'] >= 0) & (priorities_df['Sales Rank: 90 days avg.'] < 500000) & (priorities_df['roi'] >= 0.25) & (priorities_df['roi'] < 0.5), 'priority'] = '4.3'
    # Apply the priority values based on the additional conditions
    priorities_df.loc[(priorities_df['New Offer Count: Current']>0)&(priorities_df['Sales Rank: 90 days avg.'] >= 500) & (priorities_df['Sales Rank: 90 days avg.'] < 1000000) & (priorities_df['roi'] > 1), 'priority'] = '5.1'
    priorities_df.loc[(priorities_df['New Offer Count: Current']>0)&(priorities_df['Sales Rank: 90 days avg.'] >= 500) & (priorities_df['Sales Rank: 90 days avg.'] < 1000000) & (priorities_df['roi'] >= 0.5) & (priorities_df['roi'] < 1), 'priority'] = '5.2'
    priorities_df.loc[(priorities_df['New Offer Count: Current']>0)&(priorities_df['Sales Rank: 90 days avg.'] >= 500) & (priorities_df['Sales Rank: 90 days avg.'] < 1000000) & (priorities_df['roi'] >= 0.25) & (priorities_df['roi'] < 0.5), 'priority'] = '5.3'

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
    merged_df['price']=merged_df['price'].str.replace(',', '.').astype(float) #Scrapper sometimes the price is 49.99 or 49,99

    # Create columns in the DataFrame
    merged_df['costo logistico'] = (merged_df['Referral Fee %']*merged_df['precio Sugerido de Venta'])+10+ merged_df['FBA Fees:']
    merged_df['costo logistico']=merged_df['costo logistico'].astype(float)

    #Look the utilidad column because price column name must always be the same in scrappers
    merged_df['utilidad'] = merged_df['precio Sugerido de Venta']-merged_df['price']-merged_df['costo logistico'] 
    merged_df['utilidad']=merged_df['utilidad'].astype(float)
    merged_df['roi'] = merged_df['utilidad']/(10+merged_df['price'])
    merged_df['roi']=merged_df['roi'].astype(float)

    return merged_df

def reorderColumns(merged_df):
    newOrder=['Title','ASIN', 'upc (ean)','precio Sugerido de Venta','price','costo logistico', 
       'utilidad', 'roi','availability', 'sku','title','OriginalPrice','Sales Rank: Current', 
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
    merged_df=merged_df[newOrder]
    return merged_df

def createExcel(dataframe, path):
    dataframe.to_excel(path)