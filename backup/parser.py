# encoding=utf8
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import feedparser
import pandas as pd
import os
from lxml import etree
import urllib2
import time
from datetime import datetime, timedelta
import datetime as dt
from langdetect import detect

#Csv read
path = raw_input('Path for the feed file without user: ')
filename = raw_input('Type file name for the feed file: ')
if ".csv" not in filename:
    filename = filename + ".csv"

iterations = raw_input('How many iterations: ')
waiting = raw_input('Set waiting time between iterations in seconds: ')


userhome = os.path.expanduser('~')
path= os.path.join(userhome, path, filename)
open(path, "r")

feeds = pd.read_csv(path, sep=";",encoding="UTF-8-sig")

list = []
x = 0
y = 0
for i in range(int(iterations)):

    for ind in feeds.index:
        start = time.time()
        link = feeds.loc[ind,"feeds"]

        print link

        try:
            if "xml" in link:
                #XML
                headers = { 'User-Agent' : 'Mozilla/5.0' }
                req = urllib2.Request(link, None, headers)
                feed_file = urllib2.urlopen(req).read()

                feed = etree.fromstring(feed_file)

                for item in feed.xpath('/rss/channel/item'):

                    article_title = item.xpath("./title/text()")[0]
                    article_link = item.xpath("./link/text()")[0]
                    article_summary = item.xpath("./description/text()")[0]
                    article_published_at_parsed = item.xpath("./pubDate/text()")[0]
                    list.append({'title' : "{}".format(article_title.encode("utf-8")) , 'link' : "{}".format(article_link.encode("utf-8")), 'summary' : "{}".format(article_summary).encode("utf-8"), 'published': "{}".format(article_published_at.encode("utf-8"))})




            else:
                feed = feedparser.parse(link)

                feed_title = feed['feed']['title']
                feed_entries = feed.entries

                for entry in feed.entries:

                    article_title = entry.title
                    article_link = entry.link
                    article_summary = entry.summary
                    article_published_at = entry.published # Unicode string
                    article_published_at_parsed = entry.published_parsed # Time object
                    list.append({'title' : "{}".format(article_title.encode("utf-8")) , 'link' : "{}".format(article_link.encode("utf-8")), 'summary' : "{}".format(article_summary).encode("utf-8"), 'published': "{}".format(article_published_at.encode("utf-8"))})


        except:
            print link, "Cannot get feed"
            pass

        df = pd.DataFrame(list,columns=["title","link","summary","published"])
        end = time.time()
        print "Request completed in: ", round(end-start,2), "s"

    df = df.drop_duplicates("title")
    dflen = len(df)
    print "Amount of news:", dflen
    x=x+1
    print "Iteration", x



    if x < int(iterations):
        time.sleep(int(waiting))

summaries = pd.DataFrame(index=df.index, columns=["summary"])

for ind in df.index:
    s = df.loc[ind,"summary"]
    s = re.sub(r'<.+?>', '', s)
    s = re.sub(r'(?:&#.+?;)', ' ', s)
    summaries.loc[ind] = s

df = df.drop(columns=['summary'])
frames = [df, summaries]

df = pd.concat(frames, axis=1)

lvl = pd.DataFrame(index=df.index, columns=["published"])

