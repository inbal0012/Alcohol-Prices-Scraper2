import requests
import re
from bs4 import BeautifulSoup
from Generics.base_site import BaseSite


class Alcohol123(BaseSite):
    base_url = "https://www.alcohol123.co.il/"
    page = {
        "name": {"element": "h1", "attrs_prop": "class", "attrs": "product_title", "data": "text"},
        "price": {"element": "div", "attrs_prop": "class", "attrs": "price", "data": {
                      "element": "span", "data": "price"}},
        "volume": {"element": "div", "attrs_prop": "class", "attrs": "prod-summary", "data": {
                       "element": "li", "data": "text"}},
        "available": {"element": "div", "attrs_prop": "class", "attrs": "qib-container", "data": "exist"}
    }
    search = {
        "name": {"element": "h5", "attrs_prop": "class", "attrs": "jet-woo-product-title", "data": {
            "element": "a", "data": "text"}},
        "price": {"element": "div", "attrs_prop": "class", "attrs": "jet-woo-product-price",
                  "data": {
                      "element": "span", "attrs_prop": "class", "attrs": "woocommerce-Price-amount",
                      "data": {
                          "element": "bdi", "data": "price"}}},
        "volume": {"element": "div", "attrs_prop": "class", "attrs": "jet-woo-product-tags", "data": "text"},
        "available": {"element": "div", "attrs_prop": "class", "attrs": "qib-container", "search_word": "מלאי", "data": "exist"}
    }
    results = {
        "element": "div",
        "attrs_prop": "class",
        "attrs": "jet-woo-products__item"
    }
    product_page_check = {
        "element": "title",
        "search_word": "You searched",
        "data": "text"
    }
    search_string = "&post_type=product&dgwt_wcas=1"
    sheet_name = "Alcohol Prices"

    con_j = dict(
        base_url="https://www.alcohol123.co.il/",
        page={
            "name": {"element": "h1", "attrs_prop": "class", "attrs": "catalog-title", "data": "text"},
            "price": {"element": "div", "attrs_prop": "class", "attrs": "price", "data": {
                "element": "span", "data": "price"}},
            "volume": {"element": "div", "attrs_prop": "class", "attrs": "prod-summary", "data": {
                "element": "li", "data": "text"}},
            "available": {"element": "div", "attrs_prop": "class", "attrs": "product-box-button-quantity",
                          "data": "exist"}
        },
        search={
            "name": {"element": "h5", "attrs_prop": "class", "attrs": "jet-woo-product-title", "data": {
                "element": "a", "data": "text"}},
            "price": {"element": "div", "attrs_prop": "class", "attrs": "jet-woo-product-price",
                      "data": {
                          "element": "span", "attrs_prop": "class", "attrs": "woocommerce-Price-amount",
                          "data": {
                              "element": "bdi", "data": "price"}}},
            "volume": {"element": "div", "attrs_prop": "class", "attrs": "jet-woo-product-tags", "data": "text"},
            "available": {"element": "div", "attrs_prop": "class", "attrs": "qib-container", "search_word": "מלאי",
                          "data": "exist"}
        },
        results={
            "element": "div",
            "attrs_prop": "class",
            "attrs": "jet-woo-products__item"
        },
        product_page_check={
            "element": "title",
            "search_word": "You searched",
            "data": "text"
        },
        search_string="&post_type=product&dgwt_wcas=1",
        sheet_name="Alcohol Prices"
    )

    def __init__(self):
        """Constructor for testSite"""
        super().__init__(self.base_url, self.page, self.search, self.results, self.product_page_check, self.search_string)
        # super().from_config(self.con_j)
        super().create_saver(self.sheet_name)

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

    def build_search_url(self, name):
        value = self.base_url + "/?s=" + name + self.search_string
        return value

    def page_get_volume(self, soup, dictionary):
        bottle_volume = soup.find(string="נפח בקבוק").find_parent("div", class_=re.compile("elementor-column"))
        volume = bottle_volume.next_sibling.next_sibling
        return volume.text.split()[0].replace(',', '')

    def page_select_sub_soup(self, soup):
        details = soup.find(string="פרטי מוצר").find_parent("section", class_=re.compile("elementor-section"))
        return details.find_parent("div", re.compile("elementor-widget-wrap"))

    def search_get_volume(self, soup, dictionary):
        val = super().search_get_volume(soup, dictionary)
        if isinstance(val, Exception):
            print(f'123 search_get_price {val}')
            return self.parse_volume_from_name(soup)
            # do it differently
        return val

    def parse_volume_from_name(self, soup):
        name = self.search_get_name(soup, self.search)
        if 'מ”ל' in name:
            name = name.split()
            return f'{name[-2]}'
            # print('וודקה פינלנדיה – 700 מ”ל')
        elif 'ליטר' in name:
            return 'ליטר'
        return "N/A"
