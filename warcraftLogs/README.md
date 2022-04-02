# WarcraftLogs TBC Restoration Druid Data Scraper v1.04  

#-----------------------------------------  
Author: Mercychan - Benediction (US)  
Discord: Mercy#9226  
#-----------------------------------------  


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
  
The scraped datasets are stored in data/ as excel spreadsheets.  

The individual character scraper can be run via scrape_character_data.ipynb  
The top druid rank scraper can be run via top_rank_scraper.ipynb  
(Note: general users don't need to run these, you can just use the premade datasets found in data/)

The related source code can be found in src.py  


# Dependencies  
&emsp; • Selenium, pandas, openpyxl, win32com  
  
&emsp; • Get the selenium chromedriver at (version number must match your Google Chrome version):   
&emsp; https://chromedriver.storage.googleapis.com/index.html   

&emsp; • Get Adblock plus for selenium (see the following link for installation guide):  
&emsp; https://www.reddit.com/r/learnpython/comments/4zzn69/how_do_i_get_adblockplus_to_work_with_selenium/d70036l/
  
&emsp; • Other browsers (Firefox, IE6, etc) are not currently supported 
 
&emsp; • All other dependencies can be installed via pip


# TODO list

&emsp; • Add a dashboard to visualize the top rotations used per boss with filters for kill time, N healers, spriest/innervate, etc

&emsp; • Track hasted rotations (Lifebloom + 4 instants, LB + 3I + 1RG, etc).

&emsp; • Track non-rotations (RG spam, 3 RG + 1I, etc)

