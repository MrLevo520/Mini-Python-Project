# -*- coding: utf-8 -*-
#Author:哈士奇说喵
#用户加密存储系统
import base64
import pymysql
import hashlib



#初始化数据库子函数
def Init():
    #创建数据库
    try:
        cur.execute('create database MD5_Storetest')#创建名为professors数据库
        cur.execute('use MD5_Storetest')#切到该数据库
        cur.execute('create TABLE store(id BIGINT(7) NOT NULL AUTO_INCREMENT,user_name VARCHAR(100),passwd VARCHAR(100),encrypt_words VARCHAR(10000),encrypt_password VARCHAR(100),created TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,PRIMARY KEY(id))')
        print '-------------------------------Create Database Succeed-------------------------------'
    except:
        #print 'database existed'
        cur.execute('use MD5_Storetest')#切到该数据库

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

#密码加密与明文加密存储子函数
def PasswdSecretWD_encrypt(name,keywords,cho,key_content,content_key):

    #根据选项进行下一步操作
    if cho == '1':

        mix = encrypt(key_content, content_key)
        print "############################################\n#MD5-Password&Plaintext Encryption Succeed!#\n############################################"

        try:
            key_content_sha1 = sha1(key_content)#对KEY进行加密
            store(name,md5(keywords),mix,key_content_sha1)
        except:
            print "Warning!Can't Find SQL!"

    elif cho == '2':

        mix = encrypt(key_content, content_key)
        print "#############################################\n#SHA1-Password&Plaintext Encryption Succeed!#\n#############################################"
        try:
            key_content_md5 = md5(key_content)[0]#对KEY进行加密
            store(name,sha1(keywords),mix,key_content_md5)
        except:
            print 'Warning!Insert SQL Failed!'
    else:
        print "Warning!Something Wrong in Your Encryption Algorithm!"

#数据库的存储子函数
def store(user_name,passwd,encrypt_str,key_content):
    cur.execute("insert into store(user_name,passwd,encrypt_words,encrypt_password) VALUES (%s,%s,%s,%s)",(user_name,passwd,encrypt_str,key_content))

    cur.connection.commit()#commit()提交事物，做出改变后必须提交事务，不然不能更新

#数据库的提取子函数
def check(user_name):
    cur.execute('select * FROM store WHERE user_name=%s',(user_name))
    return cur.fetchall()#抓取符合的一整行，元组形式返回

#加密内容解密子函数
def getSecret(key,sql_str):#获取数据库中加密数据后解密

    try:
        ans = decrypt(key,sql_str)
        return ans
    except:
        print "Warning!Decryption Failed!Can't Get Secret Words!"

#更新密码子函数
def updatePasswd(existed_name):

    try:
        #判断是否为该用户，要求输入原始密码，经过校验后，才允许修改
        ori_passwd = raw_input("Please Enter Original Password:")
        if str(check(existed_name)[0][2]) == md5(ori_passwd)[0] or str(check(existed_name)[0][2]) == sha1(ori_passwd):
            new_passwd = raw_input("Please Enter New Password:")
            new_passwdmd5 = md5(new_passwd)#新密码一律采用md5加密，实在懒得再写加密子函数了
            try:
                cur.execute('update store SET passwd =%s WHERE user_name=%s',(new_passwdmd5[0],existed_name))
                cur.connection.commit()#commit()提交事物！！！！
                print "##########################\n#Update Password Succeed!#\n##########################"
            except:
                print "Warning!Update Password Failed!"
        else:
            print "Warning!Wrong Password!"
    except:
        print "Warning!Update Password Failed!"

#更新KEY子函数
def updateKEY(existed_name):
    try:
        ori_KEY = raw_input("Please Enter Original KEY:")
        if str(check(existed_name)[0][4]) == md5(ori_KEY)[0] or str(check(existed_name)[0][4]) == sha1(ori_KEY):
            new_KEY = raw_input("Please Enter New KEY:")
            new_KEYmd5 = md5(new_KEY)
            #因为自己设计的加密解密函数和key绑定，随key变换而变化，所以需要更新下Plaintext
            secwd = getSecret(ori_KEY,str(check(existed_name)[0][3]))
            mix_update = encrypt(new_KEY, secwd)
            try:
                cur.execute('update store SET encrypt_words =%s WHERE user_name=%s',(mix_update,existed_name))
                #因为自己设计的加密算法有key的加入，所以更换key后，加密内容也会改变，所以执行更新加密内容
                cur.execute('update store SET encrypt_password =%s WHERE user_name=%s',(new_KEYmd5[0],existed_name))
                cur.connection.commit()#commit()提交事物！！！！
                print "#####################\n#Update KEY Succeed!#\n#####################"
            except:
                print "Warning!Update KEY Failed!"
        else:
            print "Warning!Wrong KEY!"
    except:
        print "Warning!Update KEY Failed!"

#删除用户子函数
def DeleteUser(name_req):
    try:
        cur.execute('delete FROM store WHERE user_name=%s',(name_req))
        cur.connection.commit()#commit()提交事物！！！！
        print "######################\n#Delete User Succeed!#\n######################"
    except:
        print "Warning!Delete User Failed!"

