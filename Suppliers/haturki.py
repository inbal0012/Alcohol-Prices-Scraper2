import requests
import re
from bs4 import BeautifulSoup
from Generics.base_site import BaseSite


class Haturki(BaseSite):
    base_url = "https://www.haturki.com/"
    page = {
        "name": {"element": "div", "attrs_prop": "class", "attrs": "product_info Products", "data": {"element": "h1", "data": "text"}},
        "price": {"element": "div", "attrs_prop": "class", "attrs": "boxPrice", "data": {
                      "element": "span", "attrs_prop": "class", "attrs": "priceNum", "data": "price"}},
        "volume": {"element": "div", "attrs_prop": "class", "attrs": "prod-summary", "data": {
                       "element": "li", "data": "text"}},
        "available": {"element": "div", "attrs_prop": "class", "attrs": "product-box-button-quantity", "data": "exist"}
    }
    search = {
        "name": {"element": "span", "attrs_prop": "class", "attrs": "pname", "data": "text"},
        "price": {"element": "span", "attrs_prop": "class", "attrs": "boxPrice", "data":
            {"element": "span", "attrs_prop": "class", "attrs": "priceNum", "data": "price"}},
        "volume": {"element": "span", "attrs_prop": "class", "attrs": "short_text", "data": "text"},
        "available": {"element": "div", "attrs_prop": "class", "attrs": "cartButton", "search_word": "מלאי", "data": "exist"}
    }
    results = {
        "element": "li",
        "attrs_prop": "class",
        "attrs": "productItem"
    }
    product_page_check = {
        "element": "title",
        "search_word": "חיפוש",
        "data": "text"
    }
    search_string = "תוצאות-חיפוש/?search="
    sheet_name = "Alcohol Prices"

    def __init__(self):
        """Constructor for testSite"""
        super().__init__(self.base_url, self.page, self.search, self.results, self.product_page_check, self.search_string)
        super().create_saver(self.sheet_name)
        self.saver.get_name_index_supplier_col('E')

    def first_attempt(self):
        # url = "https://www.haturki.com/%D7%A7%D7%9C%D7%95%D7%90%D7%94/"
        url = "https://www.haturki.com/%D7%92%D7%A7-%D7%93%D7%A0%D7%99%D7%90%D7%9C%D7%A1-1.75-%D7%9C/"    # out of stock
        # url = "https://www.drinks4u.co.il/index.php?dir=site&page=catalog&op=item&cs=7176"    # 500 ml
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        # print(soup)

        self.data_from_page(soup)

    def data_from_page(self, soup):
        name = soup.find("div", class_=re.compile("product_info Products")).find('h1')
        print("name: " + name.text.strip())

        price = soup.find('div', class_=re.compile("boxPrice")).find("span", class_=re.compile("priceNum"))
        print("price: " + price.text)

        # volume = soup.find('div', class_=re.compile("prod-summary")).find("li")
        # print("volume: " + volume.text)

        # print(soup.find('div', id=re.compile("quantityAndPurchaseButtonsWrapper")))
        available = soup.find('div', class_=re.compile("product-box-button-quantity"))
        # if not available:
            # print("outOfStock")

    def search_get_volume(self, soup, dictionary):
        val = super().search_get_volume(soup, dictionary)
        val = val.split(',')
        return val[0]

    def volume_cleanup(self, volume):
        # TODO handle litter
        return volume
