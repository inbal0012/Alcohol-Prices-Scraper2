from Generics.base_site import BaseSite
import re


class Drinks4u(BaseSite):
    base_url = "https://www.drinks4u.co.il/"
    page = {
        "name": {"element": "h1", "attrs_prop": "class", "attrs": "catalog-title"},
        "price": {"element": "div", "attrs_prop": "class", "attrs": "price",
                  "inner_search": {
                      "element": "span",
                  }},
        "volume": {"element": "div", "attrs_prop": "class", "attrs": "prod-summary",
                   "inner_search": {
                       "element": "li",
                   }},
        "available": {"element": "div", "attrs_prop": "class", "attrs": "product-box-button-quantity", }
    }
    page2 = {
        "name": {"element": "h1", "attrs_prop": "class", "attrs": "catalog-title", "data": "text"},
        "price": {"element": "div", "attrs_prop": "class", "attrs": "price", "data": {
                      "element": "span", "data": "price"}},
        "volume": {"element": "div", "attrs_prop": "class", "attrs": "prod-summary", "data": {
                       "element": "li", "data": "text"}},
        "available": {"element": "div", "attrs_prop": "class", "attrs": "product-box-button-quantity", "data": "exist"}
    }
    search = {
        "name":     {"element": "div", "attrs_prop": "class", "attrs": "prod-box__title"},
        "price":    {"element": "div", "attrs_prop": "class", "attrs": "prod-box__price"},
        "volume":   {"element": "div", "attrs_prop": "class", "attrs": "prod-box__volume"},
        "available": {"element": "h1",  "attrs_prop": "class", "attrs": "catalog-title", "search_word": "מלאי"}
    }
    search2 = {
        "name": {"element": "div", "attrs_prop": "class", "attrs": "prod-box__title", "data": "text"},
        "price": {"element": "div", "attrs_prop": "class", "attrs": "prod-box__price", "data": "price"},
        "volume_per_100": {"element": "div", "attrs_prop": "class", "attrs": "prod-box__volume", "data": "text"},
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
    sheet_name = "Alcohol Prices"

    def __init__(self):
        """Constructor for testSite"""
        super().__init__(self.base_url, self.page2, self.search2, self.results, self.product_page_check, self.search_string)
        super().create_saver(self.sheet_name)


    def search_get_volume(self, soup, dictionary):
        price = self.search_get_price(soup, self.search)

        price_per_100_str = self.find_element(soup, self.search2["volume_per_100"])
        words = price_per_100_str.split()

        price_per_100ml = words[-1]
        volume = "NA"
        if re.match(r'^-?\d+(?:\.\d+)$', price_per_100ml) is not None:
            volume = round(float(price) / float(price_per_100ml)) * 100
        return volume

    def search_get_available(self, soup, dictionary):
        available = re.search(self.search["available"]["search_word"], self.search_get_name(soup, dictionary))
        availability = True
        if available:
            availability = False
        return availability
