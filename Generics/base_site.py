import requests
import re
from bs4 import BeautifulSoup
from SaveTo.save_to_google_sheets import SaveToGoogleSheets
import urllib.parse


class BaseSite:
    """some documentation"""
    volume_in_name_threshold = 5
    data_not_found_str = "Data not found"
    ml_variations = ['מ"ל', 'מ”ל', 'מ״ל', 'מל', 'ml']

    def __init__(self, base_url, page, search, results, product_page_check, search_string):
        """Constructor for BaseSite"""
        self.base_url = base_url
        self.page = page
        self.search = search
        self.results = results
        self.product_page_check = product_page_check
        self.search_string = search_string
        self.saver = None

    @classmethod
    def from_config(self, config_json):
        """Constructor for BaseSite"""
        # TODO add KeyError check
        self.base_url = config_json["base_url"]
        self.page = config_json["page"]
        self.search = config_json["search"]
        self.results = config_json["results"]
        self.product_page_check = config_json["product_page_check"]
        self.search_string = config_json["search_string"]
        self.sheet_name = config_json["sheet_name"]

    # TODO: remove מ"ל & ₪ sign from all sites. handle litters for all sites
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
        name = urllib.parse.quote(name)
        url = self.build_search_url(name)
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

    def create_saver(self, sheet_name):
        saver = SaveToGoogleSheets()
        self.set_saver(saver, sheet_name)

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
        sub_soup = self.page_select_sub_soup(soup)

        name = self.page_get_name(sub_soup, self.page)
        name = self.name_cleanup(name)
        print(f'Name: {name}')

        price = self.page_get_price(sub_soup, self.page)
        print(f'Price: {price}')

        volume = self.page_get_volume(sub_soup, self.page)
        print(f'volume: {volume}')

        available = self.page_get_available(sub_soup, self.page)
        if not available:
            print("outOfStock")

        if volume == 50 and 'מיני' not in name:
            name = f'{name} מיני'

        return_value = {
            "name": name,
            "price": price,
            "volume": volume,
            "available": available
        }
        self.save_item(return_value)
        return return_value

    def data_from_search_list(self, soup):
        # TODO add page checking (and ABD in movement)
        pages = self.get_pages(soup, self.search)
        if pages:
            # TODO scan all pages
            print("TODO scan all pages")
        results = self.get_results(soup)
        return_value = []
        # print(results)
        for result in results:
            res = self.data_from_result(result)
            return_value.append(res)

        self.save_items(return_value)
        return return_value

    def data_from_result(self, result):
        name = self.search_get_name(result, self.search)
        print(f'Name: {name}')
        name = self.name_cleanup(name)

        price = self.search_get_price(result, self.search)
        print(f'Price: {price}')

        volume = self.search_get_volume(result, self.search)
        print(f'volume: {volume}')

        available = self.search_get_available(result, self.search)
        if not available:
            print("outOfStock")

        print("")
        return {
            "name": name,
            "price": price,
            "volume": volume,
            "available": available
        }

    def is_product_page(self, soup, name):
        search = self.find_element(soup, self.product_page_check)

        if not re.search(self.product_page_check["search_word"], search):
            print("product page")
            return True

    def get_results(self, soup):
        return soup.find_all(self.results["element"],
                             attrs={self.results["attrs_prop"]: re.compile(self.results["attrs"])})

    def _find(self, soup, dictionary):
        if "attrs" in dictionary:
            return soup.find(dictionary["element"], attrs={dictionary["attrs_prop"]: re.compile(dictionary["attrs"])})
        else:
            return soup.find(dictionary["element"])

    def _find_all(self, soup, dictionary):
        if "attrs" in dictionary:
            return soup.find_all(dictionary["element"],
                                 attrs={dictionary["attrs_prop"]: re.compile(dictionary["attrs"])})
        else:
            return soup.find_all(dictionary["element"])

    def find_element(self, soup, data):
        sub_soup = self._find(soup, data)
        if data["data"] == "exist":
            # if data only needs to exist return value here
            return sub_soup is not None
        elif data["data"] == "not_exist":
            return sub_soup is None
        elif sub_soup is None:
            # Data does not exists raise exception
            return self.data_not_found_str
        elif not isinstance(data["data"], str):
            # Go deeper into the element
            return self.find_element(sub_soup, data["data"])
        elif data["data"] == "text":
            return sub_soup.text.strip()
        elif data["data"] == "price":
            return sub_soup.text.split()[0].replace(',', '')
        elif data["data"] == "element":
            return sub_soup
        elif data["data"] == "find_all":
            return self._find_all(soup, data)
        elif data["data"] == "search":
            pass

    def is_not_found_or_none(self, data):
        val = data == self.data_not_found_str or data is None
        return val

    def get_text_safe(self, soup):
        if soup is not None:
            return soup.text.strip()
        else:
            return self.data_not_found_str

    # TODO change func names to get_X_from_Y

    # region page funcs
    def page_get_name(self, soup, dictionary):
        return self.find_element(soup, dictionary["name"])

    def page_get_price(self, soup, dictionary):
        res = self.find_element(soup, dictionary["price"])
        return self.price_cleanup(res)

    def page_get_volume(self, soup, dictionary):
        res = self.find_element(soup, dictionary["volume"])
        return self.volume_cleanup(res)

    def page_get_available(self, soup, dictionary):
        return self.find_element(soup, dictionary["available"])

    # endregion

    # region search funcs
    def search_get_name(self, soup, dictionary):
        return self.find_element(soup, dictionary["name"])

    def search_get_price(self, soup, dictionary):
        res = self.find_element(soup, dictionary["price"])
        return self.price_cleanup(res)

    def search_get_volume(self, soup, dictionary):
        res = self.find_element(soup, dictionary["volume"])
        return self.volume_cleanup(res)

    def search_get_available(self, soup, dictionary):
        return self.find_element(soup, dictionary["available"])

    # endregion

    def is_saver_defined(self):
        return self.saver is not None

    def page_select_sub_soup(self, soup):
        return soup

    def build_search_url(self, name):
        return self.base_url + self.search_string + name

    # region volume
    def get_volume_from_price_per_100ml(self, soup, dictionary):
        price = self.search_get_price(soup, dictionary)

        price_per_100_str = self.get_price_per_100ml_str(soup, dictionary)
        if self.is_not_found_or_none(price_per_100_str):
            return self.data_not_found_str

        if '100 מ"ל' not in price_per_100_str:
            return self.data_not_found_str

        words = price_per_100_str.split()

        volume_per_100 = words[self.price_per_100ml_location()]
        volume = self.data_not_found_str
        if re.match(r'([0-9]*[.]*[0-9]+)', volume_per_100) is not None:
            volume = round(float(price) / float(volume_per_100) * 100)
        return volume

    def get_volume_from_name(self, name):
        # pattern = re.compile('(?<!\/)([0-9]*[.]*[0-9]+)\s*מ"ל(?![\/A-z])')
        # volume = re.search(pattern, name)
        # if volume is not None:
        volume = self.get_ml_from_str(name)
        if not self.is_not_found_or_none(volume):
            print(f'vol from name = {volume}')
            return self.volume_cleanup(volume)

        volume = self.get_volume_from_litter(name)
        if not self.is_not_found_or_none(volume):
            print(f'vol from name = {volume}')
            return volume
        return self.data_not_found_str

    def get_price_per_100ml_str(self, soup, dictionary):
        return self.find_element(soup, dictionary["volume_per_100"])

    def price_per_100ml_location(self):
        pass

    def get_ml_from_str(self, name):
        words = self.ml_variations
        for word in words:
            pattern = re.compile(f'(?<!\/)([0-9]*[.]*[0-9]+)\s*{word}(?![\/A-z])')
            volume = re.search(pattern, name)
            if volume is not None:
                return f'{volume.group(1)} {word}'

            pattern = re.compile(f'(?<!\/)([0-9]*[.]*[0-9]+)\s* {word}(?![\/A-z])')
            volume = re.search(pattern, name)
            if volume is not None:
                return f'{volume.group(1)} {word}'
        return self.data_not_found_str

    def get_volume_from_litter(self, name):
        volume = self.get_litter_from_str(name)
        if self.is_not_found_or_none(volume):
            return self.data_not_found_str

        pattern = re.compile(f'(?<!\/)([0-9]*[.]*[0-9]+)\s*ליטר(?![\/A-z])')
        number = re.search(pattern, name)
        if number:
            if self.isfloat(number.group(1)):
                number = float(number.group(1))
                if number < self.volume_in_name_threshold:
                    return number * 1000
        if "חצי" in name:
            return self.parse_half_litter(name)
        return 1000

    # endregion

    # region cleanup
    def name_cleanup(self, name):
        # TODO remove volume from name OR search name partially in name_index
        # TODO remove כשר
        # TODO remove (חסר במלאי)

        # Remove '-'
        name = self.remove_hyphen_from_name(name)
        # if 'מ"ל' in name:
        # Remove 2 words
        name = self.remove_ml_from_name(name)
        name = self.remove_litter_from_name(name)
        # if 'ליטר' in name:
        # handle חצי ליטר
        # handle english 1L / 3L etc
        # Check for num in words[-2]?
        # remove as necessary
        # if 'מארז שי' in name:
        # Rename to 'מארז שי - {name1}'
        return re.sub(' +', ' ', name)

    def price_cleanup(self, price):
        return price.replace('₪', '')

    def volume_cleanup(self, volume):
        remove_words = self.ml_variations
        if volume == 'Data not found':
            return volume
        return_volume = volume
        for word in remove_words:
            return_volume = return_volume.replace(word, '')
        return return_volume.strip()
    # endregion

    def get_pages(self, soup, dictionary):
        if "paging" in dictionary:
            res = self.find_element(soup, dictionary["paging"])
            if res == 'Data not found':
                return []
            return res
        else:
            return []

    def get_litter_from_str(self, name):
        if 'ליטר' in name:
            pattern = re.compile(f'(?<!\/)([0-9]*[.]*[0-9]+)\s*ליטר(?![\/A-z])')
            number = re.search(pattern, name)
            if number:
                if self.isfloat(number.group(1)):
                    number = float(number.group(1))
                    if number < self.volume_in_name_threshold:
                        return f'{number} ליטר'
            if "חצי" in name:
                return self.parse_half_litter(name)
            return 1000
        else:
            return self.data_not_found_str

    def parse_half_litter(self, name):
        return 500

    def remove_hyphen_from_name(self, name):
        name = name.replace("–", "-")
        name = name.replace(" - ", " ")
        name = name.replace(" -", " ")
        name = name.replace("- ", " ")
        name = name.replace("-", " ")
        name = name.replace("|", " ")
        name = name.replace("*", " ")
        name = name.replace(",", " ")
        return name

    def remove_ml_from_name(self, name):
        volume = self.get_ml_from_str(name)
        if not self.is_not_found_or_none(volume):
            if ' 50' in volume:
                name = name.replace(f'{volume}', " מיני")
            else:
                name = name.replace(f'{volume}', "")
        return name.strip()

    def remove_litter_from_name(self, name):
        if 'ליטר' in name:
            pattern = re.compile(f'(?<!\/)([0-9]*[.]*[0-9]+)\s*ליטר(?![\/A-z])')
            number = re.search(pattern, name)
            if number:
                if self.isfloat(number.group(1)):
                    fnumber = float(number.group(1))
                    if fnumber < self.volume_in_name_threshold:
                        name = self.remove_litter_with_number(name, number.group(0))
            elif "חצי" in name:
                name = self.remove_litter_and_half(name)
            else:
                name = self.remove_litter_no_additions(name)

        pattern = re.compile(f'(?<!\/)([0-9]*[.]*[0-9]+)\s*L(?![\/A-z])')
        number = re.search(pattern, name)
        if number:
            name = self.remove_litter_with_number(name, number.group(0))

        return name

    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def remove_litter_with_number(self, name, number):
        val = name.replace(number, "")
        print(f"remove_litter_with_number {val}")
        return val.strip()

    def remove_litter_and_half(self, name):
        print("remove_litter_and_half")
        return name

    def remove_litter_no_additions(self, name):
        print("remove_litter_no_additions")
        name = name.replace("ליטר", "").strip()
        return re.sub(' +', ' ', name)

