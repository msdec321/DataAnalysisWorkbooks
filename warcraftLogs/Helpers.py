import selenium, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import pandas as pd
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
            
            
            
            
            
            
def get_spell_info(browser, table_dict):

    df = pd.DataFrame(pd.np.empty((0, 10)))
    df.columns = ["Spell", "Amount", "Casts", "Avg Cast", "Hits", "Avg Hit", "Crit %", "Uptime %", "Overheal", "HPS"]

    spell_ids = ['ability-33763-0', 'ability-33778-0', 'ability-26982-0', 'ability-26980-0', 'ability-18562-0']

    for spell in spell_ids:
        search = scroll(browser.find_element_by_id(spell))

        td_p_input = search.find_element_by_xpath('.//ancestor::td')
        tr_p_input = search.find_element_by_xpath('.//ancestor::tr')
        td_p_input = tr_p_input.find_elements(By.XPATH, 'td')

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

        df = df.append(table_dict, ignore_index=True)
        
    print(df.head())
    
    return table_dict
    

def get_tanks(browser):
    temp_url = browser.current_url
        
    a = browser.find_element_by_id("filter-fight-boss-text")
    a.click()
    time.sleep(1)

    b = browser.find_element_by_link_text("Encounters and Trash Fights")
    b.click()
    time.sleep(1)

    # Get tanks via top 3 damage taken
    scroll_click(browser.find_element_by_link_text("Damage Taken"))
    time.sleep(1)

    search = browser.find_element_by_id("main-table-0")
    tb_p_input = search.find_elements(By.XPATH, 'tbody')
    td_p_input = tb_p_input[0].find_elements(By.XPATH, 'tr')
    
    tanks = []
    for i in range(3):
       tanks.append(td_p_input[i].text.split("\n")[0])

    # Return to boss page
    browser.get(temp_url)
    
    return tanks


def get_boss_tanks(boss, browser, tanks):
    temp_url = browser.current_url
    
    nTanks = tanks#boss_nTanks_dict[boss]
    
    scroll_click(browser.find_element_by_link_text("Damage Taken"))
    time.sleep(1)

    search = browser.find_element_by_id("main-table-0")
    tb_p_input = search.find_elements(By.XPATH, 'tbody')
    td_p_input = tb_p_input[0].find_elements(By.XPATH, 'tr')

    tanks = []
    for i in range(nTanks):
       tanks.append(td_p_input[i].text.split("\n")[0])
    
    browser.get(temp_url)
    
    return tanks


def get_player_HPS(browser, char_name):
    search = browser.find_element_by_id("main-table-0")
    tb_p_input = search.find_elements(By.XPATH, 'tbody')
    td_p_input = tb_p_input[0].find_elements(By.XPATH, 'tr')

    for i, item in enumerate(td_p_input):
        temp = td_p_input[i].text.split("\n")
    
        if temp[1] == char_name: 
            return temp[3].split(" ")[-1]
        
        
        
def download_cast_sequence(browser):

    body = browser.find_element_by_css_selector('body')
    body.send_keys(Keys.HOME)
    time.sleep(1)

    a = browser.find_element_by_link_text("Events")
    a.click()
    time.sleep(1)

    body.send_keys(Keys.HOME)
    time.sleep(1)

    scroll_click(browser.find_element_by_link_text("Casts"))
    time.sleep(1)
    
    body = browser.find_element_by_css_selector('body')
    body.send_keys(Keys.END)
    time.sleep(1)

    a = body.find_element_by_tag_name("button")
    a.click()
    
    
def clean_csv():
    df = pd.read_csv('cast_sequences/casts.csv')
    df = df.drop(['Unnamed: 4'], axis=1)

    temp_df = df['Ability'].str.split(" ", expand=True)
    df['Ability'] = temp_df[0]
    df['Cast Time'] = temp_df[1]

    temp_df = df['Source → Target'].str.split(" ", expand=True)
    df['Target'] = temp_df[2]

    df = df.drop(['Source → Target'], axis=1)
    
    # Split time into minute and second
    temp_df = df['Time'].str.split(":", expand=True)
    df['Minute'] = temp_df[0]
    df['Second'] = temp_df[1]

    df['Minute'] = pd.to_numeric(df['Minute'])
    df['Second'] = pd.to_numeric(df['Second'])
    
    return df


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


