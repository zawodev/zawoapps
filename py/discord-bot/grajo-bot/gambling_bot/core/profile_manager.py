import discord
from gambling_bot.casino import casino
from gambling_bot.models.profile.profile import Profile

def create_player_profile(user_id: str, user_name: str):
    if user_id not in casino.player_profiles:
        player_profile = Profile({'name': user_name}, 'profiles', 'players', user_id)
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
    names = ['Marek', 'Romper', 'Extreme', 'Gambler', 'WYGRAŁEM',
             'NIE', 'Fenomenalnie', 'Jogurt', 'Dealer', 'Krupier',
             'Wojtek', 'Pięcia', 'Nice Cnie', 'Jakub', 'Janek']
    for name in names:
        create_dealer_profile(f"Dealer {name}")

def create_player_profiles_in_guild(guild: discord.Guild):
    for member in guild.members:
        create_player_profile(str(member.id), member.display_name)
