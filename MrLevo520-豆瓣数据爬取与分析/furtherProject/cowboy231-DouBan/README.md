## 环境说明

- Python 2.7（代码根据py2.7编写）
- selenium(别忘记配置Chrome driver 以及PhantomJS driver)
- echarts（项目内已包含，无需特别配置）


-----
# 项目目的
1. 使用selenium获取数据（基本元素定位，句柄切换等）
2. 数据基本处理（目前使用python文本处理）
3. 使用echarts进行数据可视化




## 快速开始

### 克隆（clone项目到本地）通过调试已有的代码熟悉基本功能

1.运行work9文件夹中的work9.py，进行数据扒取

预期：进入豆瓣电影页面→选择冷门电影→选择高分排序→逐个对影片信息进行扒取并在文件夹下生成douban.txt（记录扒取信息）

2.运行work9文件夹中的Demo1.html并观察其代码（熟悉echarts）

观察点：echarts元素以及数据的基本应用（坐标轴、折线图、饼图、排版布局）

## 代码简述

1. work9.py

![](https://raw.githubusercontent.com/cowboy231/Mini-Python-Project/master/MrLevo520-%E8%B1%86%E7%93%A3%E6%95%B0%E6%8D%AE%E7%88%AC%E5%8F%96%E4%B8%8E%E5%88%86%E6%9E%90/furtherProject/cowboy231-DouBan/img/163851.png)



2. echarts

   图表由1个折线图和一个饼图组成

   ![2017-09-04_195451](https://raw.githubusercontent.com/cowboy231/Mini-Python-Project/master/MrLevo520-%E8%B1%86%E7%93%A3%E6%95%B0%E6%8D%AE%E7%88%AC%E5%8F%96%E4%B8%8E%E5%88%86%E6%9E%90/furtherProject/cowboy231-DouBan/img/195451.png)

   折线图部分，坐标轴

   ![2017-09-09_170851](https://github.com/cowboy231/Mini-Python-Project/blob/master/MrLevo520-%E8%B1%86%E7%93%A3%E6%95%B0%E6%8D%AE%E7%88%AC%E5%8F%96%E4%B8%8E%E5%88%86%E6%9E%90/furtherProject/cowboy231-DouBan/img/170851.png)

   数据填充

   ![2017-09-09_171821](https://raw.githubusercontent.com/cowboy231/Mini-Python-Project/master/MrLevo520-%E8%B1%86%E7%93%A3%E6%95%B0%E6%8D%AE%E7%88%AC%E5%8F%96%E4%B8%8E%E5%88%86%E6%9E%90/furtherProject/cowboy231-DouBan/img/171821.png)

饼图部分

​	![2017-09-09_172311](https://raw.githubusercontent.com/cowboy231/Mini-Python-Project/master/MrLevo520-%E8%B1%86%E7%93%A3%E6%95%B0%E6%8D%AE%E7%88%AC%E5%8F%96%E4%B8%8E%E5%88%86%E6%9E%90/furtherProject/cowboy231-DouBan/img/172311.png)

使用echarts的图表工具转换数据

​	![2017-09-09_174243](https://github.com/cowboy231/Mini-Python-Project/blob/master/MrLevo520-%E8%B1%86%E7%93%A3%E6%95%B0%E6%8D%AE%E7%88%AC%E5%8F%96%E4%B8%8E%E5%88%86%E6%9E%90/furtherProject/cowboy231-DouBan/img/174243.png)

## 延伸

目前的脚本功能仍不完善，以下简单列举几个可以延伸的点

1. selenium操作：可以补充登录操作
2. 数据处理：目前只是用split命令进行简单提取，可以使用正则表达式进行优化
3. 数据展示：折线图只填充了3组数据不能定位到具体影片，可以把片名和跳转链接嵌入进去

