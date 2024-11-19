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
    parser_alert.add_argument("stats_file", help="The file containing the stats data.")
    parser_alert.add_argument("days",help="The number of days to generate activity for starting from today.")


    args = parser.parse_args()


    if args.command == "setup":
        days = int(args.days)
        base_day = datetime.now().date()
        end_day = base_day + timedelta(days=(days-1))
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

        # Clean existing data
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
        if os.path.exists("./exports"):
            print("=> Cleaning existing exports")
            os.system("rm -rf ./exports")
        if not os.path.exists("./exports"):
            os.makedirs("./exports")

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
        alertEngine(args.stats_file,args.days)



if __name__ == "__main__":
    main()