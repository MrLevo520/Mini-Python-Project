***From  [Python基于Tkinter的二输入规则器(乞丐版)](http://blog.csdn.net/mrlevo520/article/details/51812096)***

- Python 2.7
- IDE Pycharm 5.0.3

------

```
有想法就去做，等等等等就没机会了
```



------

## 起因

> ​	昨天接触了Tkinter框架，之后就迫不及待的想写个计算器出来，结果呢，可想而知了，当初自己犟脾气，掌握几个语法后就想什么都不参考写自己的一段四则运算器出来，结果。。。。。。花了我一天时间，我竟然歪打正着写了个规则器出来窝草。。。。

------



## 对比

> ​	贴个图，别人家的计算器是这样的；而且用了五十行，说的貌似很了不起的样子（老纸的规则器，只要40-就可以！不算上Scrollbar，分割子框架这类的）

![你们认为的‘计算器’](http://upload-images.jianshu.io/upload_images/2671133-ddcfd9df5f6bb6cc?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 大家计算器都一个模样，大家都是一个idea么？还是局限于计算机就应该这样，本小白不服！

![吼吼](http://upload-images.jianshu.io/upload_images/2671133-b7af6424ab0b8634?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

------

## But

>  我的规则器是这样的。。。。

![规则器](http://upload-images.jianshu.io/upload_images/2671133-334ebc80c9070bd1?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
我知道布局排丑了，不要在意这些细节好么0.0



## 说说优点

1，以计算器角度说，能完美实现计算，而且带标号，记录存储等功能，知道上一步计算结果。

2，最大的优点在于二输入，调用各种def的函数，而四则运算只是最简单的函数而已，比如说我又写了字符串连接函数，相似度比较函数等等，做个实例而已，大家可以大开脑洞

------

## 缺点

1，需要键盘输入，与普通计算器按键输入不同

2，我的代码冗余量比较大，因为自己需要看懂，所以不像别的教程那样直接跟着lambda和pack，一长串的，不利于我们这种小白读。等我水平再高一些，或许我也会采用lambda，这样才够pythontic~

------

## 后续

1.本身在做分类聚类方面的课题，结合这个规则器，我完全可以把k-means中的k参数在交互界面上输入，这样就不用每次上程序里面改了！还有DBSCAN里面的Eps和MinPts也可以直接用这个框架！！想想有点小激动呢！(挖的坑不计其数)

2.需要优化下布局，尝试用grid来做，感觉pack里面参数略多啊。

------

## 构思框架

放代码之前，先来设计思路，我设计了两个框架，输入和输出在两个框架上，这样便于写代码思路清晰，框架大概是这样的；
![框架结构](http://upload-images.jianshu.io/upload_images/2671133-a4236fa14580a55a?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

------

## 代码

此代码(就算再烂)绝此一家，别无分店哈哈

```
#-------------------二输入规则计算器--------------------
#Author：哈士奇说喵(第一次署名有点怕)
# -*- coding: utf-8 -*-
from Tkinter import *
import difflib
#主框架部分
root = Tk()
root.title('乞丐版规则器0.0')
root.geometry()
Label_root=Label(root,text='规则运算(根框架)',font=('宋体',15))

#-----------------------定义规则------------------------

def Plus(a,b):
    return round(a+b, 2)

def Sub(a,b):
    return round(a-b,2)

def Mult(a,b):
    return round(a*b, 2)

def Div(a,b):
    return round(a/b, 2)

def P_str(a,b):
    return a+b

def Rep(a,b):
    return difflib.SequenceMatcher(None,a,b).ratio()
    #difflib可以看看其中的定义，计算匹配率的

#还可以继续增加规则函数，只要是两输入的参数都可以
#----------------------触发函数-----------------------

def Answ():#规则函数

    if lb.get(lb.curselection()).encode('utf-8') == '加':
        Ans.insert(END,'规则:+ ->'+str(Plus(float(var_first.get()),float(var_second.get()))))
    if lb.get(lb.curselection()).encode('utf-8')=='减':
        Ans.insert(END,'规则:- ->'+str(Sub(float(var_first.get()),float(var_second.get()))))
    if lb.get(lb.curselection()).encode('utf-8')=='乘':
        Ans.insert(END,'规则:x ->'+str(Mult(float(var_first.get()),float(var_second.get()))))
    if lb.get(lb.curselection()).encode('utf-8')=='除':
        Ans.insert(END,'规则:/ ->'+str(Div(float(var_first.get()),float(var_second.get()))))
    if lb.get(lb.curselection()).encode('utf-8')=='字符串连接':
        Ans.insert(END,'规则：字符串连接 ->' +P_str(var_first.get(),var_second.get()).encode('utf-8'))
    if lb.get(lb.curselection()).encode('utf-8')=='字符串相似度':
        Ans.insert(END,'规则:字符串相似度 ->'+str(Rep(var_first.get(),var_second.get())))

    #添加规则后定义规则函数

def Clea():#清空函数
    input_num_first.delete(0,END)#这里entry的delect用0
    input_num_second.delete(0,END)
    Ans.delete(0,END)#text中的用0.0


#----------------------输入选择框架--------------------
frame_input = Frame(root)
Label_input=Label(frame_input, text='(输入和选择框架)', font=('',15))
var_first = StringVar()
var_second = StringVar()
input_num_first = Entry(frame_input, textvariable=var_first)
input_num_second = Entry(frame_input, textvariable=var_second)

#---------------------选择运算规则---------------------
#还可以添加其他规则

lb = Listbox(frame_input,height=4)
list_item=['加', '减', '乘', '除','字符串连接','字符串相似度']
for i in list_item:
    lb.insert(END,i)

#---------------------计算结果框架---------------------
frame_output = Frame(root)
Label_output=Label(frame_output, text='(计算结果框架)', font=('',15))
Ans = Listbox(frame_output, height=5,width=30)#text也可以，Listbox好处在于换行


#-----------------------Button-----------------------

calc = Button(frame_output,text='计算', command=Answ)
cle = Button(frame_output,text='清除', command=Clea)


#---------------------滑动Scrollbar-------------------
scr1 = Scrollbar(frame_input)
lb.configure(yscrollcommand = scr1.set)
scr1['command']=lb.yview

scr2 = Scrollbar(frame_output)
Ans.configure(yscrollcommand = scr2.set)
scr2['command']=Ans.yview


#-------------------------布局------------------------
#布局写在一块容易排版，可能我low了吧
Label_root.pack(side=TOP)
frame_input.pack(side=TOP)
Label_input.pack(side=LEFT)

input_num_first.pack(side=LEFT)
lb.pack(side=LEFT)
scr1.pack(side=LEFT,fill=Y)
input_num_second.pack(side=RIGHT)

frame_output.pack(side=TOP)
Label_output.pack(side=LEFT)
calc.pack(side=LEFT)
cle.pack(side=LEFT)
Ans.pack(side=LEFT)
scr2.pack(side=LEFT,fill=Y)

#-------------------root.mainloop()------------------

root.mainloop()
```

Tkinter还是比价好上手的，知道一些基本语法就可以实现自己想要的效果了，这里我把自己遇到的问题写一下，如果也有人遇到，恰好能帮助的话，我很荣幸。

------

## 问题&解决

1.Q.button或插件不显示
   A.记得加上pack显示函数！！一般我都定义完了插件直接补上   pack函数

------

2.Q.插件位置显示问题
   A.这个要看你的pack函数写在哪了，所以我一般直接写在最后，容易排序，比如side都是LEFT的话，就按先后顺序显示的

------

3.Q.刚开始键入的被get之后，直接运算出错。
   A.结果是str类型，所以记得用float强制转换，不用int是因为int做除法时候不好使，需要float，切记（python2.7）



------

## Pay Attention

1. 在自定义规则的时候，主要get抓到的数据类型和你的def里面的数据类型，保持一致。


1. 清空函数中，text和entry，listbox的delect清空不一样！比如被实例的是Listbox(Entry)的，那么清空是Obj.delect(0,END),而如果是Text的对象，那么就是Obj.delect(0.0,END)，这个是我之前没想到的，只有实践过才记得住把。而且，用listbox好处在于计算一个值之后，下一个值自动换行，用text时候\n还不好使


1. 如果使用python3，会出现，no model name Tkinter,其实py3只是把它改成小写了，所以导入包的时候改成tkinter 小写就行
2. 出现点击运算符之后无法输出结果或者gui中文乱码问题，一般也是出现在python3的问题上，所以解决方案是吧encode('utf-8')删掉就可以了。

------

