import os
import time
from zipfile import ZipFile

from selenium import webdriver
import csv
import mechanize
import cookielib
import MySQLdb


def get_credentials():
    user_pass = []
    with open('C:/Aditya-Main/GitHub/Empatica-Pass.txt', 'rb') as f:
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
    with open('Output/sessions_list.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(sessions_list)
    print 'Data successfully saved in sessions_list.csv file'
    driver.close()


# fetch_links()


# cj = cookielib.CookieJar()
# br = mechanize.Browser()
# br.set_cookiejar(cj)
# br.open("https://www.empatica.com/connect/login.php")
#
# br.select_form(nr=0)
# br.form['username'] = get_credentials()[0]
# br.form['password'] = get_credentials()[1]
# br.submit()
#
# f = open('Output/sessions_list.csv', 'rb')
# reader = csv.reader(f)
# for row in reader:
#     print row
#     br.retrieve(row[4], 'Output/Zipped/'+row[3]+'.zip')
#     os.makedirs('Output/Unzipped/'+row[3])
#     zip_ref = ZipFile('Output/Zipped/'+row[3]+'.zip', 'r')
#     zip_ref.extractall('Output/Unzipped/'+row[3])
#     zip_ref.close()
#     os.remove('Output/Zipped/'+row[3]+'.zip')
# f.close()



db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                     user="root",  # your username
                     passwd="1234",  # your password
                     db="e4",)  # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
cur.execute("SELECT * FROM test")

# print all the first cell of all the rows
for row in cur.fetchall():
    print row[0]

db.close()
