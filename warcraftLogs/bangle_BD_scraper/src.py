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


def load_scraper(path_ublock, chrome, firefox):
    if chrome and not firefox:
        chrome_options = Options()
        chrome_options.add_argument('load-extension=' + path_ublock)

        browser = webdriver.Chrome(chrome_options=chrome_options)

        time.sleep(5)
        
    elif not chrome and firefox:
        browser = webdriver.Firefox() 
        browser.install_addon('C:/Users/Matth/Downloads/adblock_plus-3.11.4-an+fx.xpi')
        
    else:
        print("Error: Please choos either Chrome or Firefox for selenium.")
        return None

    browser.switch_to.window(browser.window_handles[0])
    browser.get(f"https://classic.warcraftlogs.com/zone/rankings/1011/#metric=speed&boss=704")
    time.sleep(3)
    
    cookie = browser.find_element_by_class_name("cc-compliance")
    cookie.click()
    
    return browser.current_url, browser 


def get_latest_ranks(browser, nParses):
    
    temp_df = pd.DataFrame(pd.np.empty((0, 3)))
    temp_df.columns = ["Rank", "Guild name", "Duration"]
    
    page = 1

    for i in range(1, nParses + 200):
        if i % 100 == 0: print(i)
            
        row = browser.find_element_by_id(f"row-704-{i}")
        
        try:
            rank = row.text.split("\n")[0]
            guild_name = row.text.split("\n")[1]
            duration = row.text.split("\n")[3].split(" ")[-1]
        
        except: continue
        
        to_append = [rank, guild_name, duration]

        series = pd.Series(to_append, index = temp_df.columns)
        temp_df = temp_df.append(series, ignore_index = True)
        
        if i % 50 == 0: 
            page += 1
            browser.get(f'https://classic.warcraftlogs.com/zone/rankings/1011/#metric=speed&boss=704&page={page}')
            time.sleep(3) 

    temp_df.to_csv(f"temp.csv", index = None, encoding='utf-8-sig')
    
    return update_ranks()


def update_ranks():

    wb = openpyxl.load_workbook("bangle_bluedragon.xlsx")

    ws = wb.get_sheet_by_name("BangleBD")
    rows = ws.max_row
    
    already_recorded_indices = []

    for row in ws.iter_rows():
        if row[0].value in ["Rank", None]: continue  # Skip headers

        with open(f'temp.csv', 'r', encoding='utf-8-sig') as csvfile:

            for i, line in enumerate(csvfile.readlines()):
                if i==0: continue

                line = line[ : -1]  # Remove the newline character at the end of each string
                elements = line.split(",")      

                # If player in spreadsheet but different rank than on WCL then update the spreadsheet
                if [elements[1], elements[2]] == [row[2].value, row[3].value] and int(float(elements[0])) != row[0].value:
                    print(f"Rank updated: {row[0].value} to {int(float(elements[0]))}, {elements[1]}, {elements[2]}")
                    row[0].value = int(float(elements[0]))
                    already_recorded_indices.append(int(float(elements[0])))

                # If player found in spreadsheet, note to not scrape this rank and move to the next player.
                elif [int(float(elements[0])), elements[1], elements[2]] == [row[0].value, row[2].value, row[3].value]:
                    already_recorded_indices.append(row[0].value)
                    
                 
    wb.save("bangle_bluedragon.xlsx")
    wb.save("bangle_bluedragon_backup.xlsx")
    os.remove(f"temp.csv")
        
    return already_recorded_indices

        
def click_on_element_by_id(browser, id_tag):    
    tag = browser.find_element_by_id(id_tag)
    time.sleep(1)
    
    for j in range(20):
        action = ActionChains(browser)
        action.move_to_element(tag)
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
    

def export_to_csv(to_append, player_df, char_name):
    series = pd.Series(to_append, index = player_df.columns)
    player_df = player_df.append(series, ignore_index = True)

    # Export dataframe to csv
    player_df.to_csv(f"bangleBD_{char_name}.csv", index = None, encoding='utf-8-sig')
    add_row_to_xlsx(char_name)
    
    
