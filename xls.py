# This script requires the installation of xlwt, openpyxl and xlrd

import pandas as pd
import openpyxl

# A method that modifies only one cell
# The row and col start at 0
def modifyCell(row, col, file, data):
    df = pd.read_excel(file)
    df.loc[row, col] = data.strip()
    df.to_excel(file, index=False, header=False)

# A method that modifies one row of an excel sheet
# The row starts at 0
def modifyRow(row, file, data):
    try:
        df = pd.read_excel(file)
        for i in range(len(data)):
            df.loc[row, i] = data[i].strip()
    except:
        print("being in excpetion")
        df = pd.DataFrame([data])
#        for i in range(len(data)):
#            df.loc[i, row] = data[i].strip()
    df.to_csv(file, index=False, header=False)

# A method that writes a two-dimensional array to an excel sheet.
# It might overwrite existing excel sheets
# The row and col start at 1
def writeExcelFile(file, data):
    df = pd.DataFrame(data)
    df.to_excel(file)

def writeExcelFile(file, data, rowNames, columnNames):
    df = pd.DataFrame(data, index=rowNames, columns=columnNames)
    df.to_excel(file)
