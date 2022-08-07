# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
from Generics.base_site import BaseSite


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def test_supplier(supplierClass):
    supplier = supplierClass()
    keep_testing = True
    while keep_testing:
        print(f'\n\ntesting {type(supplier).__name__}')
        print("what do you want to do?")
        print("first_attempt enter f")
        print("""
first_attempt   enter first
search_attempt  enter search
specific_page   enter page
to exit         enter exit
        """)
        choise = input("please select: ")
        if choise in "exit":
            keep_testing = False
        if choise in "first":
            supplier.first_attempt()
        elif choise in "search":
            supplier.search_attempt("טנקרי")
        elif choise in "page":
            url = input("enter URL: ")
            supplier.specific_page(url)


def search_my_list_in(supplier):
    print(f'\nmuahahaha lets hack {type(supplier).__name__} site')
    sh = SaveToGoogleSheets()
    sh.set_sheet("מחירון ברבית")
    sh.set_worksheet("אלכוהול לחיפוש")
    alcohol_array = sh.worksheet.col_values(1)
    print(alcohol_array)

    # run_on(supplier, alcohol_array[79])
    # run_on(supplier, alcohol_array[16])

    for alcohol in alcohol_array:
        if alcohol == "אלכוהול" or alcohol == "":
            continue
        run_on(supplier, alcohol)


def run_on(supplier, name):
    print(name)
    supplier.search_attempt(name)
    time.sleep(3)


from Suppliers.the_importer import TheImporter
from Suppliers.alcohol123 import Alcohol123
from Suppliers.drinks4u import Drinks4u
from Suppliers.haturki import Haturki
from Suppliers.paneco import Paneco
from Suppliers.blend import Blend
from Suppliers.terminal3 import Terminal3
from Suppliers.wine_direct import WineDirect
from Suppliers.wnf import WNF
from Suppliers.test_site import TestSite
from SaveTo.save_to_google_sheets import SaveToGoogleSheets
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # first_attempt()
    # test_supplier(Alcohol123)
    # test_supplier(Drinks4u)
    # test_supplier(Haturki)
    # test_supplier(Paneco)
    # test_supplier(TheImporter)
    # test_supplier(Blend)
    # test_supplier(WineDirect)
    test_supplier(WNF)

    # item = {'name': 'קלואה', 'price': '80', 'volume': '700 מ"ל', 'available': True}
    # google_sheet = SaveToGoogleSheets()
    # google_sheet.set_sheet("Alcohol Prices")
    # google_sheet.set_worksheet("Drinks4u")
    # google_sheet.save_item(item)
    # google_sheet.save_items(items)

    # search_my_list_in(importer)
    # search_my_list_in(alcohol123)
    # search_my_list_in(drinks4u)
    # search_my_list_in(haturki)
    # search_my_list_in(paneco)



def for_nadav():
    search = []
    # for brand in search:
        # drinks4u = Drinks4u()
        # items = drinks4u.search_attempt(brand)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
