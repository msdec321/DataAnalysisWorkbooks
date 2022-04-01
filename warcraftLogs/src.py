import selenium, time, csv, os, openpyxl, fnmatch, shutil, win32com.client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime


def load_environment(path, char_name, char_server, char_region):
    chrome_options = Options()
    chrome_options.add_argument('load-extension=' + path)

    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.create_options()
    time.sleep(5)

    browser.switch_to.window(browser.window_handles[0])
    browser.get(f"https://classic.warcraftlogs.com/character/{char_region.lower()}/{char_server.lower()}/{char_name.lower()}")
    time.sleep(3)
    
    cookie = browser.find_element_by_class_name("cc-compliance")
    cookie.click()
    
    return browser.current_url, browser    
    

def get_t6_bosses(browser):
    link = browser.find_elements_by_id("boss-table-1011")

    table = list(link[0].text.split("\n"))
    bosses = []

    for i in range(8, 36, 2):
        bosses.append(table[i])

    return bosses


def get_character_info(char_url):
    
    temp = char_url.split("/")
    char_name = temp[-1].capitalize()
    char_server = temp[-2].capitalize()
    char_region = temp[-3].swapcase()
    
    return char_name + " " + "(" + char_server + " " + char_region + ")"
         
            
def check_if_parse_already_recorded(i, browser, search, boss, char_name, char_server, char_region):
    
    try:
        wb = openpyxl.load_workbook('character_data/character_data.xlsx')
        
    except FileNotFoundError: 
        return False

    date = browser.find_element_by_id('date-hps-'+str(i+1))
    date = date.text
    date = date.replace(",", "")

    rank = browser.find_element_by_link_text(search[i*6].text)
    rank = rank.text
    
    try:
        ws = wb.get_sheet_by_name(boss.replace(" ", ""))
        for row in ws.iter_rows():
            if [char_name, char_server + " " + char_region, date, rank] == [row[0].value, row[1].value, row[2].value, row[4].value]:
                wb.save('character_data/character_data.xlsx')
                return True

    # If the boss sheet isn't in the excel file, add it
    except KeyError:
        temp = str(boss).replace(" ", "")
        wb.create_sheet(temp)
        sheet = wb[temp]
        header = ["Name", "Server", "Date", "Kill time", "Rank", "nHealers", "Spriest?", "Innervate?", "LB_uptime", "HPS", "% LB (tick) HPS", "% LB (bloom) HPS", "% Rejuv HPS", "% Regrowth HPS", "% Swiftmend HPS", "Rotations"]
        for i, item in enumerate(header):
            sheet[chr(i + 65) + str(1)] = item
            
        wb.save('character_data/character_data.xlsx')
        return False
       
    return False       
                  
            
def get_boss_data(browser, i):
    search = browser.find_elements_by_class_name("character-table-link")

    rank = browser.find_element_by_link_text(search[i*6].text)
    date = browser.find_element_by_id('date-hps-'+str(i+1))
    HPS = browser.find_element_by_link_text(search[(i*6)+2].text)
    time = browser.find_element_by_link_text(search[(i*6)+3].text)
    
    date = date.text
    date = date.replace(",", "")
    return rank, date, rank.text, HPS.text.replace(",", ""), time.text, HPS           
            
            
def get_spell_info(browser, total_HPS):

    # Lifebloom (tick), Lifebloom (bloom), Rejuv, Regrowth, Swiftmend
    spell_percent_HPS_dict = {"ability-33763-0" : 0, "ability-33778-0" : 0, "ability-26982-0" : 0, "ability-26980-0" : 0, "ability-18562-0" : 0}
    spell_ids = ['ability-33763-0', 'ability-33778-0', 'ability-26982-0', 'ability-26980-0', 'ability-18562-0']
    LB_uptime = 0
    
    for spell in spell_ids:
        
        try:
            search = browser.find_element_by_id(spell)

            td_p_input = search.find_element_by_xpath('.//ancestor::td')
            tr_p_input = search.find_element_by_xpath('.//ancestor::tr')
            td_p_input = tr_p_input.find_elements(By.XPATH, 'td')
            
            spell_percent_HPS_dict[spell] = round(float(td_p_input[9].text.replace(",", "")) / float(total_HPS), 2)
            
            if spell == 'ability-33763-0':
                LB_uptime = td_p_input[7].text
            
        except:
            pass
        
    return spell_percent_HPS_dict['ability-33763-0'], spell_percent_HPS_dict['ability-33778-0'], spell_percent_HPS_dict['ability-26982-0'], spell_percent_HPS_dict['ability-26980-0'], spell_percent_HPS_dict['ability-18562-0'], LB_uptime
    
    
