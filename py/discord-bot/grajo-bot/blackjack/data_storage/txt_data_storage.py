# w pliku dealer_names.txt zapisujemy nazwy dealerów, którzy się stworzą kiedy bedzie brakować dealerów
DATA_FILE_NAME = 'dealer_names.txt'

def save_data(data):
    with open(DATA_FILE_NAME, 'w') as file:
        file.write(data)

def load_data():
    with open(DATA_FILE_NAME, 'r') as file:
        return file.read()

def load_data_as_list():
    with open(DATA_FILE_NAME, 'r') as file:
        return file.read().splitlines()
