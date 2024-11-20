import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import argparse
from src.db import *
from src.models import *
from src.setup import read_events, read_stats
from datetime import datetime, timedelta
from src.activityEngine import activityEngine
from src.analysisEngine import analysisEngine
from src.alertEngine import alertEngine
from src.utils import clean_up
# User generates data based on initial stats and events
# System saves the initial stats and events in a shelve database
# User analyses generated data to get new events and stats
# System saves the new stats in shelve database 
# System exports new stats to AnalysedEventStats_data.txt
# User instantiate alert engine with new events and stats, take generated data and calculate anomaly scores




def main():
    parser = argparse.ArgumentParser(description="Read stats and events from files and store them in a shelve database.")
    subparser = parser.add_subparsers(dest="command", help="The command to run.")

    # Subcommand for setup
    parser_setup = subparser.add_parser("setup", help="Generate activity for a number of days.")
    parser_setup.add_argument("events_file", help="The file containing the events data.")
    parser_setup.add_argument("stats_file", help="The file containing the stats data.")
    parser_setup.add_argument("days",help="The number of days to generate activity for starting from today.")

    # Subcommand for analysis
    parser_analysis = subparser.add_parser("analyse", help="Analyse the generated activity.")
    parser_analysis.add_argument('--baseline',action='store_true', help="Reset baseline statistics using the data.")


    # Subcommand for alert
    parser_alert = subparser.add_parser("alert", help="Run the alert engine.")


    args = parser.parse_args()


    if args.command == "setup":
        # * Input validation
        if not os.path.exists(args.events_file):
            print("Events file does not exist")
            return
        if not os.path.exists(args.stats_file):
            print("Stats file does not exist")
            return
        if not args.days.isdigit() and int(args.days) <= 0:
            print("Invalid number of days")
            return
        days = int(args.days)
        base_day = datetime.now().date()
        end_day = base_day + timedelta(days=(days-1))

        # Clean existing data
        clean_up()


        # * Setup
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


        print(f'=> Cleaning complete')
        print(f"\n *** Generating activity for {args.days} days ***")
        activityEngine(base_day,int(args.days))
        print(f"=> Activity generation complete")
        print(f"=> Setup complete")
    elif args.command == "analyse":
        print(f"\n*** Analysing activity ***")
        analysisEngine(baseline=args.baseline)
        print(f"=> Analysis complete")
    elif args.command == "alert":
        print(f"\n*** Alert Engine Monitoring ***")
        while True:
            print(f"""
*** Alert Engine Menu ***
1. Run Alert Engine
2. Exit
            """)
            choice = input("Enter your choice: ")
            if choice == "2":
                break
            else:
                stats_file = input("Enter the stats file to use: ")
                days = input("Enter the number of days to generate events: ")

                # input validation
                if not os.path.exists(stats_file):
                    print("File does not exist")
                    continue
                if not days.isdigit() and int(days) <= 0:
                    print("Invalid number of days")
                    continue

                # Run the alert engine
                alertEngine(stats_file,days)



if __name__ == "__main__":
    main()