def get_nHealers(browser):
    row = browser.find_elements_by_class_name("composition-row")
    
    return len(row[2].text.split("\n")) - 1
    

def get_tanks(browser):
    click_on_element_by_id(browser, "filter-summary-tab")  
    time.sleep(0.5)
    
    row = browser.find_elements_by_class_name("composition-row")
    
    tanks = row[0].text.split("\n")
    tanks.pop(0)
    
    return tanks
        
        
def check_spriest(browser):
    body = browser.find_element_by_css_selector('body')
    body.send_keys(Keys.PAGE_UP)
    time.sleep(1)
    
    click_on_element_by_id(browser, "filter-resources-tab") 
    time.sleep(0.5)
    
    click_on_element_by_id(browser, "filter-resource-selection-dropdown")
    time.sleep(1.5)
    
    a = browser.find_element_by_id("spell-100")
    time.sleep(0.5)
    a.click()
    
    time.sleep(1)
    b = browser.find_elements_by_class_name("main-table-name")
    
    for i in range(len(b)):
        if b[i].text == 'Vampiric Touch':
            return 'Yes'
            
    return 'No'


def check_innervate(browser):
    body = browser.find_element_by_css_selector('body')
    body.send_keys(Keys.PAGE_UP)
    time.sleep(1)
    
    click_on_element_by_id(browser, "filter-buffs-tab")
    time.sleep(0.5)
    
    try:
        a = browser.find_element_by_id("main-table-256-0")
        b = a.text.split('\n')

        # Check if innervate is present in the table.
        if len(fnmatch.filter(b, 'Innervate??')) > 0: 
            return 'Yes'

        else: 
            return 'No'
        
    # If the 'major individual cooldown' table is not present then the player wasn't innervated.
    except: 
        return 'No'
   
        
def click_on_element_by_id(browser, id_tag):    
    a = browser.find_element_by_id(id_tag)
    time.sleep(1)
    
    while True:
        action = ActionChains(browser)
        action.move_to_element(a)
        time.sleep(0.5)
        
        try:
            action.perform()
            time.sleep(0.5)
            action.click()
            action.perform()
            break
        
        except:
            body = browser.find_element_by_css_selector('body')
            body.click()
            body.send_keys(Keys.PAGE_UP)
    

def click_on_element_by_class_name(browser, class_tag):  
    b = browser.find_element_by_class_name(class_tag)
    time.sleep(1)
    
    while True:
        action = ActionChains(browser)
        action.move_to_element(b)
        time.sleep(0.5)
        
        try:
            action.perform()
            time.sleep(0.5)
            action.click()
            action.perform()
            break
        
        except:
            body = browser.find_element_by_css_selector('body')
            body.click()
            body.send_keys(Keys.PAGE_UP)
            
            
def download_csv(browser, temp_url, id_tag, download_path, path):
    body = browser.find_element_by_css_selector('body')
    body.send_keys(Keys.PAGE_UP)
    time.sleep(1)
    
    click_on_element_by_id(browser, "filter-events-tab")    
    time.sleep(1)

    click_on_element_by_id(browser, id_tag)
    time.sleep(1)
    
    click_on_element_by_class_name(browser, "buttons-csv")
    time.sleep(3)
    
    shutil.move(f"{download_path}/Warcraft Logs - Combat Analysis for Warcraft.csv", path)
    
    browser.get(temp_url)
    time.sleep(1)
    
           
