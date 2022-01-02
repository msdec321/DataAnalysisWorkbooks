sqlcmd -S . -E -i "C:\Users\Matth\git\DataAnalysisWorkbooks\Covid19\Queries\rollingCases.sql" -o "C:\Users\Matth\git\DataAnalysisWorkbooks\Covid19\Data\Sliced_data\rollingCases.csv" -s ","
"C:\\Users\\Matth\\miniforge3\python.exe" "C:\Users\Matth\git\DataAnalysisWorkbooks\Covid19\Python_scripts\remove_whitespace.py" "rollingCases.csv"
