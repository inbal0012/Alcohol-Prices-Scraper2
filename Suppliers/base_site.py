import requests
import re
from bs4 import BeautifulSoup
from SaveTo.save_to_google_sheets import SaveToGoogleSheets


class BaseSite:
    """some documentation"""

    def __init__(self, base_url, page, search, results, product_page_check, search_string):
        """Constructor for BaseSite"""
        self.base_url = base_url
        self.page = page
        self.search = search
        self.results = results
        self.product_page_check = product_page_check
        self.search_string = search_string
        self.saver = None

    # Public funcs
    def first_attempt(self):
        url = self.base_url + "to be added"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        # self.data_from_page(soup)
        # self.data_from_search_list(soup)

    def specific_page(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        return self.data_from_page(soup)

    def search_attempt(self, name):
        url = self.base_url + self.search_string + name
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        if self.is_product_page(soup, name):
            print("in page")
            return self.data_from_page(soup)
        else:
            print("search")
            return self.data_from_search_list(soup)

    def set_saver(self, saver, sheet_name):
        if type(saver) is SaveToGoogleSheets:
            self.saver = saver
            self.saver.set_sheet(sheet_name)
            self.saver.set_worksheet(type(self).__name__)
        else:
            print("invalid saver")

    def save_item(self, item):
        if self.is_saver_defined():
            self.saver.save_item(item)
        else:
            print("no saver defined")

    def save_items(self, items):
        if self.is_saver_defined():
            self.saver.save_items(items)
        else:
            print("no saver defined")

    # Private funcs
    def data_from_page(self, soup):
        name = self.page_get_name(soup, self.page)
        print("Name: " + name)

        price = self.page_get_price(soup, self.page)
        print("Price: " + price)

        volume = self.page_get_volume(soup, self.page)
        print(f'volume: {volume}')

        available = self.page_get_available(soup, self.page)
        if not available:
            print("outOfStock")

        return_value = {
            "name": name,
            "price": price,
            "volume": volume,
            "available": available
        }
        self.save_item(return_value)
        return return_value

    def data_from_search_list(self, soup):

        results = self.get_results(soup)
        return_value = []
        # print(results)
        for result in results:

            name = self.search_get_name(result, self.search)
            print("Name: " + name)

            price = self.search_get_price(result, self.search)
            print("Price: " + price)

            volume = self.search_get_volume(result, self.search)
            print(f'volume: {volume}')

            available = self.search_get_available(result, self.search)
            if not available:
                print("outOfStock")

            print("")
            return_value.append({
                "name": name,
                "price": price,
                "volume": volume,
                "available": available
            })

        self.save_items(return_value)
        return return_value

    def is_product_page(self, soup, name):
        search = self.find_element(soup, self.product_page_check)

        if not re.search(self.product_page_check["search_word"], search):
            print("product page")
            return True

    def _find(self, soup, dictionary):
        if "attrs" in dictionary:
            return soup.find(dictionary["element"], attrs={dictionary["attrs_prop"]: re.compile(dictionary["attrs"])})
        else:
            return soup.find(dictionary["element"])

    def find_element(self, soup, data):
        sub_soup = self._find(soup, data)
        if not isinstance(data["data"], str):
            return self.find_element(sub_soup, data["data"])
        elif data["data"] == "text":
            return sub_soup.text.strip()
        elif data["data"] == "exist":
            return sub_soup is not None
        elif data["data"] == "price":
            return sub_soup.text.split()[0].replace(',', '')
        elif data["data"] == "search":
            pass

    def page_get_name(self, soup, dictionary):
        return self.find_element(soup, dictionary["name"])

    def page_get_price(self, soup, dictionary):
        return self.find_element(soup, dictionary["price"])

    def page_get_volume(self, soup, dictionary):
        return self.find_element(soup, dictionary["volume"])

    def page_get_available(self, soup, dictionary):
        return self.find_element(soup, dictionary["available"])

    def search_get_name(self, soup, dictionary):
        return self.find_element(soup, dictionary["name"])

    def search_get_price(self, soup, dictionary):
        return self.find_element(soup, dictionary["price"])

    def search_get_volume(self, soup, dictionary):
        return self.find_element(soup, dictionary["volume"])

    def search_get_available(self, soup, dictionary):
        return self.find_element(soup, dictionary["available"])

    def get_results(self, soup):
        return soup.find_all(self.results["element"],
                             attrs={self.results["attrs_prop"]: re.compile(self.results["attrs"])})

    def is_saver_defined(self):
        return self.saver is not None