def add_row_to_xlsx(char_name):
    wb = openpyxl.load_workbook('bangle_bluedragon.xlsx')

    ws = wb.get_sheet_by_name("BangleBD")
    sheet = wb["BangleBD"]
    rows = ws.max_row

    with open(f"bangleBD_{char_name}.csv", 'r', encoding='utf-8-sig') as csvfile:
        
        for i, line in enumerate(csvfile.readlines()):
            if i == 0: continue  # Skip header

            line = line[ : -1]  # Remove the newline character at the end of each string
            elements = line.split(",")

            for i2, element in enumerate(elements):
                sheet[chr(i2 + 65) + str(i + rows)] = element

    wb.save('bangle_bluedragon.xlsx')
            
            
def get_time_in_combat(browser):
    
    total_trash_time = 0
    trash_table = browser.find_element_by_id("fight-details-0-0")
    trash_info = trash_table.text.split("\n")

    # Get the total time a player was in combat with trash
    for trash in trash_info:
        trash_time = trash.split(" ")[-3]
        trash_time = trash_time[1:-1]
        minute = trash_time.split(":")[0]
        sec = trash_time.split(":")[1]
        total_trash_time += int(minute)*60 + int(sec)

    total_boss_time = 0
    boss_table = browser.find_elements_by_class_name("report-overview-boss-box")

    # Get the total time a player was in combat with bosses.
    # Note this method will crash if the raid wiped on a boss (Unlikely for BT speedruns, but can wipe in Hyjal if that is in the log)
    for i in range(2, len(boss_table)-1):
        if i != len(boss_table)-2:
            boss_time = boss_table[i].text.split("\n")[1]
            boss_duration = boss_time.split(" ")[1]
            boss_duration = boss_duration[1:-1]

            minute = boss_duration.split(":")[0]
            sec = boss_duration.split(":")[1]
            total_boss_time += int(minute)*60 + int(sec)

        # The last boss on the table is labeled with "Last Pull", so handled differently than above.
        else:
            boss_time = boss_table[i].text.split("\n")[1]
            boss_duration = boss_time.split(" ")[4]
            boss_duration = boss_duration[1:-1]

            minute = boss_duration.split(":")[0]
            sec = boss_duration.split(":")[1]
            total_boss_time += int(minute)*60 + int(sec)

    # Return the total time in combat (in seconds)
    return total_trash_time + total_boss_time
            

def get_int_spirit(browser):
    
    # The intellect and spirit are listed on the character's summary page of the log
    # However, the Druid's stats tend to vary of the raid (buffs, consumes) and a range of stats are given.
    # So here we take the average intellect and spirit for the raid.
    
    stats_row = browser.find_element_by_class_name("composition-label")
    stats = stats_row.text.split("\n")
    
    intellect = stats[1].split(" - ")
    int_low = intellect[0].split(" ")[1]
    int_high = intellect[1]

    try: # If the spirit is a range (example: 730 - 780)
        spirit = stats[3].split(" - ")
        sp_low = spirit[0].split(" ")[1]
        sp_high = spirit[1]
        
        avg_sp = (float(sp_low) + float(sp_high)) / 2.
        
    except: # If the spirit is given as one number instead
        avg_sp = float(int(stats[3].split(" ")[1]))
    
    avg_int = (float(int_low) + float(int_high)) / 2.
    
    return avg_int, avg_sp


def calc_mana(intellect, spirit, bd_uptime, nOverlaps, bangle_use_uptime, overlap_uptime):
    
    # For Blue Dragon, multiply mana-per-second formula by 0.7 (Full regen ignoring intensity).
    # For only Bangle, multiply mana-per-second formula by 0.3 (Casting regen with intensity).
    # Multiply mana-per-second by the time the aura was active to get the total mana received.
    
    bd_mana = (0.009327 * np.sqrt(intellect) * spirit) * bd_uptime * 0.7 # While-not-casting regen
    bangle_mana = (0.009327 * np.sqrt(intellect) * 120.) * bangle_use_uptime * 0.3  # While-casting regen
    bd_bangle_mana = (0.009327 * np.sqrt(intellect) * 120.) * overlap_uptime * 0.7 # While not-casting regen
    bd_bangle_nonoverlap_mana = (0.009327 * np.sqrt(intellect) * 120.) *((20.*nOverlaps) - overlap_uptime) * 0.3
    
    return round(bd_mana, 2), round(bangle_mana, 2), round(bd_bangle_mana, 2), round(bd_bangle_nonoverlap_mana, 2)


