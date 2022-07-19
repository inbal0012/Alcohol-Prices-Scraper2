
class BaseSave:
    """"""

    # TODO add sheet size check to next_available_row to avoid crashing in case of out od bound insert
    def __init__(self):
        """Constructor for BaseSave"""
        self.worksheet = None
        self.sheet = None

    # public funcs
    def set_sheet(self, name):
        pass

    def set_worksheet(self, name):
        pass

    def save_item(self, item):
        if self.search_item(item):
            print(f'updating {item["name"]}')
            self.update_item(item)
        else:
            print(f'creating {item["name"]}')
            self.save_new_item(item)

    def save_items(self, items):
        for item in items:
            self.save_item(item)

    # private funcs
    def next_available_row(self):
        pass

    def search_item(self, item):
        name = item['name']
        items = self.worksheet.col_values(1)
        if name in items:
            print(f'{name} found')
            return True
        else:
            print(f'{name} not found')
            return False

    def update_item(self, item):
        pass

    def save_new_item(self, item):
        pass

    def is_worksheet_exist(self, name):
        pass

    def get_letter_from_num(self, num):
        return chr(ord('a') + num-1)

