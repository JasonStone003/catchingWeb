#!/usr/bin/python
#-*- coding:UTF-8 -*-  
  
#引用爬取数据的包  
import requests  
import time  
from bs4 import BeautifulSoup 

#设置列表页URL的固定部分  
url = 'https://bj.lianjia.com/ershoufang/'  
#设置页面页的可变部分  
page=('gp')  
  
#设置访问网站的请求头部信息  
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',  
'Accept':'text/html;q=0.9,*/*;q=0.8',  
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',  
'Accept-Encoding':'gzip',  
'Connection':'close',  
'Referer':'http://www.baidu.com/link?url=_andhfsjjjKRgEWkj7i9cFmYYGsisrnm2A-TN3XZDQXxvGsM9k9ZZSnikW2Yds4s&amp;wd=&amp;eqid=c3435a7d00006bd600000003582bfd1f'  
}

#使用for循环生成1-100的数字，转化格式后与前面的URL固定部分拼成要抓取的URL。  
#设置每两个页面间隔1秒。抓取到的页面保存在html中  
  
for i in range(1,100):  
    if i == 1:  
        i = str(i)  
        a = (url + page + i + '/')  
        r =requests.get(url=a,headers=headers)  
        html = r.content  
    else:  
        i = str(i)  
        a = (url + page + i + '/')  
        r = requests.get(url=a,headers=headers)  
        html2 = r.content  
        html = html + html2  
    time.sleep(1) 


#解析页面并提取信息  
  
#解析抓取的页面内容  
lj = BeautifulSoup(html,'html.parser')  
#提取房源总价  
price = lj.find_all('div',attrs={'class':'priceInfo'})  
tp = []  
for a in price:  
    totalPrice =a.span.string  
    tp.append(totalPrice)
    
#提取房源信息  
houseInfo=lj.find_all('div',attrs={'class':'houseInfo'})  
  
hi=[]  
for b in houseInfo:  
    house=b.get_text()  
    hi.append(house)  

#提取房源关注度  
followInfo=lj.find_all('div',attrs={'class':'followInfo'})  
  
fi=[]  
for c in followInfo:  
    follow=c.get_text()  
    fi.append(follow)  
  
#将数据保存到csv文件中，别总是来回爬取链家数据不太好吧。  
import pandas as pd  
house = pd.DataFrame({'totalprice':tp,'houseinfo':hi,'followinfo':fi})  
house.to_csv('E:/lianjia/data_beijing.csv',encoding='utf-8',index=False)  
house.head()  