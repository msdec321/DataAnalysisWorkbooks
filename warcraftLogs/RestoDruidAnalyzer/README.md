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

# Analysis
Rotations are determined via the cast sequence data provided by WCL ([an example](https://classic.warcraftlogs.com/reports/VZr6X2MNY73GLktg#fight=47&type=casts&view=events&source=37)). In short, the [rotation calculator](https://github.com/msdec321/DataAnalysisWorkbooks/blob/main/warcraftLogs/src.py#L535-L623) checks when Lifebloom is cast on a tank which signals the start of a rotation. The following casts are recorded until either 1) The lifebloom is refreshed or 2) The rotation reaches 5 casts. (Note: hasted rotations can go over 5 casts, that will be supported in the future). Casts that are off the global cooldown are ignored. For purely raid healing Druids, the calculator simply counts the number of regrowths/instants cast in a 5-cast window. The rotation is recorded into a dictionary object and at the end the top 2 rotations are saved to the dataset.  

In general, the distribution of HPS for each rotation is exponentially falling with a long tail. Each distribution has a characteristic mean and width (σ), which can be used to compare the performance of each rotation. The relative uncertainty is taken as the standard error: SE = σ / √(n).    
<details> 
 <summary>Distribution of HPS</summary><p>
 
 ![alt text](https://i.imgur.com/Vz3K0hv.jpg)
</p></details>

<details> 
 <summary>Comparing multiple distributions</summary><p>
 
 ![alt text](https://i.imgur.com/VWPltCF.png)
</p></details>  

Some errorbars are large for two reasons. Primarily, the rotation performs inconsistently; some players perform exceptionally better with the rotation than others (large σ). Second, there are relatively few players doing the rotation (small n). In general, the larger the sample size the smaller the uncertainty.


# Results and discussion
=todo after data collection=

<details>
  <summary>Unfiltered dataset</summary><p>

- <details><summary>Naj'entus</summary>  
  &nbsp;

  - <details><summary>Rotation rankings</summary><p>
  
    ![alt text](https://i.imgur.com/VWPltCF.png)
    </p></details>
  
  - <details><summary>Q. What percentage of players are actually rolling Lifebloom on the tank?</summary><p>
  
    ![alt text](https://i.imgur.com/OP28oY0.png)
  
    28.1% of players are rolling Lifebloom on the main tank, the rest are purely raid healing. Interestingly, three of the top five rotations involve rolling Lifebloom on the main tank, however the vast majority of rankers choose to purely raid heal with regrowth (0LB 0I 5RG).
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
  
    ![alt text](https://i.imgur.com/x2OO1lW.png)
  
    The top five correlators of HPS in order of importance: 
    - Using more regrowth heavy rotations  
    - Having less healers in your raid  
    - Being Nature's Grace spec  
    - Not rolling Lifebloom on the tank  
    - Not using Rejuvenation  
    &nbsp;
  
    A note of caution: These are only correlations for *within* the 95th-100th percentile and isn't necessarily generalizable to the full raiding population. For example, 89% of players in the dataset had access to either innervate or shadowpriest, yet the correlation is relatively low. Does that mean having innervate is not important for getting a good parse? No, and in fact the opposite can be true. 
  
    </p></details>
  </details> 

&nbsp;
  
- <details><summary>Supremus</summary>
  &nbsp;

  - <details><summary>Rotation rankings</summary><p>
  
    ![alt text](https://i.imgur.com/yaDpQF5.png)
   
    The top performing rotation is a hasted Nature's Grace rotation (1 LB -> 4 Regrowth), however relatively few players are doing it.
    Interestingly, the third best performing rotation is a 0-Haste rotation (1 LB -> 2 Regrowths).
    </p></details>
  
  - <details><summary>Q. What percentage of players are rolling Lifebloom on the tank(s)?</summary><p>
  
    ![alt text](https://i.imgur.com/DWhUQNa.png)
  
    84.2% of players are rolling Lifebloom on *at least* one tank, the rest are purely raid healing.  
    42.6% of players roll Lifebloom on only the primary tank.  
    34.7% of players roll Lifebloom on both the primary tank and the hateful strike tank.  
  
    One-tank rotations perform better on average than two-tank rotations. Why? One interpretation is that when rolling LB on the offtank, a lot of the healing is overhealing, as hateful strikes are infrequent and the off-tank gets healed to full fairly quickly. It's arguable that your GCDs are better used with regrowths and just rotating on the primary tank. However, it's also possible that the data is biased because Druids are unlikely to 2-tank rotate during the Kite phase. It would be interesting to split the data between tank phase and kite phase and see how the top rotations differ.  
  
    Compared to other bosses, rotations perform very similarly to one another on Supremus, often only differing by tens of HPS on average. 
    </p></details>
  
  - <details><summary>Q. What percentage of players have an extra mana source?</summary><p>
  
    ![alt text](https://i.imgur.com/L8I4tKm.png)
  
    68.2% of players received either an innervate or shadow priest.
    </p></details>
  
  - <details><summary>Q. What percentage of players are playing Nature's Grace?</summary><p>
  
    ![alt text](https://i.imgur.com/KzXd5ca.png)
  
    34.9% of players are Nature's Grace spec.
    </p></details>
  
  </details>  
  
  </details>  
  
</p></details>
