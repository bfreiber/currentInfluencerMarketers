from bs4 import BeautifulSoup
import requests

## Step 1 - Read in list of 3200 streamers, filter for channels in 'en' ##
## Step 2 - For each Twitch streamer, grab all links on editable section of page (find all real ultimate links), save to excel ##
## Step 4 - (A) Shorten all links to core url and (B) rank order top sponsors in new Excel #

#from twitchInfluencerMarketers import readCSV, writeStreamersToCSV, grabTwitchStreamers, twingeCSV, streamLabs, writeMarketersToCSV
#grabTwitchStreamers(1000)
#twingeCSV(500, 'all')
#streamLabs(500, 'all')
#csvdataRows = multipleFreeContactInformations(50000, 'all')

## Step 0: Define readCSV and writeToCSV (functions to be used in multiple/all following steps) ##
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

def writeMarketersToCSV(csvFileName, csvdataRows):
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

def getTwitchLinks(twitchName):
	#class = qa-panels-container ember-view
	import urllib
	import time
	from time import sleep
	from selenium import webdriver
	from selenium.common.exceptions import NoSuchElementException
	from selenium.webdriver.common.keys import Keys
	from random import randint
	import os
	import random
	from selenium.webdriver.common.by import By
	from selenium.webdriver.support.ui import WebDriverWait
	from selenium.webdriver.support import expected_conditions as EC
	import requests
	from bs4 import BeautifulSoup

	def human_type(element, text):
	    for char in str(text):
	        #time.sleep(random.randint(1,5)) #fixed a . instead of a ,
	        time.sleep(random.uniform(0, 1))
	        element.send_keys(char)
	def miniSleep():
		sleep(random.uniform(0, 1))
		return

	def getFinalLink(link):
		linkShorteners = ['kappa.ly', 'bit.ly', 'bitly.com', 'goo.gl', 'owl.ly', 'deck.ly', 'su.pr', 'lnk.co', 'fur.ly', 'moourl.com', 't.co', 'geni.us', 'soy.lt', 'amzn.to', 'ubi.li', 'dro.ps', 'avantlink.com']
		# If a no link shortener exists, return link without selenium #
		if (any(ext in link.lower() for ext in linkShorteners) == False):
			return link
		# Otherwise, if link shorterner exists, final ultimate link #
		else:
			def miniSleep():
				sleep(random.uniform(0, 1))
				return
			url = link
			chromedriver = "/Users/brandonfreiberg/python-projects/chromedriver"
			os.environ["webdriver.chrome.driver"] = chromedriver
			driver = webdriver.Chrome(chromedriver)
			miniSleep()
			driver.get(url)
			sleep(randint(3,6))#1-5 seconds
			finalURL = driver.current_url
			driver.quit()
			return finalURL

	url = 'https://twitch.tv/%s/' % (twitchName)
	chromedriver = "/Users/brandonfreiberg/python-projects/chromedriver"
	os.environ["webdriver.chrome.driver"] = chromedriver
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--mute-audio")
	driver = webdriver.Chrome(chromedriver, chrome_options=chrome_options)
	miniSleep()
	driver.set_window_size(1150, 880)
	miniSleep()
	driver.get(url)
	sleep(randint(3,6))#1-5 seconds

	## Grab panels ##
	linkDictionary = {}
	try:
		#twitchLinks = []
		#panels = driver.find_element_by_css_selector('.qa-panels-container.ember-view')
		panels = driver.find_element_by_css_selector('.channel-panels-container')
		soup = BeautifulSoup(panels.get_attribute('innerHTML'))
		driver.quit()
		allLinks = soup.find_all("a")#, {"class":"channelGrowth__increase ng-binding"})[2].text.replace(',','').replace(' ','')
		#linkKeywordsNotToCheck = ['twitch', 'amazon', 'facebook', 'youtube', 'twitter', 'instagram', 'twitchalerts', 'paypal', 'imgur', 'streamlabs', 'patreon', 'amzn']
		#for link in allLinks:
		#	actualLink = link['href']
		#	if (any(ext in actualLink.lower() for ext in linkKeywordsNotToCheck) == False):
		#		twitchLinks.append(getFinalLink(actualLink))
		for link in allLinks:
			actualLink = link['href']
			linkDictionary[actualLink] = getFinalLink(actualLink)
	except:
		print 'Error regarding grabbing panels'

	#End function getTwitchLinks
	return linkDictionary

#### HOW TO RUN ####
#from twitchInfluencerMarketers import readCSV, writeStreamersToCSV, getTwitchLinks, twitchStreamersLinksExcel, writeMarketersToCSV,rankOrderSponsors
#csvFileName = 'streamers.csv'
#twitchStreamersLinksExcel(csvFileName)
#rankOrderSponsors(csvFileName)
def twitchStreamersLinksExcel(csvFileName):
	import json
	# (A) Read in file #
	csvdataRows = readCSV(csvFileName)
	# (B) Get data #
	count = 0
	for row in csvdataRows[1:]:
		twitchName = row[0]
		# If language is english and sponsor links is blank #
		if (row[1] == 'en') and (row[3] == ''):
			print twitchName, str(count)
			twitchLinks = getTwitchLinks(twitchName)
			row[3] = json.dumps(twitchLinks)
			count += 1
		# Save every 10 rows #
		if ((count % 10) == 0):
			writeStreamersToCSV(csvFileName, csvdataRows)
	# (C) Write to csv #
	writeStreamersToCSV(csvFileName, csvdataRows)
	return "Saved " + str(count) + " streamers to csv"

def rankOrderSponsors(csvFileName):
	import re
	import json
	# (0) Shorten link to base #
	def linkBase(link):
		from urlparse import urlparse
		try:
			url = urlparse(link)[1]
			url = url.replace('www.','')
			return url
		except:
			return ''
	# (A) Read in file #
	csvdataRows = readCSV(csvFileName)
	# (B) Analyze #
	linkBaseCount = {}
	for row in csvdataRows[1:]:
		#links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', json.loads(row[3]).values())
		try:
			links = json.loads(row[3]).values()
		except:
			links = []
		# Make unique - each link base per influencer should only count as 1 #
		linkBases = [linkBase(link) for link in links]
		uniqueLinkBases = list(set(linkBases))
		# count for 
		for uniqueLinkBase in uniqueLinkBases:
			if uniqueLinkBase not in linkBaseCount.keys():
				linkBaseCount[uniqueLinkBase] = 1
			else:
				linkBaseCount[uniqueLinkBase] += 1
	# (C) Order the unordered dictionary #
	orderedLinkBaseCount = list(reversed(sorted(linkBaseCount.iteritems(), key=lambda (k,v): (v,k))))
	orderedLinkBaseCountList = [[orderedLinkBaseCount[i][0],orderedLinkBaseCount[i][1]] for i in range(len(orderedLinkBaseCount))]
	# (D) Save to 'currentMarkters.csv'
	headers = [['Sponsors', 'Number of influencers sponsored']]
	csvdataRows = headers + orderedLinkBaseCountList
	csvFileNameSave = 'currentMarketers.csv'
	writeStreamersToCSV(csvFileNameSave, csvdataRows)
	return csvdataRows