# WarcraftLogs TBC Restoration Druid Data Scraper v1.05  

#------------------------  
Author's note: This project is now in maintainence mode.  
Data will be updated every two weeks but I do not plan to develop this project further.  
#------------------------  

This tool scrapes encounter data from WarcraftLogs which can be used for data analysis.  
The scraped datasets are stored in data/ as excel spreadsheets.  

The individual character scraper can be run via specific_character_scraper.ipynb  
The top druid rank scraper can be run via top_rank_scraper.ipynb  

A multiprocessing version of the top rank scraper is located in multiprocess_scraper/  
(Note: general users don't need to run these, you can just use the premade datasets found in data/)  

The related source code can be found in src.py  


# Dependencies for running the data scrapers  
&emsp; • Selenium, pandas, openpyxl, win32com  
  
&emsp; • Get the selenium chromedriver at (version number must match your Google Chrome version):   
&emsp; https://chromedriver.storage.googleapis.com/index.html   

&emsp; • Get ublock for selenium (see the following installation guide, which is for adblockplus but same idea for ublock):  
&emsp; https://www.reddit.com/r/learnpython/comments/4zzn69/how_do_i_get_adblockplus_to_work_with_selenium/d70036l/  
  
&emsp; • Firefox/geckodriver are supported but browser often freezes. Other browsers are not supported.   
 
&emsp; • All other dependencies can be installed via pip


# TODO list  

&emsp; • Scrape the top 3,000 - 5,000 players for each boss (ETA ~2 weeks)  

&emsp; • Export analysis code to a webapp for general use.  

&emsp; • Add a dataset for Dreamstate spec  