#用户登录&更新子函数
def LogIn(name_req,keywords_req):

    if str(check(name_req)[0][2]) == md5(keywords_req)[0] or str(check(name_req)[0][2]) == sha1(keywords_req):
        print "-------------------------------Welcome %s-------------------------------"%name_req

        while 1:
            print "-------------------------------%s:What's Next?-------------------------------"%name_req
            check_update = raw_input("Update Plaintext-1    View Plaintext-2    Update Password-3    Update KEY-4    Log out-5    Delete User-6\nYour Choice: ")
            if check_update =='1':
                key_encrypt = raw_input("KEY:")
                if sha1(key_encrypt)==str(check(name_req)[0][4]) or md5(key_encrypt)[0] ==str(check(name_req)[0][4]):
                    #显示一下以前存储的内容，看看需不需要更新
                    print "Original Plaintext:%s"%(getSecret(key_encrypt,str(check(name_req)[0][3])))
                    new_plaintext = raw_input("New Plaintext:")
                    new_mix = encrypt(key_encrypt, new_plaintext)
                    try:
                        cur.execute('update store set encrypt_words=%s WHERE user_name=%s',(new_mix,name_req))
                        cur.connection.commit()#commit()提交事物！！！！
                        print "###########################\n#Update Plaintext Succeed!#\n###########################"
                    except:
                        print "Warning!Update Plaintext Failed!"

                else:
                    print "Warning!Wrong KEY!"

            elif check_update =='2':
                key_encrypt = raw_input("KEY:")
                if str(check(name_req)[0][4]) == md5(key_encrypt)[0] or str(check(name_req)[0][4]) == sha1(key_encrypt):
                    try:
                        secwd = getSecret(key_encrypt,str(check(name_req)[0][3]))
                        print "Secret Words:%s"%(secwd)
                    except:
                        print "Warning!Get Secret Words Failed!"
                else:
                    print "Warning!Wrong KEY!"

            elif check_update =='3':
                updatePasswd(name_req)

            elif check_update =='4':
                updateKEY(name_req)

            elif check_update=='5':
                break
            elif check_update=='6':
                DeleteUser(name_req)
                break

            else:
                print "Warning!Something Wrong in Your Choice!"



    else:
        print "Warning!Can't Find The User or Wrong Password!"


def Store_Encrypt():

    print '-------------------------------Store&Encrypt-------------------------------'
    name = raw_input('New User:')
    try:
        while name == check(name)[0][1].encode('utf-8'):
            print "Warning!The Name Already Exist!"
            print "-------------------------------Make Your Choice-------------------------------------"
            update = raw_input("Change Password-1    Create New User-2\nSelect Mode:")
            if update =='1':
                updatePasswd(name)
                break
            if update =='2':
                name = raw_input('New User:')


    except:
        keywords = raw_input('Set Password:')
        print "-------------------------------Password Encrypt Algorithm-------------------------------------"
        cho = raw_input('MD5-1   SHA1-2\nSelect Algorithm:')

        print "-------------------------------What's Next?-------------------------------------"
        kc=raw_input("Store Encrypt Plaintext-1    Maybe Next Time-2\nYour Choice:")

        if kc=='1':
            key_content = raw_input('Please Design Your KEY:')
            content_key = raw_input('Plaintext:')

        else:
            key_content ='123456'
            content_key = 'Default Storage'
            print "Default KEY '123456'\nDefault Plaintext 'Default Storage'"

        PasswdSecretWD_encrypt(name,keywords,cho,key_content,content_key)
#主函数
def Main():


    while 1:
        Init()
        print "-------------------------------Mode Choice-------------------------------------"
        ty = raw_input('Store&Encrypt-1     Login&View&Update&Delete-2    Quit System-3    Clear Database-4\nSelect Mode:')

        if ty == '1':
            Store_Encrypt()

        if ty == '2':
            print '-------------------------------Login&View&Update&Delete-------------------------------'
            name_req = raw_input('User:')
            keywords_req = raw_input('Password:')
            try:
                LogIn(name_req,keywords_req)
            except:
                print "Warning!Can't Find The User or Wrong Password!"

        if ty == '3':
            print '-------------------------------Quit The System-------------------------------'
            break

        if ty == '4':
            print "-------------------------------Warning!ALL Data Will Be Wiped!-------------------------------"

            sure = raw_input('Confirm-Y    Quit-N\nYour Choice:')
            if sure.upper() =='Y':
                try:
                    cur.execute('drop database MD5_Storetest')
                    print '-------------------------------Wipe Database Succeed-------------------------------'
                    print "-------------------------------What's Next?-------------------------------"
                    new_database = raw_input('Create New Database-Y    Quit-N\nYour Choice:')
                    if new_database.upper() == 'Y':
                        Init()
                    else:
                        break
                except:
                    print 'Warning!Wipe Database Failed!'
            else:
                print '-------------------------------Operation Aborted-------------------------------'



#程序入口
if __name__ == '__main__':

    try:
        conn = pymysql.connect(host = '127.0.0.1',user='root',passwd='A089363b',db='mysql',charset='utf8')
        #与数据库建立连接
        cur = conn.cursor()
        #实例化光标
        print "-------------------------------SQL Connection Succeed-------------------------------"

    except:
        print "Warning!SQL Connection Failed!"

    #创建属于自己的伪码表，用于自己的加密算法服务
    list_key = ['G','h','S','2','M','a','m']
    Main()

    try:
        cur.close()
        conn.close()
        print "-------------------------------SQL Connection Closed-------------------------------"
        print "-------------------------------Over-------------------------------"
    except:
        print "Warning!Can't Close Connection!"