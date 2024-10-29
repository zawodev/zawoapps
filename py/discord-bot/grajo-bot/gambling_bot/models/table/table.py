from gambling_bot.models.table.table_data import TableData

class Table:
    def __init__(self, data, *path):
        self.table_data = TableData(data, *path)
