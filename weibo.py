# coding=utf-8

"""

功能: 爬取新浪微博用户的信息
信息：用户ID 用户名 粉丝数 关注数 微博数 微博内容
网址：http://weibo.cn/ 数据量更小 相对http://weibo.com/

"""

import time
import re
import os
import sys
import codecs
import shutil
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains


#先调用无界面浏览器PhantomJS或Firefox
#driver = webdriver.PhantomJS(executable_path="C:\Python27\phantomjs.exe")
driver = webdriver.Chrome()
# driver = webdriver.Firefox()
print '启动浏览器成功'
wait = ui.WebDriverWait(driver,10)


#全局变量 文件操作读写信息
inforead = codecs.open("SinaWeibo_List.txt", 'r', 'utf-8')
infofile = codecs.open("SinaWeibo_Info.txt", 'a', 'utf-8')


#********************************************************************************
#                  第一步: 登陆weibo.cn 获取新浪微博的cookie
#        该方法针对weibo.cn有效(明文形式传输数据) weibo.com见学弟设置POST和Header方法
#                LoginWeibo(username, password) 参数用户名 密码
#                             验证码暂停时间手动输入
#********************************************************************************

def LoginWeibo(username, password):

    try:
        #**********************************************************************
        # 直接访问driver.get("http://weibo.cn/5824697471")会跳转到登陆页面 用户id
        #
        # 用户名<input name="mobile" size="30" value="" type="text"></input>
        # 密码 "password_4903" 中数字会变动,故采用绝对路径方法,否则不能定位到元素
        #
        # 勾选记住登录状态check默认是保留 故注释掉该代码 不保留Cookie 则'expiry'=None
        #**********************************************************************

        #输入用户名/密码登录
        print u'准备登陆Weibo.cn网站...'
        driver.get("https://login.sina.com.cn/signup/signin.php")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(password)
        #elem_rem = driver.find_element_by_name("remember")
        #elem_rem.click()             #记住登录状态

        #重点: 暂停时间输入验证码
        #pause(millisenconds)
        # time.sleep(2)

        driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/form/div[2]/div/ul/li[7]/div[1]/input").click()
        time.sleep(2)

        #获取Coockie 推荐 http://www.cnblogs.com/fnng/p/3269450.html
        # print driver.current_url
        # print driver.get_cookies()  #获得cookie信息 dict存储
        # print u'输出Cookie键值对信息:'
        # for cookie in driver.get_cookies():
        #     #print cookie
        #     for key in cookie:
        #         print key, cookie[key]

        #driver.get_cookies()类型list 仅包含一个元素cookie类型dict
        print u'登陆成功...'


    except Exception,e:
        print "Error: ",e
    finally:
        print u'End LoginWeibo!\n\n'


#********************************************************************************
#                  第二步: 访问个人页面http://weibo.cn/5824697471并获取信息
#                                VisitPersonPage()
#        编码常见错误 UnicodeEncodeError: 'ascii' codec can't encode characters
#********************************************************************************

