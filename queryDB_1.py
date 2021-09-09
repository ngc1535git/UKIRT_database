# databaseAccessExample.py
#
# Example access script for SQLite database
# 
# More resources:
# https://www.tutorialspoint.com/sqlite/sqlite_python.htm
# https://www.w3schools.com/sql/
# 



import sqlite3
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import datetime as dt



databaseFile = "D:\\UKRIT_2021\\Database\\ukirt_2021-09-07.db"
index = 0
magnitude,colors = [],[]
sat_name,norad=[],[]
jlist,klist,zlist,hlist,ylist = [],[],[],[],[] #temporary lists to hold magnitudes per satellite visit
jmean,kmean,zmean,hmean,ymean = [],[],[],[],[] #lists to hold mean values of magnitudes for each visit (from the lists above)
elongation_list,elongation_mean = [],[]        #elongation list and mean as the above
zminusy,yminusj,jminush,hminusk = [],[],[],[]  #plotted values/color indices
zyelong,yjelong,jhelong,hkelong = [],[],[],[]  #Since some mean values may be empty (no observations), a matching elongation list is made for each color index

#not currently used, but will perhaps be later
def Colorize(filterband):
	
	color = ''
	
	if filterband == 'Z':
		color = 'blue'
	elif filterband == 'Y':
		color = 'gold'
	elif filterband == 'J':
		color = '#66AABB'
	elif filterband == 'H':
		color = 'crimson'
	elif filterband == 'K':
		color = 'purple'

	return(color)


# Open database file (will create new one if not exist)
try:
	print("Opening database...")
	conn = sqlite3.connect(databaseFile)
except Exception as e:
	print("Failed!")
	print(e)
	exit()

print("Success!")


# Cursor for accessing the DB
cursor = conn.cursor()

# Print only norad_id, name from sats table only for HS-376 models
cursor.execute( "SELECT norad_id, name FROM sats WHERE type LIKE 'HS-376%';" )
for s in cursor:
	sat_name.append(s[1])
	norad.append(s[0])

for i in range(len(norad)):
	magnitude,phase_angle,colors = [],[],[]
	select_string_statement="""SELECT sats.norad_id, images.filter, images.start_time, targets.magnitude, targets.sun_elong_predicted
				FROM ((sats INNER JOIN targets ON sats.id = targets.target_id) INNER JOIN images ON targets.image_id = images.id)
				WHERE (sats.norad_id = """+str(norad[i])+"""
					  AND targets.rejected is NULL 
					  AND targets.inst_mag IS NOT NULL
					  )
				ORDER BY images.start_time;"""

	# Print select items from combination of sats and targets and images tables
	cursor.execute(select_string_statement)
	for s in cursor:
		if s[0] == 15308: #current just one satellite.will loop over more later if desired
			if index == 0: #initialize first time
				group_start_time = dt.datetime.strptime(s[2], '%Y-%m-%d %H:%M:%S.%f') 
			current_time = dt.datetime.strptime(s[2], '%Y-%m-%d %H:%M:%S.%f')
			timedifference = (current_time - group_start_time).total_seconds()
			if timedifference >= 0 and timedifference < 1800: #finding >= zero was subtle
				#make lists of magnitudes in each band
				if s[1] == "J":
					jlist.append(s[3])
				if s[1] == "H":
					hlist.append(s[3])
				if s[1] == "Y":
					ylist.append(s[3])
				if s[1] == "K":
					klist.append(s[3])
				if s[1] == "Z":
					zlist.append(s[3])
				elongation_list.append(s[4])  #also record elongation
			else:
				group_start_time = current_time  #reset the group start time so that there so no observations are missed
				#calculate mean values. If no values, append placeholder so all lists are the same length				
				if jlist:	
					jmean.append(np.median(np.array(jlist)))
				else:
					jmean.append([])
				if hlist:	
					hmean.append(np.median(np.array(hlist)))
				else:
					hmean.append([])
				if ylist:	
					ymean.append(np.median(np.array(ylist)))	
				else:
					ymean.append([])
				if klist:	
					kmean.append(np.median(np.array(klist)))
				else:
					kmean.append([])
				if zlist:	
					zmean.append(np.median(np.array(zlist)))
				else:
					zmean.append([])
				elongation_mean.append(np.median(np.array(elongation_list)))
					
				#reset temporary lists
				jlist,klist,zlist,hlist,ylist,elongation_list = [],[],[],[],[],[]
				
				#Regardless of condition, values are appended in each part of the IF/ELSE statement
				#These then are the first in the next grouping. There is probably a better way since this is in both. 
				if s[1] == "J":
					jlist.append(s[3])
				if s[1] == "H":
					hlist.append(s[3])
				if s[1] == "Y":
					ylist.append(s[3])
				if s[1] == "K":
					klist.append(s[3])
				if s[1] == "Z":
					zlist.append(s[3])
				elongation_list.append(s[4])  #also record elongation
			#for bookeeping... but used at the moment
			index=index+1
