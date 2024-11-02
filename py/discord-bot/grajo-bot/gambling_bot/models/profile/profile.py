from gambling_bot.models.profile.profile_data import ProfileData

class Profile:
    def __init__(self, data, *path):
        self.profile_data = ProfileData(data, *path)

    def __str__(self):
        return f'{self.profile_data.data.get('name')} has {self.profile_data.data.get('chips')}$'

    def __eq__(self, other):
        if isinstance(other, str):
            return self.profile_data.path[-1] == other
        elif isinstance(other, Profile):
            return self.profile_data.path == other.profile_data.path
        return False

    def save(self):
        self.profile_data.save()

    def has_chips(self, amount):
        return self.profile_data.data.get('chips') >= amount

    def transfer_chips(self, other, amount):
        if self.has_chips(amount):
            self.profile_data.data['chips'] -= amount
            other.profile_data.data['chips'] += amount
            return True
        return False