def clean_cast_sequence_csv():
    df = pd.read_csv('character_data/cast_sequence.csv')
    
    df = df.drop(['Unnamed: 4'], axis=1)
    
    temp_df = df['Time'].str.split(":", expand=True)
    df['Minute'] = temp_df[0]
    df['Second'] = temp_df[1]

    df['Minute'] = pd.to_numeric(df['Minute'])
    df['Second'] = pd.to_numeric(df['Second'])

    temp_df = df['Ability'].str.split(" ", expand=True)
    df['Ability'] = temp_df[0]
    df['Cast Time'] = temp_df[1]

    temp_df = df['Source → Target'].str.split(" ", expand=True)
    
    # If DBM puts a marker on a tank it can mess up the pandas dataframe. Check and fix if this happens
    fixed_target = []
    for i, row in (temp_df.iterrows()):
        if row[2] != "": 
            fixed_target.append(row[2])
            
        else: 
            fixed_target.append(row[3])
            
    df['Target'] = fixed_target

    df['Boss Target'] = np.nan

    df = df.drop(['Source → Target'], axis=1)
    
    correct_csv_whitespace('character_data/cast_sequence')
    
    return df


# Fix orrcurances where there is a double whitespace in the pandas dataframe
def correct_csv_whitespace(path):

    filename = path+'.csv'
    with open(filename, 'r') as csvfile:
        outputFile = open(path+"_fixed.csv", "w")
        
        datareader = csv.reader(csvfile)
        outputWriter = csv.writer(outputFile, lineterminator='\n')

        for row in datareader:
            if len(row) == 0: continue

            for i, item in enumerate(row):
                row[i] = row[i].replace("  ", " ")
            outputWriter.writerow(row)
        outputFile.close()

    os.system("mv "+ path + "_fixed.csv " + path + ".csv")    


# For non-instant casts, the time is specified at the end of the cast. This causes issues when regrowth is followed by an instant cases
# This function changes the time specified to the start of the regrowth cast rather than the end of it. (Including cancel-casts)

def fix_cast_time(df):
    temp = []
    for i, row in df.iterrows():
        if row['Ability'] in ['Regrowth'] and row["Cast Time"] is None: 
            temp.append(row["Time"])
        
        elif row['Ability'] in ['Regrowth', 'Rebirth'] and row["Cast Time"] != "Canceled":
            a = str(datetime.strptime(str(row['Minute']) + ":" + str(row['Second']), "%M:%S.%f") - datetime.strptime(row['Cast Time'], "%S.%f"))
            a = a.split(".")
            if len(a) == 1: a.append('000000')
            b = a[0].split(":")
            c = b[1] + ":" + b[2] + "." + a[1][:3]
            temp.append(c)

        else:
            temp.append(row["Time"])

    df["Time"] = temp
    
    temp_df = df['Time'].str.split(":", expand=True)
    df['Second'] = temp_df[1]
    df['Second'] = pd.to_numeric(df['Second'])
    
    return df
   

# Rotation calculator. This function checks when lifebloom is refreshed on the primary tank and what sequence of spells (Instant, Regrowth)
# are cast before the initial lifebloom is refreshed. The rotations are tallied in a rotation dictionary and a final count is returned.
    
