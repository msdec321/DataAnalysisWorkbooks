import os

os.system(""" bash -c "cd '/mnt/c/Users/Matth/git/DataAnalysisWorkbooks/Covid19/Figures' ; git add scatter_plots ; git commit -m 'Updated figures' ; git push" """)
os.system(""" bash -c "cd '/mnt/c/Users/Matth/git/DataAnalysisWorkbooks/Covid19' ; git add Covid19_dashboard.pptx ; git commit -m 'Updated pptx dashboard' ; git push" """)