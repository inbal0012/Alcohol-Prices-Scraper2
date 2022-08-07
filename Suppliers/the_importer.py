from Generics.base_site import BaseSite
import re


class TheImporter(BaseSite):
    base_url = 'https://www.the-importer.co.il/'
    page = {
        "name":     {"element": "TODO", "attrs_prop": "class", "attrs": "TODO", "data": "text"},
        "price":    {"element": "TODO", "attrs_prop": "class", "attrs": "TODO", "data": {
                     "element": "TODO", "data": "price"}},
        "volume":   {"element": "TODO", "attrs_prop": "class", "attrs": "TODO", "data": {
                     "element": "TODO", "data": "text"}},
        "available": {"element": "TODO", "attrs_prop": "class", "attrs": "TODO", "data": "exist"}
    }
    search = {
        "name":     {"element": "div", "attrs_prop": "class", "attrs": "list-item-name-wrapper", "data": {
                     "element": "h2", "data": "text"}},
        "price":    {"element": "span", "attrs_prop": "class", "attrs": "item-price-value", "data": "text"},
        "volume":   {"element": "div", "attrs_prop": "class", "attrs": "list-item-name-wrapper", "data": {
                     "element": "a", "data": "element"}},
        "available": {"element": "div", "attrs_prop": "class", "attrs": "list-item-pic-wrapper", "search_word": "אזל מהמלאי", "data": {
                     "element": "img", "attrs_prop": "alt", "attrs": "אזל מהמלאי", "data": "not_exist"}}
    }
    results = {
        "element": "li",
        "attrs_prop": "id",
        "attrs": "liCustomCatalogItem"
    }
    product_page_check = {
        "element": "meta",
        "attrs_prop": "id",
        "attrs": "metaKeywords",
        "search_word": "TODO",
        "data": "text"
    }
    search_string = "Web/?PageType=9&SearchResults=true&searchString="
    sheet_name = "Alcohol Prices"

    def __init__(self):
        """Constructor for testSite"""
        super().__init__(self.base_url, self.page, self.search, self.results, self.product_page_check, self.search_string)
        super().create_saver(self.sheet_name)

    def is_product_page(self, soup, name):
        meta_keywords = soup.find("meta", id="metaKeywords")["content"]
        if re.search(name, meta_keywords):
            print("product page")
            return True

    def search_get_volume(self, soup, dictionary):
        vol = super().search_get_volume(soup, dictionary)
        par = vol.find_parent("span")
        volume = par.next_sibling.next_sibling.next_sibling.text.split()
        if "ליטר" in volume:
                return int(volume[0]) * 1000
        # todo handle litter
        print(volume[0])
        return volume[0]
