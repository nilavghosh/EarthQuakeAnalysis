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
    proplist.append(list(quakes[0].properties.keys()))
    for indx, quake in enumerate(quakes):
        proplist.append(list(quake.properties.values()))
    np_proplist = np.array(proplist).astype(np.str)
    df = pd.DataFrame(np_proplist[1:], columns=list(np_proplist[0]))
    df = df.set_index('time')
    df.index = pd.to_datetime(df.index, unit='ms')
    df_sorted = df.sort_index()
    return df_sorted

if __name__ == "__main__":
    if len(sys.argv)!= 3:
        print('Incorrect number of arguments. Enter starttime and endtime')
        exit(0)
    else:
        starttime = sys.argv[1]
        endtime = sys.argv[2]
        quakeRawData = getEarthquakeData(starttime,endtime)
        quake_df = getQuakeDfFromData(quakeRawData)










