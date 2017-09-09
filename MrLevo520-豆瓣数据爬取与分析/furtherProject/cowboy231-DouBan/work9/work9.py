# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import selenium.webdriver.support.ui as ui
#shift-tab多行缩进(左)
print 'please wait...system loading...'
PostUrl = "https://www.douban.com/"
driver=webdriver.Chrome()#用浏览器实现访问
driver_detail=webdriver.PhantomJS()
wait = ui.WebDriverWait(driver,15)
wait1 = ui.WebDriverWait(driver_detail,15)
driver.get(PostUrl)

def getDetails(url):

    driver_detail.get(url)
    wait1.until(lambda driver: driver.find_element_by_xpath("//div[@id='link-report']/span"))

def Write_txt(text1, text2,text3,text4,text5,title='douban.txt'):

    with open(title, "a") as f:
        print '开写'
        # print type(text1)
        # print type(text2)
        # print type(text3)
        # print type(text4)
        temp=str(text1)+"|"+text2+"|"+text3+"|"+text4+'|'+text5
        f.write(temp)
        f.write("\n")

def get_info(start):
    x=[]
    for i in range(20):
        x.append(start)
        start=start+1
    for i in x:
        #wait.until(lambda driver: driver.find_element_by_xpath("//div[@class='list']/a[%d]" % num))
        list_title = driver.find_element_by_xpath("//div[@class='list']/a[%d]" % i)
        print '----------------------------------------------' + 'NO' + str(
            i) + '----------------------------------------------'

        name = list_title.text
        name = name.split(' ', 1)
        name = name[0].encode('utf-8')

        print u'电影名: '
        print name
        print u'链接: ' + list_title.get_attribute('href')

        try:  # 获取具体内容和评论。href是每个超链接也就是资源单独的url
            getDetails(str(list_title.get_attribute('href')))
            strong = driver_detail.find_element_by_xpath('//*[@id="interest_sectl"]/div/div[2]/strong').text
            print u"分数" + strong
            PL = driver_detail.find_element_by_xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a').text
            PL = PL[:-3]
            print PL

            info = driver_detail.find_element_by_xpath('//*[@id="info"]').text
            info = info.split('\n', )
            print u"信息"
            Gz = info[4]
            Sj = info[6]
            Gz = Gz.split(" ")
            Sj = Sj.split(" ")
            Sj = Sj[1]
            if Gz[0] == u"官方网站:":
                Gz = info[5]
                Gz = Gz.split(" ")
                Sj = info[7]
            try:
                Sj = Sj.split('(')
                Sj = Sj[0]
            except:
                print '只有一个上映日期'
            Gz = Gz[1]

            Sj = Sj.encode("utf-8")
            Gz = Gz.encode("utf-8")
            PL = PL.encode("utf-8")
            strong = strong.encode("utf-8")
            print type(name)
            print type(Gz)
            Write_txt(name, strong, Gz, PL, Sj)
        except Exception as e:
            print e
            print 'can not get the details!'

print '---------------------------'
driver.find_element_by_xpath('//*[@id="anony-nav"]/div[1]/ul/li[2]/a').click()
print driver.window_handles
driver.switch_to_window(driver.window_handles[1])
time.sleep(1)
driver.find_element_by_xpath('//*[@id="db-nav-movie"]/div[2]/div/ul/li[3]/a').click()
time.sleep(1)
print driver.window_handles
wait.until(lambda driver: driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[2]/div[1]/form/div[1]/div[1]/label[6]'))
driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[2]/div[1]/form/div[1]/div[1]/label[6]').click()
#选择高分排序
driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[2]/div[1]/form/div[3]/div[1]/label[3]/input').click()
#开始爬取
num=600
# 打开几次“加载更多”
num_time = num / 20 + 1
wait.until(lambda driver: driver.find_element_by_xpath("//div[@class='list-wp']/a[@class='more']"))
starttime=1
for times in range(1, num_time):
    try:
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='list-wp']/a[@class='more']").click()
        time.sleep(1)
        t=num_time*20
        print '本次抓取的部分'
        print starttime, t
        get_info(starttime)
        starttime=starttime+20
    except Exception as e:
        print num_time
        print e
        break
    #wait.until(lambda driver: driver.find_element_by_xpath("//div[@class='list']/a[%d]" % num))