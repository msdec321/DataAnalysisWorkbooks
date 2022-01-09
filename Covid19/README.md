# Covid-19 Data Analysis Portfolio Project

• This respository is a portfolio project that produces a dashboard on Covid-19 related information. To summarize the contents of this project:

1) Data is downloaded daily from [1] via Python_scripts/get_covid_data.py. The data is downloaded in csv format and then converted to xlsx format.
2) The data is then loaded into Microsoft SQL Server Management Studio (SSMS), which is configured through the SSMS job agent and not through this repository.
3) A set of queries are run in SSMS via Batch_files/SQLQueryBatch.bat. SQL queries can be configured in the Queries/ directory. The output data is then cleaned via Python_scripts/remove_whitespace.py into a Pandas workable format. The output data is stored in Data/Sliced_data/covid_data.csv.
4) A set of time-series plots are drawn using Python_scripts/make_plots.py, the output is saved in the Figures/ directory.
5) A dashboard is created using these figures via Python_scripts/make_pptx.py, saved as Covid19_dashboard.pptx
6) Figures/ and Covid19_dashboard.pptx are committed and pushed to GitHub via Python_scripts/git_update.py.

• This collection of procedures, from data collection to dashboarding, is made to be fully automated, daily, via batch files added to the Windows Task Scheduler. These can be found in the Batch_files/ directory.
• Additional data analysis is done in Covid19_workbook.ipynb, however this notebook is not used in produced the pptx dashboard.

[1]:  The original dataset is located at: https://github.com/owid/covid-19-data/blob/master/public/data/README.md