def calc_mp5(time_in_combat, overlap_uptime, time_between_BD, bangle_uses, nOverlaps, bd_mana, bangle_mana, bd_bangle_mana, bd_bangle_nonoverlap_mana):
    
    # The mp5 (>>not normalized!<<) is the total mana received divided by the total time in combat (mana-per-second), then multiplied by 5.
    # Noralization is handled in the excel spreadsheet.
    
    bd_mp5 = (5 * bd_mana) / time_in_combat
    bangle_mp5 = (5 * bangle_mana) / time_in_combat
    bd_bangle_mp5 = (5 * bd_bangle_mana) / time_in_combat
    
    bangle_mp5_normalized = (bangle_mana) / ((bangle_uses - nOverlaps)*120) * 5
    bd_bangle_mp5_normalized = ( ( (bd_bangle_mana) / ( overlap_uptime + (nOverlaps * (120 +  time_between_BD))) ) + ( (bd_bangle_nonoverlap_mana) / ( ((20*nOverlaps) - overlap_uptime) + (nOverlaps * (120. + time_between_BD)))) ) * 5
    
    return round(bd_mp5, 2), round(bangle_mp5, 2), round(bd_bangle_mp5, 2), round(bangle_mp5_normalized, 2), round(bd_bangle_mp5_normalized, 2)

        
def get_bd_list(browser):
    headers =  browser.find_elements_by_class_name("event-view-mini-header")
    tables = browser.find_elements_by_class_name("summary-table")

    all_bd_procs = []

    for i, table in enumerate(tables):
        header_and_procs = []
        header_and_procs.append(headers[i].text)
        bd_procs = table.text.split("\n")
        
        # First four elements are just a description, remove them.
        for j in range(4):
            bd_procs.pop(0)

        all_descriptions_removed = False
        while not all_descriptions_removed:

            for j in range(len(bd_procs)):
                # Pop description elements "Aura of the Blue Dragon", etc. Leaving just the time related elements.
                if bd_procs[j][0] in ["A", "蓝"]: 
                    bd_procs.pop(j)
                    break

                # Once all description elements are popped, move to the next table
                if j == len(bd_procs) - 1:
                    all_descriptions_removed = True
                    break

        header_and_procs.append(bd_procs)
        all_bd_procs.append(header_and_procs)
    
    return all_bd_procs


def get_bangle_list(browser):

    headers =  browser.find_elements_by_class_name("event-view-mini-header")
    tables = browser.find_elements_by_class_name("summary-table")
    
    all_bangle_uses = []

    for i, table in enumerate(tables):
        header_and_uses = []
        header_and_uses.append(headers[i].text)
        bangle_use = table.text.split("\n")
        
        # First four elements are just a description, remove them.
        for j in range(4):
            bangle_use.pop(0)

        all_descriptions_removed = False
        while not all_descriptions_removed:

            for j in range(len(bangle_use)):
                
                # Pop description elements "Endless Blessings", etc. Leaving just the time related elements.
                if bangle_use[j][0] in ["E", "无", "自"]: 
                    bangle_use.pop(j)
                    break

                if j == len(bangle_use) - 1:
                    all_descriptions_removed = True
                    break

        header_and_uses.append(bangle_use)
        all_bangle_uses.append(header_and_uses)
        
    return all_bangle_uses


