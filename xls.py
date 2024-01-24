# This script requires the installation of xlwt, openpyxl and xlrd

import pandas as pd
import openpyxl

# A method that modifies only one cell
# The row and col start at 0
def modifyCell(row, col, file, data):
    try:
        df = pd.read_csv(file)
        df.loc[row, col] = data.strip()
    except:
        print("being in excpetion")
        df = pd.DataFrame([""])
        df.loc[row, col] = data.strip()
    df.to_csv(file, index=False, header=False)

# A method that modifies one row of an Csv sheet
# The row starts at 0
def modifyRow(row, file, data):
    try:
        df = pd.read_csv(file)
    except FileNotFoundError:
        df = pd.DataFrame()
    
    if row >= len(df):
        extraRows = row - len(df) + 1
        df = pd.concat([df, pd.DataFrame([[''] * len(df.columns)] * extraRows)], ignore_index=True)
    
    if len(data) > len(df.columns):
        extraCols = len(data) - len(df.columns)
        for i in range(extraCols):
            df[f'Column_{len(df.columns) + 1}'] = pd.NA
    print(row)
    df.iloc[row,0:len(data)] = data
    df.to_csv(file, index=False, header=False)

def oldModifyRow(row, file, data):
    try:
        df = pd.read_csv(file)
        for i in range(len(data)):
            df.loc[i, row] = data[i].strip()
            df.loc[row] = data
    except:
        print("being in excpetion")
        df = pd.DataFrame([data])
        for i in range(len(data)):
            df.loc[i, row] = data[i].strip()
    df.to_csv(file, index=False, header=False)

# A method that writes a two-dimensional array to an Csv sheet.
# It might overwrite existing Csv sheets
# The row and col start at 1
def writeCsvFile(file, data):
    df = pd.DataFrame(data)
    df.to_csv(file)

def writeCsvFileColRow(file, data, rowNames, columnNames):
    df = pd.DataFrame(data, index=rowNames, columns=columnNames)
    df.to_csv(file)