def calculate_rotations(df, MT):
    MT_bloom = {"LB1" : 0, "LB2" : 0}
    GCD_time = {"t1" : 0, "t2" : 0}
    rotations_dict = {"LB 1I 2RG" : 0, "LB 3I" : 0, "LB 2I 1RG" : 0, "LB 2RG" : 0, 
                      "LB 1I 1RG" : 0, "LB 2I" : 0, "LB 1RG": 0, "LB 1I": 0, "Other" : 0}
    
    abilities = ["Regrowth"]
    sequence = []

    for i, row in (df.iterrows()):

        #track_dropped_LB(row)
        temp = track_off_GCD(row, GCD_time)
        GCD_time = temp[0]
        if not temp[1]: continue  

        if row['Ability'] == 'Lifebloom' and row['Target'] == MT:
            if len(sequence) == 3:
                rotations_dict = count_rotations(sequence, rotations_dict)

            sequence = []
            sequence.append(row['Ability'])
            continue


        if row['Ability'] in abilities: 
            sequence.append(row['Ability'])

        else: 
            sequence.append("Instant")

        if len(sequence) == 4:
            rotations_dict = count_rotations(sequence, rotations_dict)
            sequence = []
            
            
    # Calculate rotation percentages
    total = 0
    total += rotations_dict['LB 1I 2RG']
    total += rotations_dict['LB 3I']
    total += rotations_dict['LB 2I 1RG']
    total += rotations_dict['LB 2RG']
    total += rotations_dict["LB 1I 1RG"]
    total += rotations_dict["LB 2I"]
    total += rotations_dict["LB 1RG"]
    total += rotations_dict["LB 1I"]
    total += rotations_dict['Other']

    rotations_dict['LB 1I 2RG'] = round(float(rotations_dict['LB 1I 2RG']) / total, 3)
    rotations_dict['LB 3I'] = round(float(rotations_dict['LB 3I']) / total, 3)
    rotations_dict['LB 2I 1RG'] = round(float(rotations_dict['LB 2I 1RG']) / total, 3)
    rotations_dict['LB 2RG'] = round(float(rotations_dict['LB 2RG']) / total, 3)
    rotations_dict['LB 1I 1RG'] = round(float(rotations_dict['LB 1I 1RG']) / total, 3)
    rotations_dict['LB 2I'] = round(float(rotations_dict['LB 2I']) / total, 3)
    rotations_dict['Other'] = round(float(rotations_dict['Other']) / total, 3)
    
    # Save the top two rotations
    
    max_key = max(rotations_dict, key=rotations_dict. get)
    rotation_1 = [max_key, rotations_dict[max_key]]

    rotations_dict.pop(max_key)

    max_key = max(rotations_dict, key=rotations_dict. get)
    rotation_2 = [max_key, rotations_dict[max_key]]

    if rotation_1[1] - rotation_2[1] > 0.5:
        return [rotation_1]
    
    else: 
        return [rotation_1, rotation_2]
    
    
    
def countX(lst, x):
    return lst.count(x)


def count_rotations(lst, rotations_dict):
    I_count = countX(lst, "Instant")
    RG_count = countX(lst, "Regrowth")
    
    if len(lst) == 4:
    
        if I_count == 1 and RG_count == 2:
            rotations_dict["LB 1I 2RG"] += 1

        elif I_count == 2 and RG_count == 1:
            rotations_dict["LB 2I 1RG"] += 1

        elif I_count == 3 and RG_count == 0:
            rotations_dict["LB 3I"] += 1


    elif len(lst) == 3:
        if I_count == 1 and RG_count == 1:
            rotations_dict["LB 1I 1RG"] += 1
            
        elif I_count == 2 and RG_count == 0:
            rotations_dict["LB 2I"] += 1
            
        elif I_count == 0 and RG_count == 2:
            rotations_dict["LB 2RG"] += 1    
            
            
    else:
        rotations_dict["Other"] += 1
        
    return rotations_dict
        
        
def track_off_GCD(row, GCD_time):  # Spell casts that are off-GCD (trinkets, etc) should not go into the rotation
    GCD_time["t1"] = GCD_time["t2"]
    GCD_time["t2"] = datetime.strptime(str(row['Minute']) + ":" + str(row['Second']), "%M:%S.%f") 
    
    if type(GCD_time["t2"]) == datetime and type(GCD_time["t1"]) == datetime:
        
        if float(str((GCD_time["t2"] - GCD_time["t1"]))[5:]) < 0.75:
            return [GCD_time, True]
        
    return [GCD_time, False]

    
def track_dropped_LB(row):
    
    if type(MT_bloom["LB2"]) == datetime and type(MT_bloom["LB1"]) == datetime:
        
        if float(str((MT_bloom["LB2"] - MT_bloom["LB1"]))[5:]) > 7.00: 
            print('Lifebloom dropped at', row['Time'] + "!\n")
            MT_bloom["LB1"], MT_bloom["LB2"] = 0, 0
            
    if row['Ability'] == 'Lifebloom' and row['Target'] == MT:
        MT_bloom["LB1"] = MT_bloom["LB2"]
        MT_bloom["LB2"] = datetime.strptime(str(row['Minute']) + ":" + str(row['Second']), "%M:%S.%f")  