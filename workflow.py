# coding: utf-8
# 从 acgdb.com 获取新番数据

import re
import os
import time
import json
import types
import urllib2

template = u'''
<?xml version="1.0"?>
<items>
{{content}}
</items>
'''

item = u'''
  <item uid="{{name}}" arg="" valid="YES">
    <title>{{name}}</title>
    <subtitle>播放时间 {{time}}</subtitle>
    <icon>./src/{{day}}.png</icon>
  </item>
'''

days = {
    u'周日': u'[日],[周日],[0],[zhouri],[ri]',
    u'周一': u'[月],[周一],[01],[1],[zhouyi],[yi]',
    u'周二': u'[火],[周二],[02],[2],[zhouer],[er]',
    u'周三': u'[水],[周三],[03],[3],[zhousan],[san]',
    u'周四': u'[木],[周四],[04],[4],[zhousi],[si]',
    u'周五': u'[金],[周五],[05],[5],[zhouwu],[wu]',
    u'周六': u'[土],[周六],[06],[6],[zhouliu],[liu]',
    u'时间未定': u'[不],[不定期],[未定],[时间未定],[budingqi],[bu],[weiding],[shijianweiding]'
}

quarters = [
    ( u'01', u'02', u'03' ),
    ( u'04', u'05', u'06' ),
    ( u'07', u'08', u'09' ),
    ( u'10', u'11', u'12' )
]


def getQuery(str):
    result = {
        u'update': False,
        u'date': getAnimesPath(),
        u'day': getDay(time.strftime('%w').decode('utf-8'))
    }
    strs = str.strip().split(u' ')
    for item in strs:
        if re.search(u'update|更新', item):
            result[u'update'] = True
        elif re.match(ur'^\d{5,6}$', item):
            result[u'date'] = item
        else:
            result[u'day'] = getDay(item)
    return result

def saveData(data, date = u''):
    if date == u'':
        date = getAnimesPath()
    if type(data) is types.DictType or type(data) is types.ListType:
        f = open(date + u'.json', u'w')
        f.write(json.dumps(data))
        f.close()

def getAnimesPath():
    month = time.strftime(u'%m')
    for m in quarters:
        if month in m:
            month = m[0]
    year = time.strftime(u'%Y')
    return year + month

def getDay(str):
    if str == '':
        str = time.strftime('%w')
    for key in days:
        if re.search(u'\[%s\]' % str.strip(), days[key]):
            return key

def getAnimesByDay(day, data):
    str = u''
    for it in data:
        if it[u'day'] == day:
            for animes in it[u'animes']:
                temp = re.sub(ur'\{\{time\}\}', animes[0], item)
                temp = re.sub(ur'\{\{name\}\}', animes[1], temp)
                temp = re.sub(ur'\{\{day\}\}', day, temp)
                str += temp
            break
    return str

def getAnimesData(update = False, date = u''):
    if date == u'':
        date = getAnimesPath()

    acgdbData = [];
    fileName = date + u'.json'

    if update or not os.path.exists(fileName):
        data = urllib2.urlopen(u'http://acgdb.com/animes%s' % date).read().decode('utf-8')
        data = data.split(u'sp-animelist')[1:]

        for it in data:
            day = {}
            g = re.search(ur'\<h3\>(.*?)(?:\<.*?)?\<\/h3\>.*?', it)
            if g != None:
                day[u'day'] = g.group(1).split(u' ')[0]
                g = re.findall(ur'em\s*acgdb-timestamp.*?\>(.*?)\<.*?\<u\>(.*?)\<\/u\>', it)
                if g != None:
                    day[u'animes'] = g
            acgdbData.append(day)
            saveData(acgdbData, date)
    else:
        f = open(fileName, u'r')
        acgdbData = json.loads(f.read())
        f.close()
    return acgdbData

def getAnimes(query):
    query = getQuery(query.decode('utf-8'))
    data = getAnimesData(query[u'update'], query[u'date'])
    content = getAnimesByDay(query[u'day'], data)
    result = re.sub(u'\{\{content\}\}', content, template)
    return result
