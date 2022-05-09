# Bangle/Blue Dragon Analyzer
#-----------------------------------------  
*Author: Mercychan - Benediction (US)*    
*Discord: Mercy#9226*  
#-----------------------------------------  

# Motivation  
Since before TBC Classic launched, Bangle of the Endless Blessings and Darkmoon Card: Blue Dragon have been and remain controversial trinkets. The reasons for player's disdain vary depending on who you ask, but the most common reasons that I've read are: 1) Druid's don't need mana, 2) They lack +heal, and 3) Blue Dragon is bad because it is random. The first reason is laughably wrong, since mana is heavily constrained by encounter length and rotation. The second reason, while true, depends on how you value mana. Blue Dragon has seen a fair amount of use in speedruns, and as encounters become longer in Sunwell Plateau I suspect Blue Dragon will become more popular among the playerbase as well. Lastly, the third reason is not a reason at all. Consider this: if the proc chance were 99% instead of 2%, it is still bad *because* it is random? Blue Dragon's worth must be judged from a statistics argument, not whatever anecdote "I saw a player go 5 minutes without a proc!" is pulled out of a hat. Thankfully, I think players have wisened up to Blue Dragon's worth over time, but you will always find critics pop up whenever it is mentioned.

# Questions  
1) How much mp5 is Blue Dragon on average?  
2) How many procs per minute can you expect with Blue Dragon?  
3) What is the mp5 of Bangle?
4) Is it better to use Bangle on cooldown or only with Blue Dragon procs?

# Dataset
WarcraftLogs data is scraped from the top 1,000 Black Temple speedruns, this includes both trash and boss encounters. In order for a Druid to be included in the dataset, they must have both Bangle and Blue Dragon equipped for *at least* 7 out of 9 bosses. The dataset (./bangle_bluedragon.xlsx) contains the following:  


&emsp; • Character name, Guild name  
&emsp; • Total duration, duration in combat (s)  
&emsp; • Average spirit, average intellect  
&emsp; • Blue Dragon uptime (s), Endless Blessings uptime (s)   
&emsp; • # of Blue Dragon procs, # of Bangle uses  
&emsp; • # of times BD and Bangle use overlap  
&emsp; • Total time of BD and bangle overlap  
&emsp; • Average time between Blue Dragon procs (s)  
&emsp; • Average time between Bangle off-cooldown and next Blue Dragon proc (s)  
&emsp; • Total mana received from BD, Bangle, and BD+Bangle overlap  
&emsp; • Mp5 of BD, Bangle use, and BD+Bangle overlap  
&emsp; • Normalized mp5 of BD, Bangle, and BD+Bangle overlap (explained below)  

# Analysis
