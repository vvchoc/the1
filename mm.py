

import xbot
from xbot import print, sleep
from.import package
from.package import variables as glv
import pymysql
import requests
from bs4 import BeautifulSoup
import mysql.connector









def main(args):
    web_page = xbot.web.create("http://www.boxofficecn.com/the-red-box-office")

    sum_data = []
    for i in range(1,6):
        for i in range(1, 21):
            name = web_page.find_by_xpath(f'/table[@id="TP_TableList"]//tr[{i}]//td[2]').get_text()
            year = web_page.find_by_xpath(f'/table[@id="TP_TableList"]//tr[{i}]//td[8]').get_text()
            diqu = web_page.find_by_xpath(f'/table[@id="TP_TableList"]//tr[{i}]//td[7]').get_text()
            lianjie = web_page.find_by_xpath(f'/table[@id="TP_TableList"]//tr[{i}]//td[2]//a/img[1]').get_attribute('src')
            daoyan = web_page.find_by_xpath(f'/table[@id="TP_TableList"]//tr[{i}]//td[8]').get_text()
            piaofang = web_page.find_by_xpath(f'/table[@id="TP_TableList"]//tr[{i}]//td[4]').get_text()
            sum_data.append(tuple([name,year,diqu,lianjie,"导演",piaofang,"yyccc266"]))
        next_page = web_page.find_by_xpath('//div[@id="layui-laypage-1"]/a[6]')
        next_page.click()
    print(f"需要写入数据库数据: {sum_data}")
    web_page.close()
    #数据写入数据库
    write_sql(sum_data)
    pass

def connection():
    try:
        mydb = pymysql.connect(
            host = "43.143.30.32",
            user = "yingdao",
            password = "9527",
            database = "ydtest",
            charset='utf8'
        )
        return mydb
    except Exception as e:
        print(f"数据库连接失败: {e}")

def write_sql(data):
    mydb = connection()
    mycursor = mydb.cursor()
    try:
        sql = "INSERT INTO movies (电影名称, 上映年份, 制片地区, 海报链接, 导演, 票房, 提交人) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        mycursor.executemany(sql, data)
        mydb.commit()
        print("成功写入数据")
    except Exception as e:
        print(f"写入数据失败: {e}")
    finally:
        mycursor.close()
        mydb.close()