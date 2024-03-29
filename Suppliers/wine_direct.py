from Generics.base_site import BaseSite
import re


class WineDirect(BaseSite):
    base_url = 'https://wine-direct.co.il/'
    page = {
        "name":     {"element": "h1", "attrs_prop": "class", "attrs": "product_title", "data": "text"},
        "price":    {"element": "div", "attrs_prop": "class", "attrs": "elementor-jet-single-price", "data": {
                     "element": "bdi", "data": "price"}},
        "volume":   {"element": "td", "attrs_prop": "class", "attrs": "woocommerce-product-attributes-item__value", "data": "text"},
        "available": {"element": "div", "attrs_prop": "class", "attrs": "jet-woo-builder-single-ajax-add-to-cart", "search_word": "TODO", "data": {"element": "div", "attrs_prop": "class", "attrs": "quantity", "data": "exist"}}
    }
    search = {
        "name":     {"element": "h5", "attrs_prop": "class", "attrs": "jet-woo-builder-archive-product-title", "data": {
                     "element": "a", "data": "text"}},
        "price":    {"element": "span", "attrs_prop": "class", "attrs": "woocommerce-Price-amount amount", "data": {
                     "element": "bdi", "data": "price"}},
        "volume_per_100":   {"element": "div", "attrs_prop": "class", "attrs": "jet-listing-dynamic-field__content", "data": "text"},
        "volume":   {"element": "div", "attrs_prop": "class", "attrs": "jet-listing-dynamic-field__content", "data": "text"},
        "available": {"element": "div", "attrs_prop": "class", "attrs": "jet-woo-builder-archive-product-stock-status", "search_word": "TODO", "data": {"element": "p", "attrs_prop": "class", "attrs": "out-of-stock", "data": "not_exist"}}
    }
    results = {
        "element": "div",
        "attrs_prop": "class",
        "attrs": "jet-listing-grid__item jet-listing-dynamic-post"
    }
    product_page_check = {
        "element": "title",
        "search_word": "You searched for",
        "data": "text"
    }
    search_string = '&jet_ajax_search_settings=%7B"search_source"%3A"product"%2C"results_order_by"%3A"relevance"%2C"results_order"%3A"asc"%7D&post_type=product'
    sheet_name = "Alcohol Prices"

    def __init__(self):
        """Constructor for testSite"""
        super().__init__(self.base_url, self.page, self.search, self.results, self.product_page_check, self.search_string)
        super().create_saver(self.sheet_name)
        self.saver.get_name_index_supplier_col('J')

    def build_search_url(self, name):
        return self.base_url + "?s=" + name + self.search_string

    def search_get_volume(self, soup, dictionary):
        volume = self.get_volume_from_price_per_100ml(soup, dictionary)
        if not self.is_not_found_or_none(volume):
            return volume

        stock_status = soup.find("div", class_=re.compile("elementor-widget-jet-woo-builder-archive-stock-status"))
        if not self.is_not_found_or_none(stock_status):
            stock_status = stock_status.previous_sibling.previous_sibling
            if not self.is_not_found_or_none(stock_status):
                volume = self.find_element(stock_status, dictionary["volume"])
                if not self.is_not_found_or_none(volume):
                    return self.volume_cleanup(volume)

        name = self.search_get_name(soup, dictionary)
        volume = self.get_volume_from_name(name)
        if not self.is_not_found_or_none(volume):
            return volume

        return self.data_not_found_str

    def get_price_per_100ml_str(self, soup, dictionary):
        stock_status = soup.find("div", class_=re.compile("elementor-widget-jet-woo-builder-archive-stock-status"))
        if not self.is_not_found_or_none(stock_status):
            stock_status = stock_status.previous_sibling.previous_sibling
            if not self.is_not_found_or_none(stock_status):
                return self.find_element(stock_status, dictionary["volume_per_100"])

    def price_per_100ml_location(self):
        return 0

    def page_get_volume(self, soup, dictionary):
        bottle_volume = soup.find(string="נפח").find_parent("th")
        volume = bottle_volume.next_sibling.next_sibling
        val = self.get_text_safe(volume)
        if self.is_not_found_or_none(val):
            return self.data_not_found_str
        else:
            val = self.get_ml_from_str(val)
            if not self.is_not_found_or_none(val):
                return val

            val = self.get_text_safe(volume)
            val = self.get_volume_from_litter(val)
            if not self.is_not_found_or_none(val):
                return val

            return self.data_not_found_str
