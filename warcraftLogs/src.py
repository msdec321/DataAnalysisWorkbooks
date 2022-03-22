import selenium, time, csv, os, openpyxl, fnmatch, shutil
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
    


def get_phase3_bosses(browser):
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


# This function will try to click on an element, but if it isn't visible on the page then it will scroll down and try again.
def scroll_click(command):
    link = command
    time.sleep(1)
    
    while True:
        try:
            link.click()
            break
            
        except ElementClickInterceptedException:
            body = browser.find_element_by_css_selector('body')
            body.click()
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            
            
# Scroll down without clicking            
def scroll(command):
    link = command
    time.sleep(1)
    
    while True:
        try:
            return link
            break
            
        except ElementClickInterceptedException:
            body = browser.find_element_by_css_selector('body')
            body.click()
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            
            
def get_boss_data(browser, i):
    search = browser.find_elements_by_class_name("character-table-link")

    rank = browser.find_element_by_link_text(search[i*6].text)
    HPS = browser.find_element_by_link_text(search[(i*6)+2].text)
    time = browser.find_element_by_link_text(search[(i*6)+3].text)
    return rank, rank.text, HPS.text, time.text           
            
            
def get_spell_info(browser, total_HPS):

    #df = pd.DataFrame(pd.np.empty((0, 10)))
    #df.columns = ["Spell", "Amount", "Casts", "Avg Cast", "Hits", "Avg Hit", "Crit %", "Uptime %", "Overheal", "HPS"]
    

    # Lifebloom (tick), Lifebloom (bloom), Rejuv, Regrowth, Swiftmend
    LB_uptime = 0
    spell_percent_HPS_dict = {"ability-33763-0" : 0, "ability-33778-0" : 0, "ability-26982-0" : 0, "ability-26980-0" : 0, "ability-18562-0" : 0}
    spell_ids = ['ability-33763-0', 'ability-33778-0', 'ability-26982-0', 'ability-26980-0', 'ability-18562-0']

    
    for spell in spell_ids:
        
        try:
            search = scroll(browser.find_element_by_id(spell))

            td_p_input = search.find_element_by_xpath('.//ancestor::td')
            tr_p_input = search.find_element_by_xpath('.//ancestor::tr')
            td_p_input = tr_p_input.find_elements(By.XPATH, 'td')

            ''' # Outdated
            table_dict["Spell"] = search.text
            table_dict["Amount"] = td_p_input[1].text.split('\n')[1]
            table_dict["Casts"] = td_p_input[2].text

            if spell == 'ability-26980-0':
                table_dict["Avg Cast"] = td_p_input[3].text.split()[0]
                table_dict["Hits"] = td_p_input[4].text.split()[0]
                table_dict["Avg Hit"] = td_p_input[5].text.split()[0]

            else:
                table_dict["Avg Cast"] = td_p_input[3].text
                table_dict["Hits"] = td_p_input[4].text
                table_dict["Avg Hit"] = td_p_input[5].text

            table_dict["Crit %"] = td_p_input[6].text
            table_dict["Uptime %"] = td_p_input[7].text
            table_dict["Overheal"] = td_p_input[8].text
            table_dict["HPS"] = td_p_input[9].text
            '''
            
            spell_percent_HPS_dict[spell] = round(float(td_p_input[9].text) / float(total_HPS), 2)
            
            if spell == 'ability-33763-0':
                LB_uptime = td_p_input[7].text
            #df = df.append(table_dict, ignore_index=True)
            
        except:
            pass
        
    #print(df.head())

    return spell_percent_HPS_dict['ability-33763-0'], spell_percent_HPS_dict['ability-33778-0'], spell_percent_HPS_dict['ability-26982-0'], spell_percent_HPS_dict['ability-26980-0'], spell_percent_HPS_dict['ability-18562-0'], LB_uptime
    #return table_dict
    
    
def get_nHealers(browser):
    click_on_element_by_id(browser, "filter-summary-tab")  
    time.sleep(0.5)
    
    click_on_element_by_id(browser, "filter-analytical-tab")
    time.sleep(1.0)
    
    d = browser.find_elements_by_class_name("composition-row")
    return len(d[2].text.split("\n")) - 1
    

def get_tanks(browser):
    NPCS = ["Akama", "Alliance Footman", "Alliance Knight", "Alliance Rifleman",
        "Alliance Priest", "Alliance Sorceress", "Horde Grunt", "Horde Headhunter",
        "Horde Shaman", "Horde Witch Doctor", "Thrall", "Night Elf Huntress",
        "Tyrande Whisperwind", "Night Elf Archer", "Druid of the Claw", "Dryad",
        "Night Elf Ancient of Lore", "Druid of the Talon", "Night Elf Ancient of War"]
    
    temp_url = browser.current_url

    click_on_element_by_id(browser, "filter-fight-boss-text") 
    time.sleep(1)

    c = browser.find_elements_by_class_name("report-overview-boss-caption")
    c[0].click()
    time.sleep(1)

    # Get tanks via top 3 damage taken
    click_on_element_by_id(browser, "filter-damage-taken-tab")
    time.sleep(1)

    search = browser.find_element_by_id("main-table-0")
    tb_p_input = search.find_elements(By.XPATH, 'tbody')
    td_p_input = tb_p_input[0].find_elements(By.XPATH, 'tr')
    
    tanks = []
    i = 0
    while True:
        if td_p_input[i].text.split("\n")[0] in NPCS: 
            i += 1
            continue
            
        if len(tanks) == 3: break
            
        tanks.append(td_p_input[i].text.split("\n")[0])
        i += 1

    # Return to boss page
    browser.get(temp_url)
    
    return tanks


