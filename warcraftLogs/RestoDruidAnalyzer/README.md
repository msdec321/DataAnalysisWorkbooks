#------------------------  
Author's note: This project is now in maintainence mode.    
Data will be updated every two weeks but I do not plan to develop this project further.  
#------------------------


# TBC Resto Druid Analyzer  

# Motivation
TBC Resto Druid is complicated. The rotation that you choose to use in an encounter can depend on several factors: number of tanks, total mana available, how much you prioritize healing the tank vs the raid, etc. While theorycrafting can determine the best rotations in a vaccuum, boss fights are messy and effective healing is difficult to model accurately for each encounter.  

The motivation of this project is to take a data-driven approach; what are the top performing players actually doing on each boss? Furthermore, what are the best rotations given your specific raid composition? There is a vast resource of data provided by WarcraftLogs that is not being used by the community (understandably, building a dataset is time consuming). Regardless of your skill level, I hope that you can learn something from this analysis to improve your playstyle.  


# Rotations and notation
Lifebloom lasts for 7 seconds, and there is a limited sequence of spells that can be cast before it must be refreshed. This is called a rotation. (See the [Elitist Jerks guide](http://web.archive.org/web/20080913120521/http://elitistjerks.com/f31/t17783-druid_raiding_tree/#Healing_Strategies) for more detail)      
  
In this analysis I use the following shorthand for rotations: &nbsp; **xLB yI zRG**,   
where x, y, z are numbers and LB, I, RG are "Lifebloom", "Instant", and "Regrowth", respectively.   

Here, "LB" refers to lifeblooms being rolled on _tanks_. Lifeblooms being used to raidheal go into the 'instant' bucket.  
* Example 1: "1LB 2I 1RG" can mean: 'Lifebloom 1 tank -> use 2x instant casts (lifebloom, rejuv, swiftmend, etc) -> cast 1x regrowth, repeat. The instants and regrowths can be cast in any order.
* Example 2: "2LB 1I 1RG" -> Lifebloom tank 1 -> Lifebloom tank 2 -> 1x Instant (like a rejuv on tank or raid) -> 1x Regrowth (on tank or raid), repeat. The order is not important, you could even do "Lifebloom tank 1 -> 1x Regrowth -> 1x rejuv -> Lifebloom tank 2, repeat and that will still be called "2LB 1I 1RG".  
 
You'll also see me use weird rotations such as 0LB 0I 6RG, 0LB 5I 1RG, etc. These aren't exactly "rotations", because the player isn't rolling lifebloom on the tank at all, and instead purely raid healing. For this analysis it's useful to keep track of these players as well.


# Dataset  
WarcraftLogs data is scraped from the top 3,000 players for each boss (in progress) for Restoration spec Druids (There are zero Dreamstate druids in the dataset). For the Black Temple dataset this encompasses roughly the 95th percentile and above, whereas for the Sunwell dataset it is roughly the 75th percentile and above. The dataset (located in data/top_N_druids.xlsx) contains the following:  

&emsp; • Rank  
&emsp; • Character name, server, region  
&emsp; • Date  
&emsp; • Duration    
&emsp; • Number of healers  
&emsp; • Shadowpriest in group?  
&emsp; • Innervate received?  
&emsp; • Bloodlust/heroism received?  
&emsp; • Is Nature's Grace spec?  
&emsp; • Lifebloom uptime %  
&emsp; • Total HPS  
&emsp; • % HPS of: Lifebloom (tick), Lifebloom (bloom), Rejuvenation, Regrowth, Swiftmend  
&emsp; • Rotating on tank? ('No' means the Druid is not rolling LB on the tank and instead just raid healing)  
&emsp; • Top two rotations used  

Available in the Sunwell dataset:  
&emsp; • Haste rating  
&emsp; • Trinkets equipped  

# Analysis
Rotations are determined via the cast sequence data provided by WCL ([an example](https://classic.warcraftlogs.com/reports/VZr6X2MNY73GLktg#fight=47&type=casts&view=events&source=37)). In short, the [rotation calculator](https://github.com/msdec321/DataAnalysisWorkbooks/blob/main/warcraftLogs/src.py#L535-L623) checks when Lifebloom is cast on a tank which signals the start of a rotation. The following casts are recorded until either 1) The lifebloom is refreshed or 2) The rotation reaches 6 casts. Casts that are off the global cooldown are ignored. For purely raid healing Druids, the calculator simply counts the number of regrowths/instants cast in a 6-cast window. The rotation is recorded into a dictionary object and at the end the top 2 rotations are saved to the dataset.  

In general, the distribution of HPS for each rotation is exponentially falling with a long tail. Each distribution has a characteristic mean and width (σ), which can be used to compare the performance of each rotation. The relative uncertainty is taken as the standard error: SE = σ / √(n).    
 - <details> 
    <summary>Distribution of HPS</summary><p>
 
    ![alt text](https://i.imgur.com/Vz3K0hv.jpg)
  </p></details>

 - <details> 
    <summary>Comparing multiple distributions</summary><p>
 
    ![alt text](https://i.imgur.com/VWPltCF.png)
  </p></details>  

Some errorbars are large for two reasons. Primarily, the rotation performs inconsistently; some players perform exceptionally better with the rotation than others (large σ). Second, there are relatively few players doing the rotation (small n). In general, the larger the sample size the smaller the uncertainty.  

Raid compositions and playstyle vary widely, so it can also be useful to look at what variables correlate the strongest with HPS.  

 - <details><summary>Naj'entus example</summary><p>
  
    ![alt text](https://i.imgur.com/3BkHcYT.png)  
  
Correlations range from +1 to -1. If variable X has a positive correlation with HPS, it means that increasing X tends to increase HPS as well. If X has a negative correlation, it means decreasing X will tend to increase HPS. If the correlation is close to zero, then X has little to no effect on HPS. **>>Caution<<**: These are correlations for *within* the 95th to 100th percentile. That is to say, these factors will help you *if you're already in the 95th percentile or above*. They are not necessarily indicative of how to break into the 95th percentile. For example, innervate appears to correlate weakly with HPS. Does that mean having innervate is not important for getting a high HPS? Not necessarily, because 90% of players in the Naj'entus dataset received an innervate! So please use caution when drawing insights from correlations.  


# Results and discussion
  
- <details><summary>Brutallus</summary>  
  &nbsp;
  
    - <details><summary>Rotation rankings</summary><p>
 
      <img src="https://github.com/msdec321/DataAnalysisWorkbooks/blob/main/warcraftLogs/RestoDruidAnalyzer/plots/brutallus/rotation_rankings.png" width="650">
  
      The top five rotations:
      - 1LB 4I 0RG: The standard 5GCD rotation, 113 Haste rating. Roll lifebloom on the primary tank and burn targets and use Rejuv for the extra GCD(s).   
      - 2LB 3I 0RG: Also the 5GCD rotation, but keeping a lifebloom on the offtank more often than above.   
      - 1LB 3I 2RG: Not a rotation. The players who cast this sequence of spells end up not refreshing Lifebloom on the tank. For the most part these players roll Lifebloom on the burn targets and weave in Regrowths with spare GCDs.   
      - 0LB 2I 4RG: Similar to the above, but rotates Lifebloom on one less burn target and uses more Regrowths.   
      - 1LB 3I 0RG: The standard 4GCD rotation, 0 Haste rating. Roll lifebloom on the primary tank and burn targets and use Rejuv for the extra GCD(s).   
      &nbsp;
  
      *Interestingly a 0 Haste rotation makes it into the top 5, which really shows how strong rolling Lifebloom on burns is. What's even more surprising to me, though, is that the standard 4GCD rotation ranks much higher than the 6GCD rotation (1LB 5I 0RG, ranked 14th). Why?  
  
      Let's drill down on some rotations.
  
      - <details><summary>Q. For players using 5 GCD, how does Lifebloom compare to rejuv?</summary><p>
  
        ![alt text](https://i.imgur.com/D5EFeFK.png)
  
        Unsurprisingly, the bulk of these players HPS comes from rolling Lifeblooms on burn. Some players use rejuv more than others.  
        </p></details>
        &nbsp;
  
      </p></details>
  
    - <details><summary>% Spell HPS scatter plots</summary><p>
  
      ![alt text](https://i.imgur.com/VJQNgxJ.png)
  
      For the bulk of players, the largest fraction of their healing comes from Lifebloom ticks (burn healing). Following that, most players get the secondary bulk of their healing from regrowth (although ironically 5GCD performs much better than using regrowths).  
      </p></details>
  
    - <details><summary>HPS vs Duration (Color = kill speed percentile, not HPS)</summary><p>
  
      ![alt text](https://i.imgur.com/HdMelSD.png)
  
      Most players fall within the 10th to 75th percentile of kill times.
      </p></details>
  
    - <details><summary>Q. What percentage of players are rolling Lifebloom on the tank(s)?</summary><p>
  
      <img src="https://github.com/msdec321/DataAnalysisWorkbooks/blob/main/warcraftLogs/RestoDruidAnalyzer/plots/brutallus/nTankRotating.png" width="450">
  
      57.8% of players are rolling Lifebloom at least one tank, the rest are purely burn healing / raid healing. For the Druids who are rotating on the tank(s), most prefer to roll Lifebloom on only the primary tank, while ~5% of players roll Lifebloom on both tanks.  
      </p></details>
  
    - <details><summary>Q. What percentage of players have an extra mana source?</summary><p>
  
      ![alt text](https://i.imgur.com/WNC6CFH.png)
  
      95.1% of players received either an innervate or shadow priest.
      </p></details>
  
    - <details><summary>Q. What percentage of players are playing Nature's Grace? (Note: There are no Dreamstate Druids in the dataset.)</summary><p>
  
      ![alt text](https://i.imgur.com/ti0CSrl.png)
  
      13.0% of players are Nature's Grace spec.
      </p></details> 
    
    - <details><summary>Q. What variables correlate the most with HPS?</summary><p>
  
      ![alt text](https://i.imgur.com/eyHHmu6.png)
  
      The top five correlators of HPS in order of importance: 
      - Haste rating    
      - Having less healers in your raid  
      - Having shadow priest    
      - Shorter fight duration  
      - Using Swiftmend less     
      &nbsp; 
  
      </p></details>
    </details> 

&nbsp;
  
- <details><summary>Felmyst</summary>  
  &nbsp;
  
  - <details><summary>Rotation rankings</summary><p>
  
    <img src="https://github.com/msdec321/DataAnalysisWorkbooks/blob/main/warcraftLogs/RestoDruidAnalyzer/plots/felmyst/rotation_rankings.png" width="650">
  
    The top five rotations:
    - 0LB 1I 5RG: Raid healing, primarily with Regrowth and the occasional lifebloom/rejuv, 5% of players do this.  
    - 0LB 0I 6RG: Raid healing with Regrowth, 8% of players do this.  
    - 1LB 1I 4RG: Not a rotation, Mostly raid healing with regrowth and putting a Lifebloom on the tank (but not refreshing it), 1.2% of players do this.    
    - 1LB 0I 3RG: ~130 Haste regrowth rotation, 1.4% of players do this.  
    - 1LB 0I 5RG: Not a rotation, similar to the above but Lifebloom does not get refreshed.  
    &nbsp;  
  
    Let's drill down on the data.
   
    - <details><summary>Q. For players raid healing with the top 2 rotations, how does Tree of Life spec compare to Nature's Grace?</summary><p>
  
        ![alt text](https://i.imgur.com/oRoLxZO.png)
  
        Tree of Life performs slightly better on average (within uncertainty) for pure regrowth spam (perhaps due to mana constraints), however for 1I 5RG the specs perform roughly the same within uncertainty.   
        </p></details>
    &nbsp;
  
    </p></details>
  
  - <details><summary>% Spell HPS scatter plots</summary><p>
  
      ![alt text](https://i.imgur.com/hTuGRoR.png)
  
      There is a lot of variation in how players heal, however the top performers tend to be using more regrowths.  
      </p></details>
  
  - <details><summary>HPS vs Duration (Color = kill speed percentile, not HPS)</summary><p>
  
      ![alt text](https://i.imgur.com/bTEXMIk.png)
  
      Most players fall slightly above the 50th percentile of kill speeds. The top parses tend to occur near the end of the 3rd ground phase or at any time in the 4th ground phase.  
      </p></details>
  
  - <details><summary>Q. What percentage of players are rolling Lifebloom on the tank?</summary><p>
  
     <img src="https://github.com/msdec321/DataAnalysisWorkbooks/blob/main/warcraftLogs/RestoDruidAnalyzer/plots/felmyst/nTankRotating.png" width="450">
  
     38.0% of players are rolling Lifebloom on a tank (either during the ground phase or during skeletons in the air phase). 
     </p></details>
  
  - <details><summary>Q. What percentage of players have an extra mana source?</summary><p>
  
      ![alt text](https://i.imgur.com/g3E8UaR.png)
  
      94.6% of players received either an innervate or shadow priest.
      </p></details>
  
  - <details><summary>Q. What percentage of players are playing Nature's Grace?</summary><p>
  
    ![alt text](https://i.imgur.com/pfCvfHa.png)
  
    25.9% of players are Nature's Grace spec.
    </p></details>
  
  - <details><summary>Q. What variables correlate the most with HPS?</summary><p>
  
      ![alt text](https://i.imgur.com/zKe2v2t.png)
  
      The top five correlators of HPS in order of importance: 
      - Casting more regrowths      
      - Casting less lifeblooms    
      - Having more spell haste      
      - Spriest    
      - Lower number of healers       
      &nbsp; 
  
      </p></details>

  </details> 

&nbsp;
  
- <details><summary>Eredar Twins</summary>  
  &nbsp;
  
  Note: Some sections of this boss are split by phase.
  
  - <details><summary>Rotation rankings (Phase 1)</summary><p>
  
    ![alt text](https://i.imgur.com/vWudPR9.png)
  
    The top five rotations:
    - 2LB 0I 2RG: 5 haste rotation, regrowths more often on the raid than tanks, 1.9% of players do this rotation.  
    - 1LB 0I 3RG: 113 haste rotation, regrowths more often on the raid than tanks, 1.6% of players do this rotation.  
    - 0LB 0I 6RG: Pure regrowth raid healing, 9.6% of players do this.  
    - 0LB 1I 5RG: Raid healing primarily with regrowth and the occasional rejuv, 11.7% of players do this.  
    - 1LB 1I 2RG: 5 haste rotation, regrowths more often on the raid than tanks, 2.2% of players do this rotation.  
    &nbsp;  

    </p></details>
  
  - <details><summary>Rotation rankings (Phase 2)</summary><p>
  
    ![alt text](https://i.imgur.com/R94eDqD.png)
  
    The top five rotations:
    - 0LB 0I 6RG: Pure regrowth raid healing, 9.6% of players do this.  
    - 0LB 1I 5RG: Raid healing primarily with regrowth and the occasional rejuv but more regrowths than the above, 11.7% of players do this.  
    - 1LB 0I 3RG: 130 Haste rotation, 1.8% of players do this rotation.  
    - 0LB 2I 4RG: Raid healing primarily with regrowth and the occasional rejuv, 7.4% of players do this.  
    - 1LB 1I 2RG: 5 haste rotation, 2.2% of players do this.  
    &nbsp;  

    </p></details>
  
  - <details><summary>Q. What percentage of players are rolling Lifebloom on the tank(s)? (Phase 1)</summary><p>
  
     ![alt text](https://i.imgur.com/lHIoP3q.png)
  
     54.2% of players are rolling Lifebloom on at least one tank, with 16.8% of players rolling LB on exactly one tank, 18.7% on exactly two tanks, and 18.8% on all three tanks.  
     </p></details>
  
  - <details><summary>Q. What percentage of players are rolling Lifebloom on the tank? (Phase 2)</summary><p>
  
     ![alt text](https://i.imgur.com/pylfz4B.png)
  
     33.8% of players are rolling Lifebloom on the tank. 
     </p></details>
  
   - <details><summary>Q. What percentage of players are playing Nature's Grace?</summary><p>
  
     ![alt text](https://i.imgur.com/4W8gwt9.png)
  
     31.2% of players are Nature's Grace spec.
     </p></details>
  
  - <details><summary>Q. What variables correlate the most with HPS? (Phase 1)</summary><p>
  
     ![alt text](https://i.imgur.com/Hx7Igis.png)
  
     The top five correlators of HPS in order of importance: 
     - Casting more regrowths  
     - Having shadow priest  
     - Casting less lifeblooms  
     - Playing Nature's grace  
     - Having more spell haste    
     </p></details>
    
  
  - <details><summary>Q. What variables correlate the most with HPS? (Phase 2)</summary><p>
  
      ![alt text](https://i.imgur.com/GUGtZds.png)
  
      The top five correlators of HPS in order of importance: 
      - Casting more regrowths  
      - Having shadow priest  
      - Casting less lifeblooms  
      - Playing Nature's grace  
      - Having more spell haste  
      &nbsp;
  
      Note: Coincidentally (or maybe not a coincidence?) these are the same top correlators as seen for phase 1.
      </p></details>
  
  - <details><summary>Trinket analysis</summary><p>
    
    - <details><summary>Q. Which trinkets are players using the most?</summary><p>
  
      ![alt text](https://i.imgur.com/iDEXs0p.png)
      </p></details>
  
    - <details><summary>Q. Which combinations of trinkets are players using the most?</summary><p>
  
      ![alt text](https://i.imgur.com/67K5GdE.png)
      </p></details>
  
    - <details><summary>Q. Does playstyle/rotation affect the distribution of trinkets?</summary><p>
  
      - <details><summary>Q. Regrowth spam (0LB 0I 6RG, 0LB 1I 5RG, 0LB 2I 4RG) - Individual trinkets</summary><p>
  
        ![alt text](https://i.imgur.com/7Kpj0Vd.png)
        </p></details>
  
      - <details><summary>Q. Regrowth spam (0LB 0I 6RG, 0LB 1I 5RG, 0LB 2I 4RG) - Trinket combinations</summary><p>
  
        ![alt text](https://i.imgur.com/7IkYNdn.png)
        </p></details>
  
      - <details><summary>Q. 5GCD Lifebloom rolling (2LB 3I 0RG, 2LB 2I 1RG, ...) - Individual trinkets</summary><p>
  
        ![alt text](https://i.imgur.com/s8AogL1.png)
        </p></details>
  
      - <details><summary>Q. 5GCD Lifebloom rolling (2LB 3I 0RG, 2LB 2I 1RG, ...) - Trinket combinations</summary><p>
  
        ![alt text](https://i.imgur.com/N2DTSfI.png)
        </p></details>
  
      </p></details>
  
    - <details><summary>Q. What are the HPS rankings for the most common trinket combinations?</summary><p>
  
      - <details><summary>Regrowth spam</summary><p>
  
        ![alt text](https://i.imgur.com/R08eBGP.png)
        </p></details>
  
      - <details><summary>5GCD Lifebloom rolling</summary><p>
  
        ![alt text](https://i.imgur.com/vIiMBKp.png)
        </p></details>
  
      </p></details> 
  
    </p></details>
  
  </details> 

&nbsp;
  
- <details><summary>M'uru</summary>  
  &nbsp;

  Note: Some sections of this boss are split by phase.
  
  - <details><summary>Rotation rankings (Phase 1)</summary><p>
  
    ![alt text](https://i.imgur.com/wKhcGn1.png)
  
    The top five rotations:
    - 2LB 0I 2RG: 5 haste rotation, regrowths more often on the raid than tanks, 2.5% of players do this rotation.  
    - 0LB 0I 6RG: Pure regrowth raid healing, 8.7% of players do this.  
    - 0LB 1I 5RG: Raid healing primarily with regrowth and the occasional rejuv, 4.5% of players do this.  
    - 0LB 2I 4RG: Raid healing primarily with regrowth and the occasional rejuv, but more rejuvs than the above, 2.9% of players do this.  
    - 1LB 1I 2RG: 5 haste rotation, regrowths more often on the raid than tanks, 1.9% of players do this rotation.  
    &nbsp;  

    </p></details>
  
  - <details><summary>Rotation rankings (Phase 2)</summary><p>
  
    ![alt text](https://i.imgur.com/aftVMjq.png)
  
    The top five rotations:
    - 0LB 0I 6RG: Pure regrowth raid healing, 14.6% of players do this.  
    - 0LB 2I 4RG: Raid healing primarily with regrowth and the occasional rejuv, 8.7% of players do this.  
    - 0LB 1I 5RG: Raid healing primarily with regrowth and the occasional rejuv, but less rejuvs than the above, 12.9% of players do this.   
    - 1LB 1I 2RG: 5 haste rotation, regrowths more often on the raid than tanks, 2.5% of players do this.  
    - 0LB 3I 3RG: Raid healing primarily with regrowth and the occasional rejuv, but more rejuvs than both of the above, 5.6% of players do this.  
    &nbsp;  

    </p></details>
  
  - <details><summary>Q. What percentage of players are rolling Lifebloom on the tank(s)? (Phase 1)</summary><p>
  
     ![alt text](https://i.imgur.com/Z9gi4NF.png)
  
     73.9% of players are rolling Lifebloom on at least one tank, with 19.6% of players rolling LB on exactly one tank, 16.9% on exactly two tanks, and 37.4% on all three tanks.  
     </p></details>
  
  - <details><summary>Q. What percentage of players are rolling Lifebloom on the tank? (Phase 2)</summary><p>
  
     ![alt text](https://i.imgur.com/TQc2rBC.png)
  
     45.2% of players are rolling Lifebloom on at least one tank (Note: I choose *at least one* tank because some groups have adds active going into phase 2).  
     </p></details>
  
  - <details><summary>Q. What percentage of players are playing Nature's Grace?</summary><p>
  
     ![alt text](https://i.imgur.com/Sjkr1gv.png)
  
     30.1% of players are Nature's Grace spec.
     </p></details>
  
  - <details><summary>Q. What variables correlate the most with HPS? (Phase 1)</summary><p>
  
     ![alt text](https://i.imgur.com/wXAsf3W.png)
  
     The top five correlators of HPS in order of importance: 
     - Casting more regrowths  
     - Having shadow priest  
     - Casting less lifeblooms  
     - Having more spell haste  
     - Casting less rejuvs  
     </p></details>

  - <details><summary>Q. What variables correlate the most with HPS? (Phase 2)</summary><p>
  
      ![alt text](https://i.imgur.com/25TiJWQ.png)
  
      The top five correlators of HPS in order of importance: 
      - Casting more regrowths  
      - Having shadow priest  
      - Casting less lifeblooms   
      - Nature's Grace spec  
      - Having innervate  
      </p></details>
  
  - <details><summary>Trinket analysis</summary><p>
    
    - <details><summary>Q. Which trinkets are players using the most?</summary><p>
  
      ![alt text](https://i.imgur.com/eZyxero.png)
      </p></details>
  
    - <details><summary>Q. Which combinations of trinkets are players using the most?</summary><p>
  
      ![alt text](https://i.imgur.com/h0S7N5c.png)
      </p></details>
  
    - <details><summary>Q. Does playstyle/rotation affect the distribution of trinkets?</summary><p>
  
      - <details><summary>Q. Regrowth spam (0LB 0I 6RG, 0LB 1I 5RG, 0LB 2I 4RG) - Individual trinkets</summary><p>
  
        ![alt text](https://i.imgur.com/3tyPN19.png)
        </p></details>
  
      - <details><summary>Q. Regrowth spam (0LB 0I 6RG, 0LB 1I 5RG, 0LB 2I 4RG) - Trinket combinations</summary><p>
  
        ![alt text](https://i.imgur.com/82aDll8.png)
        </p></details>
  
      - <details><summary>Q. 5GCD Lifebloom rolling (3LB 2I 0RG, 2LB 3I 0RG, ...) - Individual trinkets</summary><p>
  
        ![alt text](https://i.imgur.com/UnEFEOf.png)
        </p></details>
  
      - <details><summary>Q. 5GCD Lifebloom rolling (3LB 2I 0RG, 2LB 3I 0RG, ...) - Trinket combinations</summary><p>
  
        ![alt text](https://i.imgur.com/5aMqJuO.png)
        </p></details>
  
      </p></details>
  
    - <details><summary>Q. What are the HPS rankings for the most common trinket combinations?</summary><p>
  
      - <details><summary>Regrowth spam</summary><p>
  
        ![alt text](https://i.imgur.com/8gf3R1l.png)
        </p></details>
  
      - <details><summary>5GCD Lifebloom rolling</summary><p>
  
        ![alt text](https://i.imgur.com/pbqzL0a.png)
        </p></details>
  
      </p></details> 

    </p></details>
  

  </details> 

&nbsp;
  
- <details><summary>Kil'jaedan</summary>  
  &nbsp;

  - <details><summary>Rotation rankings</summary><p>
  
    ![alt text](https://i.imgur.com/bJHpuF9.png)
    </p></details> 
  
  - <details><summary>% Spell HPS scatter plots</summary><p>
  
    ![alt text](https://i.imgur.com/wS6rIdD.png)
  
    The bulk of players choose to either heal mostly with Regrowth or Lifebloom (rolling blooms on Fire Bloom targets) with relatively little use of rejuv.
    </p></details>
  
  - <details><summary>HPS vs Duration (Color = kill speed percentile, not HPS)</summary><p>
  
    ![alt text](https://i.imgur.com/z6aCFwE.png)
  
    Most players fall within the 10th to 75th percentile of kill times.
    </p></details>
  
  - <details><summary>Q. What percentage of players are rolling Lifebloom on the tank?</summary><p>
  
     ![alt text](https://i.imgur.com/OcgPS77.png)
  
     46.0% of players are rolling Lifebloom on the tank.
     </p></details>
  
  - <details><summary>Q. What percentage of players have an extra mana source?</summary><p>
  
    ![alt text](https://i.imgur.com/GpEMWR0.png)
  
    93.4% of players received either an innervate or shadow priest.
    </p></details>
  
  - <details><summary>Q. What percentage of players are playing Nature's Grace?</summary><p>
  
     ![alt text](https://i.imgur.com/uwZeiy0.png)
  
     21.6% of players are Nature's Grace spec.
     </p></details>
  
  - <details><summary>Q. What variables correlate the most with HPS?</summary><p>
  
    ![alt text](https://i.imgur.com/9BgNXHz.png)
  
    The top five correlators of HPS in order of importance: 
    - Higher spell haste rating  
    - Casting more regrowths  
    - Having shadow priest  
    - Less number of healers  
    - Casting less rejuvs    
    &nbsp; 
  
    </p></details>
  
  - <details><summary>Trinket analysis</summary><p>
    
    - <details><summary>Q. Which trinkets are players using the most?</summary><p>
  
      ![alt text](https://i.imgur.com/qePhCjE.png)
      </p></details>
  
    - <details><summary>Q. Which combinations of trinkets are players using the most?</summary><p>
  
      ![alt text](https://i.imgur.com/nCx8Wx2.png)
      </p></details>
  
    - <details><summary>Q. Does playstyle/rotation affect the distribution of trinkets?</summary><p>
  
      - <details><summary>Q. Regrowth spam (0LB 0I 6RG, 0LB 1I 5RG, 0LB 2I 4RG) - Individual trinkets</summary><p>
  
        ![alt text](https://i.imgur.com/Y3xz4Tu.png)
        </p></details>
  
      - <details><summary>Q. Regrowth spam (0LB 0I 6RG, 0LB 1I 5RG, 0LB 2I 4RG) - Trinket combinations</summary><p>
  
        ![alt text](https://i.imgur.com/k1TSNnY.png)
        </p></details>
  
      - <details><summary>Q. 5GCD Lifebloom rolling (1LB 4I 0RG, 1LB 1I 2RG, ...) - Individual trinkets</summary><p>
  
        ![alt text](https://i.imgur.com/0sCI4b1.png)
        </p></details>
  
      - <details><summary>Q. 5GCD Lifebloom rolling (1LB 4I 0RG, 1LB 1I 2RG, ...) - Trinket combinations</summary><p>
  
        ![alt text](https://i.imgur.com/bFYq67i.png)
        </p></details>
  
      </p></details>
  
    </p></details>
  
  </p></details>
    

&nbsp;

-----

- <details><summary>Black Temple</summary> 
  &nbsp;
  
  Note: This section uses Phase 4 data.
  &nbsp;
  
  - <details><summary>High Warlord Naj'entus</summary>  
    &nbsp;

    - <details><summary>Rotation rankings</summary><p>

      ![alt text](https://i.imgur.com/VWPltCF.png)

      The top five rotations:
      - 0LB 0I 5RG: Not rolling lifebloom on the tank and raid healing with regrowth, 42.1% of players do this rotation.  
      - 1LB 1I 2RG: ~20 Haste rating rotation, 1.7% of players do this rotation.  
      - 1LB 0I 3RG: ~120 Haste rotation without NG, ~20 Haste rotation with NG (and 1 of 3 regrowths proc NG), 2.5% of players do this rotation.  
      - 1LB 0I 4RG: ~250 Haste with Nature's Grace rotation (And 3/4 proc NG, or with Bloodlust), or high haste ToL spec with Bloodlust, 2.6% of players do this rotation.      
      - 0LB 1I 4RG: Mostly raid healing with Regrowth with the occasional rejuv, 19.1% of players do this rotation.    
      &nbsp;

      *Interestingly, there's a big difference between 1LB 0I 2RG and 1LB 0I 3RG, but there isn't a big difference between 1LB 0I 3RG and 1LB 0I 4RG, and the former is performing slightly better within uncertainty. Why is that? Mana constraints are one possibility, but it'd be interesting to look into further.  

      Let's drill down on some rotations.

      - <details><summary>Q. How does 0LB 0I 5RG perform for Nature's Grace vs Tree of Life spec?</summary><p>

        ![alt text](https://i.imgur.com/HVQAiu3.png)

        Nature's Grace performs significantly better than Tree of Life spec.  
        </p></details>

      - <details><summary>Q. How does 1LB 0I 3RG perform for Nature's Grace vs Tree of Life spec?</summary><p>

        ![alt text](https://i.imgur.com/4UUS5JL.png)

        They perform the same within uncertainty.    
        </p></details>

      - <details><summary>Q. How does 1LB 0I 4RG perform for Nature's Grace vs Tree of Life spec, and also filtered by Bloodlust/Hero?</summary><p>

        ![alt text](https://i.imgur.com/6pHPKAZ.png)

        The players with Bloodlust/Hero tend to perform better than those without it. Surprisingly (to me), ToL spec players with lust tend to perform similar or better than Nature's Grace players with lust. Why is that?      
        </p></details>
        &nbsp;

      </p></details>

    - <details><summary>% Spell HPS scatter plots</summary><p>

      ![alt text](https://i.imgur.com/dru9e7P.png)

      The bulk of players do not raid heal with Lifebloom or Rejuv. Players tend to either purely raid heal with regrowth, or roll Lifebloom/Rejuv on the tank and heal the raid with regrowth.  
      </p></details>

    - <details><summary>HPS vs Duration (Color = kill speed percentile, not HPS)</summary><p>

      ![alt text](https://i.imgur.com/TE1FOsV.png)

      Most players fall within the 75th to 95th percentile of kill times.
      </p></details>

    - <details><summary>Q. What percentage of players are actually rolling Lifebloom on the tank?</summary><p>

      ![alt text](https://i.imgur.com/OP28oY0.png)

      28.1% of players are rolling Lifebloom on the main tank, the rest are purely raid healing. Interestingly, three of the top five rotations involve rolling Lifebloom on the main tank, however the vast majority of rankers choose to purely raid heal.  
      </p></details>

    - <details><summary>Q. What percentage of players have an extra mana source?</summary><p>

      ![alt text](https://i.imgur.com/uuzzmEF.png)

      89.0% of players received either an innervate or shadow priest.
      </p></details>

    - <details><summary>Q. What percentage of players are playing Nature's Grace?</summary><p>

      ![alt text](https://i.imgur.com/grkG0i6.png)

      54.3% of players are Nature's Grace spec.
      </p></details> 

    - <details><summary>Q. What variables correlate the most with HPS?</summary><p>

      ![alt text](https://i.imgur.com/3BkHcYT.png)

      The top five correlators of HPS in order of importance: 
      - Using more regrowth heavy rotations  
      - Having less healers in your raid  
      - Being Nature's Grace spec  
      - Not rolling Lifebloom on the tank  
      - Not using Lifebloom to raidheal   
      &nbsp; 

      </p></details>
    </details> 

  &nbsp;

  - <details><summary>Supremus</summary>
    &nbsp;

    - <details><summary>Rotation rankings</summary><p>

      ![alt text](https://i.imgur.com/yaDpQF5.png)

      The top five rotations:
      - 1LB 0I 4RG: ~250 Haste with Nature's Grace rotation (And 3 out of 4 regrowth casts must proc NG), 3.2% of players do this rotation.
      - 0LB 1I 4RG: Raid healing mostly with Regrowth and the occasional rejuv, 10.7% of players do this rotation.  
      - 1LB 0I 2RG: 0 Haste rotation, 9.9% of players do this rotation.  
      - 0LB 2I 3RG: Raid healing with slightly more rejuvs than above. 3.5% of players do this rotation.  
      - 0LB 0I 5RG: Raid healing with only regrowth. 16.9% of players do this rotation.  
      </p></details>

    - <details><summary>% Spell HPS scatter plots</summary><p>

      ![alt text](https://i.imgur.com/Z8jXoyC.png)

      The bulk of players do not raid heal with Lifebloom or Rejuv, and instead roll Lifebloom on the main tank with 20-60% of their HPS coming from Regrowth.    
      </p></details>

    - <details><summary>HPS vs Duration (Color = kill speed percentile, not HPS)</summary><p>

      ![alt text](https://i.imgur.com/t6HNoyD.png)

      Most players fall within the 75th to 95th percentile of kill times.
      </p></details>

    - <details><summary>Q. What percentage of players are rolling Lifebloom on the tank(s)?</summary><p>

      ![alt text](https://i.imgur.com/DWhUQNa.png)

      84.2% of players are rolling Lifebloom on *at least* one tank, the rest are purely raid healing.  
      42.6% of players roll Lifebloom on only the primary tank.  
      34.7% of players roll Lifebloom on both the primary tank and the hateful strike tank.  

      One-tank rotations perform better on average than two-tank rotations. Why? One interpretation is that when rolling LB on the offtank, a lot of the healing is overhealing, as hateful strikes are infrequent and the off-tank gets healed to full fairly quickly. It's arguable that your GCDs are better used with regrowths and just rotating on the primary tank. However, it's also possible that the data is biased because Druids are unlikely to 2-tank rotate during the Kite phase. It would be interesting to split the data between tank phase and kite phase and see how the top rotations differ.  
      </p></details>

    - <details><summary>Q. What percentage of players have an extra mana source?</summary><p>

      ![alt text](https://i.imgur.com/L8I4tKm.png)

      68.2% of players received either an innervate or shadow priest.
      </p></details>

    - <details><summary>Q. What percentage of players are playing Nature's Grace?</summary><p>

      ![alt text](https://i.imgur.com/KzXd5ca.png)

      34.9% of players are Nature's Grace spec.
      </p></details>

    - <details><summary>Q. What variables correlate the most with HPS?</summary><p>

      ![alt text](https://i.imgur.com/zxFk4s2.png)

      The top five correlators of HPS in order of importance: 
      - Using more regrowth heavy rotations  
      - Having less healers in your raid  
      - Being Nature's Grace spec  
      - Shorter fight duration  
      - Rolling Lifebloom on a lower number of tanks  
      &nbsp;

      </p></details>

    </details>  

  &nbsp;

  - <details><summary>Teron Gorefiend</summary>
    &nbsp;

    - <details><summary>Rotation rankings</summary><p>

      ![alt text](https://i.imgur.com/zBfQV3C.png)

      The top five rotations:
      - 1LB 0I 3RG: ~120 Haste rotation without NG, ~20 Haste rotation with NG (and 1 of 3 regrowths proc NG), 3% of players do this rotation.     
      - 0LB 0I 5RG: Raid healing with only regrowth, 16.9% of players do this rotation.  
      - 0LB 1I 4RG: Raid healing mostly with regrowth and the occasional rejuv, 10.7% of players do this rotation.   
      - 1LB 1I 2RG: ~20 Haste rating rotation, 4.3% of players do this rotation.      
      - 0LB 2I 3RG: Raid healing mostly with regrowth, but more rejuvs than the above, 3.5% of players do this rotation.   
      &nbsp;

      Let's drill down further.

      - <details><summary>Q. How does 1LB 0I 3RG perform for Nature's Grace vs Tree of Life spec?</summary><p>

        ![alt text](https://i.imgur.com/cekncC5.png)

        Interestingly ToL performs better than NG within uncertainty, however the sample size for the former is relatively small.  
        </p></details>

      - <details><summary>Q. How does 0LB 0I 5RG perform for Nature's Grace vs Tree of Life spec?</summary><p>

        ![alt text](https://i.imgur.com/w1vituT.png)

        Nature's Grace wins.  
        </p></details>
        &nbsp;

      </p></details>

    - <details><summary>% Spell HPS scatter plots</summary><p>

      ![alt text](https://i.imgur.com/7hd2DNg.png)

      The bulk of players do not raid heal with Lifebloom or Rejuv, and instead roll Lifebloom/Rejuv on the main tank with 40-80% of their HPS coming from Regrowth.    
      </p></details>

    - <details><summary>HPS vs Duration (Color = kill speed percentile, not HPS)</summary><p>

      ![alt text](https://i.imgur.com/xNLdR8K.png)

      Most players are evenly distributed between the 25th to 95th percentile.
      </p></details>

    - <details><summary>Q. What percentage of players are rolling Lifebloom on the tank?</summary><p>

      ![alt text](https://i.imgur.com/aM4LxZa.png)

      68.1% of players are rolling Lifebloom on the tank, the rest are purely raid healing.
      </p></details>  

    - <details><summary>Q. What percentage of players have an extra mana source?</summary><p>

      ![alt text](https://i.imgur.com/3Mj4tG9.png)

      91.2% of players received either an innervate or shadow priest.    
      </p></details>

    - <details><summary>Q. What percentage of players are playing Nature's Grace?</summary><p>

      ![alt text](https://i.imgur.com/bZL4HHc.png)

      49.0% of players are Nature's Grace spec.
      </p></details>

    - <details><summary>Q. What variables correlate the most with HPS?</summary><p>

      ![alt text](https://i.imgur.com/FoLbHrt.png)

      The top five correlators of HPS in order of importance: 
      - Having power infusion  
      - Using more regrowth heavy rotations  
      - Having less healers in your raid  
      - Having shadowpriest  
      - Being Nature's Grace spec  
      &nbsp;

      </p></details>  

  &nbsp;

  - <details><summary>Gurtogg Bloodboil</summary>
    &nbsp;

    - <details><summary>Rotation rankings</summary><p>

      ![alt text](https://i.imgur.com/7OXYME5.png)

      The top five rotations:
      - 1LB 0I 3RG: ~120 Haste rotation without NG, ~20 Haste rotation with NG (and 1 of 3 regrowths proc NG), 1.6% of players do this rotation.  
      - 0LB 1I 4RG: Mostly raid with with Regrowth with the occasional LB/rejuv, 12.0% of players do this rotation.    
      - 0LB 0I 5RG: Raid healing with regrowth, 13.0% of players do this rotation.  
      - 0LB 5I 0RG: Raid healing with LB or Rejuv (see below), 15.0% of players do this rotation.   
      - 0LB 2I 3RG: Mostly raid healing with Regrowth, but with more rejuvs than the above, 6.0% of players do this rotation.          
      &nbsp;

      - <details><summary>Q. How does 1LB 0I 3RG perform for Nature's Grace vs Tree of Life spec?</summary><p>

        ![alt text](https://i.imgur.com/hsEfFTw.png)

        NG performs better than ToL within uncertainty, but the sample size for the latter is very small.    
        </p></details>

      - <details><summary>Q. How does 0LB 1I 4RG perform for Nature's Grace vs Tree of Life spec?</summary><p>

        ![alt text](https://i.imgur.com/PGaAhbx.png)

        Nature's Grace wins.    
        </p></details>

      - <details><summary>Q. How does 0LB 0I 5RG perform for Nature's Grace vs Tree of Life spec?</summary><p>

        ![alt text](https://i.imgur.com/G7UTili.png)

        Nature's Grace wins.    
        </p></details>

      - <details><summary>Q. For 0LB 5I 0RG, how does Lifebloom compare to Rejuv?</summary><p>

        ![alt text](https://i.imgur.com/lxraQ3F.png)

        Lifebloom wins by a wide margin.    
        </p></details>

      - <details><summary>Q. Follow up question, for players raidhealing with Lifebloom, are they using 1 stack of LB or rolling on the bloodboils?</summary><p>

        ![alt text](https://i.imgur.com/2vsCzPB.png)

        Rolling lifeblooms wins, also by a wide margin! A useful note: bloodboil is a very similar mechanic to Kil'jaedan's Fire Bloom. As a follow up, it would be interesting to know if these groups are soaking more than one bloodboil stacks.   
        </p></details>  

      - <details><summary>Let's look again at the top-5 rotations with all these filters.</summary><p>

        ![alt text](https://i.imgur.com/lR571Wu.png)
        </p></details>

      &nbsp;

      </p></details>  

    - <details><summary>% Spell HPS scatter plots</summary><p>

      ![alt text](https://i.imgur.com/Rfz7sHT.png)

      There is a bit of variation in what players have success with. Some players tend to mainly raidheal with regrowth, others tend to raidheal with rejuv, and for others the bulk of their effective healing comes from Lifebloom ticks. There is a lot of room for personal preference on this boss.  
      </p></details>

    - <details><summary>HPS vs Duration (Color = kill speed percentile, not HPS)</summary><p>

      ![alt text](https://i.imgur.com/hYE0hJN.png)

      Most players are evenly distributed between the 25th to 95th percentile.  
      </p></details>

    - <details><summary>Q. What percentage of players are rolling Lifebloom on the tank?</summary><p>

      ![alt text](https://i.imgur.com/8ASi4gu.png)

      48.2% of players are rolling Lifebloom on at least one tank, with 44.4% of players rolling on exactly one tank and 3.3% of players rolling on exactly two tanks.  
      </p></details>  

    - <details><summary>Q. What percentage of players have an extra mana source?</summary><p>

      ![alt text](https://i.imgur.com/5Tcb51h.png)

      88.4% of players received either an innervate or shadow priest.    
      </p></details>

    - <details><summary>Q. What percentage of players are playing Nature's Grace?</summary><p>

      ![alt text](https://i.imgur.com/d3ry8py.png)

      41.3% of players are Nature's Grace spec.  
      </p></details>

    - <details><summary>Q. What variables correlate the most with HPS?</summary><p>

      ![alt text](https://i.imgur.com/UoB5Lk5.png)

      The top five correlators of HPS in order of importance: 
      - % Rotation 1, which is to say, Druids who tend to stick to a particular rotation tend to perform better than Druids who vary their rotation during the fight.   
      - Less raidhealing with one stack of Lifebloom (Preferring rolling LB > Regrowth > Rejuv)   
      - Less raidhealing with Rejuv (Preferring Rolling LB > Regrowth)  
      - Less number of healers    
      - Shorter kill time    
      &nbsp;

      </p></details>  

    </details>  

    &nbsp;

  - <details><summary>Reliquary of Souls</summary>  
    &nbsp;

    - <details><summary>Rotation rankings</summary><p>

      **Note:** I will be splitting this section into phase 2 and phase 3, since rotations may not necessarily perform the same for both.

      ![alt text](https://i.imgur.com/GhHlQWO.png)   
      </p></details>  

    </details>  

    &nbsp;

  - <details><summary>Mother Shahraz</summary>  
    &nbsp;

    - <details><summary>Rotation rankings</summary><p>

      ![alt text](https://i.imgur.com/U4IZwL5.png)

      The top five rotations:
      - 0LB 1I 4RG: Raidhealing mostly with Regrowth and the occasional Rejuv, 15.8% of players do this rotation.
      - 0LB 0I 5RG: Raid healing with Regrowth, 22.7% of players do this rotation.  
      - 1LB 1I 2RG: ~20 Haste rotation, 2.1% of players do this rotation.  
      - 1LB 0I 3RG: ~120 Haste rotation without NG, ~20 Haste rotation with NG (and 1 of 3 regrowths proc NG), 2.1% of players do this rotation.  
      - 1LB 0I 4RG: ~250 Haste with Nature's Grace rotation (And 3 out of 4 regrowth casts must proc NG), 4.3% of players do this rotation.    
      </p></details>

    - <details><summary>% Spell HPS scatter plots</summary><p>

      ![alt text](https://i.imgur.com/xKQTQ03.png)

      The vast majority of players raid heal with regrowth, although the percentage of a player's HPS from regrowth can range anywhere from 0% to 90%. A significant portion of HPS also comes from rolling Lifebloom on exactly one tank.      
      </p></details>

    - <details><summary>HPS vs Duration (Color = kill speed percentile, not HPS)</summary><p>

      ![alt text](https://i.imgur.com/iO1rs1p.png)

      Most players are evenly distributed between the 25th to 95th percentile.  
      </p></details>

    - <details><summary>Q. What percentage of players are rolling Lifebloom on the tank(s)?</summary><p>

      ![alt text](https://i.imgur.com/Id89VBh.png)

      48.4% of players are rolling Lifebloom on at least one tank, with 37.7% of players rolling on exactly one tank and 5.3% of players rolling on exactly two tanks, and 5.3% of players rolling on all three tanks.  
      </p></details> 

    - <details><summary>Q. What percentage of players have an extra mana source?</summary><p>

      ![alt text](https://i.imgur.com/wlBwLtc.png)

      93.5% of players received either an innervate or shadow priest.    
      </p></details>

    - <details><summary>Q. What percentage of players are playing Nature's Grace?</summary><p>

      ![alt text](https://i.imgur.com/IoLp58F.png)

      49.0% of players are Nature's Grace spec.  
      </p></details>

    - <details><summary>Q. What variables correlate the most with HPS?</summary><p>

      ![alt text](https://i.imgur.com/80lsytV.png)

      The top five correlators of HPS in order of importance: 
      - More raidhealing with regrowth.   
      - Rolling lifebloom on a lower number of tanks.   
      - Playing Nature's Grace.   
      - Less number of healers    
      - Not raidhealing with Lifebloom.    
      &nbsp;

      </p></details> 

  </p></details>
  
</p></details>
  
  
  
  
  
