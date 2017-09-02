***From [Python自定义豆瓣电影种类，排行，点评的爬取与存储（初级）](http://blog.csdn.net/mrlevo520/article/details/51966992)***

> 更多豆瓣系列文章请看→_→[豆瓣数据爬取与分析及gui的制作](http://blog.csdn.net/column/details/16324.html)

- Python  2.7
- IDE Pycharm 5.0.3
- Firefox 47.0.1

> 具体Selenium和PhantomJS配置及使用请看[调用PhantomJS.exe自动续借图书馆书籍](http://blog.csdn.net/mrlevo520/article/details/51930741)



----------
    网上一溜豆瓣TOP250---有意思么？
----------

起因
--
> 就是想写个豆瓣电影的爬取，给我电影荒的同学。。。。当然自己也练手啦

----------


目的
--
1. 根据用户输入，列出豆瓣高分TOP(用户自定义)的电影，链接，及热评若干。
2. 制作不需要Python环境可运行的exe，但由于bug未修复，需要火狐浏览器支持

----------

方案
--
>  使用PhantomJS+Selenium+Firefox实现

----------

实现过程
----
1. get到首页后，根据选择，点击种类，然后根据输入需求，进行排序
2. 抓取每个电影及超链接，进入超链接后，抓取当前电影的热评及长评
3. 当用户所要求TOP数目大于第一页的20个时候，点击加载更多，再出现20个电影，重复2操作

> 以豆瓣高分，然后按评分排序的点击过程（其余操作一致，先种类后排序选择，再爬）

![这里写图片描述](http://img.blog.csdn.net/20160719165615514)

----------


实现代码
----

```
# -*- coding: utf-8 -*-
#Author:哈士奇说喵
#爬豆瓣高分电影及hot影评

from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time


print "---------------system loading...please wait...---------------"
SUMRESOURCES = 0 #全局变量
driver_detail = webdriver.PhantomJS(executable_path="phantomjs.exe")
#driver_item=webdriver.PhantomJS(executable_path="phantomjs.exe")
driver_item=webdriver.Firefox()
url="https://movie.douban.com/"
#等待页面加载方法
wait = ui.WebDriverWait(driver_item,15)
wait1 = ui.WebDriverWait(driver_detail,15)


#获取URL和文章标题

def getURL_Title():
    global SUMRESOURCES

##############################################################################
#需要键入想要获取的信息，比如种类，排序方式，想看多少内容
##############################################################################

    print "please select:"
    kind=input("1-Hot\n2-Newest\n3-Classics\n4-Playable\n5-High Scores\n6-Wonderful but not popular\n7-Chinese film\n8-Hollywood\n9-Korea\n10-Japan\n11-Action movies\n12-Comedy\n13-Love story\n14-Science fiction\n15-Thriller\n16-Horror film\n17-Cartoon\nplease select:")
    print "--------------------------------------------------------------------------"
    sort=input("1-Sort by hot\n2-Sort by time\n3-Sort by score\nplease select:")
    print "--------------------------------------------------------------------------"
    number = input("TOP ?:")
    print "--------------------------------------------------------------------------"
    ask_long=input("don't need long-comments,enter 0,i like long-comments enter 1:")
    print "--------------------------------------------------------------------------"
    global save_name
    save_name=raw_input("save_name (xx.txt):")
    print "---------------------crawling...---------------------"

    driver_item.get(url)

##############################################################################
#进行网页get后，先进行电影种类选择的模拟点击操作，然后再是排序方式的选择
#最后等待一会，元素都加载完了，才能开始爬电影，不然元素隐藏起来，不能被获取
#wait.until是等待元素加载完成！
##############################################################################

    wait.until(lambda driver: driver.find_element_by_xpath("//div[@class='fliter-wp']/div/form/div/div/label[%s]"%kind))
    driver_item.find_element_by_xpath("//div[@class='fliter-wp']/div/form/div/div/label[%s]"%kind).click()
    wait.until(lambda driver: driver.find_element_by_xpath("//div[@class='fliter-wp']/div/form/div[3]/div/label[%s]"%sort))
    driver_item.find_element_by_xpath("//div[@class='fliter-wp']/div/form/div[3]/div/label[%s]"%sort).click()

    num=number+1#比如输入想看的TOP22，那需要+1在进行操作，细节问题
    time.sleep(2)

    #打开几次“加载更多”
    num_time = num/20+1
    wait.until(lambda driver: driver.find_element_by_xpath("//div[@class='list-wp']/a[@class='more']"))

    for times in range(1,num_time):
        time.sleep(1)
        driver_item.find_element_by_xpath("//div[@class='list-wp']/a[@class='more']").click()
        time.sleep(1)
        wait.until(lambda driver: driver.find_element_by_xpath("//div[@class='list']/a[%d]"%num))
        #print '点击\'加载更多\'一次'

    #使用wait.until使元素全部加载好能定位之后再操作，相当于try/except再套个while把

    for i in range(1,num):
        wait.until(lambda driver: driver.find_element_by_xpath("//div[@class='list']/a[%d]"%num))
        list_title=driver_item.find_element_by_xpath("//div[@class='list']/a[%d]"%i)
        print '----------------------------------------------'+'NO' + str(SUMRESOURCES +1)+'----------------------------------------------'
        print u'电影名: ' + list_title.text
        print u'链接: ' + list_title.get_attribute('href')
        #print unicode码自动转换为utf-8的


        #写入txt中部分1
        list_title_wr=list_title.text.encode('utf-8')#unicode码，需要重新编码再写入txt
        list_title_url_wr=list_title.get_attribute('href')

        Write_txt('\n----------------------------------------------'+'NO' + str(SUMRESOURCES +1)+'----------------------------------------------','',save_name)
        Write_txt(list_title_wr,list_title_url_wr,save_name)

        SUMRESOURCES = SUMRESOURCES +1

        try:#获取具体内容和评论。href是每个超链接也就是资源单独的url
            getDetails(str(list_title.get_attribute('href')),ask_long)
        except:
            print 'can not get the details!'


##############################################################################
#当选择一部电影后，进入这部电影的超链接，然后才能获取
#同时别忽视元素加载的问题
#在加载长评论的时候，注意模拟点击一次小三角，不然可能会使内容隐藏
##############################################################################
def getDetails(url,ask_long):

    driver_detail.get(url)
    wait1.until(lambda driver: driver.find_element_by_xpath("//div[@id='link-report']/span"))
    drama = driver_detail.find_element_by_xpath("//div[@id='link-report']/span")
    print u"剧情简介："+drama.text
    drama_wr=drama.text.encode('utf-8')
    Write_txt(drama_wr,'',save_name)
    print "--------------------------------------------Hot comments TOP----------------------------------------------"
    for i in range(1,5):#四个短评
        try:
            comments_hot = driver_detail.find_element_by_xpath("//div[@id='hot-comments']/div[%s]/div/p"%i)
            print u"最新热评："+comments_hot.text
            comments_hot_wr=comments_hot.text.encode('utf-8')
            Write_txt("--------------------------------------------Hot comments TOP%d----------------------------------------------"%i,'',save_name)
            Write_txt(comments_hot_wr,'',save_name)
        except:
            print 'can not caught the comments!'


    #加载长评
    if ask_long==1:
        try:
            driver_detail.find_element_by_xpath("//img[@class='bn-arrow']").click()
            #wait.until(lambda driver: driver.find_element_by_xpath("//div[@class='review-bd']/div[2]/div/div"))
            time.sleep(1)
            #解决加载长评会提示剧透问题导致无法加载
            comments_get = driver_detail.find_element_by_xpath("//div[@class='review-bd']/div[2]/div")
            if comments_get.text.encode('utf-8')=='提示: 这篇影评可能有剧透':
                comments_deep=driver_detail.find_element_by_xpath("//div[@class='review-bd']/div[2]/div[2]")
            else:
                comments_deep = comments_get
            print "--------------------------------------------long-comments---------------------------------------------"
            print u"深度长评："+comments_deep.text
            comments_deep_wr=comments_deep.text.encode('utf-8')
            Write_txt("--------------------------------------------long-comments---------------------------------------------\n",'',save_name)
            Write_txt(comments_deep_wr,'',save_name)
        except:
            print 'can not caught the deep_comments!'


##############################################################################
#将print输出的写入txt中查看，也可以在cmd中查看，换行符是为了美观
##############################################################################
def Write_txt(text1='',text2='',title='douban.txt'):

        with open(title,"a") as f:
            for i in text1:
                f.write(i)
            f.write("\n")
            for j in text2:
                f.write(j)
            f.write("\n")

def main():

    getURL_Title()
    driver_item.quit()

main()

```

上面的代码是可以实现的，但需要Firefox的配合，因为我其中一个引擎调用了Firefox，另一个抓评论的用了PhantomJS。

----------


实现效果
----
这里直接上传打包成exe后的形式，如何打包exe请看[将python打包成exe](http://blog.csdn.net/mrlevo520/article/details/51840217)

![这里写图片描述](http://img.blog.csdn.net/20160720171437296)

> 存入的txt文件

![这里写图片描述](http://img.blog.csdn.net/20160720171618984)

> 因为打包成exe必须是中文的键入，所以没办法，我改成英文来着，不然会出现这种情况。。。

![这里写图片描述](http://img.blog.csdn.net/20160720171716187)

> 输出内容是没有问题的。。。。。。

----------


问题及解决方案
----

Q: 使用PhantomJS和Firefox出现不同效果的问题，第21个回到起点。

A:  解决方案，暂且我也没有找到，只有调用Firefox然后完事后再关闭，分析请见[伪解决Selenium中调用PhantomJS无法模拟点击(click)操作 ](http://blog.csdn.net/mrlevo520/article/details/51958161)

----------
Q: 在对unicode输出在txt出现的问题，但是在print可以直接中文输出的。

A:  解决方案：详见[Python输出(print)内容写入txt中保存 ](http://blog.csdn.net/mrlevo520/article/details/51967311)

----------


Pay Attention
-------------
>  这里和上篇[  伪解决Selenium中调用PhantomJS无法模拟点击(click)操作 ](http://blog.csdn.net/mrlevo520/article/details/51958161)

这里解决的问题和昨天的Pay Attention是一样的，本来程序也是增强性补充而已，所以重复了。

Q: 元素无法定位问题

A: 首先查看是不是隐藏元素，其次再看自己的规则有没有写错，还有就是是不是页面加载未完成，详见[解决网页元素无法定位（NoSuchElementException: Unable to locate element）的几种方法 ](http://blog.csdn.net/mrlevo520/article/details/51954203)

----------
Q: 只采集自己需要的数据，剔除无用数据，比如说，刚开始我用

```
driver_detail.find_elements_by_xpath
```

然后写个取出list中元素的方法，但是这样的话，一个便签下内容未必太多，并不是我想要的如图：

![这里写图片描述](http://img.blog.csdn.net/20160719172858533)

比如说，我只想要红色的部分，那么，采取elements就不太好处理。

A:  我采用的方法是格式化字符串！这个方法我在[Selenium+PhantomJS自动续借图书馆书籍（下）](http://blog.csdn.net/mrlevo520/article/details/51930741)也用过，根据元素的特性，可以发现，每个热评的正文标签不一样的，其余标签一样，只要格式化正文标签即可，像这样

```
for i in range(1,5):#取了前四条热评
        try:
            comments = driver_detail.find_element_by_xpath("//div[@id='hot-comments']/div[%s]/div/p"%i)
            print u"最新热评："+comments.text
        except:
            print 'can not caught comments!'
```

----------
Q:  一个引擎干有个事！我现在没办法，只有将第一个需要处理的页面用Firefox来处理，之后评论用PhantomJS来抓取，之后可以用quit来关闭浏览器，但是启动浏览器还是会耗费好多资源，而且挺慢，虽然PhantomJS也很慢，我12G内存都跑完了。。。。。。看样子是给我买8x2 16G双通道的借口啊。

----------
Q:  备注不标准也会导致程序出错，这个是我没想到的，我一直以为在'''备注'''之间的都可以随便来，结果影响程序运行了，之后分模块测试才注意到这个问题，也是以前没有遇到过的，切记！需要规范自己代码，特别是像Python这样缩进是灵魂的语言。。。。

----------
Q:  补充，**长评论的抓取**

![这里写图片描述](http://img.blog.csdn.net/20160720174033625)

这是点击之后的图，可以看到元素定位也是不一样的，注意

![这里写图片描述](http://img.blog.csdn.net/20160720174050807)

----------

致谢
--
- [@MrLevo520--伪解决Selenium中调用PhantomJS无法模拟点击(click)操作](http://blog.csdn.net/mrlevo520/article/details/51958161)
- [@MrLevo520--Python输出(print)内容写入txt中保存](http://blog.csdn.net/mrlevo520/article/details/51967311)
- [@MrLevo520--解决网页元素无法定位（NoSuchElementException: Unable to locate element）的几种方法  ](http://blog.csdn.net/mrlevo520/article/details/51954203)
- [@Eastmount--[Python爬虫] Selenium+Phantomjs动态获取CSDN下载资源信息和评论 ](http://blog.csdn.net/eastmount/article/details/47907341)
- [@Eastmount--[Python爬虫] 在Windows下安装PIP+Phantomjs+Selenium ](http://blog.csdn.net/eastmount/article/details/47785123)
- [@MrLevo520--解决Selenium弹出新页面无法定位元素问题（Unable to locate element）](http://blog.csdn.net/mrlevo520/article/details/51926145)





