from processor import Processor

class Gale_Shapley_Uneven:
    def __init__(self, preferences):
        self.left_preferences = preferences["left"]
        self.right_preferences = preferences["right"]
        self.preferences = preferences
        self.num_left_agents = None
        self.num_right_agents = None
    
    def match(self, type="left"):
        proposing_prefs = None
        receiving_prefs = None
        if type == "left":
            self.num_left_agents = len(self.preferences["left"].keys())
            self.num_right_agents = len(self.preferences["right"].keys())
            proposing_prefs = self.left_preferences
            receiving_prefs = self.right_preferences
        else:
            self.num_left_agents = len(self.preferences["right"].keys())
            self.num_right_agents = len(self.preferences["left"].keys())
            proposing_prefs = self.right_preferences
            receiving_prefs = self.left_preferences
        matching = self.matching_algorithm(proposing_prefs, receiving_prefs)
        return(self.format_matching(matching, type))
    
    def matching_algorithm(self, proposing_prefs, receiving_prefs):
        # If only one team left, just return that team as the preference
        print('proposing_prefs', proposing_prefs)
        print('receiving_prefs', receiving_prefs)
        if any([len(team_prefs) == 1 for award_num, team_prefs in proposing_prefs.items()]):
            return {k: v[0] for k, v in proposing_prefs.items()}
        #First, have everyone on the left propose to their top choice on the right

        proposed = {i: -1 for i in proposing_prefs.keys()}
        index_to_propose = {i: 0 for i in proposing_prefs.keys()}
        
        while -1 in proposed.values():
            for agent_num in proposing_prefs.keys():
                # if agent_num not in proposing_prefs: continue
                next_proposition = index_to_propose[agent_num]
                # if next_proposition >= len(proposing_prefs[agent_num]): next_proposition -=1
                proposed[agent_num] = proposing_prefs[agent_num][next_proposition]
            #Step 2 - See if any clashes 
            clashes = {}
            [clashes.setdefault(award_num, []).append(agent_num) for agent_num, award_num in proposed.items()]
            for award_num in clashes.keys():
                print(index_to_propose)
                sort_by_list = receiving_prefs[award_num]
                sorted_list = [x for _, x in sorted(zip(sort_by_list, clashes[award_num]))] # list of agents that we will reject
                matched = sorted_list[0] 
                sorted_list.pop(0)
                #Rejecting Step
                proposed = {agent_num: -1 if agent_num in sorted_list else award_num for agent_num, award_num in proposed.items()}
                index_to_propose = {agent_num: award_num+1 if agent_num in sorted_list else award_num for agent_num, award_num in index_to_propose.items()}  
                index_to_propose = {agent_num: -2 if award_num > len(receiving_prefs.keys()) else award_num for agent_num, award_num in index_to_propose.items()}
        return proposed

    def format_matching(self, matching, type):
        print(matching)
        if type == "left":
            return {agent_num+1: award_num+1 for agent_num, award_num in matching.items()}
        elif type == "right":
            return {award_num+1: agent_num+1 for agent_num, award_num in matching.items()}
