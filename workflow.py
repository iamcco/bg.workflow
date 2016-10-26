# coding: utf-8

import re
import json
import time
import base64
import urllib2

from util import formatQuery,siteToMainName,SITE_NAMES

TEMPLATE = u'''
<?xml version="1.0"?>
<items>
{{content}}
</items>
'''

ITEM = u'''
  <item uid="{{name}}" arg="{{params}}" valid="YES">
    <title>{{name}}</title>
    <subtitle>播放时间 {{time}}</subtitle>
    <icon>./src/{{weekday}}.png</icon>
  </item>
'''

DOWNLOAD_PREFIX = u'https://raw.githubusercontent.com/iamcco/bg.workflow/master/'

animates = json.load(open(u'data.json'))

def queryAnimates(queryStr):
    query = formatQuery(queryStr)
    output = ''
    if query[u'isUpdate']:
        update()
    if query[u'id'] in animates:
        result = animates[query[u'id']]
        for animes in result:
            temp = re.sub(ur'\{\{name\}\}', animes[u'titleCN'], ITEM)
            temp = re.sub(ur'\{\{params\}\}', query[u'id'] + ' ' + animes[u'titleCN'], temp)
            temp = re.sub(ur'\{\{time\}\}', animes[u'timeCN'], temp)
            temp = re.sub(ur'\{\{weekday\}\}', str(animes[u'weekDayCN']), temp)
            output += temp
        return re.sub(ur'\{\{\content}\}', output, TEMPLATE)

def querySites(queryStr):
    query = queryStr.split(' ')
    id = query[0]
    name = ' '.join(query[1:])
    animes = animates[id]
    output = ''
    for ani in animes:
        if ani[u'titleCN'].encode('utf-8') == name:
            for site in ani[u'onAirSite']:
                temp = re.sub(ur'\{\{name\}\}', SITE_NAMES[siteToMainName(site)], ITEM)
                temp = re.sub(ur'\{\{params\}\}', site, temp)
                temp = re.sub(ur'\{\{weekday\}\}', siteToMainName(site), temp)
                temp = re.sub(ur'\{\{time\}\}', ani[u'timeCN'], temp)
                output += temp
            return re.sub(ur'\{\{\content}\}', output, TEMPLATE)

def update():
    localVersion = json.load(open(u'version.json'))
    onlineVersion = json.loads(urllib2.urlopen(DOWNLOAD_PREFIX + u'version.json').read())
    if localVersion.version < onlineVersion.version:
        for path in onlineVersion[u'list']:
            target = urllib2.urlopen(DOWNLOAD_PREFIX + path).read()
            with open(path) as file:
                file.write(target)
