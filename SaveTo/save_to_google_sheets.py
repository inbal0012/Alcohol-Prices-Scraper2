import gspread
# from base_save import BaseSave


# class SaveToGoogleSheets(BaseSave):
class SaveToGoogleSheets:
    """"""

    # TODO add sheet size check to next_available_row to avoid crashing in case of out od bound insert
    def __init__(self):
        """Constructor for SaveToGoogleSheets"""
        self.worksheet = None
        self.sheet = None

    # public funcs
    def set_sheet(self, name):
        sa = gspread.service_account()
        self.sheet = sa.open(name)

    def set_worksheet(self, name):
        # TODO? add verification and try catch
        if self.is_worksheet_exist(name):
            self.worksheet = self.sheet.worksheet(name)
        else:
            self.worksheet = self.sheet.add_worksheet(title=name, rows=100, cols=20)

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

    # private funcs
    def next_available_row(self):
        str_list = list(filter(None, self.worksheet.col_values(1)))
        next_row = len(str_list) + 1
        return next_row

    def search_item(self, name, volume):
        list_of_lists = self.worksheet.get_all_values()
        print(f'find {name} vol {volume}')
        for idx, dict in enumerate(list_of_lists):
            if dict[0] == name and volume in dict[2]:
                print(f'found in row {idx+1}')
                return idx+1
        print(f'{name} not pound')
        return -1

    def update_item(self, item, row):
        # cell = self.worksheet.find(item['name'])
        # print(self.get_letter_from_num(cell.col), cell.row)
        start_at = f'A{row}'
        end_at = f'D{row}'
        self.worksheet.update(f'{start_at}:{end_at}',
                              [[item["name"], item["price"], item["volume"], item["available"]]])
        pass

    def save_new_item(self, item):
        print("save_new_item")
        next_row = self.next_available_row()
        start_at = f'A{next_row}'
        end_at = f'D{next_row}'  # TODO calc letter by the num of criteria in item
        self.worksheet.update(f'{start_at}:{end_at}',
                              [[item["name"], item["price"], item["volume"], item["available"]]])
        # self.worksheet.update('A83:D83', [['קלואה', '79', '700 מל', 'True']])

    def is_worksheet_exist(self, name):
        index = self.sheet.worksheet('Index')
        index.update('A1', '')
        index.update('A1', '=sheetnames()', raw=False)
        names = index.col_values(1)

        if name in names:
            print("worksheet exists")
            return True
        else:
            print(f'create worksheet {name}')
            return False

    def get_letter_from_num(self, num):
        return chr(ord('a') + num - 1)
