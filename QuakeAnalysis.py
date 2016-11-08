import sys
import pandas as pd
import numpy as np
import requests
import geojson
import json
import pickle
from dateutil import rrule
from datetime import datetime, timedelta
import datetime as dt
import folium
from folium import plugins
import matplotlib
import matplotlib.pyplot as plt

BASE_URL = url = 'http://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=%s&endtime=%s'

def getEarthquakeData(starttime, endtime):
    earthQuakes = list()
    stime = datetime.strptime(starttime, '%Y-%m-%d')
    etime = datetime.strptime(endtime, '%Y-%m-%d')
    if((etime-stime).days > 31):
        months = list(rrule.rrule(rrule.MONTHLY, count=etime.month - stime.month, dtstart=dt.datetime(stime.year, stime.month + 1, 1, 0, 0)))
        url = BASE_URL % (stime, (months[0] - timedelta(days=1)).date())
        response = requests.get(url, data=None)
        data = geojson.loads(response.text)
        earthQuakes.extend(data.features)
        print('Fetched data from %s to %s' % (str(stime.date()), str((months[0] - timedelta(days=1)).date())))

        for i in range(len(months) - 1):
            date = months[i]
            url = BASE_URL % (str(date.date()) ,str((months[i + 1] - timedelta(days=1)).date()))
            response = requests.get(url, data=None)
            data = geojson.loads(response.text)
            earthQuakes.extend(data.features)
            print('Fetched data from %s to %s' % (str(date.date()), str((months[i + 1] - timedelta(days=1)).date())))
        url = BASE_URL % ((months[len(months)-1]).date(), etime)
        response = requests.get(url, data=None)
        data = geojson.loads(response.text)
        earthQuakes.extend(data.features)
        print('Fetched data from %s to %s' % (str((months[len(months)- 1]).date()), etime))
    else:
        url = BASE_URL % (starttime,endtime)
        response = requests.get(url, data=None)
        data = geojson.loads(response.text)
        earthQuakes.extend(data.features)
    return earthQuakes

def getQuakeDfFromData(quakes):
    proplist = list()
    keys = list(quakes[0].properties.keys())
    keys.append('long')
    keys.append('lat')
    proplist.append(keys)
    for indx, quake in enumerate(quakes):
        values = list(quake.properties.values())
        values.append(quake.geometry.coordinates[0])
        values.append(quake.geometry.coordinates[1])
        proplist.append(values)
    np_proplist = np.array(proplist).astype(np.str)
    df = pd.DataFrame(np_proplist[1:], columns=list(np_proplist[0]))
    df = df.set_index('time')
    df.index = pd.to_datetime(df.index, unit='ms')
    df = df.convert_objects(convert_numeric=True)
    df = df.fillna(0)
    df_sorted = df.sort_index()
    return df_sorted


def plotEarthquakesMagHM(df):
    # Using USGS style tile
    url_base = 'http://server.arcgisonline.com/ArcGIS/rest/services/'
    service = 'NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}'
    tileset = url_base + service

    map_1 = folium.Map(location=[37.8716, -122.2727], zoom_start=2, \
                       control_scale=True, tiles=tileset, attr='USGS style')

    lons = list()
    lats = list()
    mags = list()
    for indx, quake in df[0:50000].iterrows():
        Y = quake['long']
        X = quake['lat']
        mag = quake['mag']
        lons.append(Y)
        lats.append(X)
        mags.append(mag)

    # I am using the magnitude as the weight for the heatmap
    map_1.add_children(plugins.HeatMap(zip(lats, lons, mags), radius=10))
    map_1.save('mag_heatmap.html')

def plotEQCountByMonth(df):
    pdg = pd.groupby(df, by=[df.index.month, df.index.year])
    plot = pdg.count()[['code']].plot(kind='bar',legend=False, title="Count of Earthquakes by Month in 2016")
    plot.set(xlabel="Months", ylabel="No. of EarthQuakes")
    plt.show()

if __name__ == "__main__":
    if len(sys.argv)!= 3:
        print('Incorrect number of arguments. Enter starttime and endtime')
        exit(0)
    else:
        try:
            starttime = sys.argv[1]
            endtime = sys.argv[2]
            quakeRawData = getEarthquakeData(starttime,endtime)
            quake_df = getQuakeDfFromData(quakeRawData)
            plotEQCountByMonth(quake_df)

            # Interesting to see the "Ring of Fire" - https://en.wikipedia.org/wiki/Ring_of_Fire
            # Look for a file mag_heatmap.html created in the same directory and open it in chrome
            # plotEarthquakesMagHM(quake_df)
        except Exception as ex:
            print(ex)











