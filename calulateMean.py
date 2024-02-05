import pandas as pd
import sys
import xls
from datetime import datetime, timedelta
import locale
import time



def calculateEndDateStr(startDateStr, seconds):
    # Convert the input start_date_str to a datetime object
    startDate = datetime.strptime(startDateStr, '%d.%m.%Y %H:%M')

    # Calculate the end date by adding the specified number of seconds
    endDate = startDate + timedelta(seconds=seconds)

    # Return the end date as a string
    return endDate.strftime('%d.%m.%Y %H:%M')



def calculateEndDate(startDate, seconds):
    # Calculate the end date by adding the specified number of seconds
    endDate = (startDate + timedelta(seconds=int(seconds))).replace(second=0, microsecond=0)

    # Return the end date
    return endDate



def convertDate(dateString):
    # print(dateString)
    strMod = dateString.split(" ")
    strMod = strMod[1:4] + strMod[5:6]
    strMod = ' '.join(strMod)

    formatString = "%d. %b %H:%M:%S %Y"
    locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')

    return datetime.strptime(strMod, formatString).replace(second=0, microsecond=0)



def init2DArray(rows, columns, initialValue):
    return [[initialValue for i in range(columns)] for j in range(rows)]


def getStartEndRows(runPeriods="runPeriods.csv", coresFile="cpuCoreForRun.csv", startsFile="startingTime.csv", runningFile="runningTime.csv", cpuRun1File="CPUUserPerRun1.csv", cpuRun2File="CPUUserPerRun2.csv", cpuRun3File="CPUUserPerRun3.csv"):
    runPeriods = xls.readCsv(runPeriods)
    # cores = xls.readCsv(coresFile)
    starts = xls.readCsv(startsFile)
    running = xls.readCsv(runningFile)
    cpuRun1 = xls.readCsv(cpuRun1File)
    cpuRun2 = xls.readCsv(cpuRun2File)
    cpuRun3 = xls.readCsv(cpuRun3File)
    numRuns = len(starts.columns) - 2
    numSutFuzzer = len(starts) - 1
    startRows = init2DArray(numSutFuzzer, numRuns, 0)
    startWeeks = init2DArray(numSutFuzzer, numRuns, 0)
    endRows = init2DArray(numSutFuzzer, numRuns, 0)
    endWeeks = init2DArray(numSutFuzzer, numRuns, 0)

    for row in range(1,numSutFuzzer + 1):
        for column in range(2,numRuns + 2):
            if(type(starts.iloc[row,column]) != str or starts.iloc[row,column] == "WIEDERH"):
                continue
            startDate = datetime.strptime(starts.iloc[row,column], '%d.%m.%Y %H:%M')
            duration = running.iloc[row, column]
            endDate = calculateEndDate(startDate, duration)
            # core = cores.iloc[row,column]
            weekStart = 0
            weekEnd = 0
            for period in range(1,len(runPeriods.columns)):
                startPeriod = datetime.strptime(runPeriods.iloc[1, period], '%d.%m.%Y %H:%M')
                endPeriod = datetime.strptime(runPeriods.iloc[2, period], '%d.%m.%Y %H:%M')
                if startDate >= startPeriod and startDate <= endPeriod:
                    weekStart = period
                    break
                # elif startDate < datetime.strptime(runPeriods.iloc[1, 1], '%d.%m.%Y %H:%M'):
                #     weekStart = period - 0.5
                #     break
                # elif startDate < startPeriod and startDate < datetime.strptime(runPeriods.iloc[2, period - 1], '%d.%m.%Y %H:%M'):
                #     weekEnd = period - 0.5
            for period in range(1,len(runPeriods.columns)):
                startPeriod = datetime.strptime(runPeriods.iloc[1, period], '%d.%m.%Y %H:%M')
                endPeriod = datetime.strptime(runPeriods.iloc[2, period], '%d.%m.%Y %H:%M')
                if endDate >= startPeriod and endDate <= endPeriod:
                    weekEnd = period
                    break
                elif period == len(runPeriods.columns) - 1:
                    weekEnd = float(period) + 0.5
                    break
                elif endDate > startPeriod and endDate < datetime.strptime(runPeriods.iloc[1, period + 1], '%d.%m.%Y %H:%M'):
                    weekEnd = float(period) + 0.5
                    break
            if weekStart == 0:
                print("The startdate", startDate, "of column", column, "and row", row, "doesn't seem to be within the recorded period")
                if weekEnd == 0:
                    print("The enddate", endDate, "of column", column, "and row", row, "doesn't seem to be within the recorded period")
                    sys.exit(1)
                sys.exit(1)
            if weekEnd == 0:
                print("The enddate", endDate, "of column", column, "and row", row, "doesn't seem to be within the recorded period")
                sys.exit(1)
            
            continueWhile = True
            if weekStart == 1:
                timeRow = round((startDate - convertDate(cpuRun1.iloc[1, 0])).total_seconds() / 11) + 1
                while continueWhile:
                    if ((startDate - convertDate(cpuRun1.iloc[timeRow, 0])).total_seconds()) < 0:
                        timeRow += round((startDate - convertDate(cpuRun1.iloc[timeRow, 0])).total_seconds() / 9)
                    elif ((startDate - convertDate(cpuRun1.iloc[timeRow, 0])).total_seconds()) < 1000:
                        for timeRow in range(timeRow, len(cpuRun1)):
                            if convertDate(cpuRun1.iloc[timeRow, 0]) == startDate:
                                startWeeks[row - 1][column - 2] = weekStart
                                startRows[row - 1][column - 2] = timeRow
                                continueWhile = False
                                break
                    else:
                        timeRow += round((startDate - convertDate(cpuRun1.iloc[timeRow, 0])).total_seconds() / 11)
            elif weekStart == 2:
                timeRow = round((startDate - convertDate(cpuRun2.iloc[1, 0])).total_seconds() / 11) + 1
                while continueWhile:
                    if ((startDate - convertDate(cpuRun2.iloc[timeRow, 0])).total_seconds()) < 0:
                        timeRow += round((startDate - convertDate(cpuRun2.iloc[timeRow, 0])).total_seconds() / 9)
                    elif ((startDate - convertDate(cpuRun2.iloc[timeRow, 0])).total_seconds()) < 1000:
                        for timeRow in range(timeRow, len(cpuRun2)):
                            if convertDate(cpuRun2.iloc[timeRow, 0]) == startDate:
                                startWeeks[row - 1][column - 2] = weekStart
                                startRows[row - 1][column - 2] = timeRow
                                continueWhile = False
                                break
                    else:
                        timeRow += round((startDate - convertDate(cpuRun2.iloc[timeRow, 0])).total_seconds() / 11)
            elif weekStart == 3:
                timeRow = round((startDate - convertDate(cpuRun3.iloc[1, 0])).total_seconds() / 11) + 1
                while continueWhile:
                    if ((startDate - convertDate(cpuRun3.iloc[timeRow, 0])).total_seconds()) < 0:
                        timeRow += round((startDate - convertDate(cpuRun3.iloc[timeRow, 0])).total_seconds() / 9)
                    elif ((startDate - convertDate(cpuRun3.iloc[timeRow, 0])).total_seconds()) < 1000:
                        for timeRow in range(timeRow, len(cpuRun3)):
                            if convertDate(cpuRun3.iloc[timeRow, 0]) == startDate:
                                startWeeks[row - 1][column - 2] = weekStart
                                startRows[row - 1][column - 2] = timeRow
                                continueWhile = False
                                break
                    else:
                        timeRow += round((startDate - convertDate(cpuRun3.iloc[timeRow, 0])).total_seconds() / 11)
            
            continueWhile = True
            if weekEnd == 1:
                timeRow = round((endDate - convertDate(cpuRun1.iloc[1, 0])).total_seconds() / 11) + 1
                while continueWhile:
                    if ((endDate - convertDate(cpuRun1.iloc[timeRow, 0])).total_seconds()) < 0:
                        timeRow += round((endDate - convertDate(cpuRun1.iloc[timeRow, 0])).total_seconds() / 9)
                    elif ((endDate - convertDate(cpuRun1.iloc[timeRow, 0])).total_seconds()) < 1000:
                        for timeRow in range(timeRow, len(cpuRun1)):
                            if convertDate(cpuRun1.iloc[timeRow, 0]) == endDate:
                                endWeeks[row - 1][column - 2] = weekEnd
                                endRows[row - 1][column - 2] = timeRow
                                continueWhile = False
                                break
                    else:
                        timeRow += round((endDate - convertDate(cpuRun1.iloc[timeRow, 0])).total_seconds() / 11)
            elif weekEnd == 2:
                timeRow = round((endDate - convertDate(cpuRun2.iloc[1, 0])).total_seconds() / 11) + 1
                while continueWhile:
                    if ((endDate - convertDate(cpuRun2.iloc[timeRow, 0])).total_seconds()) < 0:
                        timeRow += round((endDate - convertDate(cpuRun2.iloc[timeRow, 0])).total_seconds() / 9)
                    elif ((endDate - convertDate(cpuRun2.iloc[timeRow, 0])).total_seconds()) < 1000:
                        for timeRow in range(timeRow, len(cpuRun2)):
                            if convertDate(cpuRun2.iloc[timeRow, 0]) == endDate:
                                endWeeks[row - 1][column - 2] = weekEnd
                                endRows[row - 1][column - 2] = timeRow
                                continueWhile = False
                                break
                    else:
                        timeRow += round((endDate - convertDate(cpuRun2.iloc[timeRow, 0])).total_seconds() / 11)
            elif weekEnd == 3:
                timeRow = round((endDate - convertDate(cpuRun3.iloc[1, 0])).total_seconds() / 11) + 1
                while continueWhile:
                    if ((endDate - convertDate(cpuRun3.iloc[timeRow, 0])).total_seconds()) < 0:
                        timeRow += round((endDate - convertDate(cpuRun3.iloc[timeRow, 0])).total_seconds() / 9)
                    elif ((endDate - convertDate(cpuRun3.iloc[timeRow, 0])).total_seconds()) < 1000:
                        for timeRow in range(timeRow, len(cpuRun3)):
                            if convertDate(cpuRun3.iloc[timeRow, 0]) == endDate:
                                endWeeks[row - 1][column - 2] = weekEnd
                                endRows[row - 1][column - 2] = timeRow
                                continueWhile = False
                                break
                    else:
                        timeRow += round((endDate - convertDate(cpuRun3.iloc[timeRow, 0])).total_seconds() / 11)
            elif weekEnd == 3.5:
                endWeeks[row - 1][column - 2] = weekEnd
                endRows[row - 1][column - 2] = len(cpuRun3) - 2
                # print("The enddate", endDate, "of column", column, "and row", row, "doesn't seem to be within the recorded period. The enddate has been set to", convertDate(cpuRun3.iloc[endRows[row - 1][column - 2], 0]))
    
    return [startRows, startWeeks, endRows, endWeeks]



def calculateAveragesColumns(inputFile, outputFile, startRows=0, endRows=0, startPeriod=0, endPeriod=0):
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
    # for i in range(0, len(startRows)):
    #     print("\n\n\nrow", i + 1)
    #     print(startRows[i])
    #     print(startWeeks[i])
    #     print(endRows[i])
    #     print(endWeeks[i])

    # if len(sys.argv) < 4:
    #     print("Usage: python calculateMean.py csvToBeRead.csv csvToWrite.csv c/r(for column or row)")
    #     sys.exit(0)
    # if sys.argv[3] == "c":
    #     calculateAveragesColumns(sys.argv[1],sys.argv[2])