import requests
import re
from bs4 import BeautifulSoup


class TheImporter:
    def data_from_page(self, soup):
        name = soup.find('h1', id=re.compile("headingText"))
        print("name: " + name.text)

        price = soup.find('span', id=re.compile("lblTotalPriceStr"))
        print("price: " + price.text)

        volume = soup.find('span', id=re.compile("lblItemVolumePer100ml"))
        print("volume: " + volume.text)

        # print(soup.find('div', id=re.compile("quantityAndPurchaseButtonsWrapper")))
        available = soup.find('div', id=re.compile("quantityAndPurchaseButtonsWrapper")).find("div", id=re.compile(
            "addToCartBtn"))

        if not available:
            print("outOfStock")

        # print(soup.find('span'))
        # print(soup.find_all('td', id=re.compile("rptFeatureTemplateFieldsBelowPic")))
        f = soup.find_all('td', id=re.compile("rptFeatureTemplateFieldsBelowPic"))

        # print(f[1])
        # print(soup.find('span', 'aria-label'=re.compile("שם יצרן")))

    def data_from_search_list(self, soup):
        results = soup.find_all('li', id=re.compile("liCustomCatalogItem"))
        for result in results:
            # print(result)
            name = result.find('div', class_=re.compile("list-item-name-wrapper")).find('h2')
            # print(name)
            print(name['aria-label'])
            # print("Name: " + name.text)

            prize = result.find('div', class_=re.compile("list-item-price-wrapper")).find('span', class_=re.compile(
                "item-price-value"))
            print("Prize: " + prize.text)

            outOfStock = result.find('div', class_=re.compile("list-item-pic-wrapper")).find('img', alt=re.compile(
                "אזל מהמלאי"))
            if (outOfStock):
                print("outOfStock")

            print("")

    def search_attempt(self, name):
        url = "https://www.the-importer.co.il/Web/?PageType=9&SearchResults=true&searchString=" + name
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        # print(soup)

        if self.is_product_page(soup, name):
            print("in page")
            self.data_from_page(soup)
        else:
            print("search")
            self.data_from_search_list(soup)

        # print(soup.find('li', id=re.compile("catalogDataList")).find('div', class_=re.compile("list-item-name-wrapper")).find('h2').text)

    def is_product_page(self, soup, name):
        # r = requests.get("https://www.the-importer.co.il/Web/?PageType=9&SearchResults=true&searchString=" + name)
        # soup = BeautifulSoup(r.content, "html.parser")

        # url = soup.find("meta", property="og:url")
        # print(url)

        metaKeywords = soup.find("meta", id="metaKeywords")["content"]
        if re.search(name, metaKeywords):
            print("product page")
            return True
