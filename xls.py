# This script requires the installation of xlwt, openpyxl and xlrd

import pandas as pd
import openpyxl
import time
import warnings

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

def readCsv(file):
    try:
        df = pd.read_csv(file, header=None)
    except FileNotFoundError:
        print("Could not find the file")
        df = pd.DataFrame()
    return df

def createCsvFile(fileName, data=''):
    if type(data) is str:
        df = pd.DataFrame()
    else:
        df = data
    print("Writing to file", fileName)
    df.to_csv(fileName, mode='w', index=False, header=False)
    return df

def createCsvFrame(col = 1, rows = 1):
    df = pd.DataFrame([[''] * col] * rows)
    return df

def appendCsv(fileName, df):
    df.to_csv(fileName, mode='a', index=False, header=False)

# A method that modifies one row of an Csv sheet
# The row starts at 0
def modifyRow(row, df, data, appendRows):
    
    warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
    if max([row, appendRows - 1]) >= len(df):
        startTime = time.time()
        lenbefore = len(df)
        extraRows = max([row, appendRows]) - len(df) - 1
        df = pd.concat([df, pd.DataFrame([[''] * len(df.columns)] * extraRows)], ignore_index=True)
        # print("Expanding the rows from", lenbefore, "to", len(df) + 1, "took", round(time.time() - startTime, 2), "seconds.")
    
    if len(data) > len(df.columns):
        extraCols = len(data) - len(df.columns)
        # print("Expanding the columns from", len(df.columns), "to", len(data))
        df = pd.concat([df, pd.DataFrame([[''] * len(data)])], ignore_index=True)
        # for i in range(len(df.columns), len(data)):
        #     df[f'Column_{len(df.columns) + 1}'] = pd.NA
    df.iloc[row,0:len(data)] = data
    return df

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
