### Alfred2 workflow 查看每日新番

**显示 _周日_ 的番**
![one](https://cloud.githubusercontent.com/assets/5492542/14480876/ca41c478-015f-11e6-9820-4d2fd89d31b9.png)

**显示 _201601季度 周日_ 的番**
![two](https://cloud.githubusercontent.com/assets/5492542/14480881/d34ad726-015f-11e6-9d50-a7d628c3ac22.png)

**更新数据**
![three](https://cloud.githubusercontent.com/assets/5492542/14480884/ddfecd94-015f-11e6-90f9-15fe8cf5ef91.png)

输入说明, 一共有三个参数：

1. 周几 表示周几，具体看下表
2. 201604 表示 2016 年 4 月番，同理 201601 表示 2016 年 1 月番
3. update 表示更新本地数据

> 这几个参数顺序可以不同组合，但是要用空格隔开，比如 `日 201604 update` 和 `update 日 201604` 是一样的    
> 只有 周几 的话，会默认为当前季度的番，比如 `日` 表示现在这个季度的周日更新的番    
> update 参数会更新本地的数据    
> 201604 和 update 参数不是必要的    

周几     | 输入值
---------|-------
周日     | 日/周日/0/zhouri/ri/
周一     | 月/周一/01/1/zhouyi/yi/
周二     | 火/周二/02/2/zhouer/er/
周三     | 水/周三/03/3/zhousan/san/
周四     | 木/周四/04/4/zhousi/si/
周五     | 金/周五/05/5/zhouwu/wu/
周六     | 土/周六/06/6/zhouliu/liu/
时间未定 | 不/不定期/未定/时间未定/budingqi/bu/weiding/shijianweiding

> 在 alfred2 中输入上面的输入值一栏的任何一个值，比如 `日` 代表的是周日

##### 数据来自 [acgdb](http://acgdb.com/)，如果有更全的数据来源请告知
