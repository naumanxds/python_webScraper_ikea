import time
import csv

from datetime import datetime
from requests_html import HTMLSession
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# constants used in code
NOT_FOUND = 'None'
INCREMENT_ONE = 1
RESPONSE_WAIT = 10000

# create file with time attached to it for safty purposes
fHandle = open('csvFileCreatedAt-' + datetime.now().strftime('%Y-%m-%d') + '.csv', 'w', encoding="utf-8")

# create browser instance
session = HTMLSession()
header = {'User-agent': 'Mozilla/5.0'}

# get html of the provided page url
def getHtml(url):
    try:
        r = session.get(url, headers=header, timeout=RESPONSE_WAIT)
        r.html.render(timeout=RESPONSE_WAIT)
        return BeautifulSoup(r.html.html, 'lxml')

    except Exception as e:
        print('     >> Error in Fetching HTML from Url => ' + url)
        print('     >> ERRROR => ' + format(e))

    return False

# write in file
def writeFile(data, url = ''):
    try:
        csvWriter = csv.writer(fHandle)
        csvWriter.writerow(data)
    except Exception as e:
        print('     >> Error in Writing Data into the file => ' + url)
        print('     >> ERRROR => ' + format(e))

# iterate through the fetched links get data and place in the file
def iterateLinks(subLinks):
    for l in subLinks:
        html = getHtml(l)
        if html != False:
            try:
                # check the availibility of product in dubai
                availibility = html.find('option', {'value' : '218'})
                if str(availibility) == NOT_FOUND:
                    continue

                # title of the product
                title = html.find('span', {'class' : 'normal-font range__text-rtl'})
                if str(title) != NOT_FOUND:
                    title = title.get_text(strip=True)
                else:
                    title = 'Title not Found'

                price = html.find('span', {'class' : 'product-pip__price__value'})
                if str(price) != NOT_FOUND:
                    price = price.get_text().split('Dhs ')[1]
                else:
                    price = 'Price not Found'

                description = html.find('div', {'id' : 'pip_product_description'})
                if str(description) != NOT_FOUND:
                    description = description.get_text(strip=True, separator='\n')
                else:
                    description = 'Description Not Found'

                careInstructions = html.find('div', {'id' : 'pip_care_instructions'})
                if str(careInstructions) != NOT_FOUND:
                    careInstructions = careInstructions.get_text(strip=True)
                else:
                    careInstructions = 'Care Instructions Not Found'

                environmentMaterial = html.find('div', {'id' : 'pip_environment_and_material'})
                if str(environmentMaterial) != NOT_FOUND:
                    environmentMaterial = environmentMaterial.get_text(strip=True, separator='\n')
                else:
                    environmentMaterial = 'Environment and Material Not Found'

                size = html.find('div', {'id' : 'pip_dimensions'})
                if str(size) != NOT_FOUND:
                    size = size.get_text(strip=True, separator='\n')
                else:
                    size = 'Size Not Found'

                pictures = html.find('ul', {'class' : 'range-carousel-bullets js-carousel-bullets'})
                picArr = []
                if str(pictures) != NOT_FOUND:
                    pictures = pictures.find_all('img')
                    for pic in pictures:
                        picArr.append(pic.get('src'))
                else:
                    pictures = html.find('div', {'class' : 'range-carousel__image-container js-range-carousel__image-container'})
                    if str(pictures) != NOT_FOUND:
                        picArr.append(pictures.find('img').get('src'))
                    else:
                        picArr.append('Pictures Not Found')

                writeFile([title, price, description, careInstructions, environmentMaterial, size] + picArr, l)
                print('     == Link Done => ' + l)
            except:
                print('     >> Error in Fetching Data from Url => ' + l)
                print('     >> ERRROR => ' + format(e))

# input for user
enteredUrl = input('Please Enter Starting Point for Scrapper: ').rstrip('/')
enteredUrl = enteredUrl.split('/?page=')[0]
print('=== Starting Scrapping ===')
count = 1
while count <= 10:
    html = getHtml(enteredUrl + '/?page=' + str(count))
    paginator = html.find('div', {'class' : 'pagination pagination--center'})
    if str(paginator) == NOT_FOUND:
        break

    count += INCREMENT_ONE

print('=== Fetching Link for All Products ===')
divs = getHtml(enteredUrl + '/?page=' + str(count))
divs = divs.find_all('div' , {'class' : 'product-compact__spacer'})
links = []
for l in divs:
    links.append(l.find('a').get('href'))

# place heading in the file
writeFile([
    'Title',
    'Price',
    'Description',
    'Care Instructions',
    'Environment Material',
    'Size',
    'Pictures'
])

iterateLinks(links)
fHandle.close()
print('=== Scrapping Finished ===')
