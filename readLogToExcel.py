# This script needs the following input data:
#   filename to be read
#   excel filename to be written
#   

import sys
import xls.py as xls
import parseString.py as parse

# Checks if less then 3 arguments are existing.
if len(sys.argv) < 3:
    print("Usage: python readDataToExcel.py fileNameToBeRead ExcelToWrite.xls")
    sys.exit(0)

# opens the file to be read
filePath = sys.argv[1]
fileContent = parse.readFile(filePath)
if fileContent is None:
    print("The file is empty")
    sys.exit(0)
print(f"The file {sys.argv[1]} has been opened.")


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
stringLengthList.append(195)
occList.append(1)
cutFromBeginningList.append(103)

# CPU usage from core 0-63:
startStringList.append("Durchschn.:")
stringLengthList.append(97)
occList.append(64)
cutFromBeginningList.append(5)
#   %usr
#   %sys
#   %iowait
#   %soft
#   %idle

logResult = []
entrNumber = 0
startIndex = 0
endIndex = 0
while True:
    entryResult = []
    endIndex = fileContent.find("__________", endIndex + 1)
    if endIndex != -1:
        logEntryString = fileContent[startIndex:endIndex]
        entryResult.append(logEntryString.splitlines()[0])
        startIndex = endIndex
        entryResult = parse.getSubstringLengthList(logEntryString, startStringList, stringLengthList, occList, True, cutFromBeginningList)
        xls.modifyRow(entryNumber, argv[2], entryResult)
        break
    else:
        break
