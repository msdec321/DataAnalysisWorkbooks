# Multiprocess Top Rank Scraper  

(Note: general users don't need to run this tool. You'll find a premade dataset in the data/ directory.)  
(For a list of dependencies see the README in the parent directory)  

This is a version of the top N rank scraper that runs multiple scrapers in parallel via the multiprocessing module. This reduces time spent data scraping roughly by a factor of nCores-1. Unfortunately multiprocessing does not work well with interactive notebooks so this version must be run directly through the Python interpreter (*python multi_scraper.py*).  

Within the script you'll find [three configurables](https://github.com/msdec321/DataAnalysisWorkbooks/blob/main/warcraftLogs/multiprocess_scraper/multi_scraper.py#L17-L19): nCores, nParses and boss. I'd suggest using at most your max # of cores - 2 so as to not slow your computer too much. For nParses, check how many ranks are in data/top_N_druids.xlsx for the boss you want to scrape and pick a number larger than that (I usually do nRows + 100). For boss, use the name of the boss as you see it listed in the dictionary. Also, set your path variables in the configs.csv file.  

One last comment. You'll notice (a lot) of [warnings](https://i.imgur.com/7l8lqEc.png) in the terminal. Fortunately these don't seem to have any effect on the output.  That's all, good luck!
