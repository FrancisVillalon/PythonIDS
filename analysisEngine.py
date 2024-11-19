import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import numpy as np
import shelve
import os 

def parseData(folderPath,outputPath):
    df = pd.DataFrame(columns=['EventTime','EventName','EventValue'])
    for file in os.listdir(folderPath):
        if file.endswith('.json'):
            data = pd.read_json(os.path.join(folderPath,file))
            df = pd.concat([df,data],axis=0)
    df.to_csv(outputPath,index=False)
    return df

def consolidateData(folderPath,outputPath):
    df = pd.DataFrame(columns=['EventTime','EventName','EventValue'])
    for file in os.listdir(folderPath):
        if file.endswith('.csv'):
            data = pd.read_csv(os.path.join(folderPath,file))
            df = pd.concat([df,data],axis=0)
    df.sort_values('EventName').to_csv(outputPath,index=False)
    return df


def analysisEngine(base_day,end_day):
    # * Analysis engine setup
    if not os.path.exists('./data/temp'):
        os.makedirs('./data/temp')
    temp_dir = './data/temp'

    # * Parse data
    print('===> Parsing data')
    for day in os.listdir('./logs'):
        day_path = os.path.join('./logs', day)
        if os.path.isdir(day_path):
            parseData(day_path, f'{temp_dir}/{day}.csv')
            print(f'=> Parsed data for {day}')

    # * Consolidate
    print('===> Consolidating data')
    consolidatedDataPath = f'./data/{base_day}_{end_day}_data.csv'
    consolidateData(temp_dir, consolidatedDataPath)
    print(f"===> Data consolidated and stored in {consolidatedDataPath}")

    # * Analyse consolidated data
    print('\n===> Analysing consolidated data')
    print('=> Generator was initialised with the following parameters:')
    print(f"{'Event':<20} {'Mean':<10} {'StdDev':<10}")
    print("="*50)
    with shelve.open('csci262asgn3') as db:
        for event in sorted(db['EventStats'].keys()):
            data = db['EventStats'][event]
            event, mean, std = data.name, data.mean, data.stdDev
            print(f"{event:<20} {mean:<10.2f} {std:<10.2f}")
    df = pd.read_csv(consolidatedDataPath)

    print(f"\n=> Event statistics ")
    eventStats = df.copy().groupby('EventName').agg({'EventValue': ['mean', 'std']})
    eventStats.columns = ['Mean', 'StdDev']
    eventStats.to_csv(f'./data/{base_day}_{end_day}_eventStats.csv',index=True)
    print(eventStats)


    print(f"\n => Event Daily Totals ")
    dailyTotals = pd.DataFrame()
    for event in df['EventName'].unique():
        targetDf = df[df['EventName'] == event].set_index('EventTime')['EventValue'].to_frame(name=event)
        dailyTotals = pd.concat([dailyTotals,targetDf],axis=1)
    dailyTotals = dailyTotals.T
    dailyTotals.to_csv(f'./data/{base_day}_{end_day}_dailyTotals.csv',index=True)
    print(dailyTotals)
    print(f"=> Event daily totals stored in ./data/{base_day}_{end_day}_dailyTotals.csv")






          
      
      
        