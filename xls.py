# This script requires the installation of xlwt, openpyxl and xlrd

import pandas as pd
import openpyxl
import time

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

def add_strings_to_row(row_index, file_name, strings):
    # Try to read the existing CSV file into a DataFrame, if it exists
    try:
        df = pd.read_csv(file_name)
    except FileNotFoundError:
        df = pd.DataFrame()

    # Expand the DataFrame if there are not enough rows
    if row_index >= len(df):
        # Append empty rows
        extra_rows = row_index - len(df) + 1
        df = pd.concat([df, pd.DataFrame([[''] * len(df.columns)] * extra_rows)], ignore_index=True)

    # Expand the DataFrame if there are not enough columns
    if len(strings) > len(df.columns):
        # Add extra columns
        extra_cols = len(strings) - len(df.columns)
        for i in range(extra_cols):
            df[f'Column_{len(df.columns) + 1}'] = pd.NA

    # Add the array of strings into the specified row
    df.loc[row_index, :len(strings) - 1] = strings

# A method that modifies one row of an Csv sheet
# The row starts at 0
def modifyRow(row, file, data):
    startTime = time.time()
    try:
        df = pd.read_csv(file, header=None)
    except FileNotFoundError:
        print("being in excpetion")
        df = pd.DataFrame()

    lapTime1 = time.time()
    if row >= len(df):
        extraRows = row - len(df) + 1
        df = pd.concat([df, pd.DataFrame([[''] * len(df.columns)] * extraRows)], ignore_index=True)
    lapTime2 = time.time()
    
    if len(data) > len(df.columns):
        extraCols = len(data) - len(df.columns)
        for i in range(extraCols):
            df[f'Column_{len(df.columns) + 1}'] = pd.NA
    lapTime3 = time.time()
    df.iloc[row,0:len(data)] = data

    lapTime4 = time.time()
    df.to_csv(file, index=False, header=False)
    endTime = time.time()
    return [lapTime1 - startTime, lapTime2 - lapTime1, lapTime3 - lapTime2, lapTime4 - lapTime3, endTime - lapTime4]

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
