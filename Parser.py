# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import feedparser
import pandas as pd
import os
from lxml import etree
import urllib2
import time

#Csv tiedoston lukeminen
polku = raw_input('Path for the feed file without user: ')
tiedostonimi = raw_input('Type file name for the feed file: ')
if ".csv" not in tiedostonimi:
    tiedostonimi = tiedostonimi + ".csv"

maara = raw_input('How many iterations: ')
odotus = raw_input('Set waiting time between iterations in seconds: ')


userhome = os.path.expanduser('~')
path= os.path.join(userhome, polku, tiedostonimi)
open(path, "r")

feeds = pd.read_csv(path, sep=";",encoding="UTF-8-sig")
list=[]
x = 0

for i in range(int(maara)):
    for ind in feeds.index:
        link = feeds.loc[ind,"feeds"]
        print link
        if "xml" in link:
            #XML
            headers = { 'User-Agent' : 'Mozilla/5.0' }
            req = urllib2.Request(link, None, headers)
            reddit_file = urllib2.urlopen(req).read()

            reddit = etree.fromstring(reddit_file)

            for item in reddit.xpath('/rss/channel/item'):

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


        df = pd.DataFrame(list,columns=["title","link","summary","published"])
    x=x+1
    print "Iteration", x
    if x < int(maara):
        time.sleep(int(odotus))


tarkastus = raw_input('Do you want to update old file?(Y/N): ')
tarkastus = tarkastus.lower()
if tarkastus == "y":
    tiedosto = raw_input('File name for old csv: ')
    if ".csv" not in tiedosto:
        tiedosto = tiedosto + ".csv"

    userhome = os.path.expanduser('~')
    path= os.path.join(userhome, polku, tiedosto)
    open(path, "r")

    vanhat =  pd.read_csv(path, sep=";",encoding="UTF-8-sig")
    framet = [df, vanhat]
    df = pd.concat(framet)

else:
    tiedosto = raw_input('Give save file name: ')
    if ".csv" not in tiedosto:
        tiedosto = tiedosto + ".csv"
df = df.drop_duplicates("title")
df.to_csv(tiedosto, sep=";",index=False,encoding="UTF-8-sig")
