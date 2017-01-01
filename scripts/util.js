'use strict';

let fs = require('fs');
let path = require('path');
let http = require('https');

function queryFiles(fileList) {
    let list = [];
    fileList.forEach(file => {
        let stat = fs.statSync(file);
        if(stat.isDirectory()) {
            let files = fs.readdirSync(file).map(item => path.join(file, item));
            list = list.concat(queryFiles(files));
        } else if(!/^.*\/\.[^\.]+$|^\..*$|^.*\.pyc$/.test(file)) {
            // 只添加非 ‘.’ 开头的文件
            list.push(file);
        }
    });
    return list;
}

//get animates data from bgmlist.com
function queryAnimateData(resFun, rejFun) {
    const URL = 'https://bgmlist.com/tempapi/archive.json';
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
    let promise = new Promise(resFun, rejFun);
    // 获取数据文件索引
    http.get(URL + '?_=' + new Date().getTime(), res => {
        let rawData = '';
        res.on('data', data => {
            rawData += data;
        });
        res.on('end', () => {
            let animates = JSON.parse(rawData);
            let data = {};
            let count = 0;
            for(let year in animates.data) {
                console.log(year)
                for(let season in animates.data[year]) {
                    count++;
                    // 通过索引获取每个季度的番数据
                    http.get(animates.data[year][season]['path'], res => {
                        let seasonData = '';
                        res.on('data', thunkData => {
                            seasonData += thunkData;
                        });
                        res.on('end', () => {
                            count--;
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
                            if (count <= 0) {
                                resFun(data);
                            }
                        });
                    }).on('error', err => {
                        console.log(`get error: ${err.message}`);
                        rejFun(err);
                    });
                }
            }
        });
    }).on('error', err => {
        console.log(`get error: ${err.message}`);
        rejFun(err);
    });
    return promise;
}

module.exports = {
    queryAnimateData: queryAnimateData,
    queryFiles: queryFiles
};