# Calculates the average amount of time (in seconds) between Blue Dragon procs.
def get_seconds_between_BD_procs(all_bd_procs):
    bd_aura_clock = []

    for i in range(len(all_bd_procs)):

        # Get the time-of-day the combat started in seconds
        hm = all_bd_procs[i][0].split(" ")[-2]
        hour = hm.split(":")[0]
        hour_in_sec = int(hour) * 3600.
        minutes = hm.split(":")[1]

        aura_start, aura_end = 0, 0
        for j in range(len(all_bd_procs[i][1])):

            # Time aura begans
            if all_bd_procs[i][1][j].split(" ")[1] == "Apply":
                proc_start = all_bd_procs[i][1][j].split(" ")[0]
                proc_start_min = int(proc_start.split(":")[0])
                proc_start_sec = float(proc_start.split(":")[1])

                aura_start = hour_in_sec + (float(minutes) + proc_start_min)*60 + proc_start_sec 

            # Time aura ended
            elif all_bd_procs[i][1][j].split(" ")[1] == "Remove":
                proc_end = all_bd_procs[i][1][j].split(" ")[0]
                proc_end_min = int(proc_end.split(":")[0])
                proc_end_sec = float(proc_end.split(":")[1])

                aura_end = hour_in_sec + (float(minutes) + proc_end_min)*60 + proc_end_sec 

            # Edge case where aura active when combat ends (Apply or Refresh)
            if j == len(all_bd_procs[i][1])-1:
                if all_bd_procs[i][1][j].split(" ")[1] == "Apply":
                    aura_end = aura_start + 15.0

                elif all_bd_procs[i][1][j].split(" ")[1] == "Refresh":
                    proc_start = all_bd_procs[i][1][j].split(" ")[0]
                    proc_start_min = int(proc_start.split(":")[0])
                    proc_start_sec = float(proc_start.split(":")[1])

                    aura_refresh = hour_in_sec + (float(minutes) + proc_start_min)*60 + proc_start_sec 
                    aura_end = aura_refresh + 15.0

            # Record the times (in seconds) that BD proc began and ended
            if aura_start != 0 and aura_end != 0:
                bd_aura_clock.append([aura_start, aura_end])
                aura_start, aura_end = 0, 0
             
           
    # Calculate the time in seconds BD proc ended and the next proc occured.    
    seconds_between_procs = []
    for i in range(len(bd_aura_clock)):
        try:
            seconds_between_procs.append(round(bd_aura_clock[i+1][0] - bd_aura_clock[i][1], 2))

        except:
            pass
        
    # Return the average time between BD procs
    return round(np.mean(seconds_between_procs), 2)


def get_BD_procs(all_bd_procs):
    nProcs = 0
    total = 0

    # Loop over tables
    for i, item1 in enumerate(all_bd_procs):

        # Loop over aura rows in a table
        for j, item2 in enumerate(all_bd_procs[i]):
            start_end_times = []  # Temp will keep track of when an aura starts or ends
            apply_refresh_remove = []
            refresh_end = []

            if j==0: 
                continue  # Ignore the header

            for k in range(len(all_bd_procs[i][j])):

                lst = all_bd_procs[i][j][k].split(" ")

                # Convert the time (minute:second.millisecond) to seconds.millisconds
                minutes = float(lst[0].split(":")[0])
                seconds = float(lst[0].split(":")[1])
                time = minutes*60 + seconds

                # If aura began or ended, record the time
                if lst[1] in ["Apply", "Remove"]:
                    if lst[1] == "Apply": nProcs += 1
                    apply_refresh_remove.append(lst[1])
                    start_end_times.append(time)

                # If the aura started before combat and refreshed during combat, you don't exactly know when the first proc happened.
                # So take half the duration of a BD proc as an estimate (7.5 seconds)
                if len(apply_refresh_remove) == 0 and lst[1] == "Refresh":
                    apply_refresh_remove.append("Refresh")
                    nProcs += 1
                    start_end_times.append(time)
                    total += 7.5

                if len(start_end_times) > 0:

                    # Cases where blue dragon procs during a blue dragon proc
                    if len(apply_refresh_remove) == 1 and apply_refresh_remove[0] == "Apply" and lst[1] == "Refresh":
                        apply_refresh_remove[0] = "Refresh"
                        nProcs += 1

                    elif len(apply_refresh_remove) == 1 and apply_refresh_remove[0] == "Refresh" and lst[1] == "Refresh":
                        nProcs += 1

                    # Case where aura started before combat began
                    if len(apply_refresh_remove) == 1 and apply_refresh_remove[0] == "Remove":
                        nProcs += 1
                        total += 15
                        apply_refresh_remove = []

                    # Normal cases (Aura began/refreshed and ended in combat)
                    if apply_refresh_remove == ["Apply", "Remove"]:
                        total += start_end_times[1] - start_end_times[0]
                        apply_refresh_remove = []

                    elif apply_refresh_remove == ["Refresh", "Remove"]:
                        total += start_end_times[1] - start_end_times[0]
                        apply_refresh_remove = []

                # Edge case where aura starts but doesnt end before combat drop, just add 15 seconds to the total.
                if k == len(all_bd_procs[i][j]) - 1:
                    if len(apply_refresh_remove) == 1 and apply_refresh_remove[0] == "Apply":
                        total += 15

                    elif len(apply_refresh_remove) == 1 and apply_refresh_remove[0] == "Refresh":
                        total += 15
                    
                    
    # Return the total BD aura time in combat as well as the number of BD procs.
    return round(total, 3), nProcs


