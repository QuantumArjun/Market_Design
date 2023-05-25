#Have a processor class in DataProcessor.py
#Have a main class in main.py - Two flags, left proposing and right proposing

from processor import Processor
from gale_shapley import Gale_Shapley
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--algorithm", help="The algorithm to use", choices=["DA"], default="DA")
    parser.add_argument("-p", "--proposing", help="The side of the market that proposes first", choices=["left", "right"], default="right")
    args = parser.parse_args()

    processor = Processor("preferences.json")
    preferences = processor.get_data()

    # TODO: How to allocate multiple awards to a team 
    ranked_allocations = {}
    # if two or more winners then allow two to take awards 
    for i in range(len(preferences[args.proposing])):
        preferences = processor.get_data()
        algorithm = Gale_Shapley(preferences)
        allocation = algorithm.match(type=args.proposing)
        allocation_pretty = processor.convert_output(allocation)
        print(allocation_pretty)
        for award, team in allocation_pretty.items():
            if i == 0: ranked_allocations[award] = []
            ranked_allocations[award].append(team)
        processor.remove_winners(allocation)

    print(f"Using the {args.algorithm} algorithm, with {args.proposing} proposing, the allocation is")
    for award, teams in ranked_allocations.items():
        if award == 'no_award': continue
        print(f"{award.title()}")
        for i, team in enumerate(teams):
            print(f'{i+1}. {team}')
    
    print(f"Note, the allocation is given from the perspective of the matching side (i.e if {args.proposing} is proposing, the allocation is given from the perspective of the {args.proposing} side)")