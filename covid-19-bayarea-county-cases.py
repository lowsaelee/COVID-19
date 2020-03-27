# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 20:29:41 2020

Covid-19 Bay Area Cases Map

@author: Low
"""

import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values
import folium # map rendering library
from folium.features import DivIcon

import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 3000)
pd.set_option('display.max_colwidth', 4000)
pd.set_option('display.width', 4000)

file = "csse_covid_19_data/csse_covid_19_daily_reports/03-26-2020.csv"

df = pd.read_csv(file)


counties = ['Alameda',
            'Contra Costa',
            'Fresno',
            'Marin',
            'Merced',
            'Napa',
            'Sacramento',
            'Sonoma',
            'Solano',
            'Santa Clara',
            'Santa Cruz',
            'San Francisco',
            'San Mateo',
            'San Joaquin',
            'Shasta',
            'Stanislaus',
            'Yolo']


"""
counties = ['New York City',
            'Westchester',
            'Nassau',
            'Suffolk',
            'Rockland',
            'Orange',
            'Albany',
            'Dutchess']
"""

df_bay = df[df['Province_State'] == 'California']
#df_bay = df[df['Province_State'] == 'New York']
df_bay = df_bay[df_bay['Admin2'].isin(counties)]

print(df_bay)

address = 'Oakland, California'
#address = 'New York, New York'

geolocator = Nominatim(user_agent="ny_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of {} are {}, {}.'.format(address, latitude, longitude))



# create map and display it
bayarea_map = folium.Map(location=[latitude, longitude], zoom_start=8)

for i in range(len(df_bay)):
    county_name = str(df_bay['Admin2'].iloc[i])
    county_confirmed = str(df_bay['Confirmed'].iloc[i])
    county_death = str(df_bay['Deaths'].iloc[i])
    county_data = '<div style="font-size: 8pt; font-color: #fff"><b>' + county_name + '</b><br /> ' + county_confirmed + '</div>'
    folium.Marker(
        [df_bay['Lat'].iloc[i], df_bay['Long_'].iloc[i]],
        #popup=county_data
        icon=DivIcon(
        icon_size=(150,36),
        icon_anchor=(0,0),
        html=county_data,
        )
    ).add_to(bayarea_map)

bayarea_map.choropleth(
    geo_data="california_cb_2014_us_county_5m.json",
    data=df_bay,
    columns=['Admin2', 'Confirmed'],
    key_on='feature.properties.NAME',
    #fill_color='YlOrRd',
    fill_color='Reds',
    fill_opacity=1, 
    line_opacity=0.5,
    legend_name='COVID-19 Cases as of 3/26/2020'
)

df_bay.sort_values(by=['Confirmed'],inplace=True)
plt.bar(df_bay['Admin2'], df_bay['Confirmed'], color='green')
plt.xticks(rotation='vertical')
plt.show()

# display the map of San Francisco
bayarea_map.save("mymap.html")