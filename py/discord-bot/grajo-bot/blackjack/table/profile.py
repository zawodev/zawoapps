from blackjack.table.stats import Stats
from blackjack.data_storage.json_data_storage import load_profile_data, save_profile_data

class Profile:
    def __init__(self, category: str, profile_id: str):
        self.profile_id = profile_id
        self.category = category

        self.stats = Stats(load_profile_data(self.category, self.profile_id))

    def __str__(self):
        return f'{self.stats.name} has {self.stats.chips}$'

    def save(self):
        save_profile_data(self.category, self.profile_id, self.stats.to_dict())

    def has_chips(self, amount):
        return self.stats.chips >= amount

    def transfer_chips(self, other, amount):
        if self.has_chips(amount):
            self.stats.chips -= amount
            other.stats.chips += amount
            return True
        return False
