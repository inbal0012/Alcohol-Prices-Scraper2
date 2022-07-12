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
        "name": {"element": "div", "attrs": "prod-box__title"},
        "price": {"element": "div", "attrs": "prod-box__price"}, #if parent aria-hidden="true" go to next sibling
        "volume": {"element": "div", "attrs": "prod-box__volume"},
        "available": {"element": "h1", "attrs": "catalog-title", "search_word": "מלאי"}
    }
    results = {
        "element": "div",
        "attrs": "hp-prods__item"
    }
    product_page_check = {
        "element": "ol",
        "attrs": "breadcrumb",
        "search_word": "חיפוש",
        "inner_search2": {
            "element": "li",
            "attrs": "active",
        }
    }

    def first_attempt(self):
        url = self.base_url + "index.php?dir=site&page=catalog&op=item&cs=6818"
        # url = "https://www.drinks4u.co.il/index.php?dir=site&page=catalog&op=item&cs=6902"    # out of stock
        # url = "https://www.drinks4u.co.il/index.php?dir=site&page=catalog&op=item&cs=7176"    # 500 ml
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        self.data_from_page(soup)
        # name = soup.find('h1', class_=re.compile("product_title"))
        # print("name: " + name.text)
        #
        # price = soup.find('p', class_=re.compile("price"))
        # print("price: " + price.text)
        #
        # volume = soup.find('span', id=re.compile("lblItemVolumePer100ml"))
        #
        # print("volume: " + volume.text)
        # # print(soup.find('span'))
        # # print(soup.find_all('td', id=re.compile("rptFeatureTemplateFieldsBelowPic")))
        # f = soup.find_all('td', id=re.compile("rptFeatureTemplateFieldsBelowPic"))
        #
        # print(f[1])
        # print(soup.find('span', 'aria-label'=re.compile("שם יצרן")))

    def data_from_page(self, soup):
        name = soup.find('h1', class_=re.compile("catalog-title"))
        print("name: " + name.text.strip())

        price = soup.find('div', class_=re.compile("price")).find("span")
        print("price: " + price.text)

        volume = soup.find('div', class_=re.compile("prod-summary")).find("li")
        print("volume: " + volume.text)

        # print(soup.find('div', id=re.compile("quantityAndPurchaseButtonsWrapper")))
        available = soup.find('div', class_=re.compile("product-box-button-quantity"))
        if not available:
            print("outOfStock")

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
            name = result.find(self.search["name"]["element"], class_=re.compile(self.search["name"]["attrs"]))
            print("Name: " + name.text.strip())

            prize = result.find(self.search["price"]["element"], class_=re.compile(self.search["price"]["attrs"]))
            print("Prize: " + prize.text)
            prizeWords = prize.text.split()
            # print(prizeWords)
            # print(prizeWords[0])
            prizeWords[0] = prizeWords[0].replace(',', '')

            volume = result.find(self.search["volume"]["element"], class_=re.compile(self.search["volume"]["attrs"]))
            # print(volume)
            words = volume.text.split()
            # print(words)
            # print(words[-1])
            if re.match(r'^-?\d+(?:\.\d+)$', words[-1]) is not None:
                volume1 = round(float(prizeWords[0])/float(words[-1]))*100
                print("volume:", volume1)

            outOfStock = re.search(self.search["available"]["search_word"], name.text)
            # inStock = result.find('div', class_=re.compile("qib-container"))
            if outOfStock:
                print("outOfStock")

            print("")

    def search_attempt(self, name):
        url = self.base_url + "/index.php?dir=site&page=catalog&op=search&q=" + name
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        # print(soup)

        if self.is_product_page(soup, name):
            print("in page")
            self.data_from_page(soup)
        else:
            print("search")
            self.data_from_search_list(soup)

    def inner_find(self, soup, dictionary):
        search = soup.find(dictionary["element"], class_=re.compile(dictionary["attrs"]))
        i = 2
        while "inner_search"+str(i) in dictionary:
            inner_search = "inner_search" + str(i)
            search = soup.find(dictionary[inner_search]["element"], class_=re.compile(dictionary[inner_search]["attrs"]))
            i += 1
        return search

    def is_product_page(self, soup, name):
        # breadcrumb = soup.find(self.product_page_check["element"], class_=re.compile(self.product_page_check["attrs"]))
        # i = 2
        # while "inner_search"+str(i) in self.product_page_check:
        #     inner_search = "inner_search" + str(i)
        #     search = breadcrumb.find(self.product_page_check[inner_search]["element"], class_=re.compile(self.product_page_check[inner_search]["attrs"]))
        #     i += 1
        search = self.inner_find(soup, self.product_page_check)
        print(search)

        if not re.search(self.product_page_check["search_word"], search.text):
            print("product page")
            return True
