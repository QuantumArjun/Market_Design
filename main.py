#Have a processor class in DataProcessor.py
#Have a main class in main.py - Two flags, left proposing and right proposing

from processor import Processor
from gale_shapley import Gale_Shapley
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--algorithm", help="The algorithm to use", choices=["DA"], default="DA")
    parser.add_argument("-p", "--proposing", help="The side of the market that proposes first", choices=["left", "right"], default="left")
    args = parser.parse_args()

    processor = Processor("preferences.json")
    preferences = processor.get_data()

    algorithm = None
    if args.algorithm == "DA":
        algorithm = Gale_Shapley(preferences)

    allocation = algorithm.match(type=args.proposing)
    print(f"Using the {args.algorithm} algorithm, with {args.proposing} proposing, the allocation is {allocation}.\nNote, the allocation is given from the perspective of the matching side (i.e if {args.proposing} is proposing, the allocation is given from the perspective of the {args.proposing} side)")