import os
import time
import datetime
from zipfile import ZipFile

from selenium import webdriver
import csv
import mechanize
import cookielib
import MySQLdb

current_time = str(time.strftime("%Y-%m-%d_%H~%M~%S"))


def get_credentials():
    user_pass = []
    with open('E:/1.SnD/Studies/ITLS-EMW/pass.txt', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_pass.append(row[0])
    return user_pass


def fetch_links():
    driver = webdriver.Chrome()
    driver.get('https://www.empatica.com/connect/login.php')
    driver.find_element_by_id("username").send_keys(get_credentials()[0])
    driver.find_element_by_id("password").send_keys(get_credentials()[1])

    driver.find_element_by_name("login-button").click()

    driver.get('https://www.empatica.com/connect/sessions.php')
    driver.find_element_by_xpath("//a[contains(@onclick, 'reload')]").click()
    time.sleep(5)

    sessions_list = []
    sessions = driver.find_elements_by_id("sessionList")
    for session in sessions:
        trs = session.find_elements_by_tag_name('tr')
        for tr in trs:
            tds = tr.find_elements_by_tag_name('td')
            sessions_list.append([tds[0].text, tds[1].text, tds[2].text, tds[3].text, tds[4].find_element_by_id("fileDownloadCustomRichExperience").get_attribute('href')])

    print 'Writing data to CSV file....'
    with open('Output/Sessions_' + current_time + '.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(sessions_list)
    print 'Sessions successfully saved...'
    driver.close()


fetch_links()

cj = cookielib.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.open("https://www.empatica.com/connect/login.php")

br.select_form(nr=0)
br.form['username'] = get_credentials()[0]
br.form['password'] = get_credentials()[1]
br.submit()

f = open('Output/Sessions_' + current_time + '.csv', 'rb')
# f = open('Output/Sessions_2016-11-16_02~54~10.csv', 'rb')
reader = csv.reader(f)
for row in reader:
    print row[4]
    br.retrieve(row[4], 'Output/Zipped/' + row[3] + '.zip')
    os.makedirs('Output/Unzipped/' + row[3])
    zip_ref = ZipFile('Output/Zipped/' + row[3] + '.zip', 'r')
    zip_ref.extractall('Output/Unzipped/' + row[3])
    zip_ref.close()
    os.remove('Output/Zipped/' + row[3] + '.zip')
f.close()


# connect to the database
# db = MySQLdb.connect(host="000", port=000, user="000", passwd="0000", db="000")


# f = open('Output/sessions_list.csv', 'rb')
# reader = csv.reader(f)
# datas = []
# for row in reader:
#     l = [row[0], row[1], row[2], row[3]]
#     datas.append(l)
#
# datas = list(map(tuple, datas))
#
# db = MySQLdb.connect(host="000", port=000, user="000", passwd="000", db="000")
# cursor = db.cursor()
# sql = "INSERT INTO session VALUES (%s, %s, %s, %s)"
# cursor.executemany(sql, datas)
# db.commit()


# f = open('Output/Unzipped/194269/EDA.csv', 'rb')
# reader = csv.reader(f)
#
# data = []
# initial_utc = 0
# for i, row in enumerate(reader):
#     if i == 0:
#         print type(row)
#         initial_utc = int(float(row[0]))
#         break
#
# doop = -1
# for i, row in enumerate(reader):
#     if i > 1:
#         doop += 1
#     if doop == 4:
#         initial_utc += 1
#         doop = 0
#     if i >= 4:
#         d = tuple([time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(initial_utc)), row[0]])
#         data.append(d)
#
# db = MySQLdb.connect(host="000", port=000, user="000", passwd="000", db="000")
# cursor = db.cursor()
# sql = "INSERT INTO data VALUES (%s, %s)"
# cursor.executemany(sql, data)
# db.commit()
