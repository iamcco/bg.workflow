# coding: utf-8

import re
import time
import datetime

WEEKDAY_KEYS = {
    u'0': u'[日],[周日],[0],[zhouri],[ri]',
    u'1': u'[月],[周一],[01],[1],[zhouyi],[yi]',
    u'2': u'[火],[周二],[02],[2],[zhouer],[er]',
    u'3': u'[水],[周三],[03],[3],[zhousan],[san]',
    u'4': u'[木],[周四],[04],[4],[zhousi],[si]',
    u'5': u'[金],[周五],[05],[5],[zhouwu],[wu]',
    u'6': u'[土],[周六],[06],[6],[zhouliu],[liu]'
}

SITE_NAMES = {
    u'acfun': u'AcFun',
    u'bilibili': u'哔哩哔哩',
    u'iqiyi': u'爱奇艺',
    u'kankan': u'响巢看看',
    u'le': u'乐视视频',
    u'mgtv': u'芒果TV',
    u'pptv': u'PPTV',
    u'qq': u'腾讯视频',
    u'sohu': u'搜狐视频',
    u'tucao': u'TUCAO',
    u'tudou': u'土豆',
    u'youku': u'优酷'
}

# 获取网址主域名，blog.yuuko.cn => yuuko

def siteToMainName(site):
    reg = u'^https?://(\w+?\.)*(\w+)\.\w+(/.*)?$'
    g = re.match(reg, site)
    if g:
        return g.group(2)
    else:
        return False


# 转换月份为季度，1，4，7，10
def monthToSeason(month):
    month = int(month)
    season = ''
    if month < 4:
        season = '1'
    elif month < 7:
        season = '4'
    elif month < 10:
        season = '7'
    elif month <= 12:
        season = '10'
    else:
        # TODO: 显示出错结果
        pass
    return season

# 日期转为星期
def dayToWeekday(year, month, day):
    if len(month ) < 2:
        month = u'0%s' % str(month)
    weekday = datetime.datetime.strptime(year + month + day, u'%Y%m%d').weekday() + 1
    if weekday == 7:
        weekday = 0
    return str(weekday)

# 用户输入的星期转化为 [0,1,2,3,4,5,6]，分别为 周一 至 周日
def formatWeekDay(query):
    for key in WEEKDAY_KEYS:
        if re.search(u'\[%s\]' % query.strip(), WEEKDAY_KEYS[key]):
            return key
    return time.strftime(u'%w')

# 输入字符串 2016xxxx 转化为: (year, season, week)
def formatTime(query):
    year = time.strftime(u'%Y')
    month = time.strftime(u'%m')
    day = ''
    weekday = time.strftime(u'%w');
    if weekday == '7':
        weekday = '0'
    queryLen = len(query)
    if queryLen >= 4:
        year = query[0:4]
    if queryLen >=5:
        month = query[4:6]
    if queryLen >= 7:
        day = query[6:8]
    if day != '':
        weekday = dayToWeekday(year, month, day)

    return [year, monthToSeason(month), weekday]

# 处理输入字串
def formatQuery(query):
    weekday = ''
    isUpdate = False
    id = formatTime('')
    items = query.strip().split(u' ')
    for item in items:
        if re.search(u'update|更新', item):
            isUpdate = True
        elif re.match(ur'^\d{4,8}$', item):
            id = formatTime(item)
        elif item != u'':
            weekday = formatWeekDay(item)
    if weekday != '':
        id[2] = weekday

    return {
        u'isUpdate': isUpdate,
        u'id': '_'.join(id)
    }

