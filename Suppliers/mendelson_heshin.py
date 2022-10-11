import requests
import re
from bs4 import BeautifulSoup
from Generics.base_site import BaseSite


class MendelsonHeshin(BaseSite):
    base_url = 'https://mendelson-heshin.com/'
    page = {
        "name": {"element": "h1", "attrs_prop": "class", "attrs": "product_title entry-title", "data": "text"},
        "price": {"element": "p", "attrs_prop": "class", "attrs": "price", "data": "price"},
        "special price": {"element": "p", "attrs_prop": "class", "attrs": "price", "data": {
            "element": "ins", "data": "price"}},
        "volume": {"element": "div", "attrs_prop": "class", "attrs": "woocommerce-product-details__short-description",
                   "data": "text"},  # TODO find כמות and move to next sib
        "available": {"element": "div", "attrs_prop": "class", "attrs": "quantity buttons_added", "data": "exist"}
    }
    search = {
        "name": {"element": "li", "attrs_prop": "class", "attrs": "title", "data": {
            "element": "h2", "data": "text"}},
        "price": {"element": "li", "attrs_prop": "class", "attrs": "price-wrap", "data": {
            "element": "span", "attrs_prop": "class", "attrs": "woocommerce-Price-amount amount", "data": "price"}},
        "special price": {"element": "li", "attrs_prop": "class", "attrs": "price-wrap", "data": {
            "element": "ins", "data": "price"}},
        "volume": {"element": "TODO", "attrs_prop": "class", "attrs": "TODO", "data": "text"},
        "available": {"element": "div", "attrs_prop": "class", "attrs": "outofstock-badge", "search_word": "TODO",
                      "data": "not_exist"},
        "paging": {"element": "nav", "attrs_prop": "class", "attrs": "woocommerce-pagination", "data": {
            "element": "li", "data": "find_all"}},
    }
    results = {
        "element": "li",
        "attrs_prop": "class",
        "attrs": "product-type-simple"
    }
    product_page_check = {
        "element": "title",
        "search_word": "חיפוש עבור",
        "data": "text"
    }
    page_sub_soup_dict = {"element": "div", "attrs_prop": "class", "attrs": "elementor-widget-woocommerce-breadcrumb",
                          "data": "element",
                          "parent_element": "div",
                          "parent_attr": "elementor-widget-wrap", }
    search_string = '&jet_ajax_search_settings=%7B"search_taxonomy"%3A"product_cat"%2C"results_order_by"%3A"relevance"%2C"results_order"%3A"asc"%2C"search_source"%3A"any"%7D&jet_ajax_search_categories=0'
    sheet_name = "Alcohol Prices"

    def __init__(self):
        """Constructor for testSite"""
        super().__init__(self.base_url, self.page, self.search, self.results, self.product_page_check,
                         self.search_string)
        # super().from_config(self.con_j)
        super().create_saver(self.sheet_name)
        self.saver.get_name_index_supplier_col('M')

    def build_search_url(self, name):
        value = self.base_url + "/?s=" + name + self.search_string
        return value

    def page_select_sub_soup(self, soup):
        res = self.find_element(soup, self.page_sub_soup_dict)
        parent = res.find_parent(self.page_sub_soup_dict["parent_element"],
                                 class_=re.compile(self.page_sub_soup_dict["parent_attr"]))
        return parent

    def search_get_price(self, soup, dictionary):
        val = self.find_element(soup, dictionary["special price"])
        if val == 'Data not found':
            return super().search_get_price(soup, dictionary)
        return val

    def search_get_volume(self, soup, dictionary):
        name = self.search_get_name(soup, dictionary)
        vol = self.get_volume_from_name(name)
        return vol

    def page_get_price(self, soup, dictionary):
        val = self.find_element(soup, dictionary["special price"])
        if val == 'Data not found':
            return super().page_get_price(soup, dictionary)
        return val

    def page_get_volume(self, soup, dictionary):
        bottle_volume = soup.find(string="כמות").find_parent("th")
        volume = bottle_volume.next_sibling.next_sibling
        val = self.get_text_safe(volume)
        if val == "Data not found" or val == "":
            return "Data not found"
        else:
            return volume.text.split()[0].replace(',', '')
