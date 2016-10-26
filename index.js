'use strict';

let fs = require('fs');
let bangumiData = require('bangumi-data');

const SITE_TYPES = {
    info: '资讯',
    onair: '在线播放',
    resource: '资源'
};

// 时间转为 ID: year_season_weekday
function dateToID(dateStr) {
    let date = new Date(dateStr);
    return date.getFullYear() + '_' + monthToSeason(date.getMonth() + 1) + '_' + date.getDay();
}

// 月转为季
function monthToSeason(month) {
    let season;
    if (month < 4) {
        season = 1;
    } else if (month < 7) {
        season = 4;
    } else if (month < 10) {
        season = 7;
    } else if (month <= 12) {
        season = 10;
    } else {
        throw new Error('No match season for month input');
    }
    return season;
}

// 获取播放时间
function dateToTime(dateStr) {
    let date = new Date(dateStr);
    return date.getHours() + ':' + date.getMinutes();
}

// 动漫信息
let data = {};
bangumiData.items.forEach(function(item) {
    let titleTranslate = item.titleTranslate;
    let animate = {
        name: titleTranslate && titleTranslate['zh-Hans'] && titleTranslate['zh-Hans'].length && titleTranslate['zh-Hans'][0] || item.title,
        id: dateToID(item.begin),
        weekday: dateToID(item.begin).split('_').pop(),
        time: dateToTime(item.begin),
        lang: item.lang,
        sites: item.sites.map(function(site) {
            let siteDate = bangumiData.sites[site.site];
            return {
                name: siteDate.title,
                url: siteDate.urlTemplate.replace(/\{\{id\}\}/, site.id),
                type: SITE_TYPES[siteDate.type]
            };
        })
    };
    data[animate.id] = (data[animate.id] || []).concat([animate]);
});

// 动漫信息写到文件：data.json
fs.writeFileSync('data.json', JSON.stringify(data));

