import pandas as pd
import sys
import xls
from datetime import datetime, timedelta


def calculate_end_date(start_date_str, seconds):
    # Convert the input start_date_str to a datetime object
    start_date = datetime.strptime(start_date_str, '%d.%m.%Y %H:%M')

    # Calculate the end date by adding the specified number of seconds
    end_date = start_date + timedelta(seconds=seconds)

    # Return the end date as a string
    return end_date.strftime('%d.%m.%Y %H:%M')

def getStartEndRows(weekFile="weekForRun.csv", coresFile="cpuCureForRun.csv", startsFile="startingTime.csv", runningFile="runningTime.csv", cpuRun1File="CPUUserPerRun1.csv", cpuRun2File="CPUUserPerRun2.csv", cpuRun3File="CPUUserPerRun3.csv"):
    weeks = xls.readCsv(weekFile)
    cores = xls.readCsv(coresFile)
    starts = xls.readCsv(startsFile)
    running = xls.readCsv(runningFile)
    cpuRun1 = xls.readCsv(cpuRun1File)
    cpuRun2 = xls.readCsv(cpuRun2File)
    cpuRun3 = xls.readCsv(cpuRun3File)
    numRuns = len(weeks.columns) - 2
    numSutFuzzer = len(weeks) - 1
    startRows = [[0] * numRuns] * numSutFuzzer
    startWeeks = [[0] * numRuns] * numSutFuzzer
    endRows = [[0] * numRuns] * numSutFuzzer
    endWeeks = [[0] * numRuns] * numSutFuzzer

    for row in range(1,numSutFuzzer + 1):
        for column in range(2,numRuns + 2):
            week = weeks.iloc[row, column].split(",")
            if len(week) == 1:
                weekStart = week[0]
                weekEnd = week[0]
            elif len(week) == 2:
                weekStart = week[0]
                weekEnd = week[1]
            else:
                print("A week-field can not have less than one or more than two entries but", row, column, "did.")
                sys.exit(1)
            core = cores.iloc[row,column]
            start = starts.iloc[row,column]
            duration = running.iloc[row, column]
            end = calculate_end_date([start, duration])
            if int(weekStart) == 1:
                for row in range(0, len(cpuRun1)):
                    if str(cpuRun1.iloc[row, 0]).startswith(start):
                        startWeeks[row, column] = weekStart
                        startRows[row, column] = row
                        break
            elif int(weekStart) == 2:
                for row in range(0, len(cpuRun2)):
                    if str(cpuRun2.iloc[row, 0]).startswith(start):
                        startWeeks[row, column] = weekStart
                        startRows[row, column] = row
                        break
            elif int(weekStart) == 3:
                for row in range(0, len(cpuRun3)):
                    if str(cpuRun3.iloc[row, 0]).startswith(start):
                        startWeeks[row, column] = weekStart
                        startRows[row, column] = row
                        break
            
            if int(weekEnd) == 1:
                for row in range(len(cpuRun1), 0):
                    if str(cpuRun1.iloc[row, 0]).startswith(end):
                        endWeeks[row, column] = weekEnd
                        endRows[row, column] = row
                        break
            elif int(weekEnd) == 2:
                for row in range(len(cpuRun2), 0):
                    if str(cpuRun2.iloc[row, 0]).startswith(end):
                        endWeeks[row, column] = weekEnd
                        endRows[row, column] = row
                        break
            elif int(weekEnd) == 3:
                for row in range(len(cpuRun3), 0):
                    if str(cpuRun3.iloc[row, 0]).startswith(end):
                        endWeeks[row, column] = weekEnd
                        endRows[row, column] = row
                        break
    
    return [startRows, startWeeks, endRows, endWeeks]






def calculateAveragesColumns(inputFiles, outputFile, startRows=0, endRows=0):
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
    startRows, startWeeks, endRows, endWeeks = getStartEndRows()
    if len(sys.argv) < 4:
        print("Usage: python calculateMean.py csvToBeRead.csv(if multiple separate with comma) csvToWrite.csv c/r(for column or row)")
        sys.exit(0)
    if sys.argv[3] == "c":
        calculateAveragesColumns(sys.argv[1].split(","),sys.argv[2])