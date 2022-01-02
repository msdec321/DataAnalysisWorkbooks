import csv, sys
from pathlib import Path

print('Loading file...')

filename = sys.argv[1]

p = Path(r"C:\Users\Matth\git\DataAnalysisWorkbooks\Covid19\Data\Sliced_data")
inputFile = open(p / f"{filename}")

reader = csv.reader(inputFile)
myList = list(reader)
inputFile.close()


print(f'Removing whitespace from: {filename}')

#Remove whitespace from data entries.
for i in range(len(myList)):
    
    for j in range(len(myList[i])):
        newStr = ''
        
        for k in range(len(myList[i][j])):
            if myList[i][j][k] != ' ': 
                newStr += myList[i][j][k]
                
        myList[i][j] = newStr
                

#Remove the '--------' like that SSMS outputs.
for i in range(len(myList)):
    if i==0: continue
    else:
        try:
            myList[i] = myList[i+1]
        except IndexError: pass

outputFile = open(p / f"{filename}", "w")
outputWriter = csv.writer(outputFile, lineterminator="\n")
for i in range(len(myList)):
    outputWriter.writerow(myList[i])
    
outputFile.close()

print('Whitespace removed successfully.')