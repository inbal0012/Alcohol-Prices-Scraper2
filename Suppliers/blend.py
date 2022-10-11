from Generics.base_site import BaseSite
import re


class Blend(BaseSite):
    base_url = 'https://blend.co.il/'
    page = {
        "name": {"element": "h1", "attrs_prop": "class", "attrs": "product-name", "data": "text"},
        "price": {"element": "div", "attrs_prop": "class", "attrs": "logged-price list", "data": {
            "element": "p", "attrs_prop": "class", "attrs": "total-price", "data": "text"}},
        "volume": {"element": "div", "attrs_prop": "class", "attrs": "value long-description", "data": {
            "element": "li", "data": "text"}},
        "available": {"element": "div", "attrs_prop": "class", "attrs": "product-label", "search_word": "אזל מהמלאי",
                      "data": {
                          "element": "p", "data": "text"}}
    }
    search = {
        "name": {"element": "div", "attrs_prop": "class", "attrs": "tile-body", "data": {
            "element": "a", "data": "text"}},
        "price": {"element": "div", "attrs_prop": "class", "attrs": "logged-price list", "data": {
            "element": "p", "attrs_prop": "class", "attrs": "total-price", "data": "text"}},
        "volume": {"element": "TODO", "attrs_prop": "class", "attrs": "TODO", "data": "text"},
        "available": {"element": "div", "attrs_prop": "class", "attrs": "product-label", "search_word": "אזל מהמלאי",
                      "data": {
                          "element": "p", "data": "text"}}
    }
    results = {
        "element": "div", "attrs_prop": "class", "attrs": "tiles__item", "data":
            {"element": "div", "attrs_prop": "class", "attrs": "product-tile", "data": "element"}
    }
    product_page_check = {
        "element": "li",
        "attrs_prop": "class",
        "attrs": "breadcrumb-item",
        "search_word": "TODO",
        "data": "exist"
    }
    search_string = "search?q="
    sheet_name = "Alcohol Prices"

    def __init__(self):
        """Constructor for testSite"""
        super().__init__(self.base_url, self.page, self.search, self.results, self.product_page_check, self.search_string)
        super().create_saver(self.sheet_name)
        self.saver.get_name_index_supplier_col('I')

    def is_product_page(self, soup, name):
        prod_page = self.find_element(soup, self.product_page_check)

        if prod_page:
            print("product page")
            return True

    def page_get_price(self, soup, dictionary):
        val = super().page_get_price(soup, dictionary)
        return val.split()[1].replace(',', '')

    def page_get_volume(self, soup, dictionary):
        val = super().page_get_volume(soup, dictionary)
        vals = val.split()
        if "נפח" in vals[0]:
            return val.split()[1]
        return "Data not found"

    def page_get_available(self, soup, dictionary):
        val = self.find_element(soup, dictionary["available"])
        if val == "Data not found":
            return True

        search = re.search(dictionary["available"]["search_word"], val)
        if search is not None:
            return False
        return True

    def search_get_price(self, soup, dictionary):
        val = super().search_get_price(soup, dictionary)
        return val.replace(',', '')

    def search_get_available(self, soup, dictionary):
        val = self.find_element(soup, dictionary["available"])
        if val == "Data not found":
            return True

        search = re.search(dictionary["available"]["search_word"], val)
        if search is not None:
            return False
        return True

