import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.models import *
from src.db import *
from datetime import datetime, timedelta
import pandas as pd

def generateDiscreteEvents(target_day,Events,logFile,i,EventGenerator):
  EventData = []
  with open(logFile, 'w') as file:
    EventLog = EventLogDiscrete(
      EventGenerator.name,
      target_day)
    for _ in range(int(Events[i])):
      EventData.append(EventLog.to_dict())
    json.dump(EventData, file, indent=2)
  return

def generateContinuousEvents(target_day,logFile,i,EventGenerator):
  EventData = []
  Events = EventGenerator.generate()
  with open(logFile, 'w') as file:
    for event in Events:
      EventLog = EventLogContinuous(
        EventGenerator.name,
        target_day,
        event
        )
      EventData.append(EventLog.to_dict())
    json.dump(EventData, file, indent=2)
  return


# main
def activityEngine(days):
    print("\n---------------------------------")
    # Set Daytime
    base_day = datetime.now().date()
    print(f"Generate Events for {datetime.now().date()}")
    print(f"Start Date: {base_day}, End Date: {base_day + timedelta(days=days)}")

    # Generate 
    with shelve.open('csci262asgn3') as db:
       for key in db['EventStats']:
          print("\n---------------------------------")
          print(f"=> Generating {key} Events")
          EventStats = get_from_shelve('EventStats', key)
          EventData = get_from_shelve('Event', key)
          print(f"{key} Generator initiated with mean: {EventStats.mean}, stdDev: {EventStats.stdDev}, min: {EventData.min}, max: {EventData.max}")
          EventGen = EventGenerator(
            key,
            EventData.type,
            EventStats.mean,
            EventStats.stdDev,
            EventData.min,
            EventData.max,
            days
            )
          Events = EventGen.generate()
          for i in range(days):
            target_day = base_day + timedelta(days=i)
            base_path = f"./logs/{target_day}"
            if not os.path.exists(base_path):
              os.makedirs(base_path)
            file_path = f'{base_path}/{target_day}_{key}_Logs.json'
            if EventData.type == 'D':
              generateDiscreteEvents(target_day,Events,file_path,i,EventGen)
            else:
              generateContinuousEvents(target_day,file_path,i,EventGen)

          print(f"=> {key} Events generated and stored in {file_path}")