import requests
import re
from bs4 import BeautifulSoup


class Drinks4u:
    base_url = "https://www.drinks4u.co.il/"
    page = {
        "name": {"element": "h1", "attrs": "catalog-title"},
        "price": {"element": "h1", "attrs": "catalog-title"},
        "volume": {"element": "h1", "attrs": "catalog-title"},
        "available": {"element": "h1", "attrs": "catalog-title"}
    }
    search = {
        "name":     {"element": "div", "attrs_prop": "class", "attrs": "prod-box__title"},
        "price":    {"element": "div", "attrs_prop": "class", "attrs": "prod-box__price"},
        "volume":   {"element": "div", "attrs_prop": "class", "attrs": "prod-box__volume"},
        "available": {"element": "h1",  "attrs_prop": "class", "attrs": "catalog-title", "search_word": "מלאי"}
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
        name = soup.find('h1', class_=re.compile("catalog-title")).text.strip()
        print("name: " + name)

        price = soup.find('div', class_=re.compile("price")).find("span").text
        print("price: " + price)

        volume = soup.find('div', class_=re.compile("prod-summary")).find("li").text
        print("volume: " + volume)

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

        # cont = soup.find_all('section', class_=re.compile("elementor-section-full_width"))
        # cont[0].
        # print(cont)
        #
        # def h2fromcont(container):
        #     container.find_all()
        # h2 = map(h2fromcont, cont)
        # print(soup.find('span'))
        # print(soup.find_all('td', id=re.compile("rptFeatureTemplateFieldsBelowPic")))
        # f = soup.find_all('td', id=re.compile("rptFeatureTemplateFieldsBelowPic"))

        # print(f[1])
        # print(soup.find('span', 'aria-label'=re.compile("שם יצרן")))

    def data_from_search_list(self, soup):
        results = soup.find_all('div', class_=re.compile("hp-prods__item"))
        # print(results)
        for result in results:
            # print(result)
            name = self.find(result, self.search["name"])
            print("Name: " + name.text.strip())

            price = self.find(result, self.search["price"])
            print("Price: " + price.text)
            price_words = price.text.split()
            # print(price_words)
            # print(price_words[0])
            price_words[0] = price_words[0].replace(',', '')

            volume = self.find(result, self.search["volume"])

            # print(volume)
            words = volume.text.split()
            # print(words)
            # print(words[-1])
            if re.match(r'^-?\d+(?:\.\d+)$', words[-1]) is not None:
                volume1 = round(float(price_words[0])/float(words[-1]))*100
                print("volume:", volume1)

            available = re.search(self.search["available"]["search_word"], name.text)
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

    def is_product_page(self, soup, name):
        # breadcrumb = soup.find(self.product_page_check["element"], class_=re.compile(self.product_page_check["attrs"]))
        # i = 2
        # while "inner_search"+str(i) in self.product_page_check:
        #     inner_search = "inner_search" + str(i)
        #     search = breadcrumb.find(self.product_page_check[inner_search]["element"], class_=re.compile(self.product_page_check[inner_search]["attrs"]))
        #     i += 1
        search = self.inner_find(soup, self.product_page_check)

        if not re.search(self.product_page_check["search_word"], search.text):
            print("product page")
            return True

    def inner_find(self, soup, dictionary):
        search = soup.find(dictionary["element"], class_=re.compile(dictionary["attrs"]))
        dict_iter = dictionary["inner_search"]

        while True:
            if "attrs" in dict_iter:
                search = search.find(dict_iter["element"], class_=re.compile(dict_iter["attrs"]))
            else:
                search = search.find(dict_iter["element"])
            if "inner_search" not in dict_iter:
                break
            dict_iter = dict_iter["inner_search"]
        return search

    def find(self, soup, dictionary):
        return soup.find(dictionary["element"], attrs={dictionary["attrs_prop"]: re.compile(dictionary["attrs"])})
