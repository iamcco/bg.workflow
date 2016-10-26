'use strict';

//get animates data from bgmlist.com

let fs = require('fs');
let http = require('https');

const HOST = 'https://bgmlist.com/';
const URL = 'https://bgmlist.com/json/archive.json';

let escapeWords = function(str) {
    const words = [{
        key: '&',
        value: '&amp;'
    }, {
        key: '"',
        value: '&quot;'
    }, {
        key: '<',
        value: '&lt;'
    }, {
        key: '>',
        value: '&gt;'
    }, {
        key: '?',
        value: '&iexcl;'
    }];
    words.forEach(word => {
        str = str.replace(word.key, word.value);
    });
    return str;
};

// 获取数据文件索引
http.get(URL + '?_=' + new Date().getTime(), res => {
    let rawData = '';
    res.on('data', data => {
        rawData += data;
    });
    res.on('end', () => {
        let animates = JSON.parse(rawData);
        let data = {};
        for(let year in animates.data) {
            for(let season in animates.data[year]) {
                // 通过索引获取每个季度的番数据
                http.get(HOST + animates.data[year][season]['path'], res => {
                    let seasonData = '';
                    res.on('data', thunkData => {
                        seasonData += thunkData;
                    });
                    res.on('end', () => {
                        // 处理番数据，并分类
                        seasonData = JSON.parse(seasonData);
                        for(let key in seasonData) {
                            let ani = seasonData[key];

                            // 播放星期
                            ani.weekDayCN = ani.weekDayCN !== '' ? ani.weekDayCN : ani.weekDayJP;

                            // 动画标题
                            ani.titleCN = escapeWords(ani.titleCN || ani.titleJP || ani.titleEN || '');
                            // 动画播放时间
                            ani.timeCN = (seasonData[key].timeCN || seasonData[key].timeJP).split('');
                            ani.timeCN.splice(2, 0, ':');
                            ani.timeCN = ani.timeCN.join('');
                            // 把动画按 年_季_星期 分类
                            let itemKey = year + '_' + season + '_' + ani.weekDayCN;
                            data[itemKey] = (data[itemKey] || []).concat([ani]);

                        }
                        fs.writeFileSync('data.json', JSON.stringify(data));
                    });
                }).on('error', err => {
                    console.log(`get error: ${err.message}`);
                });
            }
        }
    });
}).on('error', err => {
    console.log(`get error: ${err.message}`);
});
