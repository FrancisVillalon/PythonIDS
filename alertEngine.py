import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import numpy as np 
import shelve
from activityEngine import activityEngine 
from analysisEngine import analysisEngine
from src.db import *
from src.main import *
from datetime import datetime, timedelta
import sys




def calculateAnomaly(std,mean,weight,value):
    # Calculate the absolute z-score
    mean = float(mean)
    std = float(std)
    weight = float(weight)
    value = float(value)
    z = abs((value - mean) / std)
    return z * weight


def alertEngine(stats_file, days):

    # * date range
    days = int(days)
    base_day = datetime.now().date()
    end_day = base_day + timedelta(days=(days-1))

    # * clean up existing data and logs
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

    # * Read the stats file 
    read_stats(stats_file)
    # * Generate data based on new stats file
    activityEngine(base_day, days)
    with shelve.open('csci262asgn3') as db:
        # * Check
        if 'Event' not in db:
            print('Event not found in db')
            sys.exit(1)
        if 'BaseLineEventStats' not in db:
            print('BaseLineEventStats not found in db')
            sys.exit(1)

        # * Get weights from events definition
        event_definition = db['Event']
        event_data = []
        for event in event_definition:
            event_info = event_definition[event]
            event_data.append({
                'Event': event,
                'type': event_info.type,
                'min': event_info.min,
                'max': event_info.max,
                'weight': event_info.weight,
            })
        Events = pd.DataFrame(event_data)

        # * Read baseline stats
        eventStats = db['BaseLineEventStats']
        statData = []
        for event in eventStats:
            stat = eventStats[event]
            statData.append({
                'EventName': event,
                'Mean': stat.mean,
                'StdDev': stat.stdDev,
            })
        eventStats = pd.DataFrame(statData,columns=['EventName','Mean','StdDev'])

    # * Analyse generated events but do not update baseline
    analysisEngine(baseline=False)

    print(eventStats)
    # * Read in the analysis results
    dailyTotals = pd.read_csv(f'./data/{base_day}_{end_day}_dailyTotals.csv')
    dailyTotals.columns = ['Event'] + dailyTotals.columns[1:].tolist()

    # * Calculate the threshold
    threshold = Events['weight'].sum() * 2

    # * Calculate the anomaly score for each cell
    def calculate_cell_anomaly(value, event, column):
        std = eventStats.loc[eventStats['EventName'] == event]['StdDev'].values[0]
        mean = eventStats.loc[eventStats['EventName'] == event]['Mean'].values[0]
        weight = Events.loc[Events['Event'] == event]['weight'].values[0]
        return calculateAnomaly(std, mean, weight, value)

    # * For each row -> For each element -> calculate the anomaly score
    anomalyScore = dailyTotals.copy().set_index('Event').apply(lambda row: row.apply(lambda x: calculate_cell_anomaly(x, row.name, row.index)),axis=1)
    anomalyScore = anomalyScore.T
    anomalyScore['Total Score'] = anomalyScore.sum(axis=1)
    anomalyScore['Anomaly'] = anomalyScore['Total Score'] > threshold

    print(f"\nAnomaly Score")
    print(anomalyScore)

    