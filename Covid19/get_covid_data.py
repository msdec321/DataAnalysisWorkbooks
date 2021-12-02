# This script runs daily at 10:00am EST to scrape Covid-19 data using Windows Task Scheduler. 

import requests

res = requests.get('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv')

if res.status_code==requests.codes.ok:

    covidFile = open("owid-covid-data.csv", "wb")
    for chunk in res.iter_content(100000):
        covidFile.write(chunk)

    covidFile.close()