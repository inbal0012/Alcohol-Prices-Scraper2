import gspread
import time

# from base_save import BaseSave


# class SaveToGoogleSheets(BaseSave):
class SaveToGoogleSheets:
    """"""

    # TODO add sheet size check to next_available_row to avoid crashing in case of out of bound insert
    def __init__(self):
        """Constructor for SaveToGoogleSheets"""
        self.worksheet = None
        self.sheet = None
        self.supplier_col = None

    # public funcs
    def set_sheet(self, name):
        sa = gspread.service_account()
        self.sheet = sa.open(name)

    def set_worksheet(self, name):
        # TODO? add verification and try catch
        if self.is_worksheet_exist(name):
            self.worksheet = self.sheet.worksheet(name)
        else:
            self.worksheet = self.sheet.add_worksheet(title=name, rows=1500, cols=20)

    def save_item(self, item):
        index = self.search_item(item["name"], item["volume"])
        if index != -1:
            print(f'updating {item["name"]}')
            self.update_item(item, index)
        else:
            print(f'creating {item["name"]}')
            self.save_new_item(item)

    def save_items(self, items):
        for item in items:
            self.save_item(item)
            time.sleep(1.5)

    # private funcs
    def next_available_row(self):
        str_list = list(filter(None, self.worksheet.col_values(1)))
        next_row = len(str_list) + 1
        return next_row

    def search_item(self, name, volume):
        list_of_lists = self.worksheet.get_all_values()
        print(f'find {name} vol {volume}')
        for idx, array in enumerate(list_of_lists):
            if array[2] == name and str(volume) in array[4]:
                print(f'found in row {idx+1}')
                return idx+1
        print(f'{name} not pound')
        return -1

    def update_item(self, item, row):
        # cell = self.worksheet.find(item['name'])
        # print(self.get_letter_from_num(cell.col), cell.row)
        start_at = f'C{row}'
        end_at = f'F{row}'
        self.worksheet.update(f'{start_at}:{end_at}',
                              [[item["name"], item["price"], item["volume"], item["available"]]], raw=False)

    def save_new_item(self, item):
        print("save_new_item")
        next_row = self.next_available_row()
        start_at = f'A{next_row}'
        end_at = f'F{next_row}'  # TODO calc letter by the num of criteria in item
        helper = f'=JOIN("|", A{next_row},E{next_row})'
        id = f'=IFNA(INDEX(Name_Index!$A:$A,MATCH(C{next_row}, Name_Index!$B:$B, 0),1), IFNA(INDEX(Name_Index!$A:$A,MATCH(C{next_row}, Name_Index!$C:$C, 0),1), INDEX(Name_Index!$A:$A,MATCH(C{next_row}, INDEX(Name_Index!$A:$A,MATCH(C{next_row}, Name_Index!${self.supplier_col}:${self.supplier_col}, 0),1)))))'
        self.worksheet.update(f'{start_at}:{end_at}',
                              [[id, helper, item["name"], item["price"], item["volume"], item["available"]]], raw=False)
        # self.worksheet.update('A83:D83', [['קלואה', '79', '700 מל', 'True']])

    def is_worksheet_exist(self, name):
        index = self.sheet.worksheet('Index')
        index.update('A1', '')
        index.update('A1', '=sheetnames()', raw=False)
        names = index.col_values(1)

        if name in names:
            print(f'{name} worksheet exists')
            return True
        else:
            print(f'create worksheet {name}')
            return False

    def get_letter_from_num(self, num):
        return chr(ord('a') + num - 1)

    def get_name_index_supplier_col(self, supplier_col):
        self.supplier_col = supplier_col
