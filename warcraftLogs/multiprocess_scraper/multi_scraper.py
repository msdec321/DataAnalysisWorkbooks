#encoding: utf-8

from multiprocessing import Pool
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')

import selenium, time, os
from selenium import webdriver

import src

# Verbose printout flags
verbose = False
verbose_rotation = False

# Enable/disable SMS
twilio = True

# Other configurations
nCores = 5
nParses = 701
nParse_start = 201
nParse_stop = 241
boss = "Eredar Twins"
phase = 1
boss_link_dict = {"High Warlord Naj'entus" : "#boss=601", "Supremus" : "#boss=602", "Shade of Akama" : "#boss=603", 
                  "Teron Gorefiend" : "#boss=604", "Gurtogg Bloodboil" : "#boss=605", "Reliquary of Souls" : "#boss=606", 
                  "Mother Shahraz" : "#boss=607", "The Illidari Council" : "#boss=608", "Illidan Stormrage" : "#boss=609", 
                  "Rage Winterchill" : "#boss=618", "Anetheron" : "#boss=619", "Kaz'rogal" : "#boss=620", 
                  "Azgalor" : "#boss=621", "Archimonde" : "#boss=622",
                  "Brutallus" : "#boss=725", "Felmyst" : "#boss=726", "Eredar Twins" : "#boss=727",
                  "M'uru" : "#boss=728", "Kil'jaedan" : "#boss=729"}


def main(i):
    
    browser = src.get_browser_page(boss, boss_link_dict, i)
    path_to_ublock, path_to_download_dir, path_to_data_dir = src.get_path_settings()
        
    rank, name, server, region, date, HPS, duration = src.get_boss_data_top_N_scraper(browser, i, boss, boss_link_dict)
    if name in ['Chapu', '世外', 'Tables']: return i
    time.sleep(2)
    
    link = browser.find_element_by_link_text(name)
    link.click()
    
    player_df = pd.DataFrame(pd.np.empty((0, 25)))
    player_df.columns = ["Rank", "Name", "Server", "Date", "Duration", "Haste", "nHealers", "Spriest?", "Innervate?", "Bloodlust?", "Nature's Grace?", "Trinket 1", "Trinket 2", "LB_uptime", "HPS", "% LB (tick) HPS", "% LB (bloom) HPS", "% Rejuv HPS", "% Regrowth HPS", "% Swiftmend HPS", "Rotating on tank?", "Rotation 1", "% Rotation 1", "Rotation 2", "% Rotation 2"]
    
    if boss in ["Eredar Twins", "M'uru"]:
         src.click_on_element_by_id(browser, "filter-phase-text")
         time.sleep(1)
         src.click_on_element_by_id(browser, f"phase-menu-{phase}")
         time.sleep(1)

    temp_url = browser.current_url
    time.sleep(1)
    
    try:
        boss_tanks = src.get_tanks(browser)
        nHealers = src.get_nHealers(browser)
        
        if boss == "Eredar Twins":
            fire_tank = src.get_fire_tank(browser)
            if fire_tank not in boss_tanks: 
                boss_tanks.append(fire_tank)
        
    except: return i
    
    browser.get(temp_url)
    time.sleep(4)
    
    player_link = browser.find_element_by_link_text(name)
    player_link.click()
    time.sleep(2)
    
    # Scrape HPS data
    LBtick_HPS, LBbloom_HPS, rejuv_HPS, regrowth_HPS, swiftmend_HPS, LB_uptime = src.get_spell_info(browser, HPS)
    time.sleep(2)
    
    #Get haste and trinkets
    haste = src.get_haste(browser)
    try:
        trinket1, trinket2 = src.get_trinkets(browser)
    except: return i
    time.sleep(1)
    
    # Check for buffs
    spriest = src.check_spriest(browser)
    innervate, bloodlust, powerInfusion, naturesGrace = src.check_buffs(browser)
    time.sleep(2)
    
    # Download the cast-sequence CSV.
    try:
        src.download_csv(browser, temp_url, "filter-casts-tab", path_to_download_dir, path_to_data_dir + f"\csv\cast_sequence_{name}.csv", name, nCores)
        
    except: return i
    time.sleep(2)
    
    # Clean the csv
    df = src.clean_cast_sequence_csv(name, path_to_data_dir)
    df = src.fix_cast_time(df)
    time.sleep(1)
    
    # Get the rotations
    rotation1, rotation1_percent, rotation2, rotation2_percent, rotating_on_tank = src.calculate_rotations(df, boss, boss_tanks, LB_uptime, verbose, verbose_rotation)
    
    # Export data and cleanup
    to_append = [rank, name, server + " " + region, date, duration, str(haste), str(nHealers), spriest, innervate, bloodlust, naturesGrace, trinket1, trinket2, LB_uptime, HPS, LBtick_HPS, LBbloom_HPS, rejuv_HPS, regrowth_HPS, swiftmend_HPS, rotating_on_tank, rotation1, rotation1_percent, rotation2, rotation2_percent]
    src.export_to_csv(path_to_data_dir, boss, to_append, player_df, name)#, 'top_N_druids', True)
    
    os.remove(path_to_data_dir + f"\csv\cast_sequence_{name}.csv")
    
    print("-----")
    print(f"Rank: {rank}, Druid: {name}, boss tanks: {boss_tanks}, nHealers: {nHealers}")
    print(f'Rotations: {rotation1} ({rotation1_percent}), {rotation2} ({rotation2_percent})')  
    
    browser.quit()
    
    return i


if __name__ == '__main__':
    
    path_to_ublock, path_to_download_dir, path_to_data_dir = src.get_path_settings()
    
    if twilio: 
        from twilio.rest import Client
        accountSID, authToken, myTwilioNumber, myCellPhone = src.get_twilio_info()
        twilioCli = Client(accountSID, authToken)
    
    #for j in range(1, 11):
    print("Checking for rank changes since last scrape...")
    not_recorded = src.get_non_recorded_players(path_to_ublock, boss, boss_link_dict, phase, nParses)   
    #not_recorded = src.get_non_recorded_players(path_to_ublock, boss, boss_link_dict, phase, nParse_start, nParse_stop)
    print("Rank updates complete.")
    print('-----------')
    time.sleep(2)

    print("Beginning data scrape...")
    with Pool(nCores) as pool:
        results = pool.map(main, not_recorded)
        print(f"Ranks successfully added: {results}")

    # Add scraped data to the spreadsheet
    print("Adding data to spreadsheet...")
    src.combine_csv_files(boss)
    src.add_rows_to_xlsx(path_to_data_dir, boss, phase, "top_N_druids", True)
    src.sort_excel(path_to_data_dir, boss, phase, "top_N_druids")
    print("Spreadsheet updated! Scraping complete.")

    src.remove_xlsx_duplicates(path_to_data_dir, boss, phase, "top_N_druids")
    src.clean_csv_dir(path_to_data_dir)

    #nParse_start += 40
    #nParse_stop += 40

    if twilio:
         message = twilioCli.messages.create(body = 'Data scraping complete!', from_ = myTwilioNumber, to = myCellPhone)