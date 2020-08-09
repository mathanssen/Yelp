import custom_func as cf
import numpy as np
from sklearn.cluster import DBSCAN
import pandas as pd
import re

path_references = '..\\references\\'
list_businesses = cf.load_obj('businesses_updated', path_references)

# Convert list to dataframe
for i in range(0, len(list_businesses)):
    for j in range(0, 7):
        if 'schedule' in list_businesses[i]:
            weekday = list_businesses[i]['schedule']['day'][j]
            time = list_businesses[i]['schedule']['time'][j]
            df_row = pd.json_normalize(list_businesses[i])
            df_row['weekday'] = weekday
            df_row['time'] = time
            try:
                df_businesses = pd.concat([df_businesses, df_row], sort=False)
            except NameError:
                df_businesses = df_row
df_businesses.reset_index(drop=True, inplace=True)

# Create schedule columns
c1 = df_businesses['time'] != 'Closed'
c2 = df_businesses.time.notnull()
df_businesses = df_businesses[c1 & c2]
chars = ['-', ' ', 'Normally']
df_businesses = df_businesses.assign(time_opened = '', time_closed = '', 
                                     time_opened2 = '', time_closed2 = '') 
df_businesses.reset_index(drop=True, inplace=True)
for i in range(0, len(df_businesses)):
    s = df_businesses['time'][i]
    if s == 'Open 24 hours':
        df_businesses['time'][i] = '12:00 am - 11:59 pm'
    for c in chars:
        df_businesses['time'][i] = df_businesses['time'][i].replace(c, '')
    sep = 'm'
    list_time = [t + sep for t in re.split(sep, df_businesses['time'][i])]
    if len(list_time) >= 5:
        df_businesses['time_opened'][i] = list_time[0]
        df_businesses['time_closed'][i] = list_time[1]
        df_businesses['time_opened2'][i] = list_time[2]
        df_businesses['time_closed2'][i] = list_time[3]
    else:
        df_businesses['time_opened'][i] = list_time[0]
        df_businesses['time_closed'][i] = list_time[1]
        df_businesses['time_opened2'][i] = list_time[0]
        df_businesses['time_closed2'][i] = list_time[1]

for col in ['time_opened', 'time_opened2', 'time_closed', 'time_closed2']:
    df_businesses[col] = pd.to_datetime(df_businesses[col],format='%I:%M%p')

# Clusterization of the coordinates
coords = df_businesses[['coordinates.latitude', 'coordinates.longitude']].values
kms_per_radian = 6371.0088
epsilon = 0.1 / kms_per_radian
db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
cluster_labels = db.labels_
df_businesses['region'] = cluster_labels.tolist()
