import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))# Get the current directory of main.py
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))# Get the parent directory by going one level up
sys.path.append(parent_dir)# Append the parent directory to sys.path
import json
import pandas
import csv
import tkinter as tk

def excelToPandas(path):   
    print("accesing excel to pandas") 
    return pandas.read_excel(path)

def csvToPandas(path, sep):
    #THE CLIENT SHOULD HAVE AN OPTION TO CHANGE DE DELIMETER OF THE FILE IF IT IS DIFFERENT IN THE FILE THAN ;
    print("accesing excel to pandas") 
    return pandas.read_csv(path , sep=sep)

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

