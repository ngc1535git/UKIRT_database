# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 16:59:45 2020

@author: ngc1535
"""
#returns contemporaneous TLEs given satellit ID and window of time surrounding time of observation

from spacetrack import SpaceTrackClient
import spacetrack.operators as op
import datetime as dt
import bisect



#account credentials at SpaceTrack.org
st = SpaceTrackClient('ngc1535@caelumobservatory.com','')


#(int,int,string(Y-m-d H:M:S)) fraction seconds are OK and stripped
def Bounding_TLEs(sat_ID,window,obs_date):
	
	closest_to_obs_date = 0
		
	print('Retrieving archived TLEs for satellite: {}'.format(sat_ID))
	
	epoch = [] #list of datetimes extracted from returned TLEs
	
	#drop any fractional seconds because strptime does not like them
	split_date = obs_date.split('.')
	obs_date = split_date[0]
	
	#convert the string for the date of observation to a datetime object
	obs_date = dt.datetime.strptime(obs_date, '%Y-%m-%d %H:%M:%S') 
	
	#add and subtract from this time to create a window
	left = obs_date - dt.timedelta(days=window)
	right = obs_date + dt.timedelta(days=window)
	
	#create a SpaceTrack object of range of dates (accepts datetime objects)
	drange = op.inclusive_range(left,right)
	
	#get the resulting text stream of 2 lines for each TLE and split it on the returns
	TLE_query_result = (st.tle(norad_cat_id=sat_ID, epoch = drange, orderby='epoch', limit=30, format='tle')).split('\n')
	if TLE_query_result[-1] == '':
		del TLE_query_result[-1]
		
	
	#trying again if necessary with expanded window
	if len(TLE_query_result) < 6:
		print('SpaceTrack returned less than 3 TLEs within the window.')
		print('Expanding the window of time to two weeks on either side of the requested time.')
		left = obs_date - dt.timedelta(days=15)
		right = obs_date + dt.timedelta(days=15)
		drange = op.inclusive_range(left,right)
		TLE_query_result = (st.tle(norad_cat_id=sat_ID, epoch = drange, orderby='epoch', limit=30, format='tle')).split('\n')
		if TLE_query_result[-1] == '':
			del TLE_query_result[-1]
		if len(TLE_query_result) < 2:
			print(len(TLE_query_result))
			print('No luck, expanding window of time did not help.')
	print(*TLE_query_result, sep = "\n")

	
	if len(TLE_query_result) > 0:	
		print('{:.0f} TLEs were found in the alotted time window.The epochs are below.'.format(len(TLE_query_result)/2))
		#go through the list looking at only the even lines. Note, the last even line is a return and should be ignored.
		for i in range(0,len(TLE_query_result)-1,2):
			line1 = TLE_query_result[i].split()
			year_part = line1[3][0]+line1[3][1]
			if int(year_part) > 56:
				year=('19'+ year_part)
			else:
				year=('20'+ year_part)
			fractional_day = dt.timedelta(float(line1[3][2:]))
			print( dt.datetime.strptime(year,'%Y')+fractional_day) #These are the dates
			epoch.append( dt.datetime.strptime(year,'%Y')+fractional_day)
		
		if len(TLE_query_result) == 2:
			prior_TLE = TLE_query_result
			post_TLE = TLE_query_result
			closest_to_obs_date = 0
			print ('There was only one TLE returned. Returning the same TLE for Prior and Post results.')
		else:
			if obs_date <= epoch[0]:  #obs is before all returned TLEs
				prior_TLE = TLE_query_result[0]+'\n'+TLE_query_result[1]
				post_TLE = "None\nNone"
				closest_to_obs_date = 0
				print('The observation {} took place before the first returned result. This first result is the best we can do.'.format(obs_date))
			elif obs_date >= epoch[-1]:  #obs is after all returned TLEs
				print("The observation {} took place after the last published TLE. This last published result is the best we can do.".format(obs_date))
				prior_TLE = "None\nNone"
				post_TLE = TLE_query_result[-2]+'\n'+TLE_query_result[-1]	
				closest_to_obs_date = 1
			else: #index is multiplied by 2 b/c only epochs (first lines) were extracted with respect to TLE_query_result
				found_index = bisect.bisect_left(epoch,obs_date) - 1 #this is the first entry less than the insertion position
				if abs((epoch[found_index] - obs_date).total_seconds()) <= abs((epoch[found_index +1] - obs_date).total_seconds()):
					print(abs((epoch[found_index] - obs_date).total_seconds()),abs((epoch[found_index +1] - obs_date).total_seconds()))
					closest_to_obs_date = 0
				else:
					closest_to_obs_date = 1
				prior_TLE_index = 2 * found_index
				print('Entry number {} in the list above was chosen as the time immediately prior to the observation at {}.'.format(found_index+1,obs_date))
				prior_TLE = TLE_query_result[prior_TLE_index]+'\n'+TLE_query_result[prior_TLE_index+1]
				post_TLE_index =prior_TLE_index + 2
				post_TLE = TLE_query_result[post_TLE_index]+'\n'+TLE_query_result[post_TLE_index+1]
		
	else:
		prior_TLE = "None\nNone"
		post_TLE =  "None\nNone"
		closest_to_obs_date = 0
		print('There were no published TLEs found. Returning None.')

	if closest_to_obs_date == 0 and not (prior_TLE == 'None\nNone' or post_TLE == 'None\nNone'):
		print('At {:.2f} hours  (compared to a difference of {:.2f} hours), the observation at {} is closest to {} in time. Thus the prior TLE will be used for calculations.'.format(abs((epoch[found_index] - obs_date).total_seconds())/3600,abs((epoch[found_index +1] - obs_date).total_seconds())/3600,obs_date,epoch[found_index]))
	elif closest_to_obs_date == 1 and not (prior_TLE == 'None\nNone' or post_TLE == 'None\nNone'):
		print('At {:.2f} hours  (compared to a difference of {:.2f} hours), the observation at {} is closest to {} in time. Thus the post TLE will be used for calculations.'.format(abs((epoch[found_index+1] - obs_date).total_seconds())/3600,abs((epoch[found_index] - obs_date).total_seconds())/3600,obs_date,epoch[found_index]))
		
	
	return  (prior_TLE,post_TLE,closest_to_obs_date)

#submitted_date = '2019-10-25 10:20:00'
#sat_ID = 36499
#window = 10
#prior_TLE,post_TLE = (Bounding_TLEs(sat_ID,window,submitted_date))
#print(prior_TLE)
#print('\n')
#print(post_TLE)