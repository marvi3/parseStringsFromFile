import pandas as pd
import sys

def copyColumns(inputFile, outputFile, columnsToCopy):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(inputFile)

        # Check if specified columns exist in the input file
        if any(index >= len(df.columns) for index in columnsToCopy):
            print(f"One or more columns where not found in the input file {inputFile}.")
            return

        print(f"The programm will copy {columnsToCopy} from {inputFile} into {outputFile}")

        # Create a new DataFrame with the specified columns
        dfSelectedColumns = df.iloc[:,columnsToCopy]

        # Write the selected columns to the output CSV file
        dfSelectedColumns.to_csv(outputFile, index=False)

        print("Columns copied successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    if len(sys.argv) < 4:
        print("Usage: python copyCsvColumnsIntoNewFile.py csvToBeRead.csv csvToWrite.csv commaSeparatedListOfColumnsToCopy")
        sys.exit(0)
    copyColumns(sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(",")])
