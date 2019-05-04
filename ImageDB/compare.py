import os
import csv
import sys

def fileInCSV(folderPath, csvPath):
    try:
        # Store entire list of files in specified folderPath
        filesInFolder = os.listdir(folderPath)
    except:
        print("ERROR: Specified folder path (first argument) doesn't exist")
        exit(1)

    # List to store file names
    fileNames = []

    # List to store all files that don't exist
    missingCSV = []
    missingFolder = []

    try:
        with open(csvPath) as csvfile:
            # Store entire CSV file
            readCSV = csv.reader(csvfile, delimiter=',')
            # Ignore first row; headers
            next(readCSV)

            # Get all file names form CSV
            for row in readCSV:
                fileName = row[0]
                fileNames.append(fileName)

            # For each row in the fileNames list,
            # get the currFilename and check if its in the folder
            for currFilename in fileNames:
                if currFilename not in filesInFolder:
                    missingFolder.append(currFilename)

            # For each row in the filesInFolder list,
            # get the currFilename and check if its in the CSV
            for currFilename in filesInFolder:
                if currFilename not in fileNames:
                    missingCSV.append(currFilename)

            # Print missing files, if any
            if missingFolder:
                print("The following files are missing from the folder:")
                print(missingFolder)
            if missingCSV:
                print("The following files are missing from the CSV file:")
                print(missingCSV)
    except:
        print("ERROR: Specified file path (second argument) doesn't exist")
        exit(1)

if (len(sys.argv) != 3):
    print("ERROR: Incorrect arguments.")
    print("Please specify the folder path, followed by the CSV file path.")

    exit(1)

fileInCSV(sys.argv[1], sys.argv[2])
