# This script runs daily at 10:00am EST to scrape Covid-19 data using Windows Task Scheduler. 

import requests, openpyxl, os
from pathlib import Path

res = requests.get('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv')

if res.status_code==requests.codes.ok:

    covidFile = open(r"C:\Users\Matth\git\DataAnalysisWorkbooks\Covid19\owid-covid-data.csv", "wb")
    for chunk in res.iter_content(100000):
        covidFile.write(chunk)

    covidFile.close()
    
    
# Convert csv file to xlsx  
print('Converting csv data to excel spreadsheet..')
wb = openpyxl.Workbook()
sheet = wb['Sheet']
p = Path(r"C:\Users\Matth\git\DataAnalysisWorkbooks\Covid19")
myFile = open(p / "owid-covid-data_backup.csv")

for i, line in enumerate(myFile.readlines()):
    if i % 50000 == 0: print(f'Rows processed: {i}')
    
    myList = line.split(',')      # "line" is a string, convert to a list seperated by commas.
    myList[-1] = myList[-1][ : -1]  # Remove newline character in last element of the row.
    
    for j, item in enumerate(myList): # TODO: Find the correct way to do these loops..     
        if j < 26:  # Loop from A to Z
            sheet[chr(j + 65) + str(i + 1)] = item 
            
        elif j < 52 and j >= 26:  # Loop from AA to AZ
            sheet[chr(65) + chr( (j - 26) + 65 ) + str(i + 1)] = item
            
        elif j >= 52 and j < 79:  # Loop from BA to BO
            sheet[chr(66) + chr( (j - 52) + 65 ) + str(i + 1 )] = item

            
myFile.close()
wb.save("owid-covid-data.xlsx")