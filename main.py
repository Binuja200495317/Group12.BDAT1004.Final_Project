from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import sqlite3

from pandas.io.formats import style
import lxml
import json
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

import mysql.connector as mysql
import datetime

from selenium.webdriver.chrome.options import Options


chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")


# db=mysql.connect(
#     host="us-cdbr-east-05.cleardb.net",
#     user="b57a78d90c3d19",
#     password="3ecb7d0e",
#     database="heroku_239d08d8782debc",
#     autocommit=True
# )

conn = sqlite3.connect("fda_data_db.db", check_same_thread=False)
db_cursor = conn.cursor()
db_cursor.execute("create table if not exists fda_data(Date text,Drug_Name text,Submision text,Active_Ingredients text,Company text,Submission_Classification text,Submission_Status text,PRIMARY KEY(Date,Drug_Name)) ")

# db_cursor.execute("Select * from fda_data")
# data =db_cursor.fetchall()

# for l in data:
#     print(l[0])


def get_data():
    driver = webdriver.Chrome(executable_path=os.environ.get(
        "CHROMEDRIVER_PATH"), options=chrome_options)
    #driver = webdriver.Chrome("C:/Users/gayan/OneDrive/Desktop/Python Project/SeleniumDrivers/chromedriver.exe", options=chrome_options)
    data = pd.DataFrame()

    time.sleep(5)
    driver.get(
        "https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=reportsSearch.process")
    driver.maximize_window()

    for i in range(2011, 2022):

        select = Select(driver.find_element_by_id('reportSelectYear'))

        select.select_by_visible_text(str(i))

        for a in range(1, 13):
            select_1 = Select(driver.find_element_by_id('reportSelectMonth'))
            select_1.select_by_value(str(a))
            button = driver.find_element_by_xpath(
                '/html/body/div[2]/div/div/div/div/div/div[3]/div/form/div[2]/button')

            button.click()
            time.sleep(3)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            row = soup.find_all('tr', class_="odd")

            for details in row:
                data = details.text.strip().splitlines()
                data[0] = data[0][-4:]+"-"+data[0][0:2]+"-"+data[0][3:5]
                # print(data[0])
                query = "insert into fda_data(Date,Drug_Name,Submision,Active_Ingredients,Company,Submission_Classification,Submission_Status) values(?,?,?,?,?,?,?)"
                try:
                    db_cursor.execute(query, data)
                    print("done....")
                    conn.commit()
                    print(data)
                except:
                    continue
                print(data)
            # df = pd.read_html(str(table))[0]
            # data =pd.concat([data , df] , axis=0 , ignore_index=True)
            # print(data)
            # data.to_csv(f"FDA_scrape_full_1983_2021.csv" , index = False)

            time.sleep(2)
    driver.quit()
    conn.close()


get_data()
