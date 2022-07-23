from Generics.base_site import BaseSite
import re


class Paneco(BaseSite):
    base_url = "https://www.paneco.co.il"
    page = {
        "name": {"element": "h1", "attrs_prop": "class", "attrs": "catalog-title", "data": "text"},
        "price": {"element": "div", "attrs_prop": "class", "attrs": "price", "data": {
                      "element": "span", "data": "price"}},
        "volume": {"element": "div", "attrs_prop": "class", "attrs": "prod-summary", "data": {
                       "element": "li", "data": "text"}},
        "available": {"element": "div", "attrs_prop": "class", "attrs": "product-box-button-quantity", "data": "exist"}
    }
    search = {
        "name": {"element": "strong", "attrs_prop": "class", "attrs": "product-item-name", "data": {"element": "a", "attrs_prop": "class", "attrs": "product-item-link", "data": "text"}},
        "price": {"element": "div", "attrs_prop": "class", "attrs": "unit-price-wrapper", "data": {"element": "span", "attrs_prop": "class", "attrs": "unit", "data": "text"}},
        "volume_per_100": {"element": "div", "attrs_prop": "class", "attrs": "prod-box__volume", "data": "text"},
        "available": {"element": "h1", "attrs_prop": "class", "attrs": "catalog-title", "search_word": "מלאי", "data": "text"}
    }
    results = {
        "element": "li",
        "attrs_prop": "class",
        "attrs": "product product-item"
    }
    product_page_check = {
        "element": "div",
        "attrs": "breadcrumb",
        "attrs_prop": "class",
        "search_word": "חיפוש",
        "data": {
            "element": "li",
            "attrs_prop": "class",
            "attrs": "search",
            "data": "exist"
        }
    }
    search_string = "/catalogsearch/result/?q="

    def __init__(self):
        """Constructor for testSite"""
        super().__init__(self.base_url, self.page, self.search, self.results, self.product_page_check, self.search_string)

    def is_product_page(self, soup, name):
        search = self.find_element(soup, self.product_page_check)

        if not search:
            print("product page")
            return True

    def search_get_volume(self, soup, dictionary):
        price = self.search_get_price(soup, self.search)

        volume_per_100 = self.find_element(soup, self.search["volume_per_100"])
        words = volume_per_100.split()

        volume = "NA"
        if re.match(r'^-?\d+(?:\.\d+)$', words[-1]) is not None:
            volume = round(float(price) / float(words[-1])) * 100
        return volume

    def search_get_available(self, soup, dictionary):
        available = re.search(self.search["available"]["search_word"], self.search_get_name(soup, dictionary))
        availability = True
        if available:
            availability = False
        return availability
