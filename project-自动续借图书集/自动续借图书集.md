- Python 2.7 
- IDE Pycharm 5.0.3
- Firefox浏览器：47.0.1

>  具体环境，Selenium及PhantomJS使用等看我前一篇博客[Python+Selenium+PIL+Tesseract真正自动识别验证码进行一键登录 ](http://blog.csdn.net/mrlevo520/article/details/51901579)

----------

# 上篇

吐槽
--

	自从我欠图书馆6块钱的过期书后，立马要写一个自动续约的小工具压压惊
----------


目的
--

自动实现图书馆借书籍的书单截图，并一键续约全部书籍，我登录校图书馆的目的无非就这两个咯，我才不去预约没有的书呢--反正没有一次预约成功过0.0

----------


实现方法
----

Selenium+PhantonJS自动化脚本执行

----------


实现方案
----

1. 采用Firefox浏览器进行模拟登录，这个比较酷炫把，可以看着浏览器自己在那边跑，欢快的停不下来。。。
2. 调用PhantomJS.exe，不展现浏览器的运作，直接在cmd窗口跑（用pyinstaller打包成exe后有cmd窗）

----------


方案实现过程
-------

1.采用Selenium+Firefox方式：
先来个最后成品动图：
![这里写图片描述](http://img.blog.csdn.net/20160716154214757)

（自从剪成动图之后，根本停不下来。更加生动形象有木有！）

----------


然后来程序代码--主模块（被调用模块，也可单独执行）

```
# -*- coding: utf-8 -*-
#Author:哈士奇说喵

from selenium import webdriver
import time

#shift-tab多行缩进(左)
print 'please wait...system loading...'
#reload(sys)

PostUrl = "http://lib.hrbeu.edu.cn/#"

driver=webdriver.Firefox()#用浏览器实现访问
#driver = webdriver.PhantomJS(executable_path="phantomjs.exe")#没用浏览器
driver.get(PostUrl)

elem_user = driver.find_element_by_name('number')
elem_psw = driver.find_element_by_name('passwd')


#选择我的图书馆，点击后才能看到输入账号密码
click_first = driver.find_element_by_xpath("//ul[@id='imgmenu']/li[4]")
click_first.click()
elem_user.send_keys('S315080092')
elem_psw.send_keys('xxxxxxxxx')

#点击登录
click_second = driver.find_element_by_name('submit')
click_second.click()
print 'log in...'
time.sleep(1)

#定位新页面元素，将handle重定位即可

driver.switch_to_window(driver.window_handles[1])#定位弹出的第一个页面，也就是当前页面
#sreach_window = driver.current_window_handle  #此行代码用来定位当前页面#不可行
driver.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[3]/a").click()
driver.save_screenshot('image_booklist_firefox.jpg')
print 'turning to the mylib...'
time.sleep(1)#搜索结果页面停留片刻

#driver.switch_to_window(driver.window_handles[1])
#没有跳出新窗口就是在同一页面的！
for i in range(2,30):#这里限定是29本书，一般我们都不会借那么多书的
    try:
        #driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/table/tbody/%s/td[8]/div/input"%('tr[%s]'%i)).click()#下面的比较好理解
        driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/table/tbody/tr[%s]/td[8]/div/input"%i).click()
        print 'renewing...the %d\'th book renewed '%(i-1)
    except:
        print '%d books have been renewed !'%(i-2)
        a=i-2
        time.sleep(4)
        driver.save_screenshot('image_done_firefox.jpg')
        print 'the picture is saving...'
        print 'done!'
        break

time.sleep(1)

driver.close()
driver.quit()
```

调用上述模块的主执行函数（其实就是为了封装上述模块而已，封装成gui界面，为后续的打包做准备，如何打包请见博文[将自己的python程序打包成exe(秀同学一脸呐)  
 ](http://blog.csdn.net/mrlevo520/article/details/51840217)）：

```
# -*- coding: utf-8 -*-
#Author:哈士奇说喵

from Tkinter import *
import tkMessageBox#执行gui窗
import time

def check_renew():
    print 'checking and renewing...'
    tkMessageBox.showinfo('提示','即将开启装逼模式，请确认已安装Firefox浏览器')
    #time.sleep(4)
    import Selenium_PhantomJS_lib_firefox
    tkMessageBox.showinfo('提示','已执行成功!\n(截图已保存于程序目录)')



#主框架部分
root = Tk()
root.title('图书馆查询续约(哈尔滨工程大学专版)--by 哈士奇说喵')
label=Label(root,text='   图书馆一键查询与续约Firefox版本 (✪ω✪)  ')
button_check=Button(root,text='查询书单并续期━Σ(ﾟДﾟ|||)━开启Firefox有形装逼模式 ',background='green',command=check_renew)

label.pack()
button_check.pack()
root.mainloop()
```
实现效果如图所示：
![这里写图片描述](http://img.blog.csdn.net/20160716154059598)

程序中的注释相信可以把程序解释的差不多了把。。。。

----------


遇到问题和解决方案
---------

1.selenium对新页面元素无法定位抛出
```
NoSuchElementException: Message: Unable to locate element
```
错误，导致无法进行对新的界面进行点击操作。
1.解决方案：专门写了一篇博客，请见
[解决Selenium弹出新页面无法定位元素问题（Unable to locate element）](http://blog.csdn.net/mrlevo520/article/details/51926145)

----------
2.对打包后的版本无法运行，抛出如图错误Errno 10054
![这里写图片描述](http://img.blog.csdn.net/20160716210003855)
2.解决方案：暂未找到解决方案，exe文件不可用，程序执行可用

----------
3.对未知书籍数目重复点击操作，代码冗余
3.解决方案：因为点击续借按钮的元素每个都不一样，通过观察可知其中的规律，之后就知道在那进行修改，但是，光修改的话，十本书就有十个相似的代码串，很不pythontic，所以，采用格式化字符串的方式进行for循环带入，方便又漂亮！

----------
4.使用了1中的解决方案还是不能定位元素
4.可能查找元素的方式出现错误，我现在的使用方法是采用xpath的方式来找，比如说这样
```
driver.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[3]/a")
```
虽然看起来有点长，但是元素相当好找，而且定位很准，如果采用类似这种`driver.find_element_by_xpath("//ul[@id='imgmenu']/li[4]")`，我现在还不能很好地驾驭，出错可能性有点大，下次要多进行尝试。

----------

下篇预告
----

实现方案二，调用PhantomJS.exe，不展现浏览器的运作，直接在cmd窗口跑（用pyinstaller打包成exe后有cmd窗）



----

----

# 下篇

接着上篇
----

[Selenium+PhantomJS自动续借图书馆书籍（上）  
 ](http://blog.csdn.net/mrlevo520/article/details/51924757)接下来实现方案二的构思：
调用PhantomJS.exe，不展现浏览器的运作，直接在cmd窗口跑（用pyinstaller打包成exe后有cmd窗）

----------

方案实现过程
-------

### 效果

![这里写图片描述](http://img.blog.csdn.net/20160717084320058)

### 代码

> 被调模块（可单独执行）

```
# -*- coding: utf-8 -*-
#Author:哈士奇说喵

from selenium import webdriver
import time
import sys
from PIL import Image
#shift-tab多行缩进(左)
print 'please wait...system loading...'
reload(sys)

PostUrl = "http://lib.hrbeu.edu.cn/#"

driver = webdriver.PhantomJS(executable_path="phantomjs.exe")#没用浏览器
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
print 'log in...'
time.sleep(1)

#定位新页面元素，将handle重定位即可

driver.switch_to_window(driver.window_handles[1])#定位弹出的第一个页面，也就是当前页面
driver.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[3]/a").click()
driver.save_screenshot('image_booklist.jpg')
print 'turning to the mylib...'
time.sleep(1)#搜索结果页面停留片刻

#driver.switch_to_window(driver.window_handles[1])
#没有跳出新窗口就是在同一页面的！
for i in range(2,30):#这里限定是29本书，一般我们都不会借那么多书的
    try:
        driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/table/tbody/%s/td[8]/div/input"%('tr[%s]'%i)).click()
        print 'renewing...the %d\'th book renewed '%(i-1)
    except:
        print '%d books have been renewed !'%(i-2)
        a=i-2
        time.sleep(4)
        driver.save_screenshot('image_done.jpg')
        print 'the picture is opening...please wait...'
        break
time.sleep(2)
driver.close()
driver.quit()

def show_img():
    im_check=Image.open('image_booklist.jpg')
    im_check.show()
    im_done =Image.open('image_done.jpg')
    im_done.show()
```
>  然后是程序入口

```
# -*- coding: utf-8 -*-
#Author:哈士奇说喵

from Tkinter import *
import tkMessageBox

def check_renew():
    print 'checking and renewing...'
    tkMessageBox.showinfo('提示','执行速度取决于网速和电脑，能等着就按"确定"\n(请允许phantomjs.exe访问网络)\nBTW 你现在按啥都不好使，程序照样执行（*゜Д゜）σ凸')
    from Selenium_PhantomJS_lib import show_img
    show_img()#show一下预约前和预约后截图，好确认
    tkMessageBox.showinfo('提示','已执行成功!\n(若没有弹出图片则请自行打开程序目录)')

#主框架部分
root = Tk()
root.title('图书馆查询续约(哈尔滨工程大学专版)--by 哈士奇说喵')
label=Label(root,text='   图书馆一键查询与续约cmd版本 (✪ω✪)  ')
button_check=Button(root,text='查询书单并续期━Σ(ﾟДﾟ|||)━开启cmd无形装逼模式 ',background='green',command=check_renew)

label.pack()
button_check.pack()
root.mainloop()
```
>  之后启动的画面应该是这样的

![这里写图片描述](http://img.blog.csdn.net/20160717084827560)

>  最后完成的画面应该是这样的，截图，确认框，cmd窗口，一个都不少；

![这里写图片描述](http://img.blog.csdn.net/20160717084911670)

----------



原理和上篇并没有什么区别，只是调用了一个`phantomjs.exe`文件而已，实际上的处理都是这个exe在进行处理的，所以，在进行打包的时候，打包出来的exe需要和此文件在一个文件夹下才可以，就像这样

![这里写图片描述](http://img.blog.csdn.net/20160717085228015)

而如何用pyinstaller进行打包操作请见[如何将python程序打包成exe](http://blog.csdn.net/mrlevo520/article/details/51840217)

----------

遇到问题和解决方案
----------

1.找不到执行文件，phantomjs.exe
1.解决方案：把phantomjs.exe添加到工作路径下，最方便的方法就是，你的工程在哪，直接添加到工程文件夹下就可以了

----------
2.截图的图片没有显示出来，或者提示”在禁用UAC时无法激活此应用“
2.解决方案：图片有没有显示，可以看有没有调用show方法，如果调用了，那在自己电脑测试肯定是没有问题的，我在测试别的电脑的时候遇到UAC问题，直接启用就可以了，一般没有问题的，如果不想麻烦启动，那就直接去工作文件夹下手动打开看，截图已保存在本地的工作路径下的。

----------

最后
--
这个程序是可以打包在别的电脑进行运行的，不过账号和密码我都直接输在程序里面了，而且也只是我自己学校的专版，主要还是自己用，如果有哈尔滨工程大学的小伙伴想用，可联系我，或者你只要自己改个账号密码参数就可以了，前提是你有完整的python开发环境。

----------

灵感来源与致谢
----
[@崔庆才--Python爬虫实战七之计算大学本学期绩点](http://cuiqingcai.com/997.html)
[@崔庆才--Python爬虫利器五之Selenium的用法](http://cuiqingcai.com/2599.html)
[@崔庆才--Python爬虫利器四之PhantomJS的用法](http://cuiqingcai.com/2577.html)
[@milkty--webdriver（python）学习笔记一 ](http://www.cnblogs.com/kongzhongqijing/p/3532082.html?utm_source=tuicool&utm_medium=referral)
[@buptlrw--Python抓取网页动态数据——selenium webdriver的使用 ](http://blog.csdn.net/buptlrw/article/details/48828201)

