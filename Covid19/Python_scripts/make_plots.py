import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.style.use('seaborn')

def make_plot(df, xCol, yCol, plotTitle, img_name):
    _ = df.plot(x = xCol, y = yCol, style = '.', figsize = (15,5), title = plotTitle)
    save_plot(_, img_name)
    
def save_plot(ax, img_name):
    fig = ax.get_figure()
    fig.savefig("C:/Users/Matth/git/DataAnalysisWorkbooks/Covid19/Figures/scatter_plots/" + img_name + ".png")
    plt.close()

data = pd.read_csv(r"C:\Users\Matth\git\DataAnalysisWorkbooks\Covid19\Data\Sliced_data\covid_data.csv")

df1 = data.set_index('location')

continents = ['Africa', 'Asia', 'Europe', 'NorthAmerica', 'SouthAmerica', 'Oceania']
cont_caption = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania']

countries = ['UnitedStates', 'Canada', 'Mexico', 'UnitedKingdom', 'France', 'Germany', 'Japan', 'SouthKorea']
country_caption = ['United States', 'Canada', 'Mexico', 'United Kingdom', 'France', 'Germany', 'Japan', 'South Korea']

# Worldwide daily case and death statistics
make_plot(df1.loc['World'], 'date', 'new_cases', f'Daily Covid-19 Cases (Global)', f'newCases_World')
make_plot(df1.loc['World'], 'date', 'new_deaths', f'Daily Covid-19 Deaths (Global)', f'newDeaths_World')

for i, country in enumerate(countries):
    make_plot(df1.loc[country], 'date', 'new_cases', f'Daily Covid-19 Cases ({country_caption[i]})', f'newCases_{country}')
    make_plot(df1.loc[country], 'date', 'new_deaths', f'Daily Covid-19 Deaths ({country_caption[i]})', f'newDeaths_{country}')

for i, continent in enumerate(continents):
    make_plot(df1.loc[continent], 'date', 'new_cases', f'Daily Covid-19 Cases ({cont_caption[i]})', f'newCases_{continent}')
    make_plot(df1.loc[continent], 'date', 'new_deaths', f'Daily Covid-19 Deaths ({cont_caption[i]})', f'newDeaths_{continent}')
    
    
# Total Covid-19 cases
for i, continent in enumerate(continents):
    if i == 0:
        ax = df1.loc[continent].plot(x = 'date', y = 'total_cases', style = '.', figsize = (15,5), label = cont_caption[i], title = '')
    else:
        df1.loc[continent].plot(x = 'date', y = 'total_cases', style = '.', figsize = (15,5), label = cont_caption[i], ax=ax) 

save_plot(ax, 'total_cases')
    
    
# Total Covid-19 deaths     
for i, continent in enumerate(continents):
    if i == 0:
        ax = df1.loc[continent].plot(x = 'date', y = 'total_deaths', style = '.', figsize = (15,5), label = cont_caption[i], title = '')
    else:
        df1.loc[continent].plot(x = 'date', y = 'total_deaths', style = '.', figsize = (15,5), label = cont_caption[i], ax=ax) 
      
save_plot(ax, 'total_deaths')
    
    
# Cases per capita per continent
for i, continent in enumerate(continents):
    if i == 0:
        ax = df1.loc[continent].plot(x = 'date', y = 'caseRate', style = '.', figsize = (15,5), label = cont_caption[i], title = '')
    else:
        df1.loc[continent].plot(x = 'date', y = 'caseRate', style = '.', figsize = (15,5), label = cont_caption[i], ax=ax)
           
save_plot(ax, 'casesPerCapitaPerContinent')


# Deaths per capita per continent
for i, continent in enumerate(continents):
    if i == 0:
        ax = df1.loc[continent].plot(x = 'date', y = 'deathRate', style = '.', figsize = (15,5), label = cont_caption[i], title = '')
    else:
        df1.loc[continent].plot(x = 'date', y = 'deathRate', style = '.', figsize = (15,5), label = cont_caption[i], ax=ax)
        
save_plot(ax, 'deathsPerCapitaPerContinent')


# Death-case ratio per continent
for i, continent in enumerate(continents):
    if i == 0:
        ax = df1.loc[continent].plot(x = 'date', y = 'deathCaseRatio', style = '.', figsize = (15,5), label = cont_caption[i]) 
    else:
        df1.loc[continent].plot(x = 'date', y = 'deathCaseRatio', style = '.', figsize = (15,5), label = cont_caption[i], ax=ax) 
        
ax.set_ylim(0, 0.11)
save_plot(ax, 'deathsCaseRatio')