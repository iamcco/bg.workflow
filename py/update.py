# coding: utf-8
#!/usr/bin/env python

import json
import urllib2

DOWNLOAD_PREFIX = u'https://raw.githubusercontent.com/iamcco/bg.workflow/master/'

def update():
    localVersion = json.load(open(u'version.json'))
    onlineVersion = json.loads(urllib2.urlopen(DOWNLOAD_PREFIX + u'version.json').read())
    if localVersion[u'version'] < onlineVersion[u'version']:
        for path in onlineVersion[u'list']:
            target = urllib2.urlopen(DOWNLOAD_PREFIX + path).read()
            with open(path, 'wb') as file:
                file.write(target)

# 抓取文件更新
update()
