import time
from selenium import webdriver
import csv


def get_credentials():
    user_pass = []
    with open('E:/1.SnD/Studies/ITLS-EMW/pass.txt', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_pass.append(row[0])
    return user_pass


def start():
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


start()