def get_boss_tanks(browser, all_tanks, nTanks):
    
    temp_url = browser.current_url
    
    scroll_click(browser.find_element_by_link_text("Damage Taken"))
    time.sleep(1)

    search = browser.find_element_by_id("main-table-0")
    tb_p_input = search.find_elements(By.XPATH, 'tbody')
    td_p_input = tb_p_input[0].find_elements(By.XPATH, 'tr')

    tanks = []
    
    i = 0
    while True:
        if len(tanks) == nTanks: break
     
        if td_p_input[i].text.split("\n")[0] not in all_tanks:
            i += 1
            continue
         
        else:
            tanks.append(td_p_input[i].text.split("\n")[0])
            
        i += 1
    
    browser.get(temp_url)
    
    return tanks


def get_player_HPS(browser, char_name):
    time.sleep(1)
    search = browser.find_element_by_id("main-table-0")
    tb_p_input = search.find_elements(By.XPATH, 'tbody')
    td_p_input = tb_p_input[0].find_elements(By.XPATH, 'tr')

    for i, item in enumerate(td_p_input):
        temp = td_p_input[i].text.split("\n")
    
        if temp[1] == char_name: 
            return temp[3].split(" ")[-1]
        
        
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
        a = browser.find_element_by_id("main-table-128-0")
        b = a.text.split('\n')

        # Check if innervate is present in the table.
        if len(fnmatch.filter(b, 'Innervate??')) > 0: 
            return 'Yes'

        else: 
            return 'No'
        
    # If the 'major group cooldown' table is not present then the player wasn't innervated.
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
            #a.click()
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
            #a.click()
            action.perform()
            time.sleep(0.5)
            action.click()
            action.perform()
            break
        
        except:
            body = browser.find_element_by_css_selector('body')
            body.click()
            body.send_keys(Keys.PAGE_UP)
            
            
def download_csv(browser, temp_url, id_tag, path):
    body = browser.find_element_by_css_selector('body')
    body.send_keys(Keys.PAGE_UP)
    time.sleep(1)
    
    click_on_element_by_id(browser, "filter-events-tab")    
    time.sleep(1)

    click_on_element_by_id(browser, id_tag)
    time.sleep(1)
    
    click_on_element_by_class_name(browser, "buttons-csv")
    time.sleep(3)
    
    shutil.move("C:/Users/Matth/Downloads/Warcraft Logs - Combat Analysis for Warcraft.csv", f"C:/Users/Matth/git/DataAnalysisWorkbooks/warcraftLogs/{path}")
    
    browser.get(temp_url)
    time.sleep(1)
    
           
def clean_dmg_taken_csv(boss):

    df = pd.read_csv('damage_taken/dmg_taken.csv')
    df = df.drop(['Unnamed: 2'], axis=1)

    temp_df = df['Event'].str.split(" ", expand=True)
    
    if boss in ["Kaz'rogal", "Archimonde", "Supremus"]:
        df['Source'] = temp_df[0]
        df['Action'] = temp_df[1]
        df['Target'] = temp_df[2]
        
    elif boss in ["Rage Winterchill", "Teron Gorefiend", "Gurtogg Bloodboil", "Mother Shahraz"]:
        df['Source'] = temp_df[0] + " " + temp_df[1]
        df['Action'] = temp_df[2]
        df['Target'] = temp_df[3]
        
    elif boss in ["High Warlord Naj'entus"]:
        df['Source'] = temp_df[0] + " " + temp_df[1] + " " + temp_df[2]
        df['Action'] = temp_df[3]
        df['Target'] = temp_df[4]
        
    df = df.drop(['Event'], axis=1)
    
    return df    

 
def clean_cast_sequence_csv():
    df = pd.read_csv('cast_sequence/casts.csv')
    
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
    
    correct_cast_csv_whitespace()
    
    return df


# Fix orrcurances where there is a double whitespace in the pandas dataframe
def correct_cast_csv_whitespace():

    filename = 'cast_sequence/casts.csv'
    with open(filename, 'r') as csvfile:
        outputFile = open("cast_sequence/casts_fixed.csv", "w")

        datareader = csv.reader(csvfile)
        outputWriter = csv.writer(outputFile, lineterminator='\n')

        for row in datareader:
            if len(row) == 0: continue

            for i, item in enumerate(row):
                row[i] = row[i].replace("  ", " ")
            outputWriter.writerow(row)
        outputFile.close()

    os.system("mv cast_sequence/casts_fixed.csv cast_sequence/casts.csv")



