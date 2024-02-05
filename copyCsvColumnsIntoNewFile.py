import pandas as pd
import sys
import time

def sumRowsOfColumns(df):
    return df.sum(axis=1)

def copyColumns(inputFile, outputFile, columnsToCopy, sumRight=1):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(inputFile)

        # Check if specified columns exist in the input file
        if any(index >= len(df.columns) for index in columnsToCopy):
            print(f"One or more columns where not found in the input file {inputFile}.")
            return

        # Create a new DataFrame with the specified columns
        dfSelectedColumns = pd.DataFrame()
        for column in columnsToCopy:
            if column == 0:
                dfSelectedColumns = pd.concat([dfSelectedColumns, df.iloc[:,int(column)]], axis=1)
                # print(dfSelectedColumns)
            else:
                dfSelectedColumns = pd.concat([dfSelectedColumns, df.iloc[:,int(column): int(column) + int(sumRight)].sum(axis=1)], axis=1)

        print(f"The programm will copy {columnsToCopy} from {inputFile} into {outputFile}")

        # Write the selected columns to the output CSV file
        dfSelectedColumns.to_csv(outputFile, index=False)

        print("Columns copied successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    if len(sys.argv) < 4:
        print("Usage: python copyCsvColumnsIntoNewFile.py csvToBeRead.csv csvToWrite.csv commaSeparatedListOfColumnsToCopy(optional)")
        sys.exit(0)
    if len(sys.argv) > 4:
        copyColumns(sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(",")], sys.argv[4])
    else:
        copyColumns(sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(",")])
