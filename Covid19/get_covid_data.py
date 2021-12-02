# This script runs daily at 10:00am EST to scrape Covid-19 data using Windows Task Scheduler. 

import requests, openpyxl, time, sys
from pathlib import Path

filename = 'owid-covid-data'

print('Downloading Covid-19 csv data...')

res = requests.get('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv')

if res.status_code == requests.codes.ok:

    covidFile = open(r"C:\Users\Matth\git\DataAnalysisWorkbooks\Covid19\owid-covid-data.csv", "wb")
    for chunk in res.iter_content(100000):
        covidFile.write(chunk)

    print('CSV data downloaded successfully!')
    time.sleep(2)
    covidFile.close()
    
else:
    print('Error: Unable to download CSV data. Aborting program.')
    time.sleep(5)
    sys.exit()
    

# Convert csv file to xlsx 
print(f'Converting {filename}.csv to excel spreadsheet..')
time.sleep(2)
           
print(f"""\n---------------------
WARNING: This process will crash if {filename}.xlsx is currently open!
Please close any instances of the spreadsheet. Thank you!
---------------------\n""")

wb = openpyxl.Workbook()
sheet = wb['Sheet']
p = Path(r"C:\Users\Matth\git\DataAnalysisWorkbooks\Covid19")
myFile = open(p / f"{filename}.csv")
time.sleep(1)

for i, line in enumerate(myFile.readlines()):
    if i % 50000 == 0: print(f'Rows processed: {i}')
    
    myList = line.split(',')      # "line" is a string, convert to a list seperated by commas.
    myList[-1] = myList[-1][ : -1]  # Remove newline character in last element of the row.
    
    for j, item in enumerate(myList): # TODO: Find the correct way to do these loops..     
        if j < 26:  # Loop from A to Z
            sheet[chr(j + 65) + str(i + 1)] = item 
            
        elif j >= 26 and j < 52:  # Loop from AA to AZ
            sheet[chr(65) + chr( (j - 26) + 65 ) + str(i + 1)] = item
            
        elif j >= 52 and j < 79:  # Loop from BA to BO
            sheet[chr(66) + chr( (j - 52) + 65 ) + str(i + 1)] = item

            
myFile.close()
wb.save(p / f"{filename}.xlsx")
print(f'{filename}.xlsx saved successfully! Closing program.')
time.sleep(4)