def total_calculator(dict_cont, loc, month, cont, variable, index):  
    
    if loc[0] == loc[1] and month[0] != month[1]: 
        if month[0] == '12':
            dict_cont[month[0]][0] += int(variable[0])  # Always adds December values to year 2020

        else:
            dict_cont[month[0]][index] += int(variable[0])  # Otherwise adds to correct year 

    if cont[0] != cont[1]:
        if month[0] == '12':
                dict_cont[month[0]][0] += int(variable[0])

        else:
            dict_cont[month[0]][index] += int(variable[0])

