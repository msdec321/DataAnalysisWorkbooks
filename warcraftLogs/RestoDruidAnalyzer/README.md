# Resto Druid Analyzer  
#-----------------------------------------  
*Author: Mercychan - Benediction (US)*    
*Discord: Mercy#9226*  
#-----------------------------------------  

# Motivation
TBC Resto Druid is complicated. The rotation that you choose to use in an encounter can depend on several factors: how many tanks are there? How much mana will you have available? How much do you prioritize healing the tank vs the raid? Is the raid damage constant (Bloodboil, ROS, Azgalor) or sudden and unpredictable (Najentus, Mother)? While theorycrafting can determine the best rotations in a vaccuum, boss encounters are messy and effective healing is difficult to model accurately for every encounter.  

The motivation of this project is to take a data-driven approach to this problem; what are the top performing players *actually* doing on each boss? Furthermore, what are the best rotations given *your* specific raid composition? (For example: On Najentus if your raid has 4, 5, or 6 healers, whether you get innervate/Spriest or not, rolling HoTs on the tank or not, playing Nature's Grace or not, your kill times, etc.). There is a vast resource of data provided by WarcraftLogs that is currently not being used by the community (understandably, building a dataset is difficult and time consuming). Regardless of your skill level, I hope that the results of this analysis will help improve our understanding of the class.


# The elephant in the room
"Healing parses don't matter". Have you heard this before? Whenever I see Druids soliciting feedback online (reddit or elsewhere), this is the most common response. "Did your tank die? No? Then you're fine". Not only is this feedback unsatisfying, but it's not even advice. It's anti-advice, because it leaves the asker with the impression that there's no room for improvement. The hard truth for Druids is that rotations are not built equally. If I want to roll HoTs on the tank(s) and do some raid healing, some rotations are just better than others. In my opinion HPS is the best KPI to compare rotations. While there are some shenanigans that occur in the 99th percentile of Druid parses (for example, Druids who just raid heal with Nature's Grace and ignore their tanks entirely), by aggregating large amounts of data these things are easy to filter out, and comparing Druids who are playing "honestly" becomes relatively straightforward.  


# Rotations and notation
Lifebloom lasts for 7 seconds. When refreshing lifebloom on a tank there is a limited sequence of spells that you can cast before you need to refresh that lifebloom. This is called a rotation. For a more detailed explanation on rotations, please refer to the [Elitist Jerks guide](http://web.archive.org/web/20080913120521/http://elitistjerks.com/f31/t17783-druid_raiding_tree/#Healing_Strategies).  

Although rotations have been documented since original TBC, a lot has changed a decade later. For example, much faster kill times these days allow Druids to use more mana-intensive rotations that are regrowth heavy. Additionally, the popularity of Nature's Grace in TBCC adds several new rotations into the mix. With so many rotations available to choose it becomes less clear which subset of rotations are best for specific encounters and the specifics of your raid composition. In my opinion, Resto Druid remains "unsolved" even a decade after original TBC; there is just too much complexity built into the spec.  

To simplify things I use the following notation when talking about rotations:  
"xLB yI zRG", where x, y, z are numbers and LB, I, RG are "Lifebloom", "Instant", and "Regrowth", respectively.  
Here, "LB" refers to lifeblooms being rolled on _tanks_. Lifeblooms being used to raidheal go into the 'instant' bucket.  
* Example 1: "1LB 2I 1RG" can mean: 'Lifebloom 1 tank -> use 2x instant casts (lifebloom, rejuv, swiftmend, etc) -> cast 1x regrowth, repeat. The instants and regrowths can be cast in any order.
* Example 2: "2LB 1I 1RG" -> Lifebloom tank 1 -> Lifebloom tank 2 -> 1x Instant (like a rejuv on tank or raid) -> 1x Regrowth (on tank or raid), repeat. The order is not important, you could even do "Lifebloom tank 1 -> 1x Regrowth -> 1x rejuv -> Lifebloom tank 2, repeat and that will still be called "2LB 1I 1RG".  
 
You'll also see weird rotations such as 0LB 0I 5RG, 0LB 4I 1RG, etc. These aren't exactly "rotations", because the player isn't rolling lifebloom on the tank at all. They're just raid healing. For this analysis it's useful to keep track of these as well.


# Dataset info
WarcraftLogs data is scraped from the top 3,000 players for each boss, biweekly. This encompasses roughly the 95th percentile and above. For a detailed list of all data scraped, refer to the [README](https://github.com/msdec321/DataAnalysisWorkbooks/blob/main/warcraftLogs/README.md) in the parent directory. Rotations are determined via the cast sequence data provided by WCL ([an example](https://classic.warcraftlogs.com/reports/VZr6X2MNY73GLktg#fight=47&type=casts&view=events&source=37)). In short, the [rotation calculator](https://github.com/msdec321/DataAnalysisWorkbooks/blob/main/warcraftLogs/src.py#L529-L617) checks when Lifebloom is cast on a tank which signals the start of a rotation. The following casts are recorded until either 1) The lifebloom is refreshed or 2) The rotation reaches 5 casts. (Note: hasted rotations can go over 5 casts, that will be supported in the future). The rotation is recorded into a dictionary object and at the end the top 2 rotations are saved to the dataset.    


# Analysis
=todo=


# Results
=todo=
