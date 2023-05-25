import json
import random

NAME_TO_MARKET_SIDE = {'Team Preferences': 'left', 'Judge Preferences': 'right'}

class Preprocess:
    def __init__(self, data):
        self.unique_teams = {}
        self.unique_awards = {}
        self.data = data
        self.preprocessed_dict = {'left': {}, 'right': {}}
        self.preprocess()

    def preprocess(self):
        market_sides = list(self.data.keys())
        # TEAM SIDE
        for team in self.data[market_sides[0]]:
            self.unique_teams[team.lower()] = str(self.unique_teams.get(team.lower(), len(self.unique_teams)+1))
            award_choices = [x.strip() for x in self.data[market_sides[0]][team]['ranking'].lower().split(',')]
            award_choices.append('no_award')
            for i, award in enumerate(award_choices):
                self.unique_awards[award.lower()] = str(self.unique_awards.get(award.lower(), len(self.unique_awards)+1))
                award_choices[i] = str(self.unique_awards[award.lower()])
            award_choices = ', '.join(award_choices)
            self.preprocessed_dict['left'][self.unique_teams[team.lower()]] = {'ranking': award_choices}
        # AWARD SIDE
        for award in self.data[market_sides[1]]:
            team_choices = [x.strip() for x in self.data[market_sides[1]][award]['ranking'].lower().split(',')]
            for i, team in enumerate(team_choices):
                team_choices[i] = str(self.unique_teams[team.lower()])
            team_choices_str = ', '.join(team_choices)
            self.preprocessed_dict['right'][self.unique_awards[award.lower()]] = {'ranking': team_choices_str}
        # TODO: ask arjun about a better way 
        random.shuffle(team_choices)
        team_choices_str = ', '.join(team_choices)
        self.preprocessed_dict['right'][self.unique_awards['no_award']] = {'ranking': team_choices_str}
        assert len(self.unique_teams) == 6, "{self.unique_teams} is not the right size"
        assert len(self.unique_awards) == 6, "{self.unique_awards} is not the right size"

    def get_data(self):
        return self.preprocessed_dict
    
    def convert_output(self, data):
        processed_data = {}
        unique_awards = {v: k for k, v in self.unique_awards.items()}
        unique_teams = {v: k for k, v in self.unique_teams.items()}
        for award, team in data.items():
            processed_data[unique_awards[str(award)]] = unique_teams[str(team)]
        return processed_data
