import discord
from gambling_bot.casino import casino
from gambling_bot.models.profile.profile import Profile

def create_player_profile(interaction: discord.Interaction):
    profile_id = str(interaction.user.id)
    profile_name = interaction.user.name
    if profile_id not in casino.player_profiles:
        player_profile = Profile({'name': profile_name}, 'profiles', 'players', profile_id)
        casino.player_profiles.append(player_profile)

def get_player_profile_with_id(player_profile_id):
    for profile in casino.player_profiles:
        if profile.profile_data.path[-1] == player_profile_id:
            return profile
    return None



def create_dealer_profile(name: str):
    if name not in casino.dealer_profiles:
        dealer_profile = Profile({'name': name}, 'profiles', 'dealers', name)
        casino.dealer_profiles.append(dealer_profile)

def remove_dealer_profile(name: str):
    for profile in casino.dealer_profiles:
        if profile.profile_data['name'] == name:
            profile.profile_data.delete()
            casino.dealer_profiles.remove(profile)
            return

def create_default_dealers():
    names = ['Marek', 'Romper', 'Extreme', 'Gambler', 'WYGRAŁEM', 'NIE', 'Fenomenalnie', 'Jogurt']
    for name in names:
        create_dealer_profile(f"Dealer {name}")
