#Have a processor class in DataProcessor.py
#Have a main class in main.py - Two flags, left proposing and right proposing

from processor import Processor
from gale_shapley import Gale_Shapley
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--proposing", help="The side of the market that proposes first", choices=["left", "right"], default="left")
    args = parser.parse_args()

    processor = Processor("preferences.json")
    preferences = processor.get_data()
    gale_shapley = Gale_Shapley(preferences)

    allocation = gale_shapley.match(type=args.proposing)
    print(f"Under {args.proposing} proposing, the allocation is {allocation}")