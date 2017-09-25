- Python  3.6
- Jupyter Notebook 5.0
- ECharts

----------

起因
--
> DT君Python精英群作业，学习使用n-gram，分析了奥巴马第二任期内4次白宫记者招待会晚宴演讲。

----------

目的
--
1. 学习调试n-gram
2. 使用ECharts进行结果展示
3. 使用1-gram分析4次演讲的听众反映，（Laughter and Applause）

----------

数据说明及展示
----

演讲记录中会根据实际情况标注听众laughter和applause的情况。使用1-gram简单统计，能够得出段子手奥巴马的2016年演讲“笑果”最好。

首先，2016年演讲中的laughter及applause次数均为历年之最。

![听众反映计数](https://raw.githubusercontent.com/ZLFlyApple/DTTest/master/%E5%90%AC%E4%BC%97%E5%8F%8D%E6%98%A0%E8%AE%A1%E6%95%B0.png)

再考虑到每年演讲长度不同：

![字数](https://raw.githubusercontent.com/ZLFlyApple/DTTest/master/wordscount.png)

我们再计算laughter及applause的频次（即平均多少个words会有一次laughter或applause），也会发现2016年演讲的“笑果”最密集。

![听众反映频次统计](https://raw.githubusercontent.com/ZLFlyApple/DTTest/master/%E5%90%AC%E4%BC%97%E5%8F%8D%E6%98%A0%E9%A2%91%E6%AC%A1%E7%BB%9F%E8%AE%A1.png)


----------


代码及文本数据
----

均包含在本文件夹中。

----------

参考
----
- MrLevo520
- 《Python网络数据采集》
- 文本来源 https://obamawhitehouse.archives.gov/

