import unittest
import QuakeAnalysis
import requests
import pickle
import os


def fun(x):
    return x + 1

class QuakeTests(unittest.TestCase):

    def shortDescription(self):
        return "This UnitTest set is to run tests on the EarthQuake Analysis Dataset"

    def setUp(self):
        self.starttime = "2016-01-01"
        self.endtime = "2016-05-25"

    # To test whether the number of earthquakes in a timeframe is correct
    def testForCountOfEarthQuakesInATimeFrame(self):
        self.starttime = "2016-03-01"
        self.endtime = "2016-03-31"
        countURL = "http://earthquake.usgs.gov/fdsnws/event/1/count?starttime=%s&endtime=%s"
        countURL = countURL % (self.starttime, self.endtime)
        response = requests.get(countURL, data=None)
        count = int(response.text)
        quakes = QuakeAnalysis.getEarthquakeData(self.starttime, self.endtime)
        self.assertEqual(len(quakes), count)

    # To check whether the number of earthquakes in a geojson is all converted into a dataframe
    def testToCheckForCorrectNumberOfItemsInDataFrame(self):
        jan_earthquakes = pickle.load(open("..\earthquake_Jan2016.p", "rb"))
        count_list = len(jan_earthquakes)
        count_df = len(QuakeAnalysis.getQuakeDfFromData(jan_earthquakes))
        self.assertEqual(count_list, count_df)

    # To test whether a heatmap (magnitude of earthquakes) is generated from the dataframe
    def testToCheckCreationofHeatMap(self):
        jan_earthquakes = pickle.load(open("..\earthquake_Jan2016.p", "rb"))
        quake_df = QuakeAnalysis.getQuakeDfFromData(jan_earthquakes)
        QuakeAnalysis.plotEarthquakesMagHM(quake_df)
        filename = "mag_heatmap.html"
        self.assertEqual(os.path.isfile(filename), True)