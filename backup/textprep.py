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
import numpy as np

df = pd.read_csv('worldbnews.csv', sep=";",encoding="UTF-8-sig")

summaries = pd.DataFrame(index=df.index, columns=["summary"])

###for ind in df.index:
#    s = df.loc[ind,"summary"]
#    s = re.sub(r'<.+?>', '', s)
#    s = re.sub(r'(?:&#.+?;)', ' ', s)
#    summaries.loc[ind] = s
#df = df.rename(columns={'summary': 'summary2'})
#frames = [df, summaries]


teksti1 = pd.DataFrame(index=df.index, columns=["title"])
teksti2 = pd.DataFrame(index=df.index, columns=["summary"])
teksti3 = pd.DataFrame(index=df.index, columns=["published"])
#df = pd.concat(frames, axis=1)
for ind in df.index:
     teksti = df.loc[ind,"title"]
     teksti = teksti.replace(';', ' ')
     teksti = teksti.replace('"', '')
     teksti1.loc[ind] = teksti

for ind in df.index:
     teksti = df.loc[ind,"summary"]
     teksti = teksti.replace(';', ' ')
     teksti = teksti.replace('"', '')
     teksti = teksti.replace('\n', '')
     teksti2.loc[ind] = teksti

for ind in df.index:
     teksti = df.loc[ind,"published"]
     teksti = teksti.replace(';', ' ')
     teksti = teksti.replace('"', '')
     teksti3.loc[ind] = teksti

df = df.drop(columns=['title'])
df = df.drop(columns=['summary'])
df = df.drop(columns=['published'])
frames = [df, teksti1, teksti2,teksti3]

df = pd.concat(frames, axis=1)

df['published'].replace('  ', np.nan, inplace=True)
df.dropna(subset=['published'], inplace=True)

df.to_csv('worldbnews.csv', sep=";",index=False,encoding="UTF-8-sig")
