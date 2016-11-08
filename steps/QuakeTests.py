from behave import *
import requests
from behave import *
import os
import QuakeAnalysis

starttime = None
endtime = None
count = None

@given('starttime is {stime}')
def step_impl(context, stime):
    global starttime
    starttime = stime

@step('endtime is {etime}')
def step_impl(context, etime):
    global endtime
    endtime = etime

@when('we fetch the earthquakes in that duration')
def step_impl(context):
    global starttime,endtime,count
    countURL = "http://earthquake.usgs.gov/fdsnws/event/1/count?starttime=%s&endtime=%s"
    countURL = countURL %(starttime, endtime)
    response = requests.get(countURL, data=None)
    count = int(response.text)

@then("we check if we have got the correct count")
def step_impl(context):
    global starttime,endtime,count
    quakes = QuakeAnalysis.getEarthquakeData(starttime,endtime)
    assert (count == len(quakes)) is True


@when("we plot the magnitudes of the earthquakes on a map")
def step_impl(context):
    global starttime,endtime
    quakeRawData = QuakeAnalysis.getEarthquakeData(starttime, endtime)
    quake_df = QuakeAnalysis.getQuakeDfFromData(quakeRawData)
    QuakeAnalysis.plotEarthquakesMagHM(quake_df)


@then("we check for a file created by the name {filename}")
def step_impl(context, filename):
    assert os.path.isfile(filename) is True