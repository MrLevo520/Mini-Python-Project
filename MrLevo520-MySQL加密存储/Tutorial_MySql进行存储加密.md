***From [Python+MySQL用户加密存储验证系统（进阶）](http://blog.csdn.net/mrlevo520/article/details/52089545)***



- Python 2.7 
- IDE Pycharm 5.0.3 
- PyMySQL 0.7.6 
- MySQL 5.7 
- MySQL Workbench 6.3

> 至于MySQL和Python如何联调使用请看上期[Python与MySQL联动实例一两则 ](http://blog.csdn.net/mrlevo520/article/details/52083615)

----------
    我要填以前挖过的坑了，用户存储加密验证系统beta上线
----------

填坑&目的
--
> ​	这坑是[Python用户存储加密及登录验证系统（乞丐版）](http://blog.csdn.net/mrlevo520/article/details/51789914)挖的，当时还不会使用数据库，现在学到了，不填坑不太好是不是？

----------

应用场景
--
> ​	如果数据库是暂存在第三方，而且存入的数据又不想让第三方数据库管理员看到，消息涉及隐私，只有自己可见，那么怎么办呢，我自己设计了一套用户加密验证系统，对登录密码进行MD5/SHA1可选加密，对明文进行自定义的加密算法进行加密存储。短时间内无法破解（私以为）

----------

特点
--

> ​	用户加密存储系统--用于托管第三方数据库，内容进行加密后存储，没有秘钥无法破解

1. 用户存储，登录，查看，删除操作，存储在数据库中
2. 用户密码加密存储，密码加密方式可选，目前只可选MD5和SHA1，用户存储内容加密存储，加密方式自定义
3. 自定义（我自己定义了一个加密解密函数）加密序列，拿到内容没有序列无法解密（自以为）
4. 可更改用户密码，更改自定义KEY值，更改加密存储内容
5. 支持任何位数和形式设置密码，甚至可以设置成中文！但是请注意，最好是杂乱无序字母夹杂的，不然被破解第一层密码后，KEY值可能会暴露！

----------

实现流程框架
------
	这尼玛我图用Visio花了一个多小时。。。。可能我毕设都没那么较真的画图。。。。
![算法流程图](http://upload-images.jianshu.io/upload_images/2671133-70dc3fb3a64e675c?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 其实上面流程图的最左边如果新建用户和数据库中用户重名，则有两个选择，一个是重新命名，另一个就是对原来用户名进行修改密码，线有点多，太乱了连过去，所以这里省略了，实现效果请看下面的IDE交互章节。

好了，整体的思路框架就是这样，当然一开始我没有想那么多，只是做着做着，想着不断增加功能，更加完善性考虑，才会加入那么多选择项的，因为自己设计的，所以，难免存在瑕疵，也没有参考实际大的加密工程中如何处理，下次去看看。

----------

实现代码
----
**这里我就不贴详细代码了，太长了，估计三四百行把，我上传资源在同级目录的mysql_encryptWD中，包括源码（带注释）+exe（exe由于打包软件限制只能用于英文字符输入）+README（请先阅读）**

>  这里只是贴上自己写的加密算法部分。

```
#自定义加密、解密算法子函数。结合base64
def encrypt(key,content): # key:密钥,content:明文
    s1 = base64.encodestring(str(content)) #将内容进行base64加密
    len1 = len(key) % 7 #取余数
    len1_list = list_key[len1] #取余数对应list_key中伪码
    mix_first = str(key)+s1 #将key转化为字符串后拼接第一次加密的内容
    mix = len1_list+base64.encodestring(mix_first) #对拼接后字符串再进行加密，再加个伪码

    return mix #存入数据库中，不能被反解

def decrypt(key,mix): # key:密钥,content:密文

      len2 = len(key) % 7
      len2_findlist = list_key[len2]

      if len2_findlist==mix[0]: #先确定伪码
        s2_first = base64.decodestring(mix[1:])#反解出第一次的base64编码
        s2_second = s2_first[0:len(key)] #获取第一次解出前缀是否为key

        if s2_second==str(key):#key值对应了
            s2_end = base64.decodestring(s2_first[len(key):])#反解出去掉前缀后的真实内容的64位编码
            print '-------------------------------Validation Succeed!-------------------------------'

            return s2_end
        else:
          print "Warning!Validation Failed！Can't Get Secret Words!"

      else:
          print "Warning!Validation Failed！Can't Get Secret Words!"

```
解释就在上面的注释上了，这里说一下实现效果，存入数据库中形式应该是这样的
![数据库表现形式](http://upload-images.jianshu.io/upload_images/2671133-b6da39552e213ecf?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

***对于自己的加密算法：自己尝试写，肯定会有纰漏的地方，如果以后有机会，可以学一下密码学，自己接触的到底还是太少了，只是添加了伪码表，然后两次base64加密，当然，数据库中内容直接拿来base64解码肯定是不会成功的。***

*登录密码是用MD5/SHA1进行加密的，而第二层，登陆之后，可以自己选择KEY值，对输入的明文进行加密，如果没有我的伪字典和KEY应该是不能反解出加密的内容的，所以对于数据库管理员来说，根本不能解密存入数据库中的内容，对于有特殊需求的记录也好，项目也好，我想应该有应用的地方。*

----------

交互效果
----
这里显示的是整个IDE交互界面，如何处理这些；

----------


0.进行新用户注册（可以选择不设置明文默认KEY为123456）

```
-------------------------------Mode Choice-------------------------------------
Store&Encrypt-1     Login&View&Update&Delete-2    Quit System-3    Clear Database-4
Select Mode:1
-------------------------------Store&Encrypt-------------------------------
New User:k3
Set Password:k3
-------------------------------Password Encrypt Algorithm-------------------------------------
MD5-1   SHA1-2
Select Algorithm:1

```

----------
1.进行设置KEY和明文加密

```
-------------------------------What's Next?-------------------------------------
Store Encrypt Plaintext-1    Maybe Next Time-2
Your Choice:1
Please Design Your KEY:k4
Plaintext:k4'secret
#############################################
#SHA1-Password&Plaintext Encryption Succeed!#
#############################################
```
以下是默认KEY与明文设置，选择2即可
```
-------------------------------What's Next?-------------------------------------
Store Encrypt Plaintext-1    Maybe Next Time-2
Your Choice:2
Default KEY '123456'
Default Plaintext 'Default Storage'
############################################
#MD5-Password&Plaintext Encryption Succeed!#
############################################
```

----------
2.查看加密明文
（第0步中，如果没有自己设置KEY等，会有个默认值进行存储）

以下为自己设置了KEY和明文（没有设置时候，则KEY为123456），查看明文
```
-------------------------------k4:What's Next?-------------------------------
Update Plaintext-1    View Plaintext-2    Update Password-3    Update KEY-4    Log out-5    Delete User-6
Your Choice: 2
KEY:k4
-------------------------------Validation Succeed!-------------------------------
Secret Words:k4'secret
```
更加详细的请自己测试使用。代码和上述流程图保持一致。

----------

3.遇到新用户重名，解决途径，修改密码或者更换新名字

```
-------------------------------Mode Choice-------------------------------------
Store&Encrypt-1     Login&View&Update&Delete-2    Quit System-3    Clear Database-4
Select Mode:1
-------------------------------Store&Encrypt-------------------------------
New User:k1
Warning!The Name Already Exist!
-------------------------------Make Your Choice-------------------------------------
Change Password-1    Create New User-2
Select Mode:2
New User:k2
Set Password:k3

```

----------

4.更新登录密码选择，需要有以前密码，才能修改

```
-------------------------------Welcome k1-------------------------------
-------------------------------k1:What's Next?-------------------------------
Update Plaintext-1    View Plaintext-2    Update Password-3    Update KEY-4    Log out-5    Delete User-6
Your Choice: 3
Please Enter Original Password:k1
Please Enter New Password:k2
##########################
#Update Password Succeed!#
##########################
```

----------
5.更新KEY值

```
-------------------------------Welcome k1-------------------------------
-------------------------------k1:What's Next?-------------------------------
Update Plaintext-1    View Plaintext-2    Update Password-3    Update KEY-4    Log out-5    Delete User-6
Your Choice: 4
Please Enter Original KEY:k1
Please Enter New KEY:k2
-------------------------------Validation Succeed!-------------------------------
#####################
#Update KEY Succeed!#
#####################
```

----------
6.更新明文

```

-------------------------------k4:What's Next?-------------------------------
Update Plaintext-1    View Plaintext-2    Update Password-3    Update KEY-4    Log out-5    Delete User-6
Your Choice: 1
KEY:k4
-------------------------------Validation Succeed!-------------------------------
Original Plaintext:k4'secret
New Plaintext:k4's secret2
###########################
#Update Plaintext Succeed!#
###########################
```



----------

遇到的问题及解决方案
----------
Q: MD5/SHA1加密存储时候的类型不同引起的错误。
A:  解决方案，多进行try/except使用抛出错误，定位错误，常用输出语句进行和预期值之间的排错，如下，md5加密后为元组形式，而sha1为str类型
```
import hashlib

#MD5和SHA1加密算法
def md5(str1):
    md = hashlib.md5()
    md.update(str1)
    md_5=md.hexdigest()
    return md_5,

def sha1(str1):
    sh = hashlib.sha1()
    sh.update(str1)
    sha_1 = sh.hexdigest()
    return sha_1

print md5("123")
print type(md5("123"))
print sha1("123")
print type(sha1("123"))
```
运行后

```
('202cb962ac59075b964b07152d234b70',)
<type 'tuple'>
40bd001563085fc35165329ea1ff5c5ecbdbbeef
<type 'str'>
```
知道所出现的形式之后，对症下药就可以了！

----------
Q: 对数据库进行插入，删除，更新操作，数据库内容不改变问题
A:  解决方案，没有进行事务提交！
比如，我实现添加操作，最后需要添加语句commit

```
cur.execute("insert into store(user_name,passwd,encrypt_words,encrypt_password) VALUES (%s,%s,%s,%s)",(user_name,passwd,encrypt_str,key_content))

cur.connection.commit()#commit()提交事物，做出改变后必须提交事务，不然不能更新
```

----------
Q: 数据库出现Lock wait timeout exceeded错误，原因是如图

![原因解析](http://upload-images.jianshu.io/upload_images/2671133-fad1c3842980bb8a?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

A: 解决方案；这里应该运行时候断开以前运行的程序，这点我做的不好，调试的时候，以前的程序还在运行，全部断开连接，只要一个运行就行

----------
Q: 结构功能问题
A:  需要实践积累，怎样实现目的，产生比较清晰的架构，子函数应该怎么写，才能最大程度的调用，这些我都比较弱，需要不断的进行学习和测试，我的框架结构也是改了很多次，都是进行测试之后慢慢修改成型的，考虑到了几乎所有的操作需求，你能信当时我只是想弄个加密写入和读取的玩意就行了么，最后还是写成比较完善的一个小项目了，所以，这个问题，只有不断练习把，不过下次我会先拟构好一个流程图框架再写。

----------

What's new？
-------------
从最初涉及到全部功能实现，写函数的时间大概只占了百分之三十，其余时间都在进行排错调试，因为功能的繁多，并不知道哪里会出错，可能功能和功能之间衔接，可能大的分选项，退出到几级菜单，这些问题我几乎每个都遇到过，最后一一解决，感觉很棒！以后分块写模块调试，还是很重要的，还有就是，模块包裹的成分多少我还没把握好，最高效的调用模块才是个好模块呢！



## 致谢

- Python网络数据采集[Ryan Mitchell著][人民邮电出版社]
- [@Mrlevo520--Python用户存储加密及登录验证系统（乞丐版）](http://blog.csdn.net/mrlevo520/article/details/51789914)
- [在线转换工具--将代码以BASE64方式加密、解密](http://www1.tc711.com/tool/BASE64.htm)
- [@Mrlevo520--Python与MySQL联动实例一两则 ](http://blog.csdn.net/mrlevo520/article/details/52083615)
- [@li_feibo--关于Lock wait timeout exceeded; try restarting transaction](http://www.51testing.com/html/16/390216-838016.html)