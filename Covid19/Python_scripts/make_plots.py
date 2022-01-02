import pandas as pd
import matplotlib.pyplot as plt

rollingCases = pd.read_csv(r"C:\Users\Matth\git\DataAnalysisWorkbooks\Covid19\Data\Sliced_data\rollingCases.csv")

df1 = rollingCases.set_index('location')
rollingCasesAfrica = df1.loc['Africa']

_ = rollingCasesAfrica.plot(x='date',y='new_cases', style='.', figsize=(15,5), title='')
fig = _.get_figure()
fig.savefig(r"C:\Users\Matth\git\DataAnalysisWorkbooks\Covid19\Figures\newCases_Africa.png")