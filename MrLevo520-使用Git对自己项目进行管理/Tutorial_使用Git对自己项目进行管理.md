## 学习使用Git对自己项目进行管理

## First - 创建自己的仓库

> 教程只需要看到分支管理之前的基本操作就行，知道如何提交自己的项目到github并进行版本管理

- 墙裂建议自学从这里开始→_→[廖雪峰的git教程](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)

任务1：先自己建个仓库，然后提交一下自己的项目



## Second - fork项目并pull request

> 提交自己认为满意的作业至furtherProject，提交方式请见提交方式.md文件

- 过程先看一下这里→_→ *[Github上怎么修改别人的项目并且提交给原作者！图文并茂](http://blog.csdn.net/qq26787115/article/details/52133008)*

1. **注册好Github账号，最好使用outlook邮箱进行注册**，且需要验证下才能用
2. **fork项目，进入到别人的项目页下**

![这里写图片描述](http://img.blog.csdn.net/20170903112646542?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTXJMZXZvNTIw/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

3. **进入到自己的仓库可以看到从原作者项目中fork过来的项目，就是一个复刻版本，所有的都保持一致**

![这里写图片描述](http://img.blog.csdn.net/20170903112620790?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTXJMZXZvNTIw/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

4. **clone到自己本地，然后更新自己的文件夹到对应的项目的furtherProject文件夹下**
5. **需要提交的目录结构如下**

![这里写图片描述](http://img.blog.csdn.net/20170903112707161?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTXJMZXZvNTIw/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

6. **这里我写好了一个提交的版本，其实其余的什么你都不需要动，只需要提交自己的项目到对应的文件夹，至于怎么提交项目到自己的仓库，请参考廖雪峰的教程，提交规范请看提交方式.md说明文档**

![这里写图片描述](http://img.blog.csdn.net/20170903112718957?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTXJMZXZvNTIw/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

7. **然后pull request给原作者，意思是，我想要把这个版本和原作者版本进行合并，这样别人fork原作者的项目时候，你的项目也被fork了，相当于给原作者添砖加瓦**

![这里写图片描述](http://img.blog.csdn.net/20170903112734092?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTXJMZXZvNTIw/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

8. **如果是多次pull ，则会出现下面的现象，不用管，create pull request**

![这里写图片描述](http://img.blog.csdn.net/20170903112757567?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTXJMZXZvNTIw/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

9. **对自己pull的项目进行简单描述，不然原作者根本不知道你更新了啥**

![这里写图片描述](http://img.blog.csdn.net/20170903112808779?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTXJMZXZvNTIw/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)



---



> 这里是原始仓库角度，收到了贡献者的pull request

![这里写图片描述](http://img.blog.csdn.net/20170903112823067?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTXJMZXZvNTIw/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

> 原作者会看到你自己pull的项目描述等，考虑是否将其merge到原项目

![这里写图片描述](http://img.blog.csdn.net/20170903112833444?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTXJMZXZvNTIw/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)



> ​	进行pull request项目，就是告诉我，我这里有添加的新项目，想要合并到原始项目中，审核后我会进行merge，这样大家以后fork原始项目的时候，就会把你的新添加的project也fork过去。对于大家的操作，其实就是fork原项目，然后clone到本地，进行自己项目的相应更新，然后push到自己的仓库，然后再从自己的仓库pull request到原仓库，你自己的仓库任何改造都不会影响原仓库，如果你想贡献自己的一份延伸项目给别人也进行fork，那么，pull给我吧！



任务二：挑选以前做过的项目，根据撰写规范进行排版总结，发pull到原项目进行联合开发



---

## About Tool

### Markdown 编辑器

> 个人推荐Typora，全平台兼容，至于md语法，百度下，很简单



![typora.gif](http://upload-images.jianshu.io/upload_images/2671133-86de28680ae3ea37.gif?imageMogr2/auto-orient/strip)



### git GUI

> 对于win的用户，推荐使用 [git bash](https://git-for-windows.github.io/)
>
> 对于mac用户，自带终端即可使用
>
> 当然对于两种平台，首先先装一下git，如何装git，请自行百度
>
> BTW，sourceTree也是个不错的git工具，也是双平台

