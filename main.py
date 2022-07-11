# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import re
from bs4 import BeautifulSoup


def first_attempt():
    url = "https://www.the-importer.co.il/Web/?PageType=9&itemid=141204"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    name = soup.find('h1', class_=re.compile("product_title"))
    print("name: " + name.text)

    price = soup.find('p', class_=re.compile("price"))
    print("price: " + price.text)

    volume = soup.find('span', id=re.compile("lblItemVolumePer100ml"))

    print("volume: " + volume.text)
    # print(soup.find('span'))
    # print(soup.find_all('td', id=re.compile("rptFeatureTemplateFieldsBelowPic")))
    f = soup.find_all('td', id=re.compile("rptFeatureTemplateFieldsBelowPic"))

    # print(f[1])
    # print(soup.find('span', 'aria-label'=re.compile("שם יצרן")))


def search_attempt(name):
    url = "https://www.the-importer.co.il/Web/?PageType=9&SearchResults=true&searchString=" + name
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # print(soup)

    results = soup.find_all('li', id=re.compile("liCustomCatalogItem"))
    for result in results:
        # print(result)
        name = result.find('div', class_=re.compile("list-item-name-wrapper")).find('h2')
        # print(name)
        print(name['aria-label'])
        # print("Name: " + name.text)

        prize = result.find('div', class_=re.compile("list-item-price-wrapper")).find('span', class_=re.compile("item-price-value"))
        print("Prize: " + prize.text)

        outOfStock = result.find('div', class_=re.compile("list-item-pic-wrapper")).find('img', alt=re.compile("אזל מהמלאי"))
        if (outOfStock):
            print("outOfStock")

        print("")


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # first_attempt()
    search_attempt('גורדונס')
    # print("-------------------kalua---------------------")
    search_attempt('קלואה')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
