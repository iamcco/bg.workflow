'use strict';

let fs = require('fs');

let util = require('./scripts/util.js');

//从 bgmlist.com 获取动漫信息
console.log('从 bgmlist.com 获取动漫信息');
util.queryAnimateData(data => {
    // 动画信息写入 data.json
    fs.writeFileSync('data.json', JSON.stringify(data));

    // 生成 version.json
    let fileList, version;
    version = JSON.parse(fs.readFileSync('version.json'));
    fileList = util.queryFiles(['src', 'py', 'data.json', 'version.json', 'info.plist']);
    version.version++;
    version.list = fileList;
    fs.writeFileSync('version.json', JSON.stringify(version));
});


