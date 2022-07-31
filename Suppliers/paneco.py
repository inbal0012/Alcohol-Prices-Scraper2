from Generics.base_site import BaseSite
import re


class Paneco(BaseSite):
    base_url = 'https://www.paneco.co.il/'
    page = {
        "name": {"element": "h1", "attrs_prop": "class", "attrs": "page-title", "data": "text"},
        "price": {"element": "div", "attrs_prop": "class", "attrs": "price-final_price", "data": {
            "element": "span", "attrs_prop": "class", "attrs": "price", "data": "price"}},
        "special price": {"element": "span", "attrs_prop": "class", "attrs": "special-price", "data": {
            "element": "span", "attrs_prop": "class", "attrs": "price-wrapper", "data": {
                "element": "span", "attrs_prop": "class", "attrs": "price", "data": "price"}}},
        "volume": {"element": "span", "attrs_prop": "class", "attrs": "product-list-per-100", "data": {
            "element": "span", "attrs_prop": "class", "attrs": "unit", "data": "text"}},
        "available": {"element": "div", "attrs_prop": "class", "attrs": "stock unavailable", "search_word": "TODO",
                      "data": "not_exist"}
    }
    search = {
        "name": {"element": "a", "attrs_prop": "class", "attrs": "product-item-link", "data": "text"},
        "price": {"element": "span", "attrs_prop": "class", "attrs": "price-final_price", "data": {
            "element": "span", "attrs_prop": "class", "attrs": "price", "data": "price"}},
        "special price": {"element": "span", "attrs_prop": "class", "attrs": "special-price", "data": {
            "element": "span", "attrs_prop": "class", "attrs": "price-wrapper", "data": {
            "element": "span", "attrs_prop": "class", "attrs": "price", "data": "price"}}},
        # price-final_price ISN'T the final price. thats the regular price
        "volume": {"element": "span", "attrs_prop": "class", "attrs": "product-list-per-100", "data": {
            "element": "span", "attrs_prop": "class", "attrs": "unit", "data": "text"}},
        "available": {"element": "div", "attrs_prop": "class", "attrs": "stock unavailable", "search_word": "TODO",
                      "data": "not_exist"}
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
        super().__init__(self.base_url, self.page, self.search, self.results, self.product_page_check, self.search_string)
        super().create_saver(self.sheet_name)

    def search_get_price(self, soup, dictionary):
        val = self.find_element(soup, dictionary["special price"])
        if val == 'Data not found':
            return super().search_get_price(soup, dictionary)
        return val
