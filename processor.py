import json

class Processor:
    def __init__(self, path):
        self.path = path
        self.data = None
        self.load_data()

    def load_data(self):
        data = None

        try:
            preference_file = open(self.path, 'r')
            data = json.loads(preference_file.read())
        except:
            print("Error loading file")
    
        self.process_data(data)
    
    def process_data(self, data):
        processed_dict = {}
        for market_side in data.keys():
            processed_dict[market_side] = {}
            for team in data[market_side]:
                processed_dict[market_side][int(team) - 1] = None
                ranking = data[market_side][team]["ranking"]
                pref_list = ranking.replace(" ", "").split(",")
                casted_pref_list = list(map(int, pref_list))
                zero_index = list(map(lambda x: x - 1, casted_pref_list))
                processed_dict[market_side][int(team) - 1] = zero_index
        self.data = processed_dict
    
    def get_data(self):
        return self.data

if __name__ == "__main__":
    processor = Processor("preferences.json")
    