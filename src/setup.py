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