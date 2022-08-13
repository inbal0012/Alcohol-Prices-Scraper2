from Generics.base_site import BaseSite
import re


class WNF(BaseSite):    # Wine & Flavors
    base_url = 'https://wnf.co.il/'
    page = {
        "name": {"element": "h1", "attrs_prop": "class", "attrs": "page-title", "data": "text"},
        "price": {"element": "span", "attrs_prop": "id", "attrs": "product-price", "data": {
            "element": "span", "attrs_prop": "class", "attrs": "price", "data": "price"}},
        "volume": {"element": "div", "attrs_prop": "class", "attrs": "al_details", "data": {
            "element": "span", "data": "text"}},
        "available": {"element": "div", "attrs_prop": "class", "attrs": "add-to-cart-block", "data": "exist"}
    }
    search = {
        "name": {"element": "div", "attrs_prop": "class", "attrs": "product-item-details top", "data": {
            "element": "a", "data": "text"}},
        "price": {"element": "span", "attrs_prop": "id", "attrs": "product-price", "data": {
            "element": "span", "attrs_prop": "class", "attrs": "price", "data": "price"}},
        "volume": {"element": "div", "attrs_prop": "class", "attrs": "product-item-details top", "data": {
            "element": "div", "attrs_prop": "class", "attrs": "details", "data": "text"}},
        "available": {"element": "div", "attrs_prop": "class", "attrs": "add-to-cart-block", "data": "exist"}
    }
    results = {
        "element": "li",
        "attrs_prop": "class",
        "attrs": "item product product-item"
    }
    product_page_check = {
        "element": "title",
        "search_word": "תוצאות חיפוש",
        "data": "text"
    }
    search_string = "catalogsearch/result/?q="
    sheet_name = "Alcohol Prices"

    def __init__(self):
        """Constructor for testSite"""
        super().__init__(self.base_url, self.page, self.search, self.results, self.product_page_check,
                         self.search_string)
        super().create_saver(self.sheet_name)
        self.saver.get_name_index_supplier_col('K')

    def search_get_volume(self, soup, dictionary):
        val = super().search_get_volume(soup, dictionary)
        words = val.split()
        volume = words[0].replace("ml", "")
        return volume

    def page_select_sub_soup(self, soup):
        return soup.find("div", class_=re.compile("product-top"))
