import requests
import re
from bs4 import BeautifulSoup


class Drinks4u:
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
        "inner_search": {
            "element": "li",
            "attrs_prop": "class",
            "attrs": "active",
        }
    }

    # Public funcs
    def first_attempt(self):
        url = self.base_url + "index.php?dir=site&page=catalog&op=item&cs=6818"
        # url = "https://www.drinks4u.co.il/index.php?dir=site&page=catalog&op=item&cs=6902"    # out of stock
        # url = "https://www.drinks4u.co.il/index.php?dir=site&page=catalog&op=item&cs=7176"    # 500 ml
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        self.data_from_page(soup)

    def specific_page(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        return self.data_from_page(soup)

    def search_attempt(self, name):
        url = self.base_url + "/index.php?dir=site&page=catalog&op=search&q=" + name
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        # print(soup)

        if self.is_product_page(soup, name):
            print("in page")
            return self.data_from_page(soup)
        else:
            print("search")
            return self.data_from_search_list(soup)

    # Private funcs
    def data_from_page(self, soup):


        name = self.find_in_page(soup, self.page2["name"])
        # self.find(soup, self.page["name"]).text.strip()
        print("Name: " + name)

        price = self.find_in_page(soup, self.page2["price"])
        # self.find(soup, self.page["price"]).text.strip()
        print("Price: " + price)

        available = self.find_in_page(soup, self.page2["available"])
        print(f'Available: {available}')

        # volume = soup.find('div', class_=re.compile("prod-summary")).find("li").text

        volume = self.inner_find(soup, self.page["volume"]).text
        print(f'volume: {volume}')



        # print(soup.find('div', id=re.compile("quantityAndPurchaseButtonsWrapper")))
        available = soup.find('div', class_=re.compile("product-box-button-quantity"))
        availability = True
        if not available:
            print("outOfStock")
            availability = False

        return {
            "name": name,
            "price": price,
            "volume": volume,
            "availability": availability
        }

    def data_from_search_list(self, soup):
        results = soup.find_all('div', class_=re.compile("hp-prods__item"))
        return_value = []
        # print(results)
        for result in results:
            # print(result)
            name = self.find(result, self.search["name"]).text.strip()
            print("Name: " + name)

            price_text = self.find(result, self.search["price"]).text
            price = price_text.split()[0].replace(',', '')
            print("Price: " + price)

            volume_per_100 = self.find_in_page(result, self.search2["volume_per_100"])
            words = volume_per_100.split()
            
            volume = "NA"
            if re.match(r'^-?\d+(?:\.\d+)$', words[-1]) is not None:
                volume = round(float(price)/float(words[-1]))*100
                print("volume:", volume)

            available = re.search(self.search["available"]["search_word"], name)
            availability = True
            if available:
                print("outOfStock")
                availability = False

            print("")
            return_value.append({
                "name": name,
                "price": price_text,
                "volume": volume,
                "availability": availability
            })

        return return_value

    def is_product_page(self, soup, name):
        search = self.inner_find(soup, self.product_page_check)

        if not re.search(self.product_page_check["search_word"], search.text):
            print("product page")
            return True

    def inner_find(self, soup, dictionary):
        # search = soup.find(dictionary["element"], attrs={dictionary["attrs_prop"]: re.compile(dictionary["attrs"])})
        search = soup # self.find(soup, dictionary)
        dict_iter = dictionary # ["inner_search"]

        while True:
            search = self.find(search, dict_iter)
            if "inner_search" not in dict_iter:
                break
            dict_iter = dict_iter["inner_search"]
        return search

    def find(self, soup, dictionary):
            if "attrs" in dictionary:
                return soup.find(dictionary["element"], attrs={dictionary["attrs_prop"]: re.compile(dictionary["attrs"])})
            else:
                return soup.find(dictionary["element"])
        # return soup.find(dictionary["element"], attrs={dictionary["attrs_prop"]: re.compile(dictionary["attrs"])})

    def find2(self, soup, page):
        ret = {}
        for element in page:
            value = self.inner_find(soup, page[element]).text.strip()
            print(f'{element} : {value}')
            ret[element] = value

        return ret

    def find_element(self, soup, dictionary):
        if "attrs" in dictionary:
            return soup.find(dictionary["element"], attrs={dictionary["attrs_prop"]: re.compile(dictionary["attrs"])})
        else:
            return soup.find(dictionary["element"])

    def find_in_page(self, soup, data):
        sub_soup = self.find_element(soup, data)
        if not isinstance(data["data"], str):
            return self.find_in_page(sub_soup, data["data"])
        elif data["data"] == "text":
            return sub_soup.text.strip()
        elif data["data"] == "exist":
            return sub_soup is not None
        elif data["data"] == "price":
            return sub_soup.text.split()[0].replace(',', '')