for ind in df.index:

    time = df.loc[ind,"published"]

    if isinstance(time, dt.datetime) == True:

        lvl.loc[ind] = time

    elif time[:1]=="2":
        time = time[:19]
        time = time.replace('T', ' ')
        lvl.loc[ind] = time


    elif "+" in time:
        if time[-1].isdigit() == True:
            time = time[4:]
            if "Jan" in time:
                time = time.replace('Jan', '-1-')
            elif "Feb" in time:
                time = time.replace('Feb', '-2-')
            elif "Mar" in time:
                time = time.replace('Mar', '-3-')
            elif "Apr" in time:
                time = time.replace('Apr', '-4-')
            elif "May" in time:
                time = time.replace('May', '-5-')
            elif "Jun" in time:
                time = time.replace('Jun', '-6-')
            elif "Jul" in time:
                time = time.replace('Jul', '-7-')
            elif "Aug" in time:
                time = time.replace('Aug', '-8-')
            elif "Sep" in time:
                time = time.replace('Sep', '-9-')
            elif "Oct" in time:
                time = time.replace('Oct', '-10-')
            elif "Nov" in time:
                time = time.replace('Nov', '-11-')
            elif "Dec" in time:
                time = time.replace('Dec', '-12-')
            else:
                time = time

            time = time[:-6]
            year = time[8:-9]
            d = time[:3]
            mm = time[3:-14]
            clock = time[-8:]
            time = year + mm + d
            time = time.replace(' ', '')
            time = time + " " + clock

            lvl.loc[ind] = time

    elif "+" in time:
        if time[-1] == "0":
            time = time[4:]

            if "Jan" in time:
                time = time.replace('Jan', '-1-')
            elif "Feb" in time:
                time = time.replace('Feb', '-2-')
            elif "Mar" in time:
                time = time.replace('Mar', '-3-')
            elif "Apr" in time:
                time = time.replace('Apr', '-4-')
            elif "May" in time:
                time = time.replace('May', '-5-')
            elif "Jun" in time:
                time = time.replace('Jun', '-6-')
            elif "Jul" in time:
                time = time.replace('Jul', '-7-')
            elif "Aug" in time:
                time = time.replace('Aug', '-8-')
            elif "Sep" in time:
                time = time.replace('Sep', '-9-')
            elif "Oct" in time:
                time = time.replace('Oct', '-10-')
            elif "Nov" in time:
                time = time.replace('Nov', '-11-')
            elif "Dec" in time:
                time = time.replace('Dec', '-12-')
            else:
                time = time

            time = time[:-6]
            year = time[8:-9]
            d = time[:3]
            mm = time[3:-14]
            clock = time[-8:]
            time = year + mm + d
            time = time.replace(' ', '')
            time = time + " " + clock

            lvl.loc[ind] = time

    elif "-" in time:
        if time[-1].isdigit() == True:
            time = time[4:]

            if "Jan" in time:
                time = time.replace('Jan', '-1-')
            elif "Feb" in time:
                time = time.replace('Feb', '-2-')
            elif "Mar" in time:
                time = time.replace('Mar', '-3-')
            elif "Apr" in time:
                time = time.replace('Apr', '-4-')
            elif "May" in time:
                time = time.replace('May', '-5-')
            elif "Jun" in time:
                time = time.replace('Jun', '-6-')
            elif "Jul" in time:
                time = time.replace('Jul', '-7-')
            elif "Aug" in time:
                time = time.replace('Aug', '-8-')
            elif "Sep" in time:
                time = time.replace('Sep', '-9-')
            elif "Oct" in time:
                time = time.replace('Oct', '-10-')
            elif "Nov" in time:
                time = time.replace('Nov', '-11-')
            elif "Dec" in time:
                time = time.replace('Dec', '-12-')
            else:
                time = time

            time = time[:-6]
            year = time[8:-9]
            d = time[:3]
            mm = time[3:-14]
            clock = time[-8:]
            time = year + mm + d
            time = time.replace(' ', '')
            time = time + " " + clock

            lvl.loc[ind] = time


    else:
        time = time[4:]
        if "Jan" in time:
            time = time.replace('Jan', '-1-')
        elif "Feb" in time:
            time = time.replace('Feb', '-2-')
        elif "Mar" in time:
            time = time.replace('Mar', '-3-')
        elif "Apr" in time:
            time = time.replace('Apr', '-4-')
        elif "May" in time:
            time = time.replace('May', '-5-')
        elif "Jun" in time:
            time = time.replace('Jun', '-6-')
        elif "Jul" in time:
            time = time.replace('Jul', '-7-')
        elif "Aug" in time:
            time = time.replace('Aug', '-8-')
        elif "Sep" in time:
            time = time.replace('Sep', '-9-')
        elif "Oct" in time:
            time = time.replace('Oct', '-10-')
        elif "Nov" in time:
            time = time.replace('Nov', '-11-')
        elif "Dec" in time:
            time = time.replace('Dec', '-12-')
        else:
            time = time
        time = time[:-4]
        year = time[8:-9]
        d = time[:3]
        mm = time[3:-14]
        clock = time[-8:]
        time = year + mm + d
        time = time.replace(' ', '')
        time = time + " " + clock

        lvl.loc[ind] = time


df = df.reset_index(drop=True)

df = df.rename(columns={'published': 'publishedORG'})

#df = df.drop(columns=['published'])
frames = [df, lvl]

df = pd.concat(frames, axis=1)

lang = pd.DataFrame(index=df.index, columns=["lang"])

for ind in df.index:
    try:
        text = df.loc[ind,"title"]
        text = text.replace('’', '')
        text = text.replace("’", '')
        text = text.replace("‘", '')
        text = text.replace("’", '')
        text = text.replace("-", '')
        text = text.replace('“', '')
        text = text.replace('”', '')
        text = text.replace('.', '')
        text = text.replace('ä', 'a')
        text = text.replace('ö', 'o')
        text = text.replace('–', '')
        text = text.replace(',', '')
        text = text.replace('"', '')
        text = text.replace('–', '')
        text = text.replace(':', '')
        teksti = teksti.replace(';', ' ')
        teksti = teksti.replace('"', '')
        language = detect(text)
        lang.loc[ind] = language
    except:
        pass

teksti2 = pd.DataFrame(index=df.index, columns=["summary"])
teksti3 = pd.DataFrame(index=df.index, columns=["published"])

for ind in df.index:
     teksti = df.loc[ind,"summary"]
     teksti = teksti.str.replace(';', ' ')
     teksti = teksti.replace('"', '')
     teksti2.loc[ind] = teksti


df = df.drop(columns=['title'])
df = df.drop(columns=['summary'])
frames = [df, teksti1, teksti2,teksti3,lang]

df = pd.concat(frames, axis=1)

df['published'].replace('  ', np.nan, inplace=True)
df.dropna(subset=['published'], inplace=True)

df = pd.concat(frames, axis=1)

print "languages found:\n",df['lang'].value_counts()

choose = raw_input('Choose specific language?(Y/N):')

choose = choose.lower()

if choose == "y":
    choosenlang = raw_input('Choose specific language?(language):')
    df = df.loc[df['lang']==choosenlang]

check = raw_input('Do you want to update old file?(Y/N): ')
check = check.lower()

if check == "y":

    path = raw_input('Insert path where save file is: ')
    old2 = raw_input('File name for old csv: ')
    if ".csv" not in old2:
        old2 = old2 + ".csv"

    userhome = os.path.expanduser('~')
    path= os.path.join(userhome, path, old2)
    print path
    open(path, "r")

    old =  pd.read_csv(old2, sep=";",encoding="UTF-8-sig")
    pituus = len(old)

    frames = [df, old]
    df = pd.concat(frames)

    df = df.drop_duplicates("title")

    pituus2 = len(df)

    print pituus2-pituus, "New records"

    df.to_csv(old2, sep=";",index=False,encoding="UTF-8-sig")

else:
    file = raw_input('Give save file name: ')
    if ".csv" not in file:
        file = file + ".csv"

    print len(df)

    df.to_csv(file, sep=";",index=False,encoding="UTF-8-sig")
