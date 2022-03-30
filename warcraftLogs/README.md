# WarcraftLogs Restoration Druid Data Scraper v1.03  

This repository scrapes encounter data from WarcraftLogs which can be used in a data analysis. Currently scrapes:   
&emsp; • Character name, server, region  
&emsp; • Date  
&emsp; • Kill time  
&emsp; • Parse percentile  
&emsp; • Number of healers  
&emsp; • Shadowpriest in group  
&emsp; • Innervate used on player  
&emsp; • Lifebloom uptime %  
&emsp; • Total HPS  
&emsp; • % HPS of: Lifebloom (tick), Lifebloom (bloom), Rejuvenation, Regrowth, Swiftmend  
&emsp; • Top two rotations used  
  
The dataset is stored in character_data/ as an excel spreadsheet.  

The data scraper can be run via scrape_character_data.ipynb  
The related source code can be found in src.py  

# Dependencies  
&emsp; • Selenium, pandas, openpyxl, win32com  
  
&emsp; • Get the selenium chromedriver at (version number must match Google Chrome version):  
&emsp; https://chromedriver.storage.googleapis.com/index.html  
  
&emsp; • For firefox users, can try using GeckoDriver (not yet tested and likely won't work).  
  
&emsp; • In the Configurations cell of scrape_character_data.ipynb, specify the path to the webdriver.  
 
&emsp; • All other dependencies can be installed via pip
