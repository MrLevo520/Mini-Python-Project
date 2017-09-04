**From  [Python+Selenium+PIL+Tesseract真正自动识别验证码进行一键登录](http://blog.csdn.net/mrlevo520/article/details/51901579)**

- Python 2.7
- IDE Pycharm 5.0.3
- Firefox浏览器：47.0.1
- Selenium：[Selenium的介绍及使用，强烈推荐@ Eastmount的博客](http://blog.csdn.net/eastmount/article/details/47825633)
- PIL : Pillow-3.3.0-cp27-cp27m-win_amd64.whl [PIL第三方库的下载](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pil)，[win下安装whl文件](http://www.cnblogs.com/2589-spark/p/4501816.html)
- Pytesser：依赖于PIL ，Tesseract [了解pytesser及基本使用](http://blog.sina.com.cn/s/blog_5d56279201017fta.html)
- Tesseract：3.0.2 [tesseract下载及安装](http://blog.csdn.net/wanghui2008123/article/details/37694307)


------

# 前言

> 自动登陆时候遇到验证码，采用Tesseract+PIL进行识别和自动填充，不让验证码成为我们自动化登录的阻碍，哈哈哈

------



# Talk is cheap, Show me the code

>  **自动识别验证码模拟登陆，注意是自动**，一键登录，不是那种扫出验证码，然后手动输入登录！首先来代码实现吧！

```
# -*- coding: utf-8 -*-
#Author：哈士奇说喵
from selenium import webdriver
import os
import pytesser
import sys,time
from PIL import Image,ImageEnhance

#shift+tab多行缩进(左)
reload(sys)
PostUrl = "http://yjsymis.hrbeu.edu.cn/gsmis/indexAction.do"

driver=webdriver.Firefox()
driver.get(PostUrl)


i=0
while 1:#sb登录系统，即使输对所有消息还是登不进去的，需要登录两次及以上

    i=i+1
    try:
        elem_user = driver.find_element_by_name('id')
        elem_psw = driver.find_element_by_name('password')
        elem_code = driver.find_element_by_name('checkcode')
    except:
        break
    #-------------------对验证码进行区域截图，好吧，这方法有点low------------------
    driver.get_screenshot_as_file('C:\Users\MrLevo\image1.jpg')#比较好理解
    im =Image.open('C:\Users\MrLevo\image1.jpg')
    box = (516,417,564,437)  #设置要裁剪的区域
    region = im.crop(box)     #此时，region是一个新的图像对象。
    #region.show()#显示的话就会被占用，所以要注释掉
    region.save("e:/image_code.jpg")

    #-------------------------------------------------------------------

    #--------------ImageGrab.grab()直接可以区域截图，但是有bug，截图不全-------
    '''
    bbox = (780, 0, 1020, 800)
    img = ImageGrab.grab()
    img.save("E:\image_code.jpg")
    img.show()
    '''
    #-------------------------手动输入验证码：适用范围更广，但不够方便------------------------------
    '''
    response = opener.open(CaptchaUrl)
    picture = response.read()
    with open('e:/image.jpg', 'wb') as local:
        local.write(picture)
    # 保存验证码到本地

    #------------对于不能用pytesser+ocr进行识别，手动打开图片手动输入--------
    # 打开保存的验证码图片 输入
    #SecretCode = raw_input('please enter the code: ')
    #----------------------------------------------------------------------
    '''

    #--------------------图片增强+自动识别简单验证码-----------------------------
    #time.sleep(3)防止由于网速，可能图片还没保存好，就开始识别
    def image_file_to_string(file):
        cwd = os.getcwd()
        try :
            os.chdir("C:\Users\MrLevo\Anaconda2\Lib")
            return pytesser.image_file_to_string(file)
        finally:
            os.chdir(cwd)
    im=Image.open("E:\\image_code.jpg")
    imgry = im.convert('L')#图像加强，二值化
    sharpness =ImageEnhance.Contrast(imgry)#对比度增强
    sharp_img = sharpness.enhance(2.0)
    sharp_img.save("E:\\image_code.jpg")
    #http://www.cnblogs.com/txw1958/archive/2012/02/21/2361330.html
    #imgry.show()#这是分布测试时候用的，整个程序使用需要注释掉
    #imgry.save("E:\\image_code.jpg")

    code= pytesser.image_file_to_string("E:\\image_code.jpg")#code即为识别出的图片数字str类型
    print code
    #打印code观察是否识别正确


    #----------------------------------------------------------------------
    if i <= 2: # 根据自己登录特性，我这里是验证码失败一次，重填所有，失败两次，重填验证码
        elem_user.send_keys('S315080092')
        elem_psw.send_keys('xxxxxxxxxx')

    elem_code.send_keys(code)
    click_login = driver.find_element_by_xpath("//img[@src='main_images/images/loginbutton.gif']")
    click_login.click()


#time.sleep(5)#搜索结果页面停留片刻
#driver.save_screenshot('C:\Users\MrLevo\image.jpg')
#driver.close()
#driver.quit()
```

# Show Gif ( :

> 第一次放动图，心理还有点小激动~

![这里写图片描述](http://img.blog.csdn.net/20160713193103690)

# 遇到问题及解决方法

1：验证码取得问题，因为每次刷新之后验证码动态刷新，所以如果不采用cookie的话（我还不太会用cookie）,根本捉不到元素，这个我在下篇文章中采用cookie来登录的，但不是调用浏览器，这个跑远了，下次说。
1：解决方案：用了`driver.get_screenshot_as_file`方法，机智的进行全截图，然后采用PIL中的crop进行再截图操作，可能有人会说，为什么不采用`ImageGrab.grab()`函数来做，好吧，因为这个函数在win10上尽然！截不了全图！！自己试了才知道，btw，我的分辨率1920x1080，难道和分辨率有关？反正这个我截了好久都没有成功，到最后才想到，截全部看看，结果，tmd只有一半，我说怎么都找不到要截图的部分！

------

2：验证码验证错误率高问题
2：解决方案，采用PIL强大的图像处理功能，我先将图片二值化，本来是蓝色字体的，，然后再进行对比度强化来锐化图片，然后再调用Tesseract.exe进行处理，提高的识别精度不是一点两点：看图比较，左1是用cookie抓的原图，右边是全景截图，再定位截图，再进行二值化和锐化处理的图，本来我想着用matlab做图像识别的，但是想想还要调用，感觉有点麻烦。。。

![这里写图片描述](http://img.blog.csdn.net/20160713202718096)

------

3：调用Tesseract.exe问题
3：解决方案因为程序执行图像识别需要调用Tesseract.exe，所以必须把路径切到有这个exe的路径下，刚开始，以为和包依赖，结果根本没有识别出任何图！折腾一个多小时才写好验证码识别的问题----单独测试的确很重要，记一笔！
![这里写图片描述](http://img.blog.csdn.net/20160713211043265)

------

4：登录失败问题--mdzz学校教务系统二次验证
4：解决方案，写了一个while循环，把主程序很大部分都扔进去了，目的也很明确，如果第一次登录失败，再重复进行登录，注意采用try试探元素是否仍然存在，except来抛出break结束循环，因为登录成功后，比如说`driver.find_element_by_name('id')`是不存在的！所以当这个元素在登陆后的界面找不到时，那就说明登录成功，ok，跳出循环，进行下一步操作。

------

5：明明图片已截取，为什么没有识别
5：解决方案，这个我真的没想到，我一直以为可能因为save时候还没下载好，导致库中没有这张图，那就不能识别，但是我用time.sleep函数让它停下来缓缓，还是不行，我就很无语了，想了半天，可能是因为图片被占用！因为我有一个img.show()函数，为了检测有没有截取到标准的图，然后show之后这个图像就被占用了！就像你在编辑word时候，是无法删除word文档一样！果然在注释掉show之后，一切可行，真是差错查了小半天啊！！
![这里写图片描述](http://img.blog.csdn.net/20160713211120437)

------

6：元素一切就位，为什么不执行操作
6：解决方案，这个有点脑残了，不过的确是我遇到的，还是记上一笔，然后骂自己一遍sb，没有click()你让它怎么处理！！！就像用cookie登录时候还有个ENTRY呢！

------

7：两次验证失败后，用户名重复累加
7：解决方案，直接加了个变量，计数循环次数，观察到只要超过两次没有登录上，就会累加登录名和用户密码，直接写了个if进行判断，完事！

------

8：im.crop(box)裁剪区域选择困难症
8：解决方案，多试几次，反正我是试出来的。。。。当然，你点击图片进行审查元素时候，可以看到图片大小，那么，你就可以知道横纵坐标差值多少，但是大范围区域还得自己试，如有更好的办法，请告知，以下为我截图实验次数，次数30+
![这里写图片描述](http://img.blog.csdn.net/20160713204507521)

------

9：导入不了Image,ImageEnhance
9：解决方案，因为PIL用的是第三方库，所以，采用的导入方式是这样的，多看看官方文档就可以，官方描述如下
`Use `from PIL import Image` instead of `import Image`. `

------

10：找不到应该键入的元素
10：这个问题，请单击要输入的空白处右键，审查元素，就可以看到，然后根据`driver.find_element_by_`各种方法来定位元素，如果输入进行了隐藏，在当前页面找不到怎么办，就像如下图，需要先点击我的图书馆，才能看到输入的账户和密码，那么先找我的图书馆的元素，进行click操作，之后再找元素，一句话，把自己想成浏览器，阿不，把python想成浏览器。。。。。

![这里写图片描述](http://img.blog.csdn.net/20160713193212394)

上图的代码我也放上，大同小异，比有验证码的简单，但是多了一个click操作。

```
# -*- coding: utf-8 -*-
#Author：哈士奇说喵
from selenium import webdriver
import time
import sys


#shift+tab多行缩进(左)
reload(sys)
PostUrl = "http://lib.hrbeu.edu.cn/#"
driver=webdriver.Firefox()
driver.get(PostUrl)

elem_user = driver.find_element_by_name('number')
elem_psw = driver.find_element_by_name('passwd')

#选择我的图书馆，点击后才能看到输入账号密码
click_first = driver.find_element_by_xpath("//ul[@id='imgmenu']/li[4]")
click_first.click()
elem_user.send_keys('S315080092')
elem_psw.send_keys('xxxxxxxx')

#点击登录
click_second = driver.find_element_by_name('submit')
click_second.click()

time.sleep(5)
#登陆后选择
click_third = driver.find_element_by_xpath("//*[@id='mainbox']/div/div/ul/li/a")
click_third.click()

time.sleep(5)#搜索结果页面停留片刻
#driver.save_screenshot('C:\Users\MrLevo\image.jpg')

driver.close()
driver.quit()
```



------



# 致谢



- [tesseract-ocr识别英文和中文图片文字以及扫描图片实例讲解 ](http://blog.csdn.net/wanghui2008123/article/details/37694307)
- [用pytesser作图片验证码识别 ](http://blog.sina.com.cn/s/blog_5d56279201017fta.html)
- [  [Python爬虫] Selenium实现自动登录163邮箱和Locating Elements介绍 ](http://blog.csdn.net/eastmount/article/details/47825633)
- [ [Python爬虫] Selenium自动访问Firefox和Chrome并实现搜索截图 ](http://blog.csdn.net/eastmount/article/details/47799865)
- [初试PIL及基本操作 ](http://blog.csdn.net/yockie/article/details/8498301)
- [Python爬虫模拟登录带验证码网站_手动输入验证码版本](http://www.jb51.net/article/78498.htm)
- [selenium-webdriver(python) (十五) -- 鼠标事件](http://www.cnblogs.com/fnng/p/3288444.html)