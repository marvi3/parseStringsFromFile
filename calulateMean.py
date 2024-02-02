import pandas as pd
import sys
import xls

# def getStartEndRows():


def calculateAveragesColumns(inputFile, outputFile, startRows=0, endRows=0):
    df = pd.read_csv(inputFile)
    numColumns = len(df.columns)
    if startRows == 0 and endRows == 0:
        startRows = [0] * numColumns
        endRows = [len(df) - 1] * numColumns
    elif type(startRows) == int:
        if type(endRows) == int:
            startRows = [startRows] * numColumns
            endRows = [endRows] * numColumns
        elif type(endRows) == list:
            startRows = [startRows] * numColumns
        else:
            print("Wrong typ of the endRows")
            return
    elif type(endRows) == list:
        if type(startRows) == int:
            startRows = [startRows] * numColumns
        elif type(endRows) != list:
            print("Wrong typ of the endRows")
            return
    else:
        print("Wrong typ of the startRows")
        return

    if len(endRows) != numColumns:
        print("Wrong length of the endRows")
        return
    if len(startRows) != numColumns:
        print("Wrong length of the startRows")
        return

    averages = {i: df.iloc[startRows[i]:endRows[i], i].mean() for i in range(1,numColumns)}
    averageDf = xls.createCsvFrame(numColumns, 2)
    averageDf.iloc[0,0:len(averages)] = averages
    xls.createCsvFile(outputFile, averageDf)


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    if len(sys.argv) < 4:
        print("Usage: python calculateMean.py csvToBeRead.csv csvToWrite.csv c/r(for column or row)")
        sys.exit(0)
    if sys.argv[3] == "c":
        calculateAveragesColumns(sys.argv[1],sys.argv[2])