# Add boss target to df by checking the boss' melee target
def add_boss_target(boss, df, df2):
    for index, row in (df.iterrows()):
    
        for index2, row2 in (df2.iterrows()):

            t1 = datetime.strptime(str(row['Time']), "%M:%S.%f") 
            t2 = datetime.strptime(str(row2['Time']), "%M:%S.%f") 

            if str(t2 - t1)[0] != "-" and row["Source"] == boss and row["Action"] == "Melee":

                df2["Boss Target"].iloc[index2] = row["Target"]
                break
                
    return df2



# Fix NaN boss targets by replacing NaN with the most recent boss target
def fix_boss_target(df):

    temp = ['', '']
    for i, row in df.iterrows():

        if pd.isna(row['Boss Target']):
            df["Boss Target"].iloc[i] = temp[0]

        else:
            temp[0] = temp[1]
            temp[1] = row['Boss Target']
        
    return df


# For non-instant casts, the time is specified at the end of the cast. This causes issues when regrowth is followed by an instant cases
# This function changes the time specified to the start of the regrowth cast rather than the end of it. (Including cancel-casts)

def fix_regrowth_cast_time(df):
    temp = []
    for i, row in df.iterrows():
        if row['Ability'] == 'Regrowth' and row["Cast Time"] != "Canceled":
            a = str(datetime.strptime(str(row['Minute']) + ":" + str(row['Second']), "%M:%S.%f") - datetime.strptime(row['Cast Time'], "%S.%f"))
            a = a.split(".")
            b = a[0].split(":")
            c = b[1] + ":" + b[2] + "." + a[1][:3]
            temp.append(c)

        else:
            temp.append(row["Time"])

    df["Time"] = temp
    
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
        temp = track_off_GCD(row, GCD_time)
        GCD_time = temp[0]
        if not temp[1]: continue  
            
        # For most single-tank bosses, the main tank is the boss' current melee target.
        if boss in ["Rage Winterchill", "Kaz'rogal", "Archimonde", "High Warlord Naj'entus", "Supremus", 
                    "Teron Gorefiend", "Gurtogg Bloodboil", "Mother Shahraz"]:
            
            if row['Ability'] == 'Lifebloom' and row['Target'] == row['Boss Target']:
                if len(sequence) >= 2:
                    rotations_dict = count_rotations(sequence, rotations_dict)

                sequence = []
                sequence.append(row['Ability'])
                continue  
                
        else:   
            # If LB refreshed on primary tank, restart the sequence
            if row['Ability'] == 'Lifebloom' and row["Target"] == starting_tank:
                rotations_dict = count_rotations(sequence, rotations_dict)
                sequence = []
                LB_tank_flags = [False, False, False]
                sequence.append(row["Ability"])
                continue

            # Single tank
            if row['Ability'] == 'Lifebloom' and row["Target"] == boss_tanks[0] and LB_tank_flags[0] == False:
                if LB_tank_flags[1] == False and LB_tank_flags[2] == False: 
                    starting_tank = boss_tanks[0]
                    rotations_dict = count_rotations(sequence, rotations_dict)
                    sequence = []

                sequence.append(row['Ability'])

                LB_tank_flags[0] = True
                continue

            # If two tanks (Anetheron, Azgalor, ..)
            elif row['Ability'] == 'Lifebloom' and row["Target"] == boss_tanks[1] and LB_tank_flags[1] == False:
                if LB_tank_flags[0] == False and LB_tank_flags[2] == False: 
                    starting_tank = boss_tanks[1]
                    rotations_dict = count_rotations(sequence, rotations_dict)
                    sequence = []

                sequence.append(row['Ability'])

                LB_tank_flags[1] = True
                continue


            # If three tanks (Akama, Council)
            elif row['Ability'] == 'Lifebloom' and row["Target"] == boss_tanks[2] and LB_tank_flags[2] == False:
                if LB_tank_flags[0] == False and LB_tank_flags[1] == False: 
                    starting_tank = boss_tanks[2]
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
        
        if float(str((GCD_time["t2"] - GCD_time["t1"]))[5:]) < 0.4:
            return [GCD_time, False]
        
    return [GCD_time, True]


def clear_character_data():
    p = Path('./character_data/')
    
    for f in os.listdir(p):
        os.remove(os.path.join(p, f))


# Combine multiple csv files into a single excel spreadsheet.
def combine_character_data(char_name):
    wb = openpyxl.Workbook()
    p = Path('./character_data/')

    for i, filename in enumerate(p.glob('*.csv')):
        # Pick out the boss name for the name of the worksheet
        temp = str(filename).replace('\\', '_')
        temp = temp.replace(" ", "")
        temp = temp.split("_")
        wb.create_sheet(temp[2])
        sheet = wb[temp[2]]

        with open(filename, 'r') as myFile:

            for i2, line in enumerate(myFile.readlines()):
                line = line[ : -1]  # Remove the newline character at the end of each string
                elements = line.split(",")

                for i3, element in enumerate(elements):
                    sheet[chr(i3 + 65) + str(i2 + 1)] = element

    # Remove the first blank sheet
    std = wb.get_sheet_by_name('Sheet')
    wb.remove_sheet(std)

    wb.save(p/f"{char_name}.xlsx")