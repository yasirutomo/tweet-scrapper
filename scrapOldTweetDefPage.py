# Python 3.4
import urllib.request
from bs4 import BeautifulSoup
import re
import numpy as np

tglAwal = '2017-07-31'
tglAkhir = '2017-08-01'
querySearch = 'jokowi' #spasi = %20
location = 'Jakarta%20Pusat%2C%20DKI%20Jakarta' #spasi = %20, koma = %2C

url = 'https://twitter.com/search?l=&q=%23'+querySearch+'%20near%3A%22'+location+'%22%20within%3A15mi%20since%3A'+tglAwal+'%20until%3A'+tglAkhir+'&src=typd&lang=en'

req = urllib.request.Request(url)
resp = urllib.request.urlopen(req)
respData = resp.read()

# print(respData)

names = re.findall(r'<strong class="fullname show-popup-with-id " data-aria-label-part>(.*?)</strong>',str(respData))

usernames = re.findall(r'<span class="username u-dir" dir="ltr" data-aria-label-part>(.*?)</span>',str(respData))

paragraphs = re.findall(r'<p class="TweetTextSize  js-tweet-text tweet-text" lang="in" data-aria-label-part="0">(.*?)</p>',str(respData))

# print(paragraphs)

for eachP in range(len(paragraphs)):
	print()
	
	soupNames = BeautifulSoup(names[eachP],"html.parser")
	getNames = soupNames.get_text()

	soupUsernames = BeautifulSoup(usernames[eachP],"html.parser")
	getUsernames = soupUsernames.get_text()

	soupText = BeautifulSoup(paragraphs[eachP],"html.parser")
	getText = soupText.get_text()
	
	print(getNames)
	print(getUsernames)
	print(getText)

	form = '"'+getNames+'","'+getUsernames+'","'+getText+'","'+tglAwal+'-'+tglAkhir+'"'
	output = open('outputScrap.txt',"a") #tinggal ubah nanti jadi csv
	output.write(str(form))
	output.write('\n')
	output.close()