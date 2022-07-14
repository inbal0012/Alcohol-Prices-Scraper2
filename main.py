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


def data_from_page(soup):
    name = soup.find('h1', class_=re.compile("product_title"))
    print("name: " + name.text)

    price = soup.find('p', class_=re.compile("price"))
    print("price: " + price.text)

    # volume = soup.find('span', id=re.compile("lblItemVolumePer100ml"))
    # print("volume: " + volume.text)

    # print(soup.find('div', id=re.compile("quantityAndPurchaseButtonsWrapper")))
    available = soup.find('button', class_=re.compile("add_to_cart_button"))
    if not available:
        print("outOfStock")

    # cont = soup.find_all('section', class_=re.compile("elementor-section-full_width"))
    # cont[0].
    # print(cont)
    #
    # def h2fromcont(container):
    #     container.find_all()
    # h2 = map(h2fromcont, cont)
    # print(soup.find('span'))
    # print(soup.find_all('td', id=re.compile("rptFeatureTemplateFieldsBelowPic")))
    # f = soup.find_all('td', id=re.compile("rptFeatureTemplateFieldsBelowPic"))

    # print(f[1])
    # print(soup.find('span', 'aria-label'=re.compile("שם יצרן")))


def data_from_search_list(soup):
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


def search_attempt(name):
    url = "https://www.the-importer.co.il/Web/?PageType=9&SearchResults=true&searchString=" + name
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # print(soup)

    if is_product_page(soup, name):
        print("in page")
        data_from_page(soup)
    else:
        print("search")
        data_from_search_list(soup)

    # print(soup.find('li', id=re.compile("catalogDataList")).find('div', class_=re.compile("list-item-name-wrapper")).find('h2').text)


def is_product_page(soup, name):
    # r = requests.get("https://www.the-importer.co.il/Web/?PageType=9&SearchResults=true&searchString=" + name)
    # soup = BeautifulSoup(r.content, "html.parser")

    # url = soup.find("meta", property="og:url")
    # print(url)

    metaKeywords = soup.find("meta", id="metaKeywords")["content"]
    if re.search(name, metaKeywords):
        print("product page")
        return True


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


from the_importer import TheImporter
from alcohol123 import Alcohol123
from drinks4u import Drinks4u
from haturki import Haturki
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # first_attempt()
    importer = TheImporter()
    # print("-------------------גורדונס---------------------")
    # importer.search_attempt('גורדונס')
    # print("-------------------טרי אוליבס---------------------")
    # importer.search_attempt('טרי אוליבס')
    # print("-------------------kalua---------------------")
    # importer.search_attempt('קלואה')
    # print("-------------------ג'יימסון---------------------")
    # importer.search_attempt("ג'יימסון")
    # importer.search_attempt("ג'יימסון סלקט רזרב")
    # print("-------------------ג'ק דניאלס---------------------")
    # importer.search_attempt("ג'ק דניאלס")
    alcohol123 = Alcohol123()
    # alcohol123.first_attempt()
    # alcohol123.search_attempt("ג'ק דניאלס")
    drinks4u = Drinks4u()
    # drinks4u.first_attempt()
    # print(drinks4u.search_attempt("מקאלן"))
    print(drinks4u.specific_page("https://www.drinks4u.co.il/index.php?dir=site&page=catalog&op=item&cs=7050"))
    haturki = Haturki()
    # haturki.first_attempt()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
