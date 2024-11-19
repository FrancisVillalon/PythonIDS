from models import EventStats, Event, EventLog
from db import *
import numpy as np
import pandas as pd
from datetime import datetime
import json

# Read the Stats.txt file and store the data in a shelve database
def read_stats(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        num_events = int(lines[0])
        for line in [lines[i] for i in range(1,len(lines))]:
            eventDetails = line.split(":")
            eventName = eventDetails[0]
            eventMean = float(eventDetails[1])
            eventStdDev = float(eventDetails[2])
            store_in_shelve(
                'EventStats', 
                eventName, 
                EventStats(eventName, eventMean, eventStdDev)
                )

# Read the Events.txt file and store the data in a shelve database
def read_events(filename):
    with open(filename,'r') as file:
        lines = file.readlines()
        num_events = int(lines[0])
        for line in [lines[i] for i in range(1,len(lines))]:
            eventDetails = line.split(":")
            eventName = eventDetails[0]
            eventType = eventDetails[1]
            minWeight = float(eventDetails[2])
            maxWeight = float(eventDetails[3] if eventDetails[3] else float('inf'))
            eventWeight = float(eventDetails[4])
            store_in_shelve('Event', eventName, Event(eventName, eventType, minWeight, maxWeight, eventWeight))

def calculate_Z(mean, std, value):
    return (value - mean) / std

def generateEvents(start_time,end_time,mean_time,std_dev_time,EventGenerator,logFile):
  Events = []
  EventData = []
  agents = range(ord("A"), ord("Z") + 1)
  with open(logFile, 'w') as file:
    for _ in range(10_000):
      # Create random time
      random_seconds = np.random.normal(mean_time, std_dev_time)
      random_seconds = max(start_time.timestamp(), min(random_seconds, end_time.timestamp()))
      event_time = datetime.fromtimestamp(random_seconds)
      # Get random value
      Events.append(EventGenerator.generate())
      # Log the value
      EventLogger = EventLog(
        EventGenerator.name,
        chr(np.random.choice(agents)),
        event_time,
        len(Events), 
        Events[-1])
      # Store the log data
      EventData.append(EventLogger.to_dict())
    json.dump(EventData, file, indent=4)
  return

if __name__ == "__main__":
    reset_shelve()
    read_stats('Stats.txt')
    read_events('Events.txt')
    print_shelve_contents()
    export_shelve_contents()