def get_bangle_uses(all_bangle_uses):
    nProcs = 0
    total = 0

    # Loop over tables
    for i, table in enumerate(all_bangle_uses):

        # Loop over bangle rows in a table
        for j, row in enumerate(all_bangle_uses[i]):
            start_end_times = []  # Temp will keep track of when Endless Blessings starts or ends
            apply_removes = []

            if j==0: 
                continue  # Ignore the header

            for k in range(len(all_bangle_uses[i][j])):

                lst = all_bangle_uses[i][j][k].split(" ")

                # Convert the time (minute:second.millisecond) to seconds.millisconds
                minutes = float(lst[0].split(":")[0])
                seconds = float(lst[0].split(":")[1])
                time = minutes*60 + seconds

                # Track start and end of aura
                if lst[1] in ["Apply", "Remove"]: 
                    apply_removes.append(lst[1])
                    start_end_times.append(time)

                # Edge case where aura starts before entering combat
                if len(apply_removes) > 0:
                    if apply_removes[0] == "Remove":
                        nProcs += 1
                        total += 20
                        
                        apply_removes = []
                        start_end_times = []
                        continue
                        
                # Otherwise (aura starts and ends while in combat)
                if len(start_end_times) == 2:
                    nProcs += 1
                    total += 20

                    apply_removes = []
                    start_end_times = []
       
                # Edge case where aura starts but doesnt end before combat drop
                if k == len(all_bangle_uses[i][j]) - 1:
                    if len(apply_removes) == 1 and apply_removes[0] == "Apply":
                        nProcs += 1
                        total += 20
                        
                        apply_removes = []
                        start_end_times = []

                        
    return total, nProcs


