from multiprocessing import Pool
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')

import selenium, time, os
from selenium import webdriver

import src

# Configurations
verbose = False
verbose_rotation = False

nCores = 5
nParses = 424
boss = "Shade of Akama"
boss_link_dict = {"High Warlord Naj'entus" : "#boss=601", "Supremus" : "#boss=602", "Shade of Akama" : "#boss=603", 
                  "Teron Gorefiend" : "#boss=604", "Gurtogg Bloodboil" : "#boss=605", "Reliquary of Souls" : "#boss=606", 
                  "Mother Shahraz" : "#boss=607", "The Illidari Council" : "#boss=608", "Illidan Stormrage" : "#boss=609", 
                  "Rage Winterchill" : "#boss=618", "Anetheron" : "#boss=619", "Kaz'rogal" : "#boss=620", 
                  "Azgalor" : "#boss=621", "Archimonde" : "#boss=622"}


def main(i):
    
    browser = src.get_browser_page(boss, boss_link_dict, i)
    path_to_ublock, path_to_download_dir, path_to_data_dir = src.get_path_settings()
        
    rank, name, server, region, date, HPS, duration = src.get_boss_data_top_N_scraper(browser, i, boss, boss_link_dict)
    if name in ['Tables']: return i
    time.sleep(2)
    
    link = browser.find_element_by_link_text(name)
    link.click()
    
    player_df = pd.DataFrame(pd.np.empty((0, 23)))
    player_df.columns = ["Rank", "Name", "Server", "Date", "Duration", "nHealers", "Spriest?", "Innervate?", "Bloodlust?", "Nature's Grace?", "Power Infusion?", "LB_uptime", "HPS", "% LB (tick) HPS", "% LB (bloom) HPS", "% Rejuv HPS", "% Regrowth HPS", "% Swiftmend HPS", "Rotating on tank?", "Rotation 1", "% Rotation 1", "Rotation 2", "% Rotation 2"]

    temp_url = browser.current_url
    time.sleep(1)
    
    boss_tanks = src.get_tanks(browser)
    nHealers = src.get_nHealers(browser)
    
    browser.get(temp_url)
    time.sleep(4)
    
    player_link = browser.find_element_by_link_text(name)
    player_link.click()
    time.sleep(2)
    
    # Scrape HPS data
    LBtick_HPS, LBbloom_HPS, rejuv_HPS, regrowth_HPS, swiftmend_HPS, LB_uptime = src.get_spell_info(browser, HPS)
    time.sleep(2)
    
    # Check for buffs
    spriest = src.check_spriest(browser)
    innervate, bloodlust, powerInfusion, naturesGrace = src.check_buffs(browser)
    time.sleep(2)
    
    # Download the cast-sequence CSV.
    print(path_to_data_dir + f"\cast_sequence_{name}.csv")
    src.download_csv(browser, temp_url, "filter-casts-tab", path_to_download_dir, path_to_data_dir + f"\cast_sequence_{name}.csv", name, nCores)
    time.sleep(2)
    
    # Clean the csv
    df = src.clean_cast_sequence_csv(name, path_to_data_dir)
    df = src.fix_cast_time(df)
    time.sleep(1)
    
    # Get the rotations
    rotation1, rotation1_percent, rotation2, rotation2_percent, rotating_on_tank = src.calculate_rotations(df, boss, boss_tanks, LB_uptime, verbose, verbose_rotation)
    
    # Export data and cleanup
    to_append = [rank, name, server + " " + region, date, duration, str(nHealers), spriest, innervate, bloodlust, powerInfusion, naturesGrace, LB_uptime, HPS, LBtick_HPS, LBbloom_HPS, rejuv_HPS, regrowth_HPS, swiftmend_HPS, rotating_on_tank, rotation1, rotation1_percent, rotation2, rotation2_percent]
    src.export_to_excel(path_to_data_dir, boss, to_append, player_df, name, 'top_N_druids', True)
    
    os.remove(path_to_data_dir + f"\{boss.replace(' ', '')}_{name}.csv")
    os.remove(path_to_data_dir + f"\cast_sequence_{name}.csv")
    
    print("-----")
    print(f"Druid: {name}, boss tanks: {boss_tanks}, nHealers: {nHealers}")
    print(LBtick_HPS, LBbloom_HPS, rejuv_HPS, regrowth_HPS, swiftmend_HPS, LB_uptime)
    print(f"spriest {spriest}, innervate {innervate}, bloodlust {bloodlust}, powerInfusion {powerInfusion}, naturesGrace {naturesGrace}")
    print(f'Rotations: {rotation1} ({rotation1_percent}), {rotation2} ({rotation2_percent})')  
    
    browser.quit()
    
    return i


if __name__ == '__main__':
    
    path_to_ublock, path_to_download_dir, path_to_data_dir = src.get_path_settings()
    not_recorded = src.get_non_recorded_players(path_to_ublock, boss, boss_link_dict, nParses)   
    
    with Pool(nCores) as pool:
        results = pool.map(main, not_recorded)
        print(f"Ranks successfully added: {results}")