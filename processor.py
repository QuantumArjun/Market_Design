import json
import preprocesser

class Processor:
    def __init__(self, path):
        self.path = path
        self.data = None
        self.preprocess = None
        self.load_data()

    def load_data(self):
        data = None

        # try:
        preference_file = open(self.path, 'r')
        data = json.loads(preference_file.read())
        self.preprocess = preprocesser.Preprocess(data)
        data = self.preprocess.get_data()
        # except:
        #     print("Error loading file")
    
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

    def remove_winners(self, winners):
        # Zero indexing
        winners = {k-1: v-1 for k, v in winners.items()}
        for award, winner in winners.items():
            # Put award as last priority for winner
            award_ranking = self.data['left'][winner]
            winner_ranking = self.data['left'][award]
            self.data['left'][winner] = [x for x in award_ranking if x != award] + [award]
            self.data['right'][award] = [x for x in winner_ranking if x != winner] + [winner]
    
    def get_data(self):
        return self.data

    def convert_output(self, output):
        return self.preprocess.convert_output(output)

if __name__ == "__main__":
    processor = Processor("preferences.json")
    