# coding: utf-8

import re
import json
import time
import base64
import urllib2
from subprocess import Popen, PIPE

from py.util import formatQuery,siteToMainName,SITE_NAMES

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

DONE = u'''
<?xml version="1.0"?>
<items>
  <item uid="done" arg="" valid="YES">
    <title>更新成功</title>
    <subtitle>update completed</subtitle>
    <icon>./icon.png</icon>
  </item>
</items>
'''


def queryAnimates(queryStr):
    query = formatQuery(queryStr)
    output = ''
    if query[u'isUpdate']:
        update()
    # 获取动画信息
    animates = json.load(open(u'data.json'))
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
    # 获取动画信息
    animates = json.load(open(u'data.json'))
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
    args = [u'python', u'./py/update.py']
    Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
