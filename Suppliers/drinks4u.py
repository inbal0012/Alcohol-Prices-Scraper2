from Generics.base_site import BaseSite
import re


class Drinks4u(BaseSite):
    base_url = "https://www.drinks4u.co.il/"
    page = {
        "name": {"element": "h1", "attrs_prop": "class", "attrs": "catalog-title", "data": "text"},
        "price": {"element": "div", "attrs_prop": "class", "attrs": "price", "data": {
                      "element": "span", "data": "price"}},
        "volume": {"element": "div", "attrs_prop": "class", "attrs": "prod-summary", "data": {
                       "element": "li", "data": "text"}},
        "available": {"element": "div", "attrs_prop": "class", "attrs": "product-box-button-quantity", "data": "exist"}
    }
    search = {
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
        super().__init__(self.base_url, self.page, self.search, self.results, self.product_page_check, self.search_string)
        super().create_saver(self.sheet_name)
        self.saver.get_name_index_supplier_col('E')

    def search_get_name(self, soup, dictionary):
        name = super().search_get_name(soup, dictionary)
        return self.name_cleanup(name)

    def search_get_volume(self, soup, dictionary):
        return self.get_volume_from_price_per_100ml(soup, dictionary)

    def price_per_100ml_location(self):
        return -1

    def search_get_available(self, soup, dictionary):
        available = re.search(self.search["available"]["search_word"], super().search_get_name(soup, dictionary))
        availability = True
        if available:
            availability = False
        return availability

    def name_cleanup(self, name):
        name = name.replace("(חסר במלאי)", "")
        # TODO remove volume from name OR search name partially in name_index
        return name.strip()

