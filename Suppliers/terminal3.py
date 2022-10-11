from Generics.base_site import BaseSite
class Terminal3(BaseSite):
    base_url = 'https://terminal-3.co.il/'
    page = {
        "name": {"element": "TODO", "attrs_prop": "class", "attrs": "TODO", "data": "text"},
        "price": {"element": "TODO", "attrs_prop": "class", "attrs": "TODO", "data": {
            "element": "TODO", "data": "price"}},
        "volume": {"element": "TODO", "attrs_prop": "class", "attrs": "TODO", "data": {
            "element": "TODO", "data": "text"}},
        "available": {"element": "TODO", "attrs_prop": "class", "attrs": "TODO", "data": "exist"}
    }
    search = {
        "name": {"element": "p", "attrs_prop": "class", "attrs": "main-title", "data": "text"},
        "price": {"element": "p", "attrs_prop": "class", "attrs": "price club-price", "data": "price"},
        "volume": {"element": "TODO", "attrs_prop": "class", "attrs": "TODO", "data": "text"},
        "available": {"element": "div", "attrs_prop": "class", "attrs": "action-wrapp", "search_word": "TODO",
                      "data": "exist"}
    }
    results = {
        "element": "div",
        "attrs_prop": "class",
        "attrs": "product-item"
    }
    product_page_check = {
        "element": "div",
        "attrs_prop": "class",
        "attrs": "breadcrumbs",
        "search_word": "תוצאות חיפוש",
        "data": {"element": "p", "data": "text"}
    }
    search_string = "searchItems/"
    sheet_name = "Alcohol Prices"

    def __init__(self):
        """Constructor for testSite"""
        super().__init__(self.base_url, self.page, self.search, self.results, self.product_page_check, self.search_string)
        super().create_saver(self.sheet_name)
