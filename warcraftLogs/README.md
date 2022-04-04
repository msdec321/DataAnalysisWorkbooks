# WarcraftLogs TBC Restoration Druid Data Scraper v1.04  

#-----------------------------------------  
*Author: Mercychan - Benediction (US)*    
*Discord: Mercy#9226*  
#-----------------------------------------  


This tool scrapes encounter data from WarcraftLogs which can be used in a data analysis. Currently scrapes the following data:   
&emsp; • Rank (*Top rank scraper only*)  
&emsp; • Character name, server, region  
&emsp; • Date  
&emsp; • Kill time  
&emsp; • Parse percentile (*Individual character scraper only*)  
&emsp; • Number of healers  
&emsp; • Shadowpriest in group?  
&emsp; • Innervate received?  
&emsp; • Bloodlust/heroism received?  
&emsp; • Power Infusion received?   
&emsp; • Is Nature's Grace spec?  
&emsp; • Lifebloom uptime %  
&emsp; • Total HPS  
&emsp; • % HPS of: Lifebloom (tick), Lifebloom (bloom), Rejuvenation, Regrowth, Swiftmend  
&emsp; • Rotating on tank? ('No' means the Druid is ignoring the tank and just raid healing)  
&emsp; • Top two rotations used  
  
The scraped datasets are stored in data/ as excel spreadsheets.  

The individual character scraper can be run via specific_character_scraper.ipynb  
The top druid rank scraper can be run via top_rank_scraper.ipynb  
(Note: general users don't need to run these, you can just use the premade datasets found in data/)  

The related source code can be found in src.py  


# Dependencies for running the data scrapers  
&emsp; • Selenium, pandas, openpyxl, win32com  
  
&emsp; • Get the selenium chromedriver at (version number must match your Google Chrome version):   
&emsp; https://chromedriver.storage.googleapis.com/index.html   

&emsp; • Get Adblock plus for selenium (see the following installation guide):  
&emsp; https://www.reddit.com/r/learnpython/comments/4zzn69/how_do_i_get_adblockplus_to_work_with_selenium/d70036l/
  
&emsp; • Other browsers (Firefox, IE6, etc) are not currently supported 
 
&emsp; • All other dependencies can be installed via pip


# TODO list

&emsp; • Add other language support for rotation calculator (Russian, German, Korean, etc)

&emsp; • Add a dashboard to visualize the top rotations used per boss with filters for kill time, N healers, spriest/innervate, etc

&emsp; • Track hasted rotations (Lifebloom + 4 instants, LB + 3I + 1RG, etc).

&emsp; • Speed up scraping tool (Currently ~1min per character scrape)

&emsp; • Add a dataset for Dreamstate spec

