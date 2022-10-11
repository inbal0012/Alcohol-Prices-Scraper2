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
        self.saver.get_name_index_supplier_col('D')

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
        volume = self.get_volume_from_table(soup, dictionary)
        if volume != "Data not found":
            return volume

        details = soup.find("div", class_=re.compile("elementor-widget-woocommerce-product-title"))
        if details == "Data not found":
            return "Data not found"

        volume = details.next_sibling.next_sibling
        val = self.get_text_safe(volume)
        if val == "Data not found" or val == "":
            return "Data not found"

        if 'ל 100 מ”ל' in val:
            volume = self.get_volume_from_price_per_100ml(soup, dictionary)
            return volume

        return volume.text.split()[0].replace(',', '')

    def get_volume_from_table(self, soup, dictionary):
        bottle_volume = soup.find(string="נפח בקבוק")
        if bottle_volume == "Data not found" or bottle_volume is None:
            return "Data not found"

        bottle_volume = bottle_volume.find_parent("div", class_=re.compile("elementor-column"))
        volume = bottle_volume.next_sibling.next_sibling

        val = self.get_text_safe(volume)
        if val == "Data not found" or val == "":
            return "Data not found"

        return volume.text.split()[0].replace(',', '')

    def get_price_per_100ml_str(self, soup, dictionary):
        price_per_100 =soup.find('100 מ')
        if price_per_100 == "Data not found" or price_per_100 is None:
            return "Data not found"

        price_per_100 = price_per_100.find_parent("div")
        print(price_per_100)
        details = soup.find("div", class_=re.compile("elementor-widget-woocommerce-product-title"))
        if details == "Data not found":
            return "Data not found"

        volume = details.next_sibling.next_sibling
        val = self.get_text_safe(volume)
        if val == "Data not found" or val == "":
            return "Data not found"

        if 'ל 100 מ”ל' in val:
            print(volume.text.split())
            return volume.text.strip()
        else:
            return "Data not found"

    def price_per_100ml_location(self):
        return -2

    def page_select_sub_soup(self, soup):
        # details = soup.find(string="פרטי מוצר").find_parent("section", class_=re.compile("elementor-section"))
        title = soup.find("h1", class_=re.compile("product_title "))
        return title.find_parent("section", re.compile("elementor-top-section"))

    def search_get_volume(self, soup, dictionary):
        val = super().search_get_volume(soup, dictionary)
        if val == "Data not found":
            print(f'123 search_get_price {val}')
            val = self.parse_volume_from_name(soup)
            # do it differently
        val = super().volume_cleanup(val)
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
