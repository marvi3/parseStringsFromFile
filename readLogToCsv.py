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

logResult = []
df = xls.readCsv(fileName)
entryNumber = 0
startIndex = 0
endIndex = 0
fileName = sys.argv[2]
numOfEntries = int(sys.argv[3])
startTime = time.time()
roundTime = startTime
prepareTime = 0
splitTime = 0
writeTime = 0
reportEveryRounds = 10
if int(sys.argv[3]) == 0:
    print("Running until the whole file has been processed.")
    partStartTime = time.time()
    writeTime += time.time() - partStartTime
    while True:
        partStartTime = time.time()
        entryResult = []
        endIndex = fileContent.find("__________", endIndex + 1)
        if endIndex != -1:
            logEntryString = fileContent[startIndex:endIndex]
            prepareTime += time.time() - partStartTime
            partStartTime = time.time()
            entryResult.append(logEntryString.splitlines()[1])
            print(logEntryString.splitlines()[0:10])
            startIndex = endIndex
            entryResult = parseString.getSubstringLengthList(logEntryString, startStringList, stringLengthList, occList, True, cutFromBeginningList)
            splitTime += time.time() - partStartTime
            partStartTime = time.time()
            df = xls.modifyRow(entryNumber, df, entryResult, entryNumber + reportEveryRounds - entryNumber % reportEveryRounds - 1)
            writeTime += time.time() - partStartTime
            entryNumber += 1
            if entryNumber % reportEveryRounds == 0:
                partStartTime = time.time()
                xls.writeCsv(fileName, df)
                writeTime += time.time() - partStartTime
                endTime = time.time()
                print("So far", entryNumber, "log entries have been processed which took", round(endTime-startTime, 2), "seconds.")
                print("Processing the last", reportEveryRounds, "logEntries took", round(endTime - roundTime, 2), "seconds")
                #print("writing the results took", round(writeTime, 2), "seconds.")
                prepareTime = 0
                splitTime = 0
                writeTime = 0
                roundTime = time.time()
        else:
            break
else:
    print("Running until", numOfEntries, "entries have been processed.")
    while True:
        entryResult = []
        endIndex = fileContent.find("__________", endIndex + 1)
        if endIndex != -1:
            logEntryString = fileContent[startIndex:endIndex]
            entryResult.append(logEntryString.splitlines()[1])
            startIndex = endIndex
            entryResult = parseString.getSubstringLengthList(logEntryString, startStringList, stringLengthList, occList, True, cutFromBeginningList)
            xls.modifyRow(entryNumber, df, entryResult, numOfEntries)
            if entryNumber == numOfEntries:
                xls.writeCsv(fileName, df)
                break
            entryNumber += 1
        else:
            break
        
