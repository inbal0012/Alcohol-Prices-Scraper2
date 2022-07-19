import requests
import re
from bs4 import BeautifulSoup
from Suppliers.base_site import BaseSite


class Alcohol123(BaseSite):
    base_url = "https://www.drinks4u.co.il/"
    page = {
        "name": {"element": "h1", "attrs_prop": "class", "attrs": "catalog-title", "data": "text"},
        "price": {"element": "div", "attrs_prop": "class", "attrs": "price", "data": {
                      "element": "span", "data": "price"}},
        "volume": {"element": "div", "attrs_prop": "class", "attrs": "prod-summary", "data": {
                       "element": "li", "data": "text"}},
        "available": {"element": "div", "attrs_prop": "class", "attrs": "product-box-button-quantity", "data": "exist"}
    }
    search2 = {
        "name": {"element": "div", "attrs": "prod-box__title", "attrs_prop": "class", "data": "text"},
        "price": {"element": "div", "attrs_prop": "class", "attrs": "jet-woo-product-price",
                  "data": {
                      "element": "div", "attrs_prop": "class", "attrs": "woocommerce-Price-amount",
                      "data": {
                          "element": "bdi", "data": "price"}}},
        "volume": {"element": "div", "attrs_prop": "class", "attrs": "prod-box__volume", "data": "text"},
        "available": {"element": "h1", "attrs_prop": "class", "attrs": "catalog-title", "search_word": "מלאי", "data": "text"}
    }
    results = {
        "element": "div",
        "attrs_prop": "class",
        "attrs": "hp-prods__item"
    }
    product_page_check = {
        "element": "ol",
        "attrs": "breadcrumb",
        "attrs_prop": "class",
        "search_word": "חיפוש",
        "data": {
            "element": "li",
            "attrs_prop": "class",
            "attrs": "active",
            "data": "text"
        }
    }
    search_string = "/index.php?dir=site&page=catalog&op=search&q="

    search = {
        "name": {"element": "div", "attrs": "prod-box__title"},
        "price": {
            "element": "div",
            "attrs": "jet-woo-product-price",
            "inner_search": {
                "element": "span",
                "attrs": "woocommerce-Price-amount",
                "inner_search": {
                    "element": "bdi"
                }
            }
        },
        "volume": {"element": "div", "attrs": "prod-box__volume"},
        "available": {"element": "h1", "attrs": "catalog-title", "search_word": "מלאי"}
    }

    page2 = {
        "name": {"element": "h1", "attrs_prop": "class", "attrs": "product_title", "data": "text"},
        "price": {"element": "div", "attrs_prop": "class", "attrs": "price", "data": {
                      "element": "span", "data": "price"}},
        "volume": {"element": "div", "attrs_prop": "class", "attrs": "prod-summary", "data": {
                       "element": "li", "data": "text"}},
        "available": {"element": "button", "attrs_prop": "name", "attrs": "add-to-cart", "data": "exist"}
    }

    def __init__(self):
        """Constructor for testSite"""
        super().__init__(self.base_url, self.page2, self.search2, self.results, self.product_page_check, self.search_string)

    def first_attempt(self):
        # url = "https://alcohol123.co.il/product/%d7%95%d7%95%d7%99%d7%a1%d7%a7%d7%99-%d7%92%d7%9c%d7%a0%d7%9c%d7%99%d7%95%d7%95%d7%98-12-%d7%a9%d7%a0%d7%94-700-%d7%9e%d7%9c/"
        url = "https://alcohol123.co.il/product/%d7%95%d7%95%d7%99%d7%a1%d7%a7%d7%99-%d7%92%d7%a7-%d7%93%d7%a0%d7%99%d7%90%d7%9c%d7%a1-%d7%a1%d7%99%d7%a0%d7%92%d7%9c-%d7%91%d7%90%d7%a8%d7%9c-700-%d7%9e%d7%9c-%d7%9e%d7%97%d7%99%d7%a8/"  # out of stock
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        details = soup.find(string="פרטי מוצר").find_parent("section", class_=re.compile("elementor-section"))
        details_soup = details.find_parent("div", re.compile("elementor-widget-wrap"))
        details_soup = self.page_select_sub_soup(soup)

        name = self.page_get_name(details_soup, self.page)
        print("Name: " + name)

        price = self.page_get_price(details_soup, self.page)
        print("Price: " + price)

        volume = self.page_get_volume(details_soup, self.page)
        print(f'volume: {volume}')

        available = self.page_get_available(details_soup, self.page)
        if not available:
            print("outOfStock")

        # return_value = {
        #     "name": name,
        #     "price": price,
        #     "volume": volume,
        #     "available": available
        # }
        # self.save_item(return_value)
        # self.data_from_page(soup)
        # name = soup.find('h1', class_=re.compile("product_title"))
        # print("name: " + name.text)
        #
        # price = soup.find('p', class_=re.compile("price"))
        # print("price: " + price.text)
        #
        # volume = soup.find('span', id=re.compile("lblItemVolumePer100ml"))
        #
        # print("volume: " + volume.text)
        # # print(soup.find('span'))
        # # print(soup.find_all('td', id=re.compile("rptFeatureTemplateFieldsBelowPic")))
        # f = soup.find_all('td', id=re.compile("rptFeatureTemplateFieldsBelowPic"))
        #
        # print(f[1])
        # print(soup.find('span', 'aria-label'=re.compile("שם יצרן")))

    def page_get_volume(self, soup, dictionary):
        bottle_volume = soup.find(string="נפח בקבוק").find_parent("div", class_=re.compile("elementor-column"))
        volume = bottle_volume.next_sibling.next_sibling
        return volume.text.split()[0].replace(',', '')

    def page_select_sub_soup(self, soup):
        details = soup.find(string="פרטי מוצר").find_parent("section", class_=re.compile("elementor-section"))
        return details.find_parent("div", re.compile("elementor-widget-wrap"))