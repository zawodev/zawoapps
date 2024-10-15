from blackjack.data_storage.json_data_storage import save_data, load_data
from blackjack.table.dealer import Dealer
from blackjack.table.player import Player


def create_empty_dealers(dealer_names):
    dealer_datas = load_data('dealers')
    for dealer_name in dealer_names:
        if dealer_name not in dealer_datas:
            dealer = Dealer({'name': dealer_name})
            dealer_datas[dealer_name] = dealer.stats.to_dict()
    save_data('dealers', dealer_datas)