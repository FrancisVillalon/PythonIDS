import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import argparse
from src.db import *
from src.models import *
from src.setup import read_events, read_stats, reset_shelve
from activityEngine import activityEngine
from analysisEngine import analysisEngine


def main():
    parser = argparse.ArgumentParser(description="Read stats and events from files and store them in a shelve database.")
    parser.add_argument("events_file", help="The file containing the events data.")
    parser.add_argument("stats_file", help="The file containing the stats data.")
    parser.add_argument("days",help="The number of days to generate activity for starting from today.")
    args = parser.parse_args()


    # Setup
    print(f"=> Setting up the database with data from {args.events_file} and {args.stats_file}")
    reset_shelve()
    read_stats(args.stats_file)
    read_events(args.events_file)
    print(f"=> Database setup complete.")
    print_shelve_contents()
    export_shelve_contents()


    # Generate activity
    activityEngine(int(args.days))
    analysisEngine()


if __name__ == "__main__":
    main()