from gambling_bot.data.json_manager import save_data

class DictData:
    def __init__(self, data, *path):
        self.path = path
        self.data = data

    def save(self):
        save_data(self.data, *self.path)

