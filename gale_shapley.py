from processor import Processor

class Gale_Shapley:
    def __init__(self, preferences):
        self.left_preferences = preferences["left"]
        self.right_preferences = preferences["right"]
        self.num_agents = len(preferences["left"].keys())
        num_teams = len(preferences["left"].keys())
    
    def match(self, type="left"):
        proposing_prefs = None
        receiving_prefs = None
        if type == "left":
            proposing_prefs = self.left_preferences
            receiving_prefs = self.right_preferences
        else:
            proposing_prefs = self.right_preferences
            receiving_prefs = self.left_preferences
        matching = self.matching_algorithm(proposing_prefs, receiving_prefs)
        return(self.format_matching(matching, type))
    
    def matching_algorithm(self, proposing_prefs, receiving_prefs):
        left_remaining = list(range(self.num_agents))
        left_matches = [None] * self.num_agents
        right_matches = [None] * self.num_agents
        next_left_choice = [0] * self.num_agents

        while left_remaining:
            curr_left = left_remaining[0]
            left_preferences = proposing_prefs[curr_left]
            proposed_right = left_preferences[next_left_choice[curr_left]]
            proposed_right_preferences = receiving_prefs[proposed_right]
            curr_right_match = right_matches[proposed_right]

            if curr_right_match == None:
                right_matches[proposed_right] = curr_left
                left_matches[curr_left] = proposed_right
                next_left_choice[curr_left] += 1
                left_remaining.pop(0)
            else:
                curr_index = proposed_right_preferences.index(curr_right_match)
                left_index = proposed_right_preferences.index(curr_left)

                if curr_index > left_index:
                    right_matches[proposed_right] = curr_left
                    left_matches[curr_left] = proposed_right
                    next_left_choice[curr_left] += 1
                    left_remaining.pop(0)
                    left_remaining.insert(0, curr_right_match)
                else:
                    next_left_choice[curr_left] += 1
        return left_matches

    def format_matching(self, matching, type):
        formatted_matching = {}
        if type == "left":
            for i in range(len(matching)):
                formatted_matching[i + 1] = matching[i] + 1
        else:
            for i in range(len(matching)):
                formatted_matching[matching[i] + 1] = i + 1
        print(formatted_matching)
        return formatted_matching

if __name__ == "__main__":
    processor = Processor("preferences.json")
    preferences = processor.get_data()
    gale_shapley = Gale_Shapley(preferences)
    gale_shapley.match()