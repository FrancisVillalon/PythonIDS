import pandas as pd
import numpy as np 
import shelve



def calculateAnomaly(std,mean,weight,value):
    # Calculate the absolute z-score
    z = abs((value - mean) / std)
    return z * weight


def alertEngine(base_day,end_day):
    dailyTotals = pd.read_csv(f'./data/{base_day}_{end_day}_dailyTotals.csv')
    dailyTotals.columns = ['Event'] + list(dailyTotals.columns[1:])
    eventStats = pd.read_csv(f'./data/{base_day}_{end_day}_eventStats.csv')

    with shelve.open('csci262asgn3') as db:
        event_stats = db['Event']
        event_data = []
        for event in event_stats:
            event_info = event_stats[event]
            event_data.append({
                'Event': event,
                'type': event_info.type,
                'min': event_info.min,
                'max': event_info.max,
                'weight': event_info.weight,
            })
        Events = pd.DataFrame(event_data)
    
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
    print(anomalyScore)