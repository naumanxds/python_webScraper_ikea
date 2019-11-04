# import requests
# import requests_html
# import time
# import csv

# from datetime import datetime
# from requests_html import HTMLSession
# from bs4 import BeautifulSoup

# # constants used in code
# BASE_URL = 'https://www.amazon.ae'
# NOT_FOUND = 'None'
# INCREMENT_ONE = 1
# SLEEP_SEC = 5


# # create file with time attached to it for safty purposes
# # fHandle = open('csvFileCreatedAt-' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + '.csv', 'w', encoding="utf-8")


# # get html of the provided url page
# def getHtml(url):
#     try:
#         session = HTMLSession()
#         response = session.get(url)
#         return BeautifulSoup(response.text, 'lxml')
#     except Exception as e:
#         print('Oops! Something went worng fetching the link - ' + format(e))
#     return false

# # iterate through the fetched links get price and place in the file
# def iterateLinks(subLinks):
#     data = []
#     html = getHtml(subLinks)
#     try:
#         # title of the product
#         title = html.find('span', {'class' : 'normal-font range__text-rtlmmm'})
#         if str(title) != NOT_FOUND:
#             title = title.get()
#         else:
#             title = 'Title not Found'



#     except:
#         true

# # input for user
# enteredUrl = input('Please Enter Starting Point for Scrapper: ')
# print('=== Starting Scrapping ===')
# # iterateLinks(enteredUrl)
# html = getHtml(enteredUrl)
# print(html.find('div', {'class' : 'range-stock-check__left'}))

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

url = 'https://www.ikea.com/ae/en/p/fullen-wash-basin-cabinet-white-70189041/'

options = webdriver.ChromeOptions();
options.add_argument('--headless');
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get(url)

chrome = driver.execute_script('return document.documentElement.outerHTML')
html = BeautifulSoup(chrome, 'lxml')
print(html.find_all('option', {'value' : '218'}))


