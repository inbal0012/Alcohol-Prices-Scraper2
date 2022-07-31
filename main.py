# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
from Generics.base_site import BaseSite


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def search_my_list_in(supplier):
    print(f'\nmuahahaha lets hack {type(supplier).__name__} site')
    sh = SaveToGoogleSheets()
    sh.set_sheet("מחירון ברבית")
    sh.set_worksheet("אלכוהול לחיפוש")
    alcohol_array = sh.worksheet.col_values(1)
    print(alcohol_array)

    # run_on(supplier, alcohol_array[79])
    # run_on(supplier, alcohol_array[16])

    # for alcohol in alcohol_array:
    #     if alcohol == "אלכוהול" or alcohol == "":
    #         continue
    #     run_on(supplier, alcohol)


def run_on(supplier, name):
    print(name)
    supplier.search_attempt(name)
    time.sleep(3)


from Suppliers.the_importer import TheImporter
from Suppliers.alcohol123 import Alcohol123
from Suppliers.drinks4u import Drinks4u
from Suppliers.haturki import Haturki
from Suppliers.paneco import Paneco
from Suppliers.test_site import TestSite
from SaveTo.save_to_google_sheets import SaveToGoogleSheets
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # first_attempt()
    importer = TheImporter()
    alcohol123 = Alcohol123()
    # items = alcohol123.search_attempt("פינלנדיה")
    # item = alcohol123.specific_page("https://alcohol123.co.il/product/%d7%95%d7%95%d7%99%d7%a1%d7%a7%d7%99-%d7%92%d7%9c%d7%a0%d7%9c%d7%99%d7%95%d7%95%d7%98-12-%d7%a9%d7%a0%d7%94-700-%d7%9e%d7%9c/")
    # alcohol123.save_items(items)
    drinks4u = Drinks4u()
    # items = drinks4u.search_attempt("ג'ק דניאלס")
    # item = drinks4u.specific_page("https://www.drinks4u.co.il/index.php?dir=site&page=catalog&op=item&cs=7050")
    haturki = Haturki()
    # haturki.first_attempt()
    # haturki.search_attempt("ג'ק דניאלס")
    paneco = Paneco()
    # paneco.search_attempt("ג'ק דניאלס")
    paneco.specific_page("https://www.paneco.co.il/jack-daniels-tennessee-honey-12x1000ml-35-3")

    # item = {'name': 'קלואה', 'price': '80', 'volume': '700 מ"ל', 'available': True}
    google_sheet = SaveToGoogleSheets()
    # google_sheet.set_sheet("Alcohol Prices")
    # google_sheet.set_worksheet("Drinks4u")
    # google_sheet.save_item(item)
    # google_sheet.save_items(items)
    # search_my_list_in(importer)
    # search_my_list_in(alcohol123)
    # search_my_list_in(drinks4u)
    # search_my_list_in(haturki)
    # alcohol123.search_attempt("פסואה")
    # haturki.search_attempt("M&H elements red wine")



def for_nadav():
    search = []
    # for brand in search:
        # drinks4u = Drinks4u()
        # items = drinks4u.search_attempt(brand)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
