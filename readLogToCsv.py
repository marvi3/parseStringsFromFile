# This script needs the following input data:
#   filename to be read
#   Csv filename to be written
#   

import sys
import xls
import parseString
import time
from operator import add

# Checks if less then 3 arguments are existing.
if len(sys.argv) < 4:
    print("Usage: python readDataToCsv.py fileNameToBeRead csvToWrite.csv, numOfLogEntries")
    sys.exit(0)

startTime = time.time()
# opens the file to be read
filePath = sys.argv[1]
fileContent = parseString.readFile(filePath)
if fileContent is None:
    print("The file is empty")
    sys.exit(0)
endTime = time.time()
print(f"The file {sys.argv[1]} has been opened. It took", endTime-startTime, "seconds.")


startStringList = []
stringLengthList = []
occList = []
cutFromBeginningList = []
# The following information of each log entry is extraced from the log file:
# Time (later copied directly)

# Tctl temperature 1-8
startStringList.append("Tctl:")
stringLengthList.append(21)
occList.append(1)
cutFromBeginningList.append(0)

# Tccd temperature 1-8
startStringList.append("Tccd")
stringLengthList.append(21)
occList.append(8)
cutFromBeginningList.append(2)

# Composite temperature
startStringList.append("Composite:")
stringLengthList.append(21)
occList.append(1)
cutFromBeginningList.append(0)

# Sensor 1 and 2 temperature
startStringList.append("Sensor")
stringLengthList.append(21)
occList.append(2)
cutFromBeginningList.append(3)

# CPU usage from average CPU usage:
startStringList.append("Durchschn.:")
stringLengthList.append(193)
occList.append(1)
cutFromBeginningList.append(103)

# CPU usage from core 0-63:
startStringList.append("Durchschn.:")
stringLengthList.append(96)
occList.append(64)
cutFromBeginningList.append(5)
#   %usr
#   %sys
#   %iowait
#   %soft
#   %idle

reportEveryRounds = 10000
if len(sys.argv) > 4:
    reportEveryRounds = int(sys.argv[4])
logResult = []
entryNumber = 0
startIndex = 0
endIndex = 0
fileName = sys.argv[2]
df = xls.createCsvFile(fileName)
numOfEntries = int(sys.argv[3])
startTime = time.time()
roundTime = startTime
prepareTime = 0
splitTime = 0
writeTime = 0
fileContent = "\n\n\n" + fileContent
entryResult = []
endIndex = fileContent.find("__________", endIndex + 1)
if endIndex != -1:
    logEntryString = fileContent[startIndex:endIndex]
    entryResult.append(logEntryString.splitlines()[3])
    startIndex = endIndex
    entryResult = entryResult + parseString.getSubstringLengthList(logEntryString, startStringList, stringLengthList, occList, True, cutFromBeginningList)
    df = xls.modifyRow(entryNumber % reportEveryRounds, df, range(len(entryResult)), reportEveryRounds)
    entryNumber += 1
    df = xls.modifyRow(entryNumber % reportEveryRounds, df, entryResult, reportEveryRounds)
    entryNumber += 1
if int(sys.argv[3]) == 0:
    print("Processing the whole log-file.")
    partStartTime = time.time()
    writeTime += time.time() - partStartTime
    while True:
        partStartTime = time.time()
        entryResult = []
        endIndex = fileContent.find("__________", endIndex + 1)
        if endIndex != -1:
            logEntryString = fileContent[startIndex:endIndex]
            entryResult.append(logEntryString.splitlines()[3])
            startIndex = endIndex
            entryResult = entryResult + parseString.getSubstringLengthList(logEntryString, startStringList, stringLengthList, occList, True, cutFromBeginningList)
            df = xls.modifyRow(entryNumber % reportEveryRounds, df, entryResult, reportEveryRounds)
            entryNumber += 1
            if entryNumber % reportEveryRounds == 0:
                xls.appendCsv(fileName, df)
                endTime = time.time()
                print("Processing the last", reportEveryRounds, "out of", entryNumber, "total logEntries took", round(endTime - roundTime, 2), "seconds which is a total of", round(endTime-startTime, 2), "seconds until now.")
                #print("writing the results took", round(writeTime, 2), "seconds.")
                df = xls.createCsvFrame(fileName)
                roundTime = time.time()
        else:
            df.replace(r'^s*$', float('NaN'), regex = True)
            df.dropna(inplace = True)
            df.replace(float('NaN'), '', regex = True)
            xls.appendCsv(fileName, df)
            endTime = time.time()
            print("Processing all", entryNumber, "logEntries took", round(endTime-startTime, 2), "seconds.")
            print("The process is finished.")
            break
else:
    print("Running until", numOfEntries, "entries have been processed.")
    while True:
        entryResult = []
        endIndex = fileContent.find("__________", endIndex + 1)
        if endIndex != -1:
            logEntryString = fileContent[startIndex:endIndex]
            entryResult.append(logEntryString.splitlines()[3])
            startIndex = endIndex
            entryResult = entryResult + parseString.getSubstringLengthList(logEntryString, startStringList, stringLengthList, occList, True, cutFromBeginningList)
            df = xls.modifyRow(entryNumber, df, entryResult, numOfEntries - 1)
            if entryNumber == numOfEntries - 1:
                xls.appendCsvCsv(fileName, df)
                break
            entryNumber += 1
        else:
            break
        
