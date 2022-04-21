# TBC Resto Druid Analyzer  
#-----------------------------------------  
*Author: Mercychan - Benediction (US)*    
*Discord: Mercy#9226*  
#-----------------------------------------  

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
 
You'll also see me use weird rotations such as 0LB 0I 5RG, 0LB 4I 1RG, etc. These aren't exactly "rotations", because the player isn't rolling lifebloom on the tank at all, and instead purely raid healing. For this analysis it's useful to keep track of these players as well.


# Dataset  
WarcraftLogs data is scraped from the top 3,000 players for each boss (in progress) for Restoration spec Druids (There are zero Dreamstate druids in the dataset). This encompasses roughly the 95th percentile and above. The dataset (located in data/top_N_druids.xlsx) contains the following:  

&emsp; • Rank  
&emsp; • Character name, server, region  
&emsp; • Date  
&emsp; • Duration    
&emsp; • Number of healers  
&emsp; • Shadowpriest in group?  
&emsp; • Innervate received?  
&emsp; • Bloodlust/heroism received?  
&emsp; • Power Infusion received?   
&emsp; • Is Nature's Grace spec?  
&emsp; • Lifebloom uptime %  
&emsp; • Total HPS  
&emsp; • % HPS of: Lifebloom (tick), Lifebloom (bloom), Rejuvenation, Regrowth, Swiftmend  
&emsp; • Rotating on tank? ('No' means the Druid is not rolling LB on the tank and instead just raid healing)  
&emsp; • Top two rotations used  

To be added in the near future: Haste rating, trinkets equipped, number of dead healers       

# Analysis
Rotations are determined via the cast sequence data provided by WCL ([an example](https://classic.warcraftlogs.com/reports/VZr6X2MNY73GLktg#fight=47&type=casts&view=events&source=37)). In short, the [rotation calculator](https://github.com/msdec321/DataAnalysisWorkbooks/blob/main/warcraftLogs/src.py#L535-L623) checks when Lifebloom is cast on a tank which signals the start of a rotation. The following casts are recorded until either 1) The lifebloom is refreshed or 2) The rotation reaches 5 casts. (Note: hasted rotations can go over 5 casts, that will be supported in the future). Casts that are off the global cooldown are ignored. For purely raid healing Druids, the calculator simply counts the number of regrowths/instants cast in a 5-cast window. The rotation is recorded into a dictionary object and at the end the top 2 rotations are saved to the dataset.  

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
=todo after data collection=

- <details><summary>High Warlord Naj'entus</summary>  
  &nbsp;

  - <details><summary>Rotation rankings</summary><p>
  
    ![alt text](https://i.imgur.com/VWPltCF.png)
  
    The top five rotations:
    - 0LB 0I 5RG: Not rolling lifebloom on the tank and raid healing with regrowth, 42.1% of players do this rotation.  
    - 1LB 1I 2RG: ~20 Haste rating rotation, 1.7% of players do this rotation.  
    - 1LB 0I 3RG: ~120 Haste rotation without NG, ~20 Haste rotation with NG (and 1 of 3 regrowths proc NG), 2.5% of players do this rotation.  
    - 1LB 0I 4RG: ~250 Haste with Nature's Grace rotation (And 3/4 proc NG, or with Bloodlust), or high haste ToL spec with Bloodlust, 2.6% of players do this rotation.      
    - 0LB 1I 4RG: Mostly raid with with Regrowth with the occasional rejuv, 19.1% of players do this rotation.    
    &nbsp;
  
    Let's drill down further.
  
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
  
  - <details><summary>Q. What percentage of players are playing Nature's Grace? (Note: There are no Dreamstate Druids in the dataset.)</summary><p>
  
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
  
      ![alt text](https://i.imgur.com/YGI3UrS.png)
  
      Nature's Grace performs better on average, however number of ToL players doing the rotation is relatively small.  
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
    </p></details>
  
  - <details><summary>% Spell HPS scatter plots</summary><p>
  
    ![alt text](https://i.imgur.com/Rfz7sHT.png)
  
    There is a bit of variation in what players have success with. Some players tend to mainly raidheal with regrowth, others tend to raidheal with rejuv, and for others the bulk of their effective healing comes from Lifebloom ticks. There is a lot of room for personal preference on this boss, although from the rankings, more regrowth-heavy rotations perform slightly better on average.  
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
  
    ![alt text](https://i.imgur.com/JqaWQNU.png)
  
    41.3% of players are Nature's Grace spec.  
    </p></details>
  
  - <details><summary>Q. What variables correlate the most with HPS?</summary><p>
  
    ![alt text](https://i.imgur.com/UoB5Lk5.png)
  
    The top five correlators of HPS in order of importance: 
    - % Rotation 1, which is to say, Druids who tend to stick to a particular rotation tend to perform better than Druids who vary their rotation during the fight.   
    - Less raidhealing with Lifebloom (Preferring Regrowth over Rejuv)   
    - Less raidhealing with Rejuv (Preferring Regrowth)  
    - Less number of healers    
    - Shorter kill time    
    &nbsp;
    </p></details>
  
  </details>
  
  
