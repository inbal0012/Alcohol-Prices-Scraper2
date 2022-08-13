import requests
import re
from bs4 import BeautifulSoup
from Generics.base_site import BaseSite


class Aquavita(BaseSite):
    base_url = 'https://www.aquavita.co.il/'
    page = {
        "name":     {"element": "h1", "attrs_prop": "class", "attrs": "product_title entry-title", "data": "text"},
        "price":    {
            "title": "מחיר מחירון:",
            "parent_element": "div",
            "parent_attr": "elementor-inner-column elementor-element",
            "find_price": {
            "element": "span", "attrs_prop": "class", "attrs": "woocommerce-Price-amount amount", "data": "price"}
        },
        "special price": {
            "title": "מחיר מבצע:",
            "parent_element": "div",
            "parent_attr": "elementor-inner-column elementor-element",
            "find_price": {"element": "ins", "data": {
            "element": "span", "attrs_prop": "class", "attrs": "woocommerce-Price-amount amount", "data": "price"}}
        },
        "volume":   {"element": "th", "attrs_prop": "class", "attrs": "woocommerce-product-attributes-item__label", "data": {
                     "element": "a", "data": "text"}},
        "available": {"element": "div", "attrs_prop": "class", "attrs": "elementor-add-to-cart elementor-product-simple", "data": {
            "element": "p", "attrs_prop": "class", "attrs": "stock out-of-stock", "data": "not_exist"}}
    }
    search = {
        "name":     {"element": "h2", "attrs_prop": "class", "attrs": "woocommerce-loop-product__title", "data": "text"},
        "price":    {"element": "span", "attrs_prop": "class", "attrs": "price", "data": "price"},
        "special price":    {"element": "span", "attrs_prop": "class", "attrs": "price", "data": {
                     "element": "ins", "data": "price"}},
        "volume":   {"element": "TODO", "attrs_prop": "class", "attrs": "TODO", "data": "text"},
        "available": {"element": "a", "attrs_prop": "class", "attrs": "add_to_cart_button", "search_word": "TODO", "data": "exist"}
    }
    results = {
        "element": "li",
        "attrs_prop": "class",
        "attrs": "product type-product"
    }
    product_page_check = {
        "element": "title",
        "search_word": "חיפוש עבור",
        "data": "text"
    }
    search_string = "&post_type=product&dgwt_wcas=1"
    sheet_name = "Alcohol Prices"

    def __init__(self):
        """Constructor for testSite"""
        super().__init__(self.base_url, self.page, self.search, self.results, self.product_page_check, self.search_string)
        # super().from_config(self.con_j)
        super().create_saver(self.sheet_name)
        self.saver.get_name_index_supplier_col('L')

    def build_search_url(self, name):
        value = self.base_url + "/?s=" + name + self.search_string
        return value

    def page_get_volume(self, soup, dictionary):
        bottle_volume = soup.find(string="נפח").find_parent("th")
        volume = bottle_volume.next_sibling.next_sibling
        print(volume)
        val = self.get_text_safe(volume)
        if val == "Data not found" or val == "":
            return "Data not found"
        else:
            return volume.text.split()[0].replace(',', '')

    def page_get_price(self, soup, dictionary):
        val = self.get_price(soup, dictionary["special price"])

        if val == 'Data not found':
            val = self.get_price(soup, dictionary["price"])
        return val

    def get_price(self, soup, dictionary):
        bottle_price = soup.find(string=dictionary["title"])
        parent = bottle_price.find_parent(dictionary["parent_element"], class_=re.compile(dictionary["parent_attr"]))
        print(parent)
        price = parent.next_sibling.next_sibling
        print(price)

        val = self.find_element(price, dictionary["find_price"])
        return val

    def search_get_price(self, soup, dictionary):
        val = self.find_element(soup, dictionary["special price"])
        if val == 'Data not found':
            return super().search_get_price(soup, dictionary)
        return val

    def search_get_volume(self, soup, dictionary):
        val = self.parse_volume_from_name(soup)
        if 'ליטר' in val:
            # TODO better parse litters שוופס טוניק for example
            val = '1000'
        return val

    def parse_volume_from_name(self, soup):
        name = self.search_get_name(soup, self.search)
        # TODO מארז
        if 'מ”ל' in name:
            name = name.split()
            return f'{name[-2]}'
            # print('וודקה פינלנדיה – 700 מ”ל')
        elif 'ליטר' in name:
            return '1000'
        return "N/A"