def calculate_rotations(df, boss, boss_tanks):

    GCD_time = {"t1" : 0, "t2" : 0}
    rotations_dict = {"1LB 1I 2RG" : 0, "1LB 3I" : 0, "1LB 2I 1RG" : 0, "1LB 2RG" : 0, 
                      "1LB 1I 1RG" : 0, "1LB 2I" : 0, "1LB 1RG": 0, "1LB 1I": 0, 
                      "2LB 2I" : 0, "2LB 2RG" : 0, "2LB 1I 1RG" : 0, "2LB 1I" : 0, "2LB 1RG" : 0, "2LB" : 0, 
                      "3LB 1I" : 0, "3LB 1RG" : 0, "3LB" : 0,
                      "Other" : 0}
    sequence = []

    i = 0
    while len(boss_tanks) < 3:
        boss_tanks.append("X")
        i += 1

    LB_tank_flags = [False, False, False]
    starting_tank = None

    for i, row in (df.iterrows()):
        
        if len(sequence) == 4:
            rotations_dict = count_rotations(sequence, rotations_dict)
            LB_tank_flags = [False, False, False]
            sequence = []

        # Ignore casts that are off the global cooldown
        if row["Ability"] in ["Hopped", "Essence", "Dark", "Restore"]: continue
        temp = track_off_GCD(row, GCD_time)
        GCD_time = temp[0]
        if not temp[1]: 
            continue  
            
        # If LB refreshed on primary tank, record and restart the sequence
        if row['Ability'] == 'Lifebloom' and row["Target"] == starting_tank:
            if len(sequence) > 0: 
                rotations_dict = count_rotations(sequence, rotations_dict)

            sequence = []
            LB_tank_flags = [False, False, False]
            if row["Target"] == boss_tanks[0]: LB_tank_flags[0] = True
            elif row["Target"] == boss_tanks[1]: LB_tank_flags[1] = True
            elif row["Target"] == boss_tanks[2]: LB_tank_flags[2] = True


            sequence.append(row["Ability"])
            continue

        # Single tank
        if row['Ability'] == 'Lifebloom' and row["Target"] == boss_tanks[0] and LB_tank_flags[0] == False:
            if LB_tank_flags[1] == False and LB_tank_flags[2] == False: 
                starting_tank = boss_tanks[0]
                if len(sequence) > 0: 
                    rotations_dict = count_rotations(sequence, rotations_dict)
                sequence = []

            sequence.append(row['Ability'])

            LB_tank_flags[0] = True
            continue

        # If two tanks (Anetheron, Azgalor, ..)
        elif row['Ability'] == 'Lifebloom' and row["Target"] == boss_tanks[1] and LB_tank_flags[1] == False:
            if LB_tank_flags[0] == False and LB_tank_flags[2] == False: 
                starting_tank = boss_tanks[1]
                if len(sequence) > 0: 
                    rotations_dict = count_rotations(sequence, rotations_dict)
                sequence = []

            sequence.append(row['Ability'])

            LB_tank_flags[1] = True
            continue


        # If three tanks (Akama, Council)
        elif row['Ability'] == 'Lifebloom' and row["Target"] == boss_tanks[2] and LB_tank_flags[2] == False:
            if LB_tank_flags[0] == False and LB_tank_flags[1] == False: 
                starting_tank = boss_tanks[2]
                if len(sequence) > 0: 
                    rotations_dict = count_rotations(sequence, rotations_dict)
                sequence = []

            sequence.append(row['Ability'])

            LB_tank_flags[2] = True
            continue


        if row['Ability'] == "Regrowth": 
            sequence.append("Regrowth")

        else: 
            sequence.append("Instant")    

    # Convert rotation counts to percentages
    total = 0
    for key in rotations_dict:
        total += rotations_dict[key]

    for key in rotations_dict:
        rotations_dict[key] = round(float(rotations_dict[key]) / total, 3)

    # Pick out the top two rotations used
    max_key = max(rotations_dict, key = rotations_dict. get)
    rotation_1 = [max_key, rotations_dict[max_key]]

    rotations_dict.pop(max_key)

    max_key = max(rotations_dict, key=rotations_dict. get)
    rotation_2 = [max_key, rotations_dict[max_key]]

    return [rotation_1, rotation_2]
    
    
def countX(lst, x):
    return lst.count(x)


