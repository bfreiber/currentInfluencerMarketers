################################ [3/3] APPEND LINK INFO TO LIST OF TWITCH STREAMERS ################################
from bs4 import BeautifulSoup
import requests
import datetime

#Current updates:
#[1] rankOrderSponsors -> time series
#[2] New sponsors (those that didn't exist in t-1 with >= 5 links now)
#[3] Email [DONE]

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
			lastNonEmpty = [i for i in row if i][-1]
			links = json.loads(lastNonEmpty).values()
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
	# (D) Save to 'currentMarketers.csv'
	# Read in marketer list #
	csvFileNameSave = 'currentMarketers.csv' 
	currentMarketers = readCSV(csvFileNameSave)
	# Desired output | ['twitter', 3, 'youtube', 4], []
	# Input | currentMarketers[1] = ['twitter', 3]
	#csvdataRows = headers + orderedLinkBaseCountList
	#Combine old and new
	# [0] Add date to orderedLinkBaseCountList #
	now = datetime.datetime.now()
	nowString = now.strftime("%Y-%m-%d %H:%M")
	orderedLinkBaseCountList = [[nowString, ""]] + orderedLinkBaseCountList
	# [1] Append rows until same length as necessary for new column addition #
	while (len(currentMarketers) < len(orderedLinkBaseCountList)):
		currentMarketers.append([])
	# [2] Find new position in row to start at #
	maximumLengthofRow = max([len(row) for row in currentMarketers])
	for row in currentMarketers:
		# [3] Add space until row = maximumLengthofRow #
		while (len(row) < maximumLengthofRow):
			row.append("")
	# [4] Add new elements to list #
	for i in range(len(orderedLinkBaseCountList)):
		currentMarketers[i] = currentMarketers[i] + orderedLinkBaseCountList[i]
	writeStreamersToCSV(csvFileNameSave, currentMarketers)
	return currentMarketers

def newSponsors(csvFileName):
	return

def sendEmail(fileToSend):
	import smtplib
	import mimetypes
	from email.mime.multipart import MIMEMultipart
	from email import encoders
	from email.message import Message
	from email.mime.audio import MIMEAudio
	from email.mime.base import MIMEBase
	from email.mime.image import MIMEImage
	from email.mime.text import MIMEText

	emailfrom = "Endorse team"
	emailto = "brandon@endorse.gg"
	fileToSend = fileToSend
	username = "endorseggteam@gmail.com"
	password = "endorseggteam$$"

	msg = MIMEMultipart()
	msg["From"] = emailfrom
	msg["To"] = emailto
	msg["Subject"] = "ENDORSE | Weekly Twitch influencer marketer update"
	msg.preamble = "See who's new in Twitch influencer marketing, and who's left the medium"

	ctype, encoding = mimetypes.guess_type(fileToSend)
	if ctype is None or encoding is not None:
	    ctype = "application/octet-stream"

	maintype, subtype = ctype.split("/", 1)

	if maintype == "text":
	    fp = open(fileToSend)
	    # Note: we should handle calculating the charset
	    attachment = MIMEText(fp.read(), _subtype=subtype)
	    fp.close()
	elif maintype == "image":
	    fp = open(fileToSend, "rb")
	    attachment = MIMEImage(fp.read(), _subtype=subtype)
	    fp.close()
	elif maintype == "audio":
	    fp = open(fileToSend, "rb")
	    attachment = MIMEAudio(fp.read(), _subtype=subtype)
	    fp.close()
	else:
	    fp = open(fileToSend, "rb")
	    attachment = MIMEBase(maintype, subtype)
	    attachment.set_payload(fp.read())
	    fp.close()
	    encoders.encode_base64(attachment)
	attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
	msg.attach(attachment)

	server = smtplib.SMTP("smtp.gmail.com:587")
	server.starttls()
	server.login(username,password)
	server.sendmail(emailfrom, emailto, msg.as_string())
	server.quit()
	return

################################ [B] RUN PROGRAM ################################
csvFileName = 'streamers.csv'
rankOrderSponsors(csvFileName)
csvFileName2 = 'currentMarketers.csv'
sendEmail(csvFileName2)