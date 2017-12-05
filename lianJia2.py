#!/usr/bin/python  
# -*- coding:UTF-8 -*-  
import pandas as pd  
#读取csv文件  
df = pd.read_csv('E:/lianjia/data_beijing.csv')  
house = pd.DataFrame(df)  
  
#对房源信息进行分列  
houseinfo_split = pd.DataFrame((x.split('|') for x in house.houseinfo),index=house.index,columns=['xiaoqu','huxing','mianji','chaoxiang','zhuangxiu','dianti'])  
print houseinfo_split.head()  
  
#将分列结果拼接回原数据表  
house=pd.merge(house,houseinfo_split,right_index=True, left_index=True)  
  
#对房源关注度进行分列  
followinfo_split = pd.DataFrame((x.split('/') for x in house.followinfo),index=house.index,columns=['guanzhu','daikan','fabu'])  
#将分列后的关注度信息拼接回原数据表  
house=pd.merge(house,followinfo_split,right_index=True, left_index=True)  
  
#按房源户型类别进行汇总  
huxing=house.groupby('huxing')['huxing'].agg(len)  
#查看户型汇总结果  
print huxing  
  
#导入图表库  
import matplotlib.pyplot as plt  
#导入数值计算库  
import numpy as np  
#画图了一下内容中有多个画图，运行时请注释其他的画图代码，避免互相影响  
#绘制房源户型分布条形图  
plt.rc('font', family='STXihei', size=11)  
a=np.array([1,2,3,4,5,6,7,8,9])  
plt.barh([1,2,3,4,5,6,7,8,9],huxing,color='#052B6C',alpha=0.8,align='center',edgecolor='white')  
plt.ylabel('house type')  
plt.xlabel('number')  
plt.xlim(0,1300)  
plt.ylim(0,10)  
plt.title('Housing family distribution')  
plt.legend(['Number'], loc='upper right')  
plt.grid(color='#95a5a6',linestyle='--', linewidth=2,axis='y',alpha=0.4)  
plt.yticks(a,('1shi0ting','1shi1ting','2shi1ting','2shi2ting','3shi1ting','3shi2ting','4shi1ting','4shi2ting','5shi2ting'))  
plt.show()  
#需要注意的是根据huxing输出的内容，设置a=np.array([1,2,3,4,5,6,7,8,9])的数量，我这里是9段分布，所以使用1-9，plt.yticks部分也是一样的  
# 1shi0ting为 1室0厅，1shi1ting为1室1厅，以此类推  
  
#对房源面积进行二次分列  
mianji_num_split = pd.DataFrame((x.split('平') for x in house.mianji),index=house.index,columns=['mianji_num','mi'])  
#将分列后的房源面积拼接回原数据表  
house = pd.merge(house,mianji_num_split,right_index=True,left_index=True)  
#去除mianji_num字段两端的空格  
house['mianji_num'] = house['mianji_num'].map(str.strip)  
#更改mianji_num字段格式为float  
house['mianji_num'] = house['mianji_num'].astype(float)  
#查看所有房源面积的范围值  
print house['mianji_num'].min(),house['mianji_num'].max()  
  
#对房源面积进行分组  
bins = [0, 50, 100, 150, 200, 250, 300, 350]  
group_mianji = ['less than 50', '50-100', '100-150', '150-200','200-250','250-300','300-350']  
house['group_mianji'] = pd.cut(house['mianji_num'], bins, labels=group_mianji)  
#按房源面积分组对房源数量进行汇总  
group_mianji=house.groupby('group_mianji')['group_mianji'].agg(len)  
  
#绘制房源面积分布图 需要去掉注释  
# plt.rc('font', family='STXihei', size=15)  
# a=np.array([1,2,3,4,5,6,7])  
# plt.barh([1,2,3,4,5,6,7],group_mianji,color='#052B6C',alpha=0.8,align='center',edgecolor='white')  
# plt.ylabel('mianji group')  
# plt.xlabel('number')  
# plt.title('Housing area of distribution')  
# plt.legend(['number'], loc='upper right')  
# plt.grid(color='#95a5a6',linestyle='--', linewidth=1,axis='y',alpha=0.4)  
# plt.yticks(a,('less 50', '50-100', '100-150', '150-200','200-250','250-300','300-350'))  
# plt.show()  
  
#对房源关注度进行二次分列  
guanzhu_num_split = pd.DataFrame((x.split('?') for x in house.guanzhu),index=house.index,columns=['guanzhu_num','ren'])  
#将分列后的关注度数据拼接回原数据表  
house=pd.merge(house,guanzhu_num_split,right_index=True, left_index=True)  
#去除房源关注度字段两端的空格  
house['guanzhu_num']=house['guanzhu_num'].map(str.strip)  
#更改房源关注度及总价字段的格式  
house[['guanzhu_num','totalprice']]=house[['guanzhu_num','totalprice']].astype(float)  
#查看房源关注度的区间  
print house['guanzhu_num'].min(),house['guanzhu_num'].max()  
  
#对房源关注度进行分组，这里的bins也需要根据上边的min()和max()输出值进行设置  
bins = [0, 100, 200, 300, 400, 500]  
group_guanzhu = ['小于100', '100-200', '200-300', '300-400','400-500']  
house['group_guanzhu'] = pd.cut(house['guanzhu_num'], bins, labels=group_guanzhu)  
group_guanzhu=house.groupby('group_guanzhu')['group_guanzhu'].agg(len)  
  
#绘制房源关注度分布图，去除注释  
# plt.rc('font', family='STXihei', size=15)  
# a=np.array([1,2,3,4,5])  
# plt.barh([1,2,3,4,5],group_guanzhu,color='#052B6C',alpha=0.8,align='center',edgecolor='white')  
# plt.ylabel('Interest groups')  
# plt.xlabel('Number')  
# plt.xlim(0,2200)  
# plt.title('Housing attention distribution')  
# plt.legend(['Number'], loc='upper right')  
# plt.grid(color='#95a5a6',linestyle='--', linewidth=1,axis='y',alpha=0.4)  
# plt.yticks(a,('less 100', '100-200', '200-300', '300-400','400-500'))  
# plt.show()  
  
#房源聚类分析  
#导入sklearn中的KMeans进行聚类分析  
from sklearn.cluster import KMeans  
#使用房源总价，面积和关注度三个字段进行聚类  
house_type = np.array(house[['totalprice','mianji_num','guanzhu_num']])  
#设置质心数量为3  
clf=KMeans(n_clusters=3)  
#计算聚类结果  
clf=clf.fit(house_type)  
#查看分类结果的中心坐标  
print clf.cluster_centers_  
#在原数据表中标注所属类别  
house['label'] = clf.labels_  
#显示所有数据内容  
print house  