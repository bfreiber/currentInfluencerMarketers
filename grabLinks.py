################################ [2/3] APPEND LINK INFO TO LIST OF TWITCH STREAMERS ################################
from bs4 import BeautifulSoup
import requests
import subprocess
import os
import signal
# TO DO - import os -> os.system('sudo reboot') + password?
# [1] Find all processes: ps aux --sort -rss
# [2] Kill all that have 'chrome' in the 'command' (at least 4 by my count) - https://stackoverflow.com/questions/14209064/python-sort-string-array-with-subtring
# [3] Does it work again?

################################ UNDER WORK ################################
"""import subprocess
ps = subprocess.Popen(['ps', 'aux', '--sort', '-rss'], stdout=subprocess.PIPE).communicate()[0]
processes = ps.split('\n')
processesSplit = [processesRow.split() for processesRow in processes[1:]]

import os
import signal
for process in processesSplit:
	if (('-nolisten' in process) and ('-screen' in process)):
		os.kill(int(process[1]), signal.SIGTERM)"""

################################ [A] DEFINE FUNCTIONS ################################

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
	# FOR DIGITAL OCEAN: #
	from pyvirtualdisplay import Display
	from selenium import webdriver 

	def human_type(element, text):
		for char in str(text):
			time.sleep(random.uniform(0, 1))
			element.send_keys(char)
		return

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
			#### LOCAL ####
			#chromedriver = "/Users/brandonfreiberg/python-projects/chromedriver"
			#os.environ["webdriver.chrome.driver"] = chromedriver
			#driver = webdriver.Chrome(chromedriver)
			#### DIGITAL OCEAN ####
			display = Display(visible=0, size=(800, 600))
			display.start()
			driver = webdriver.Chrome()
			miniSleep()
			driver.get(url)
			sleep(randint(3,6))#1-5 seconds
			finalURL = driver.current_url
			driver.quit()
			return finalURL

	def unshorten_url(url):
		return requests.head(url, allow_redirects=True).url

	## Kill all open chrome browser instances ##
	ps = subprocess.Popen(['ps', 'aux', '--sort', '-rss'], stdout=subprocess.PIPE).communicate()[0]
	processes = ps.split('\n')
	processesSplit = [processesRow.split() for processesRow in processes[1:]]
	for process in processesSplit:
		if (('-nolisten' in process) and ('-screen' in process)):
			os.kill(int(process[1]), signal.SIGTERM)

	#### LOCAL ####
	url = 'https://twitch.tv/%s/' % (twitchName)
	#chromedriver = "/Users/brandonfreiberg/python-projects/chromedriver"
	#os.environ["webdriver.chrome.driver"] = chromedriver
	#chrome_options = webdriver.ChromeOptions()
	#chrome_options.add_argument("--mute-audio")
	#driver = webdriver.Chrome(chromedriver, chrome_options=chrome_options)
	#miniSleep()
	#driver.set_window_size(1150, 880)
	#miniSleep()
	#driver.get(url)
	#sleep(randint(3,6))#1-5 seconds
	#### DIGITAL OCEAN ####
	display = Display(visible=0, size=(800, 600))
	display.start()
	driver = webdriver.Chrome()
	try:
		driver.get(url)
		sleep(randint(3,6))
		print driver.title
	except:
		driver.quit()
		print 'Error getting url'

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
		driver.quit()
		for link in allLinks:
			actualLink = link['href']
			try:
				linkDictionary[actualLink] = unshorten_url(actualLink)
			except:
				try:
					linkDictionary[actualLink] = getFinalLink(actualLink)
				except:
					print actualLink

	except:
		driver.quit()
		print 'Error regarding grabbing panels'

	#End function getTwitchLinks
	return linkDictionary

#### HOW TO RUN ####

def twitchStreamersLinksExcel(csvFileName):
	import json
	# (A) Read in file #
	csvdataRows = readCSV(csvFileName)
	maximumLengthofRow = max([len(row) for row in csvdataRows[1:]])
	# (B) Get data #
	count = 0
	# If all len of all rows are equal, do first row first #
	if len(set([len(row) for row in csvdataRows[1:]])) == 1:
		twitchName = csvdataRows[1][0]
		print twitchName, str(count)
		twitchLinks = getTwitchLinks(twitchName)
		csvdataRows[1].append(json.dumps(twitchLinks))
		writeStreamersToCSV(csvFileName, csvdataRows)
	for row in csvdataRows[1:]:
		twitchName = row[0]
		# Go through current cycle for all names first, before looping around to beginning again #
		print len(row)
		if (row[1] == 'en') and ((len(row) < maximumLengthofRow) or (row[len(row)-1] == '')):
			print twitchName, str(count)
			twitchLinks = getTwitchLinks(twitchName)
			row.append(json.dumps(twitchLinks))
			count += 1
		# Save every 10 rows #
		if ((count % 10) == 0):
			writeStreamersToCSV(csvFileName, csvdataRows)
	# (C) Write to csv #
	writeStreamersToCSV(csvFileName, csvdataRows)
	return "Saved " + str(count) + " streamers to csv"

################################ [B] RUN PROGRAM ################################

csvFileName = 'currentInfluencerMarketers/streamers.csv'
twitchStreamersLinksExcel(csvFileName)