def count_rotations(lst, rotations_dict):
    LB_count = countX(lst, "Lifebloom")
    I_count = countX(lst, "Instant")
    RG_count = countX(lst, "Regrowth")
    
    if len(lst) == 4:
        if LB_count == 1:
            if I_count == 1 and RG_count == 2:
                rotations_dict["1LB 1I 2RG"] += 1
                
            elif I_count == 2 and RG_count == 1:
                rotations_dict["1LB 2I 1RG"] += 1
                
            elif I_count == 3 and RG_count == 0:
                rotations_dict["1LB 3I"] += 1
            
            
        elif LB_count == 2:
            if I_count == 2 and RG_count == 0:
                rotations_dict["2LB 2I"] += 1
                
            elif I_count == 0 and RG_count == 2:
                rotations_dict["2LB 2RG"] += 1

            elif I_count == 1 and RG_count == 1:
                rotations_dict["2LB 1I 1RG"] += 1
                
        elif LB_count == 3:
            if I_count == 1 and RG_count == 0:
                rotations_dict["3LB 1I"] += 1
                
            elif I_count == 0 and RG_count == 1:
                rotations_dict["3LB 1RG"] += 1
            

    elif len(lst) == 3:
        if LB_count == 1: 
            if I_count == 1 and RG_count == 1:
                rotations_dict["1LB 1I 1RG"] += 1
            
            elif I_count == 2 and RG_count == 0:
                rotations_dict["1LB 2I"] += 1
            
            elif I_count == 0 and RG_count == 2:
                rotations_dict["1LB 2RG"] += 1  
                
        elif LB_count == 2:
            if I_count == 1 and RG_count == 0:
                rotations_dict["2LB 1I"] += 1
                
            elif I_count == 0 and RG_count == 1:
                rotations_dict["2LB 1RG"] += 1
                
        elif LB_count == 3:
            if I_count == 0 and RG_count == 0:
                rotations_dict["3LB"] += 1
            
            
    elif len(lst) == 2:
        if LB_count == 1:
            if I_count == 1 and RG_count == 0:
                rotations_dict["1LB 1I"] += 1
                
            elif I_count == 0 and RG_count == 1:
                rotations_dict["1LB 1RG"] += 1
                
        elif LB_count == 2:
            if I_count == 0 and RG_count == 0:
                rotations_dict["2LB"] += 1
                      
    else:
        rotations_dict["Other"] += 1
        
        
    return rotations_dict

        
def track_off_GCD(row, GCD_time):  # Spell casts that are off-GCD (trinkets, etc) should not go into the rotation
    GCD_time["t1"] = GCD_time["t2"]
    GCD_time["t2"] = datetime.strptime(str(row['Minute']) + ":" + str(row['Second']), "%M:%S.%f") 
    
    if type(GCD_time["t2"]) == datetime and type(GCD_time["t1"]) == datetime:
        
        try:
            if float(str((GCD_time["t2"] - GCD_time["t1"]))[5:]) < 0.4:
                return [GCD_time, False]
        except ValueError:
            return [GCD_time, True]

    return [GCD_time, True]
        
        
def export_to_excel(boss, to_append, player_df, char_name):
    series = pd.Series(to_append, index = player_df.columns)
    player_df = player_df.append(series, ignore_index = True)

    # Export dataframe to csv
    player_df.to_csv(f"character_data/{boss.replace(' ', '')}_{char_name}.csv", index = None)

    # Add data to the excel spreadsheet, sort sheet by rank
    add_row_to_xlsx(boss, char_name)
    sort_excel(boss)
    
    
def add_row_to_xlsx(boss, char_name):
    boss = boss.replace(" ", "")
    wb = openpyxl.load_workbook('character_data/character_data.xlsx')
    ws = wb.get_sheet_by_name(boss)
    sheet = wb[boss]
    rows = ws.max_row

    with open(f'character_data/{boss}_{char_name}.csv', 'r') as csvfile:
            for i, line in enumerate(csvfile.readlines()):
                if i == 0: continue  # Skip header

                line = line[ : -1]  # Remove the newline character at the end of each string
                elements = line.split(",")

                for i2, element in enumerate(elements):
                    sheet[chr(i2 + 65) + str(i + rows)] = element

    wb.save('character_data/character_data.xlsx')
    
    
def sort_excel(boss):
    boss = boss.replace(" ", "")
    wb = openpyxl.load_workbook('character_data/character_data.xlsx')
    ws = wb.get_sheet_by_name(boss)
    sheet = wb[boss]
    rows = ws.max_row
    
    excel = win32com.client.Dispatch("Excel.Application")
    wb = excel.Workbooks.Open('C:\\Users\\Matth\\git\\DataAnalysisWorkbooks\\warcraftLogs\\character_data\\character_data.xlsx')
    ws = wb.Worksheets(boss)
    ws.Range('A2:Q'+str(rows+1)).Sort(Key1 = ws.Range('E1'), Order1 = 2, Orientation = 1)
    wb.Save()
    excel.Application.Quit()