def VisitPersonPage(user_id):

    try:
        global infofile
        print u'准备访问个人网站.....', "http://weibo.com/" + user_id
        #原创内容 http://weibo.cn/guangxianliuyan?filter=1&page=2
        driver.get("http://weibo.com/" + user_id)
        time.sleep(5)
        #**************************************************************************
        # No.1 直接获取 用户昵称 微博数 关注数 粉丝数
        #      str_name.text是unicode编码类型
        #**************************************************************************

        #用户id
        print u'个人详细信息'
        print u'用户id: ' + user_id

        #昵称
        str_name = driver.find_element_by_xpath("//*[@class='username']")
        name = str_name.text
        print u'昵称: ' + name

        try:
            #关注数 粉丝数 微博数 <td class='S_line1'>
            str_elem = driver.find_elements_by_xpath("//table[@class='tb_counter']/tbody/tr/td/a")
            str_gz = str_elem[0].text    #关注数
            num_gz = re.findall(r'(\w*[0-9]+)\w*', str_gz)
            str_fs = str_elem[1].text    #粉丝数
            num_fs = re.findall(r'(\w*[0-9]+)\w*', str_fs)
            str_wb = str_elem[2].text    #微博数
            num_wb = re.findall(r'(\w*[0-9]+)\w*', str_wb)
            print u'关注数: ', num_gz[0]
            print u'粉丝数: ', num_fs[0]
            print u'微博数: ', num_wb[0]
        except IndexError:
            #关注数 粉丝数 微博数 <td class='S_line1'>
            str_elem = driver.find_elements_by_xpath("//table[@class='tb_counter']/tbody/tr/td")
            str_gz = str_elem[0].text    #关注数
            num_gz = re.findall(r'(\w*[0-9]+)\w*', str_gz)
            str_fs = str_elem[1].text    #粉丝数
            num_fs = re.findall(r'(\w*[0-9]+)\w*', str_fs)
            str_wb = str_elem[2].text    #微博数
            num_wb = re.findall(r'(\w*[0-9]+)\w*', str_wb)
            print u'关注数: ', num_gz[0]
            print u'粉丝数: ', num_fs[0]
            print u'微博数: ', num_wb[0]

        #***************************************************************************
        # No.2 文件操作写入信息
        #***************************************************************************

        # infofile.write('=====================================================================\r\n')
        infofile.write(u'用户: ' + user_id + '\r\n')
        infofile.write(u'昵称: ' + name + '\r\n')
        infofile.write(u'关注数: ' + str(num_gz[0]) + '\r\n')
        infofile.write(u'粉丝数: ' + str(num_fs[0]) + '\r\n')
        infofile.write(u'微博数: ' + str(num_wb[0]) + '\r\n')

        #***************************************************************************
        # No.3 获取关注人列表
        # http://weibo.cn/guangxianliuyan?filter=0&page=1
        # 其中filter=0表示全部 =1表示原创
        #***************************************************************************

        print '\n'
        print u'获取微博内容信息'
        num = 1
        while num <= 5:
            url_wb = "http://weibo.cn/" + user_id + "?filter=0&page=" + str(num)
            print url_wb
            driver.get(url_wb)
            #info = driver.find_element_by_xpath("//div[@id='M_DiKNB0gSk']/")
            info = driver.find_elements_by_xpath("//div[@class='c']")
            for value in info:
                print value.text
                info = value.text

                #跳过最后一行数据为class=c
                #Error:  'NoneType' object has no attribute 'groups'
                if u'设置:皮肤.图片' not in info:
                    if info.startswith(u'转发'):
                        print u'转发微博'
                        infofile.write(u'\n转发微博\r\n')
                    else:
                        print u'原创微博'
                        infofile.write(u'\n原创微博\r\n')

                    #获取最后一个点赞数 因为转发是后有个点赞数
                    str1 = info.split(u" 赞")[-1]
                    if str1:
                        val1 = re.match(r'\[(.*?)\]', str1).groups()[0]
                        print u'点赞数: ' + val1
                        infofile.write(u'点赞数: ' + str(val1) + '\r\n')

                    str2 = info.split(u" 转发")[-1]
                    if str2:
                        val2 = re.match(r'\[(.*?)\]', str2).groups()[0]
                        print u'转发数: ' + val2
                        infofile.write(u'转发数: ' + str(val2) + '\r\n')

                    str3 = info.split(u" 评论")[-1]
                    if str3:
                        val3 = re.match(r'\[(.*?)\]', str3).groups()[0]
                        print u'评论数: ' + val3
                        infofile.write(u'评论数: ' + str(val3) + '\r\n')

                    str4 = info.split(u" 收藏 ")[-1]
                    flag = str4.find(u"来自")
                    print u'时间: ' + str4[:flag]
                    infofile.write(u'时间: ' + str4[:flag] + '\r\n')

                    print u'微博内容:'
                    print info[:info.rindex(u" 赞")]  #后去最后一个赞位置
                    infofile.write(info[:info.rindex(u" 赞")] + '\r\n')
                    infofile.write('\r\n')
                    print '\n'
                else:
                    print u'跳过', info, '\n'
                    break
            else:
                print u'next page...\n'
                infofile.write('\r\n\r\n')
            num += 1
            print '\n\n'
        print '**********************************************'

    except Exception,e:
        print "Error: ",e
    finally:
        # print u'VisitPersonPage!\n\n'
        print '**********************************************\n'
        infofile.write('=====================================================================\n')


#*******************************************************************************
#                                程序入口 预先调用
#*******************************************************************************

if __name__ == '__main__':

    #定义变量
    username = '437320541@qq.com'             #输入你的用户名
    password = 'FAQQAF1314'               #输入你的密码
    user_id = 'guangxianliuyan'          #用户id url+id访问个人


    #操作函数
    LoginWeibo(username, password)      #登陆微博

    #driver.add_cookie({'name':'name', 'value':'_T_WM'})
    #driver.add_cookie({'name':'value', 'value':'c86fbdcd26505c256a1504b9273df8ba'})

    #注意
    #因为sina微博增加了验证码,但是你用Firefox登陆一次输入验证码,再调用该程序即可,因为Cookies已经保证
    #会直接跳转到明星微博那部分,即: http://weibo.cn/guangxianliuyan


    #在if __name__ == '__main__':引用全局变量不需要定义 global inforead 省略即可
    print 'Read file:'
    user_id = inforead.readline()
    while user_id!="":
        user_id = user_id.rstrip('\r\n')
        VisitPersonPage(user_id)         #访问个人页面
        user_id = inforead.readline()
        # time.sleep(5)
        #break

    infofile.close()
    inforead.close()