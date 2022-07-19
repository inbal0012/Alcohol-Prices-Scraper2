import requests
import re
from bs4 import BeautifulSoup


class Haturki:
    def first_attempt(self):
        # url = "https://www.haturki.com/%D7%A7%D7%9C%D7%95%D7%90%D7%94/"
        url = "https://www.haturki.com/%D7%92%D7%A7-%D7%93%D7%A0%D7%99%D7%90%D7%9C%D7%A1-1.75-%D7%9C/"    # out of stock
        # url = "https://www.drinks4u.co.il/index.php?dir=site&page=catalog&op=item&cs=7176"    # 500 ml
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        # print(soup)

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
        name = soup.find("div", class_=re.compile("product_info Products")).find('h1')
        print("name: " + name.text.strip())

        price = soup.find('div', class_=re.compile("boxPrice")).find("span", class_=re.compile("priceNum"))
        print("price: " + price.text)

        # volume = soup.find('div', class_=re.compile("prod-summary")).find("li")
        # print("volume: " + volume.text)

        # print(soup.find('div', id=re.compile("quantityAndPurchaseButtonsWrapper")))
        available = soup.find('div', class_=re.compile("product-box-button-quantity"))
        # if not available:
            # print("outOfStock")

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
            name = result.find('div', class_=re.compile("prod-box__title"))
            print("Name: " + name.text.strip())

            prize = result.find('div', class_=re.compile("prod-box__price"))
            print("Prize: " + prize.text)
            prizeWords = prize.text.split()
            # print(prizeWords)
            # print(prizeWords[0])
            prizeWords[0] = prizeWords[0].replace(',', '')

            volume = result.find("div", class_=re.compile("prod-box__volume"))
            # print(volume)
            words = volume.text.split()
            # print(words)
            # print(words[-1])
            if re.match(r'^-?\d+(?:\.\d+)$', words[-1]) is not None:
                volume1 = round(float(prizeWords[0])/float(words[-1]))*100
                print("volume:", volume1)

            outOfStock = re.search("מלאי", name.text)
            # inStock = result.find('div', class_=re.compile("qib-container"))
            if outOfStock:
                print("outOfStock")

            print("")

    def search_attempt(self, name):
        url = "https://www.drinks4u.co.il/index.php?dir=site&page=catalog&op=search&q=" + name
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
        breadcrumb = soup.find("ol", class_=re.compile("breadcrumb"))
        search = breadcrumb.find("li", class_=re.compile("active"))
        print(search)

        if not re.search("חיפוש", search.text):
            print("product page")
            return True