# Function to get the total time Aura of the Blue Dragon overlapped with Endless Blessings
def get_total_overlap_time(all_bd_procs, all_bangle_uses):
    total_overlapping_time = 0
    overlap_occurances = 0

    for i, bd_proc in enumerate(all_bd_procs):

        for j, bangle_use in enumerate(all_bangle_uses):

            # Pick out encounters that have both BD and bangle auras
            total = 0
            if all_bd_procs[i][0] == all_bangle_uses[j][0]:

                start_end_times_bd = []
                apply_refresh_remove_bd = []

                for k in range(len(all_bd_procs[i][1])):

                    lst_bd = all_bd_procs[i][1][k].split(" ")

                    # Convert the time of the BD proc (minute:second.millisecond) to seconds.millisconds
                    minutes = float(lst_bd[0].split(":")[0])
                    seconds = float(lst_bd[0].split(":")[1])
                    time_bd = minutes*60 + seconds

                    # Track start and end of aura
                    if lst_bd[1] in ["Apply", "Remove"]: 
                        start_end_times_bd.append(time_bd)
                        apply_refresh_remove_bd.append(lst_bd[1])

                    # Edge cases where BD aura starts before entering combat (Aura started 15 seconds before it ended)
                    if len(apply_refresh_remove_bd) > 0:
                        if apply_refresh_remove_bd[0] == "Remove":
                            start_end_times_bd.append(time_bd)
                            start_end_times_bd[0] = time_bd - 15.
                            apply_refresh_remove_bd = []

                    # If aura refreshed but started before combat, you don't know exactly when the starting proc happened.
                    # Estimate that it started about 7.5s before the refresh.
                    if len(apply_refresh_remove_bd) == 0 and lst_bd[1] == "Refresh":
                        start_end_times_bd.append(time_bd - 7.5)
                        apply_refresh_remove_bd.append(lst_bd[1])
                        continue

                    if len(apply_refresh_remove_bd) > 0:

                        # Case where blue dragon procs during a blue dragon proc
                        if len(apply_refresh_remove_bd) == 1 and apply_refresh_remove_bd[0] == "Apply" and lst_bd[1] == "Refresh":
                            apply_refresh_remove_bd[0] = "Refresh"

                    if k == len(all_bd_procs[i][1])-1 and len(apply_refresh_remove_bd) == 1 and apply_refresh_remove_bd[0] in ["Apply", "Refresh"]:
                        start_end_times_bd.append(start_end_times_bd[0] + 15.0)

                    start_end_times_bangle = []
                    if len(start_end_times_bd) == 2:

                        start_end_bangle = []
                        for l in range(len(all_bangle_uses[j][1])):

                            lst_bangle = all_bangle_uses[j][1][l].split(" ")

                            # Convert the time (minute:second.millisecond) to seconds.millisconds
                            minutes = float(lst_bangle[0].split(":")[0])
                            seconds = float(lst_bangle[0].split(":")[1])
                            time_bangle = minutes*60 + seconds

                            if lst_bangle[1] in ["Apply", "Remove"]: 
                                start_end_times_bangle.append(time_bangle)
                                start_end_bangle.append(lst_bangle[1])

                            # Edge case where bangle use starts before entering combat (Aura began 20 seconds before it ended)
                            if start_end_bangle[0] == "Remove":
                                start_end_times_bangle.append(start_end_times_bangle[0])
                                start_end_times_bangle[0] = start_end_times_bangle[0] - 20.

                        # Edge case where bangle use active when combat ends (Aura ends 20 seconds after it began)
                        if l == len(all_bangle_uses[j][1])-1 and len(start_end_times_bangle) == 1 and start_end_bangle[0] == "Apply":
                            start_end_times_bangle.append(start_end_times_bangle[0] + 20.)

                    if len(start_end_times_bd) == len(start_end_times_bangle):

                        # Get the overlap time
                        # Case 1: Bangle is used during a BD proc
                        if start_end_times_bd[0] < start_end_times_bangle[0] < start_end_times_bd[1]:
                            total = start_end_times_bd[1] - start_end_times_bangle[0]
                            total_overlapping_time += total
                            overlap_occurances += 1

                        # Case 2: BD proc occurs during bangle use
                        elif start_end_times_bangle[0] < start_end_times_bd[0] < start_end_times_bangle[1]:
                            total = start_end_times_bangle[1] - start_end_times_bd[0]
                            total_overlapping_time += total
                            overlap_occurances += 1

    # Return the total time the auras overlapped (in seconds) and the number of times this occured during the raid
    return round(total_overlapping_time, 3), overlap_occurances


# Function to record times that bangle is off cooldown
def get_bangle_ready_times(all_bangle_uses):

    bangle_ready_times = []

    # Times on the table header are given in hour:minute, convert to seconds.
    for i, item in enumerate(all_bangle_uses):

        hrmin = all_bangle_uses[i][0].split(" ")[-2]
        hr = int(hrmin.split(":")[0])
        minute = int(hrmin.split(":")[1])
        time_in_sec = (hr * 3600) + (minute * 60)

        # Procs within a table are given in minute:seconds, convert to seconds.
        for j in range(len(all_bangle_uses[i][1])):
            proc_time = all_bangle_uses[i][1][j].split(" ")[0]
            minute = float(proc_time.split(":")[0])
            second = float(proc_time.split(":")[1])
            proc_time_in_s = (minute * 60.) + second

            # Normal case, check when Endless Blessings ends and add 100 seconds
            if all_bangle_uses[i][1][j].split(" ")[1] == "Remove":
                bangle_ready_times.append(time_in_sec + proc_time_in_s + 100.)

            # If Endless Blessings is active when combat ends, it will be ready again when it was used + 2 minutes later.
            elif j == len(all_bangle_uses[i][1]) - 1 and all_bangle_uses[i][1][j].split(" ")[1] == "Apply":
                bangle_ready_times.append(time_in_sec + proc_time_in_s + 120.)   

    # Return a list of times (in seconds) when Bangle is ready
    return bangle_ready_times