# the last bit of data after the last else statement (Enters if..but never gets to Else...so lists are not averaged)		
if jlist:	
	jmean.append(np.median(np.array(jlist)))
else:
	jmean.append([])
if hlist:	
	hmean.append(np.median(np.array(hlist)))
else:
	hmean.append([])
if ylist:	
	ymean.append(np.median(np.array(ylist)))	
else:
	ymean.append([])
if klist:	
	kmean.append(np.median(np.array(klist)))
else:
	kmean.append([])
if zlist:	
	zmean.append(np.median(np.array(zlist)))
else:
	zmean.append([])
elongation_mean.append(np.median(np.array(elongation_list)))
print('++++++++++++++++++++++++++++')
print('VISITS')
print(len(elongation_mean))
print('++++++++++++++++++++++++++++')

#creating the points to plot. Checks if no value in either filter (skips if so)Thus the matching of elongation
for i in range(len(elongation_mean)):
	if zmean[i] and ymean[i]:
		zminusy.append(zmean[i] - ymean[i])
		zyelong.append(elongation_mean[i])
	if ymean[i] and jmean[i]:
		yminusj.append(ymean[i] - jmean[i])
		yjelong.append(elongation_mean[i])
	if jmean[i] and hmean[i]:
		jminush.append(jmean[i] - hmean[i])
		jhelong.append(elongation_mean[i])
	if hmean[i] and kmean[i]:
		hminusk.append(hmean[i] - kmean[i])
		hkelong.append(elongation_mean[i])


fig, (ax1) = plt.subplots(figsize=(12,6))
fig.suptitle('Satellite 15308', size=25)
ax1.set_ylabel('Color Indices',size=20)
ax1.set_xlabel('Elongation (degrees)', size = 20)
ax1.grid(True)
ax1.scatter(zyelong,zminusy,color='blue',s = 4)
ax1.scatter(yjelong,yminusj,color='gold',s = 4)
ax1.scatter(jhelong,jminush,color='#66AABB',s = 4)
ax1.scatter(hkelong,hminusk,color='crimson',s = 4)
ax1.set_xlim([50,180])
ax1.set_ylim([-2, 2])
zy = mpatches.Patch(color='blue', label='Z-Y',linewidth=.5)
yj = mpatches.Patch(color='gold', label='Y-J',linewidth=.5)
jh= mpatches.Patch(color='#66AABB', label='J-H',linewidth=.5)
hk = mpatches.Patch(color='crimson', label='H-K',linewidth=.5)


plt.rcParams["legend.fontsize"] = 12
ax1.legend(handles=[zy,yj,jh,hk])
plt.savefig('D:\\UKRIT_2021\\xx_PLOTS_xx\\test.png')
plt.close('all')

# Commit changes to database and close
conn.commit()
conn.close()
