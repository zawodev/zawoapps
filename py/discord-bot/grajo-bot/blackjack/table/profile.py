from blackjack.table.stats import Stats
from blackjack.data_storage.json_data_storage import load_profile_data, save_profile_data

class Profile:
    def __init__(self, category: str, profile_id: str):
        self.profile_id = profile_id
        self.category = category

        self.stats = Stats(load_profile_data(self.category, self.profile_id))

    def save(self):
        save_profile_data(self.category, self.profile_id, self.stats.to_dict())
