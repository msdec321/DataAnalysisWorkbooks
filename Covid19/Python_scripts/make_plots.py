import pandas as pd
import matplotlib.pyplot as plt

def make_plot(df, xCol, yCol, plotTitle, img_name):
    _ = df.plot(x = xCol, y = yCol, style = '.', figsize = (15,5), title = plotTitle)
    fig = _.get_figure()
    fig.savefig("C:/Users/Matth/git/DataAnalysisWorkbooks/Covid19/Figures/" + img_name + ".png")

rollingCasesDeaths = pd.read_csv(r"C:\Users\Matth\git\DataAnalysisWorkbooks\Covid19\Data\Sliced_data\rollingCasesDeaths.csv")

df1 = rollingCasesDeaths.set_index('location')
continents = ['Africa', 'Asia', 'Europe', 'NorthAmerica', 'SouthAmerica', 'Oceania']
cont_caption = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania']

for i, continent in enumerate(continents):
    make_plot(df1.loc[continent], 'date', 'new_cases', f'Daily Covid-19 Cases ({cont_caption[i]})', f'newCases_{continent}')
    make_plot(df1.loc[continent], 'date', 'new_deaths', f'Daily Covid-19 Deaths ({cont_caption[i]})', f'newDeaths_{continent}')

make_plot(df1.loc['Africa'], 'date', 'rollingCases', 'rolling cases (Africa)', 'rollingCases_Africa')
make_plot(df1.loc['Africa'], 'date', 'rollingDeaths', 'rolling deaths (Africa)', 'rollingDeaths_Africa')