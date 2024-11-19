import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import argparse
from src.db import *
from src.models import *
from src.setup import read_events, read_stats, reset_shelve
from datetime import datetime, timedelta
from activityEngine import activityEngine
from analysisEngine import analysisEngine
from alertEngine import alertEngine


def main():
    parser = argparse.ArgumentParser(description="Read stats and events from files and store them in a shelve database.")
    parser.add_argument("events_file", help="The file containing the events data.")
    parser.add_argument("stats_file", help="The file containing the stats data.")
    parser.add_argument("days",help="The number of days to generate activity for starting from today.")
    args = parser.parse_args()

    days = int(args.days)
    base_day = datetime.now().date()
    end_day = base_day + timedelta(days=days)


    # Setup
    print(f"\n *** Initialising IDS ***")
    print(f"=> Setting Date Range")
    print(f"Start Date: {base_day}, End Date: {end_day}")
    print(f"=> Setting up the database with data from {args.events_file} and {args.stats_file}")
    reset_shelve()
    read_stats(args.stats_file)
    read_events(args.events_file)
    print(f"=> Database setup complete.")
    print_shelve_contents()
    export_shelve_contents()

    # Clean existing logs
    print(f"\n *** Clean up ***")
    if os.path.exists("./logs"):
        print("=> Cleaning existing logs")
        os.system("rm -rf ./logs")
    if not os.path.exists("./logs"):
        print('=> Creating logs directory')
        os.makedirs("./logs")
    if os.path.exists("./data"):
        print("=> Cleaning existing data")
        os.system("rm -rf ./data")
    if not os.path.exists("./data"):
        os.makedirs("./data")
    print(f'=> Cleaning complete')


    # Generate activity
    print(f"\n *** Generating activity for {args.days} days ***")
    activityEngine(base_day,int(args.days))
    print(f"=> Activity generation complete")
    print(f"\n*** Analysing activity ***")
    analysisEngine(base_day,end_day)
    print(f"=> Analysis complete")
    print(f"\n*** Alert Engine Monitoring ***")
    alertEngine(base_day,end_day)



if __name__ == "__main__":
    main()