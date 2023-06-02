#Have a processor class in DataProcessor.py
#Have a main class in main.py - Two flags, left proposing and right proposing

from processor import Processor
from gale_shapley import Gale_Shapley
from gale_shapley_uneven import Gale_Shapley_Uneven
import argparse

def split_market(preferences):
    team_judge_awards = {}
    [team_judge_awards.setdefault(team_prefs[0], []).append(award_num) for award_num, team_prefs in preferences['right'].items()]
    # If any of the teams has three award, split the preference market
    if any([len(awards) == 3 for _, awards in team_judge_awards.items()]):
        split_preferences = [{'left': {}, 'right': {}}, {'left': {}, 'right': {}}]
        winners, awards = list(team_judge_awards.keys()), list(preferences['right'].keys())
        undecided_award_bucket =  [team_judge_awards[winners[0]][0], team_judge_awards[winners[1]][0]]
        decided_award_bucket = list(set(awards) - set(undecided_award_bucket))
        for team, award_prefs in preferences['left'].items():
            award_prefs = list(set(award_prefs) - set(decided_award_bucket))
            split_preferences[0]['left'][team] = award_prefs
        split_preferences[0]['right'] = {award_num: team_prefs  for award_num, team_prefs in preferences['right'].items() if award_num in undecided_award_bucket}
        print(team_judge_awards)
        split_preferences[1] = {team_num+1: [award+1 for award in awards] for team_num, awards in team_judge_awards.items() if len(awards) == 3}
    elif any([len(awards) == 2 for _, awards in team_judge_awards.items()]):
        split_preferences = [{'left': {}, 'right': {}}, {'left': {}, 'right': {}}]
        winners, awards = list(team_judge_awards.keys()), list(preferences['right'].keys())
        first_award_bucket =  [team_judge_awards[winners[0]][0], team_judge_awards[winners[1]][0]]
        second_award_bucket = list(set(awards) - set(first_award_bucket))
        for team, award_prefs in preferences['left'].items():
            award_prefs = list(set(award_prefs) - set(second_award_bucket))
            split_preferences[0]['left'][team] = award_prefs
        split_preferences[0]['right'] = {award_num: team_prefs  for award_num, team_prefs in preferences['right'].items() if award_num in first_award_bucket}
        for team, award_prefs in preferences['left'].items():
            award_prefs = list(set(award_prefs) - set(first_award_bucket))
            split_preferences[1]['left'][team] = award_prefs
        split_preferences[1]['right'] = {award_num: team_prefs  for award_num, team_prefs in preferences['right'].items() if award_num in second_award_bucket}
    else:  
        split_preferences = [preferences.copy()]
    return split_preferences

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--algorithm", help="The algorithm to use", choices=["DA"], default="DA")
    parser.add_argument("-s", "--single_winner", help="Whether to have a single winner or allow for multiple", choices=[True, False], default=False)
    parser.add_argument("-p", "--proposing", help="The side of the market that proposes first", choices=["left", "right"], default="right")
    args = parser.parse_args()

    processor = Processor("preferences.json")
    preferences = processor.get_data()

    # TODO: How to allocate multiple awards to a team, unique sets of awards
    # Split first into multiple categories
    # Either split second as first, as first design, or by fairness metric 
    ranked_allocations = {}
    # if two or more winners then allow two to take awards 
    for i in range(len(preferences['left'])):
        preferences = processor.get_data()
        allocations = {}
        if not args.single_winner:
            split_preferences = split_market(preferences)
            for preferences in split_preferences:
                if 'left' in preferences:
                    algorithm = Gale_Shapley_Uneven(preferences)
                    allocation = algorithm.match(type=args.proposing)
                    [allocations.setdefault(team_num, []).append(award_num) for team_num, award_num in allocation.items()]
                    # If no preferences and its decided just append the awards to the team
                else:
                    print('preferences', preferences)
                    allocations.update(preferences)
                    print('allocations', allocations)
        else:
            algorithm = Gale_Shapley_Uneven(preferences)
            allocation = algorithm.match(type=args.proposing)
            [allocations.setdefault(team_num, []).append(award_num) for team_num, award_num in allocation.items()]

        allocation_pretty = processor.convert_output(allocations)
        for i, (team, awards) in enumerate(allocation_pretty.items()):
            for award in awards:
                ranked_allocations.setdefault(award, []).append(team)
        processor.remove_winners(allocations)

    print(f"Using the {args.algorithm} algorithm, with {args.proposing} proposing, the allocation is")
    for award, teams  in ranked_allocations.items():
        if award == 'no_award': continue
        print(f"{award.title()}")
        for i, team in enumerate(teams):
            print(f'{i+1}. {team}')
    
    print(f"Note, the allocation is given from the perspective of the matching side (i.e if {args.proposing} is proposing, the allocation is given from the perspective of the {args.proposing} side)")