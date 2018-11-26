# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import feedparser
import pandas as pd
import os

#Csv tiedoston lukeminen
polku = raw_input('Path for the feed file without user: ')
tiedostonimi = raw_input('Type file name for the feed file: ')
if ".csv" not in tiedostonimi:
    tiedostonimi = tiedostonimi + ".csv"


userhome = os.path.expanduser('~')
path= os.path.join(userhome, polku, tiedostonimi)
open(path, "r")

feeds = pd.read_csv(path, sep=";",encoding="UTF-8-sig")
i=[]

for ind in feeds.index:
    link = feeds.loc[ind,"feeds"]
    feed = feedparser.parse(link)

    feed_title = feed['feed']['title']
    feed_entries = feed.entries



    for entry in feed.entries:


        article_title = entry.title
        article_link = entry.link
        article_summary = entry.summary
        article_published_at = entry.published # Unicode string
        article_published_at_parsed = entry.published_parsed # Time object
        i.append({'title' : "{}".format(article_title.encode("utf-8")) , 'link' : "{}".format(article_link.encode("utf-8")), 'summary' : "{}".format(article_summary).encode("utf-8"), 'published': "{}".format(article_published_at.encode("utf-8"))})

        print "Title: {}".format(article_title.encode("utf-8"))
        print "link: {}".format(article_link.encode("utf-8"))
        print "Summary: {}".format(article_summary).encode("utf-8")
        print "Published at {}".format(article_published_at.encode("utf-8"))

    df = pd.DataFrame(i,columns=["title","link","summary","published"])

df = df.drop_duplicates("title", keep="first")

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


print df.head(5)



df.to_csv(tiedosto, sep=";",index=False,encoding="UTF-8-sig")
