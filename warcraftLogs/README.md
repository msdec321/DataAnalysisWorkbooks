# WarcraftLogs Restoration Druid Data Scraper v1.03  

This repository scrapes encounter data from WarcraftLogs which can be used in a data analysis.   
&emsp; • Character name, server, region  
  • Date  
  • Kill time  
  • Parse percentile  
  • Number of healers  
  • Shadowpriest in group  
  • Innervate used on player  
  • Lifebloom uptime %  
  • Total HPS  
  • % HPS of: Lifebloom (tick), Lifebloom (bloom), Rejuvenation, Regrowth, Swiftmend  
  • Top two rotations used  
  
The dataset is stored in character_data/ as an excel spreadsheet.  

The data scraper can be run via scrape_character_data.ipynb  
The related source code can be found in src.py  

# Dependencies  
  • Selenium, pandas, openpyxl, win32com  
  
  • Get the selenium chromedriver at (version number must match Google Chrome version):  
  https://chromedriver.storage.googleapis.com/index.html  
  
  • For firefox users, can try using GeckoDriver (not yet tested and likely won't work).  
  
  • In the Configurations cell of scrape_character_data.ipynb, specify the path to the webdriver.  
 
  • All other dependencies can be installed via pip
