from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import datetime

class wait_for_more_than_n_elements_to_be_present(object):
    def __init__(self, locator, count):
        self.locator = locator
        self.count = count

    def __call__(self, driver):
        try:
            elements = EC._find_elements(driver, self.locator)
            return len(elements) > self.count
        except StaleElementReferenceException:
            return False

def unicodeNormalize(text):
    text = "".join([x for x in text if ord(x)<128])
    return text

def htmlCleaner(data):
    soupData = BeautifulSoup(data,"html.parser")
    getData = soupData.get_text()
    getData = unicodeNormalize(getData.encode("utf-8"))
    return getData

def defNomarlization(text):
    text = text.replace("\"", "<quote>")
    return text

## S: inisialisasi search
queryAkun = 'IDalamatcom' #usernamenya saja (tdak pake @)
tglAwal = '2012-04-24' #tahun-bulan-tanggal
tglAkhir = '2017-04-26'
hitLoadMoreLimit = 1 #berapa kali loadmore di hit
## E: inisialisasi search

## S: pemilihan query pencarian
# filter: user saja (halaman profilnya)
# url = 'https://twitter.com/'+queryAkun
# filter: user, tanggal
url = 'https://twitter.com/search?l=&q=from%3A'+queryAkun+'%20since%3A'+tglAwal+'%20until%3A'+tglAkhir+'&src=typd&lang=en'
## E: pemilihan query pencarian

## S: inisialisasi driver browser
# driver download: seleniumhq.org/download
driver = webdriver.Firefox("E:\\Python\\python27\\zgeopredict\\scrapping\\")
driver.get(url)
## E: inisialisasi driver browser

## S: hit the load more
# initial wait for the tweets to load
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[data-item-id]")))

# scroll down to the last tweet until there is no more tweets loaded
i = 1
while True:
    tweets = driver.find_elements_by_css_selector("li[data-item-id]")
    number_of_tweets = len(tweets)

    driver.execute_script("arguments[0].scrollIntoView();", tweets[-1])

    try:
        wait.until(wait_for_more_than_n_elements_to_be_present((By.CSS_SELECTOR, "li[data-item-id]"), number_of_tweets))
    except TimeoutException:
        break

    if (i==hitLoadMoreLimit):
        break
    i+=1
## E: hit the load more

## S: result
page_source = driver.page_source
driver.close()
respData = page_source.encode("utf-8")
## E: result

## S: parsing result
# print respData.encode("utf-8")
idtweet = re.findall(r'data-tweet-id="(.*?)" data-item-id',str(respData))
names = re.findall(r'<strong class="fullname show-popup-with-id " data-aria-label-part="">(.*?)</strong>',str(respData))
usernames = re.findall(r'<span class="username u-dir" dir="ltr" data-aria-label-part="">(.*?)</span>',str(respData))
paragraphs = re.findall(r'js-tweet-text tweet-text" data-aria-label-part="0" lang=".\S">(.*?)</p>',str(respData))
timestamp = re.findall(r'data-aria-label-part="last" data-time="(.*?)" data-time-ms',str(respData))

for eachP in range(len(paragraphs)):
    print ""

    getIdTweet = htmlCleaner(idtweet[eachP])
    getNames = htmlCleaner(names[eachP])
    getUsernames = htmlCleaner(usernames[eachP])
    getText = defNomarlization(htmlCleaner(paragraphs[eachP]))
    getTimeStamp = htmlCleaner(timestamp[eachP])
    getTimeStampDate = datetime.datetime.fromtimestamp(int(getTimeStamp)).strftime('%m/%d/%Y')
    getTimeStampHour = datetime.datetime.fromtimestamp(int(getTimeStamp)).strftime('%H:%M:%S')
    
    print getIdTweet
    print getNames
    print getUsernames
    print getText
    print getTimeStampDate
    print getTimeStampHour

    form = '"'+getIdTweet+'","'+getNames+'","'+getUsernames+'","'+getText+'","'+getTimeStampDate+'","'+getTimeStampHour+'"'
    output = open('outputScrap.txt',"a") #tinggal ubah nanti jadi csv
    output.write(str(form))
    output.write('\n')
    output.close()
## E: parsing result