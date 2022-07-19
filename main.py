# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


from Suppliers.the_importer import TheImporter
from Suppliers.alcohol123 import Alcohol123
from Suppliers.drinks4u import Drinks4u
from Suppliers.haturki import Haturki
from Suppliers.base_site import BaseSite
from Suppliers.test_site import TestSite
from SaveTo.save_to_google_sheets import SaveToGoogleSheets
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # first_attempt()
    importer = TheImporter()
    # print("-------------------kalua---------------------")
    # importer.search_attempt('קלואה')
    # print("-------------------ג'יימסון---------------------")
    # importer.search_attempt("ג'יימסון")
    alcohol123 = Alcohol123()
    # alcohol123.first_attempt()
    items = alcohol123.search_attempt("ג'ק דניאלס")
    # item = alcohol123.specific_page("https://alcohol123.co.il/product/%d7%95%d7%95%d7%99%d7%a1%d7%a7%d7%99-%d7%92%d7%9c%d7%a0%d7%9c%d7%99%d7%95%d7%95%d7%98-12-%d7%a9%d7%a0%d7%94-700-%d7%9e%d7%9c/")
    # print(items)
    drinks4u = Drinks4u()
    # drinks4u.first_attempt()
    # items = drinks4u.search_attempt("רום")
    # item = drinks4u.specific_page("https://www.drinks4u.co.il/index.php?dir=site&page=catalog&op=item&cs=7050")
    # print(item)
    haturki = Haturki()
    # haturki.first_attempt()
    testSite = TestSite()
    # testSite.specific_page("https://www.drinks4u.co.il/index.php?dir=site&page=catalog&op=item&cs=7050")
    # testSite.search_attempt("מקאלן")

    item = {'name': 'קלואה', 'price': '80', 'volume': '700 מ"ל', 'available': True}
    google_sheet = SaveToGoogleSheets()
    # google_sheet.set_sheet("Alcohol Prices")
    # google_sheet.set_worksheet("Drinks4u")
    # google_sheet.save_item(item)
    # google_sheet.save_items(items)
    # google_sheet.is_worksheet_exist("Sheet9")
    alcohol123.set_saver(google_sheet, "Alcohol Prices")
    alcohol123.save_items(items)
    # alcohol123.save_item(item)


def for_nadav():
    search = []
    for brand in search:
        drinks4u = Drinks4u()
        items = drinks4u.search_attempt(brand)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
