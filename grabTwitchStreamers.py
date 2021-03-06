################################ [1/3] UPDATE LIST OF TWITCH STREAMERS ################################
# File 1: Create a file of twitchNames/languages/etc. | grabTwitchStreamers.py #
# File 2: Append link information to streamers | grabLinks.py #
# File 3: Update list of sponsors, find any "new" items, email  csv file | updateMarketers.py #

from bs4 import BeautifulSoup
import requests

################################ [A] DEFINE FUNCTIONS ################################
def readCSV(csvFileName):
	import csv
	csvdataRows = []
	with open(csvFileName, 'rb') as csvfile:
		spamreader = csv.reader(csvfile)
		#for line in data:
		for row in spamreader:
			csvdataRows.append(row)
	## Return rows #
	return csvdataRows

def writeStreamersToCSV(csvFileName, csvdataRows):
	import csv
	with open(csvFileName, 'wb') as csvfile:
		spamwriter = csv.writer(csvfile)
		for row in csvdataRows:
			try:
				spamwriter.writerow(row)
			except:
				print 'There was an error with the following row:'
				print row
	return

def grabTwitchStreamers(minimumFollowers, csvFileName):
	import requests
	streamers = []
	#minimumFollowers = 10000
	minimumFollowers = int(minimumFollowers)
	count = 0
	url = 'https://api.twitch.tv/kraken/streams?client_id=nrisqw9diqmthnvxx1rknb3wxzhwm2k&limit=100'
	r = requests.get(url)
	jsonObject = r.json()
	for stream in jsonObject['streams']:
		if (stream['channel']['followers'] > minimumFollowers) and (stream['channel']['language'] == 'en'):
			streamers.append(stream)
	print len(streamers)
	for i in range(25):
		offset = str((i+1)*100)
		url = 'https://api.twitch.tv/kraken/streams?limit=100&offset=%s&stream_type=live&client_id=nrisqw9diqmthnvxx1rknb3wxzhwm2k&limit=100' % offset
		r = requests.get(url)
		jsonObject = r.json()
		for stream in jsonObject['streams']:
			if (stream['channel']['followers'] > minimumFollowers):
				streamers.append(stream)
		print len(streamers)
	# Read in CSV, append new streamers, update? existing streamers #
	#csvFileName = 'streamers.csv'
	csvdataRows = readCSV(csvFileName)

	for streamer in streamers:
		twitchNamesinCSV = [row[0] for row in csvdataRows]
		# For streamers in CSV, update #
		if streamer['channel']['name'] in twitchNamesinCSV:
			# Find index of twitchName #
			streamerIndex = twitchNamesinCSV.index(streamer['channel']['name'])
			# Update #
			csvdataRows[streamerIndex][1] = str(streamer['channel']['language']).encode("utf-8")
			csvdataRows[streamerIndex][2] = streamer['channel']['followers']
			csvdataRows[streamerIndex][3] = streamer['channel']['views']
			csvdataRows[streamerIndex][5] = streamer['channel']['mature']
			csvdataRows[streamerIndex][6] = streamer['channel']['partner']
			csvdataRows[streamerIndex][7] = str(streamer['channel']['logo']).encode("utf-8")
			try:
				csvdataRows[streamerIndex][8] = str(streamer['channel']['game']).encode("utf-8")
			except:
				print 'Error with twitch game name - ascii'
		# For streamers not in CSV, append #
		else:
			try:
				csvdataRows.append([streamer['channel']['name'].encode("utf-8"), str(streamer['channel']['language']).encode("utf-8"), streamer['channel']['followers'], streamer['channel']['views'], streamer['channel']['created_at'].encode("utf-8"), streamer['channel']['mature'], streamer['channel']['partner'], str(streamer['channel']['logo']).encode("utf-8"), str(streamer['channel']['game']).encode("utf-8"), '', '', '', '', '', '', '', '', '', '', '', ''])
			except:
				try:
					csvdataRows.append([streamer['channel']['name'], str(streamer['channel']['language']), streamer['channel']['followers'], streamer['channel']['views'], streamer['channel']['created_at'], streamer['channel']['mature'], streamer['channel']['partner'], str(streamer['channel']['logo']), str(streamer['channel']['game']), '', '', '', '', '', '', '', '', '', '', '', ''])
				except:
					print 'Error'
	# Write out CSV #
	#csvFileName = 'streamers.csv'
	writeStreamersToCSV(csvFileName, csvdataRows)

	return csvdataRows, streamers

def transferStreamerInformation(csvFileNamePRE, csvFileNamePOST):
	# Read in CSV files #
	csvdataRowsPRE = readCSV(csvFileNamePRE)
	csvdataRowsPOST = readCSV(csvFileNamePOST)
	# Add new streamers to csvdataRowsPOST #
	#twitchNamesinCSVPRE = [row[0] for row in csvdataRowsPRE[1:]]
	twitchNamesinCSVPOST = [row[0] for row in csvdataRowsPOST[1:]]
	for row in csvdataRowsPRE[1:]:
		if (row[0] not in twitchNamesinCSVPOST):
			csvdataRowsPOST.append([row[0], row[1], row[2]])
	# Write out #
	writeStreamersToCSV(csvFileNamePOST, csvdataRowsPOST)
	return csvdataRowsPOST

################################ [B] RUN PROGRAM ################################
minimumFollowers = 10000
csvFileName = 'currentInfluencerMarketers/streamersPRE.csv'
grabTwitchStreamers(minimumFollowers, csvFileName)
transferStreamerInformation('currentInfluencerMarketers/streamersPRE.csv', 'currentInfluencerMarketers/streamers.csv')
