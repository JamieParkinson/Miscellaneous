#!/usr/bin/env python

from bs4 import BeautifulSoup
import urllib2
import os

wiki = "http://en.wikipedia.org/wiki/List_of_Peep_Show_episodes"
header = {'User-Agent': 'Mozilla/5.0'}
req = urllib2.Request(wiki, headers=header)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page)

allSeries = soup.find_all("table", class_="wikitable plainrowheaders")
seriesNumber = 1

for series in allSeries: # Loop series
	episodes = series.find_all("tr", class_="vevent")
	episodeNumber = 1

	# Get this series' episodes
	os.chdir('./Season ' + str(seriesNumber))
	episodeFiles = os.listdir('.')

	print("Series " + str(seriesNumber))

	for episode in episodes: # Loop episodes in series

		# If there's a ref in the cell, remove it
		if episode.td.sup:
			episode.td.sup.extract()

		# Extract name and strip double quotes
		epName = episode.td.string[1:-1]

		# Match filename, check to see if already numbered
		try:
			thisEpFilename = [f for f in episodeFiles if epName.lower() in f.lower()][0]
		except IndexError:
			pass
		if thisEpFilename[0].isdigit(): continue

		# Perform the rename
		os.rename(thisEpFilename, str(episodeNumber).zfill(2) + '_' + thisEpFilename)
		print(str(episodeNumber).zfill(2) + '_' + thisEpFilename)

		episodeNumber += 1

	seriesNumber += 1
	os.chdir('..')
		








