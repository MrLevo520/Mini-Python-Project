## **环境**
> win10 + Python 3.6 + PyCharm

---
## **目的**
> * 对爬取到的豆瓣冷门佳片做制片国家的空间分布图
> * 分析片长与得分之间的关系

---
## **实现步骤**
1. 按照豆瓣得分爬取冷门佳片top200的相关信息并存储到csv中；
2. 调用有道在线翻译页面，逐个把“制片国家”中的中文信息翻译成英文，存储为csv中新的列；
3. 利用csv中的信息做数据分析。

---
## **实现代码**

    # 数据分析部分2017.09.01
    import pandas as pd
    from pyecharts import Map, Scatter
    
    
    #数据读取
    d = pd.read_csv(r"movie_new.csv", sep=",",encoding='gb18030')    #自己的链接
    nation = d['trans_nation'].values
    new_nation = '/'.join(nation).split('/')  #有些影片属于多个国家，使用这种方法将多个国家拆开
    print(new_nation)
    

    #new_nation中的很多国家的名称不规范，为了画出世界地图，统一替换成 pycharts中的使用的英文名称
    replace_rule = {'The United States':'United States', 'America':'United States', 'Us':'United States',
               'West Germany':'Germany', 'former west Germany':'Germany', 'German':'Germany',
               'The French':'France',
               'The British':'United Kingdom', 'UK':'United Kingdom',
               'South Korea':'Korea',
               'Hong Kong':'China', 'The Chinese mainland':'China', 'Taiwan':'China',
               'The Soviet union':'Russia',
               'Czechoslovakia':'Czech Rep.',
               'The Danish':'Denmark'}
    #rep = ['United States' if x == 'The United States' else x for x in new_nation]
    replace = [replace_rule[x] if x in replace_rule else x for x in new_nation]
    

    #统计值的个数，存储到字典中
    a = {}
    for i in replace:
        if replace.count(i) > 1:
            a[i] = replace.count(i)
    print(a)
    
    

    #画地区分布图，并根据影片数量多少做颜色渲染
    map = Map("豆瓣冷门佳片TOP200地区分布", subtitle="074——作业九", width=1200, height=600)
    attr,value = map.cast(a)
    print(map.cast(a))
    map.add("", attr, value, maptype="world", is_visualmap=True, visual_text_color='#000', visual_range= [0,46])
    map.show_config()
    map.render(r"D:\persenol\python\movie_map.html")
    

    #画片长与得分的散点图
    scatter = Scatter("豆瓣冷门佳片TOP200_片长与得分关系图", subtitle="074——作业九", width=1200, height=600)
    scatter.add("", d['time'].values,  d['score'].values, yaxis_max= '10', yaxis_min= '7.5')
    scatter.show_config()
    scatter.render(r"D:\persenol\python\movie_score.html")

---
# 实现效果
![豆瓣冷门佳片TOP200地区分布](1.png)
![豆瓣冷门佳片TOP200_片长与得分关系图](2.png)
---
# 所遇问题
1. 写入csv中文乱码：gb18030是更宽泛的unicode,可以防止中文乱码；
2. 写入csv有空行：设置参数dialect='unix'，可以防止有空行。




