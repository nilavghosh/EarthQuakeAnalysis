# Created by Nilav at 04-11-2016
Feature: Testing Earthquake Analysis
  # Enter feature description here

  Scenario: Check EarthQuake Count
    Given starttime is 2016-01-01
    And endtime is 2016-01-05
    When we fetch the earthquakes in that duration
    Then we check if we have got the correct count

  Scenario: Check if plotfile has been created for earthquake magnitudes
    Given starttime is 2016-01-01
    And endtime is 2016-01-20
    When we plot the magnitudes of the earthquakes on a map
    Then we check for a file created by the name mag_heatmap.html