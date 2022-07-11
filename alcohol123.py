import requests
import re
from bs4 import BeautifulSoup


class Alcohol123:
    def first_attempt(self):
        # url = "https://alcohol123.co.il/product/%d7%95%d7%95%d7%99%d7%a1%d7%a7%d7%99-%d7%91%d7%9c%d7%95%d7%95%d7%99%d7%a0%d7%99-14-%d7%a7%d7%90%d7%a8%d7%99%d7%91%d7%99%d7%90%d7%9f-%d7%a7%d7%90%d7%a1%d7%a7/"
        url = "https://alcohol123.co.il/product/%d7%95%d7%95%d7%99%d7%a1%d7%a7%d7%99-%d7%92%d7%9c%d7%a0%d7%9c%d7%99%d7%95%d7%95%d7%98-12-%d7%a9%d7%a0%d7%94-700-%d7%9e%d7%9c/"
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
        name = soup.find('h1', class_=re.compile("product_title"))
        print("name: " + name.text)

        price = soup.find('p', class_=re.compile("price"))
        print("price: " + price.text)

        # volume = soup.find('span', id=re.compile("lblItemVolumePer100ml"))
        # print("volume: " + volume.text)

        # print(soup.find('div', id=re.compile("quantityAndPurchaseButtonsWrapper")))
        available = soup.find('button', class_=re.compile("add_to_cart_button"))
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
        results = soup.find_all('div', class_=re.compile("jet-woo-products__item"))
        # print(results)
        for result in results:
            # print(result)
            name = result.find('h5', class_=re.compile("jet-woo-product-title"))
            print("Name: " + name.text)

            prize = result.find('div', class_=re.compile("jet-woo-product-price")).find('span', class_=re.compile("woocommerce-Price-amount")).find("bdi")
            print("Prize: " + prize.text)

            volume = result.find("div", class_=re.compile("jet-woo-product-tags")).find("a")
            print("volume: " + volume.text)

            inStock = result.find('div', class_=re.compile("qib-container"))
            if not inStock:
                print("outOfStock")

            print("")

    def search_attempt(self, name):
        url = "https://alcohol123.co.il/?s=" + name + "&post_type=product&dgwt_wcas=1"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        # print(soup)

        if self.is_product_page(soup, name):
            print("in page")
            self.data_from_page(soup)
        else:
            print("search")
            self.data_from_search_list(soup)

    def is_product_page(self, soup, name):
        title = soup.find("title").text

        if not re.search("You searched for", title):
            print("product page")
            return True
