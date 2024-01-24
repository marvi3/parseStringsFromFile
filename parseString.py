import sys

def splitIntList(numberString, delimiter):
    numberListStr = numberString.split(delimiter)

    # Convert each string to a float or int and create a new list
    numberList = []
    for numStr in numberListStr:
        numStr = numStr.strip()  # Remove leading/trailing whitespace
        try:
            # Convert to integer or float
            if '.' in numStr:
                number = float(numStr)
            else:
                number = int(numStr)
            numberList.append(number)
        except ValueError:
            # Handle the case where the conversion fails
            print(f"Warning: '{numStr}' is not a valid number and will be skipped.")

    return numberList

def readFile(filePath):
    try:
        with open(filePath, 'r') as file:
            contents = file.read()
            return(contents)
    except FileNotFoundError:
        print(f"The file at {filePath} was not found.")
    except Exception as e:
        print(f"An error occured: {e}")

def getSubstringLength(string, startString, n, occurenceList, occurenceOutOf):
    resultString = ""
    startIndex = -1
    occurenceCount = 1

    while True:
        # Find the index of the substring in the main string
        startIndex = string.find(startString, startIndex + 1)

        # Check if the substring is found
        if startIndex != -1:
            # Calculate the end indice for the substring we want to return
            endIndex = startIndex + int(n)

            # Return the substring from the main string
            if occurenceCount in occurenceList:
                resultString += string[startIndex:endIndex]
                resultString += " "
            occurenceCount += 1
            if occurenceCount == occurenceOutOf + 1:
                occurenceCount = 1
        else:
            break

    return resultString

def getSubstringLengthList(string, startStringList, stringLengthList, occList, cutStartString=False, cutFromBeginningList=0):
    resultStringList = []
    startIndex = -1
    endIndex = -1

    print(len(string))

    if cutFromBeginningList == 0:
        cutFromBeginningList = [0] * len(startStringList)
    
    if len(startStringList) != len(stringLengthList):
        print("startStringList, stringLengthList and occList must have the same length")
        sys.exit(0)
    if len(startStringList) != len(occList):
        print("startStringList, stringLengthList and occList must have the same length")
        sys.exit(0)
    if len(startStringList) != len(cutFromBeginningList):
        print("startStringList, stringLengthList and occList must have the same length")
        sys.exit(0)
    
    for i in range(len(startStringList)):
        for j in range(occList[i]):
            startIndex = string.find(startStringList[i], endIndex + 1)
            # Check if the substring is found
            if startIndex != -1:
                endIndex = startIndex + stringLengthList[i]
                startIndex += cutFromBeginningList[i]
                if cutStartString:
                    startIndex += len(startStringList[i])
                
                resultStringList = resultStringList + string[startIndex:endIndex].strip().split()
            else:
                # This adds an empty string, so that the order is not interrupted
                resultStringList.append("")

def getSubstringCharacter(string, startString, endString, inclEndString, occurenceList, occurenceOutOf):
    resultString = ""
    endIndex = -1
    endStringLength = len(endString)
    occurenceCount = 1

    while True:
        # Find the index of the substring in the main string
        startIndex = string.find(startString, endIndex + 1)
        # Check if the substring is found
        if startIndex != -1:
            if occurenceCount in occurenceList:
                if inclEndString:
                    endIndex = string.find(endString, startIndex) + endStringLength
                else:
                    endIndex = string.find(endString, startIndex + 1)
                resultString += string[startIndex:endIndex]
                resultString += " "
            else:
                endIndex = startIndex + 1
            occurenceCount += 1
            if occurenceCount == occurenceOutOf + 1:
                occurenceCount = 1
        else:
            break
    return resultString[0:len(resultString) - 1]

def main():
    if len(sys.argv) < 5:
        print("Usage: python parseString.py filename [l/e/b for length, till ending string or excluding ending string] [stringStartsWith] [length of string or what the string ends with] [optional list of nth ocurrence that should be taken split by comma] [optional number nth occurence out of number occurences]")
        sys.exit(0)
    occurenceList = [1]
    occurenceOutOf = 1
    if len(sys.argv) > 5:
        occurenceList = splitIntList(sys.argv[5], ",")
        occurenceOutOf = occurenceList[len(occurenceList) - 1]
    if len(sys.argv) > 6:
        occurenceOutOf = int(sys.argv[6])
    filePath = sys.argv[1]
    fileContent = readFile(filePath)
    if fileContent is None:
        print("The file is empty")
        sys.exit(0)
    if sys.argv[2] == "l":
        print(getSubstringLength(fileContent, sys.argv[3], sys.argv[4], occurenceList, occurenceOutOf))
    elif sys.argv[2] == "e":
        print(getSubstringCharacter(fileContent, sys.argv[3], sys.argv[4], True, occurenceList, occurenceOutOf))
    elif sys.argv[2] == "b":
        print(getSubstringCharacter(fileContent, sys.argv[3], sys.argv[4], False, occurenceList, occurenceOutOf))
    else:
        print("the second argument has to be either \"l\" if you want to select for n characters, \"e\" if you want to select until an ending string or \"b\" if you want to select til before the ending string")


if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main()
