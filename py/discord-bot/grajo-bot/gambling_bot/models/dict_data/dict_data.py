from gambling_bot.data.json_manager import save_data, delete_data

class DictData:
    def __init__(self, default_data, data, *path):
        if not isinstance(data, dict):
            print("Warning: data provided is not a dictionary. Using default values instead.")
            data = {}
        default_data.update(data)

        self.data = default_data
        self.path = path

        self.save()

    def save(self):
        save_data(self.data, *self.path)

    def delete(self):
        delete_data(*self.path)

    def __getitem__(self, key):
        try:
            return self.data[key]
        except KeyError:
            print(f"Error: key '{key}' does not exist.")
            return None

    def __setitem__(self, key, value):
        self.data[key] = value
        self.save()
