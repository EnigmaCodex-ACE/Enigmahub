from pymongo import MongoClient
from flask import escape

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep

mongo_url = "REDACTED"
mongo_client = MongoClient(mongo_url)
projects = mongo_client['projhub']['prohub']
API_ENDPOINT = "http://api.itspacchu.tk/jnturesult"
db = mongo_client['jnturesults']['jnturesult']
attddb = mongo_client['jnturesults']['studentattendance']
ecodes = mongo_client['jnturesults']['examcodes']

def fetch_db_data(limit=10,skip=0):
    return list(projects.find().limit(limit).skip(skip))

def curated_db_data():
    return list(projects.find({'curated':True}))

def fetch_db_from_id(id):
    return projects.find_one({"_id":id})

def search_db_from_query(query):
    req = projects.find({'$search': {'index': 'text', 'text': {'query': query , 'path': {'wildcard': '*'}}}})
    return list(req)

def add_value_to_db(data):
    if data:
        projects.insert_one(data)
    else:
        raise Exception("Data is empty")

if(__name__ == "__main__"):
    dat= search_db_from_query("18AG1A0401")
    print(dat)




savdict = {}

def fetchAttendance(rollno):
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)
    browser.get('https://aceexam.in/BeesERP/Login.aspx')
    browser.find_element(By.ID,'txtUserName').send_keys(rollno)
    browser.find_element(By.ID,'btnNext').click()
    sleep(0.1)
    browser.find_element(By.ID,'txtPassword').send_keys(rollno)
    sleep(0.1)
    browser.find_element(By.ID,'btnSubmit').click()

    name = browser.find_element(By.ID,'ctl00_cpHeader_ucStud_lblStudentName').text.replace("WELCOME"," ").lower().replace(str(rollno).lower(),"").replace("(","").replace(")","").strip()
    attendance = float(browser.find_element(By.ID,'ctl00_cpStud_lblTotalPercentage').text.replace("%","").strip())
    retdict = {
        "_id":rollno,
        "name":name,
        "attendance":attendance
    }
    browser.close()
    return retdict
