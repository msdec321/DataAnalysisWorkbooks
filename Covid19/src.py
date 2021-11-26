def total_calculator(myDict, key, variable, loc, cont, month, year):  
    
    #print(key, loc, cont, month, index, variable)
    
    if loc[0] == loc[1] and month[0] != month[1]: 
        if month[0] == '12':
            myDict[key][cont[0]][month[0]][0] += int(variable[0])  # Always adds December values to year 2020

        else:
            myDict[key][cont[0]][month[0]][year] += int(variable[0])  # Otherwise adds to correct year

    if cont[0] != cont[1]:
        if month[0] == '12':
                myDict[key][cont[0]][month[0]][0] += int(variable[0])

        else:
            myDict[key][cont[0]][month[0]][year] += int(variable[0])

