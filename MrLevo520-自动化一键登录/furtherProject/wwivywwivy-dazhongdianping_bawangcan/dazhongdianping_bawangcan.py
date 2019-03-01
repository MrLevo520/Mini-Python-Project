#!/usr/bin/env python
# coding: utf-8

# # 大众点评霸王餐自动抽取

# 主页得到每个页面的id字典
import requests
import json

# cookies_main = {}

headers_main = {
    'Origin': 'http://s.dianping.com',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'http://s.dianping.com/event/shanghai?utm_source=dp_pc_event',
    'Connection': 'keep-alive',
}

dic={}
for pg in range(10):
    payloadData_main={"cityId":"1","type":0,"mode":"","page":pg}
    response = requests.post('http://m.dianping.com/activity/static/pc/ajaxList', headers=headers_main, cookies=cookies_main, data=json.dumps(payloadData_main))
    if json.loads(response.text)['data']['detail']!=None:
        for item in json.loads(response.text)['data']['detail']:
            dic[item['offlineActivityId']]=item['activityTitle']
# print(len(dic))
# print(dic.keys())

# 循环每个页面，报名

# cookies = {}

headers = {
    'Origin': 'http://s.dianping.com',
    'Accept-Encoding': 'gzip, deflate',
    'X-Request': 'JSON',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8;',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept': 'application/json, text/javascript',
    'Referer': 'http://s.dianping.com/event/1119630858',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

for k in dic.keys():
    data = {'offlineActivityId': str(k),'extraCount':'0'
            ,'marryDayStr':'2019-01-31','marryStatus':'0','isShareSina':'True','isShareQQ':'True'}
    response = requests.post('http://s.dianping.com/ajax/json/activity/offline/saveApplyInfo', headers=headers, cookies=cookies, data=data)
    # print(k)
    print(json.loads(response.text)['msg']['html'])