def get_bd_proc_times(all_bd_procs):

    bd_aura_clock = []

    # Times on the table header are given in hour:minute, convert to seconds.
    for i in range(len(all_bd_procs)):
        
        hm = all_bd_procs[i][0].split(" ")[-2]
        hour = hm.split(":")[0]
        hour_in_sec = int(hour) * 3600.
        minutes = hm.split(":")[1]

        # Procs within a table are given in minute:seconds, convert to seconds.
        aura_start, aura_end = 0, 0
        for j in range(len(all_bd_procs[i][1])):

            # Get time BD proc happened
            if all_bd_procs[i][1][j].split(" ")[1] == "Apply":
                proc_start = all_bd_procs[i][1][j].split(" ")[0]
                proc_start_min = int(proc_start.split(":")[0])
                proc_start_sec = float(proc_start.split(":")[1])

                aura_start = hour_in_sec + (float(minutes) + proc_start_min)*60 + proc_start_sec 

            # Get time BD proc ended
            elif all_bd_procs[i][1][j].split(" ")[1] == "Remove":
                proc_end = all_bd_procs[i][1][j].split(" ")[0]
                proc_end_min = int(proc_end.split(":")[0])
                proc_end_sec = float(proc_end.split(":")[1])

                aura_end = hour_in_sec + (float(minutes) + proc_end_min)*60 + proc_end_sec 
                
            # Edge case where aura started before combat  (Proc happened pre-combat).
            if aura_end < aura_start and aura_end != 0:
                bd_aura_clock.append([aura_end - 15.0, aura_end])
                aura_end = 0
                continue
                
            # Edge case where there's only one entry in the table which is a remove
            if len(all_bd_procs[i][1]) == 1 and all_bd_procs[i][1][j].split(" ")[1] == "Remove":
                bd_aura_clock.append([aura_end - 15.0, aura_end])
                aura_end = 0
                continue

            # Edge case where aura active when combat ends
            if j == len(all_bd_procs[i][1])-1:
                if all_bd_procs[i][1][j].split(" ")[1] == "Apply":
                    aura_end = aura_start + 15.0

                elif all_bd_procs[i][1][j].split(" ")[1] == "Refresh":
                    proc_start = all_bd_procs[i][1][j].split(" ")[0]
                    proc_start_min = int(proc_start.split(":")[0])
                    proc_start_sec = float(proc_start.split(":")[1])

                    aura_refresh = hour_in_sec + (float(minutes) + proc_start_min)*60 + proc_start_sec 
                    aura_end = aura_refresh + 15.0

            if aura_start != 0 and aura_end != 0:
                bd_aura_clock.append([aura_start, aura_end])
                aura_start, aura_end = 0, 0

    for i in range(len(bd_aura_clock)):
        bd_aura_clock[i].pop(1)
    
    return bd_aura_clock


def get_time_between_bangle_use_and_bdproc(bangle_ready_times, bd_aura_clock):

    time_between_bangle_use_and_bdproc = []

    for bangle_time in bangle_ready_times:

        # Loop through bangle ready times and BD procs times. When the difference is positive, that is the time it took
        # for BD to proc after Bangle was ready. Record all these times and return the average.
        for i, bd_time in enumerate(bd_aura_clock):

            if bd_aura_clock[i][0] - bangle_time > 0:
                time_between_bangle_use_and_bdproc.append(round(bd_aura_clock[i][0] - bangle_time, 2))
                break
                
    return round(np.mean(time_between_bangle_use_and_bdproc), 2)