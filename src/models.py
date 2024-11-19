'''
Discrete events must take integer values and occur one at a time
Continuous events can take any real value and can occur multiple times
'''
import numpy as np 
import json
from scipy.stats import truncnorm

# Used to get event stats from Stats.txt
class EventStats:
    def __init__(self, eventName, eventMean, eventStdDev):
        self.name = eventName
        self.mean = eventMean
        self.stdDev = eventStdDev
    
    def __repr__(self):
        return f'{self.name}:{self.mean}:{self.stdDev}:'

# Used to get event data from Events.txt
class Event:
    def __init__ (self,eventName,eventType, min, max, eventWeight):
        self.name = eventName
        self.type = eventType # 'D' or 'C', C = continuous, D = discrete
        self.min = min
        self.max = max
        self.weight = eventWeight
    
    def __repr__(self):
        return f'{self.name}:{self.type}:{self.min}:{self.max}:{self.weight}:'
    
# Creates generator for given class
class EventGenerator:
    def __init__(self, eventName, eventType,mean, std,minVal,maxVal,days):
        self.name = eventName
        self.mean = mean
        self.std = std
        self.type = eventType
        self.min = minVal
        self.max = maxVal
        self.days=days

    def generate(self):
        if self.type == 'D':
            values = np.random.normal(loc=self.mean, scale=self.std, size=self.days)
            values = [int(round(value)) for value in values]
        else:
            upper_bound = (self.max - self.mean) / self.std
            lower_bound = (self.min - self.mean) / self.std
            values = truncnorm.rvs(lower_bound, upper_bound, loc=self.mean, scale=self.std, size=self.days)
        values = np.clip(values, self.min, self.max)
        return values


class EventLog:
    def __init__(self, eventName, eventTime,eventValue):
        self.eventName = eventName
        self.time = eventTime
        self.eventValue = eventValue

    def __repr__(self):
        return f'EventTime: {self.time}, EventName: {self.eventName}'
    
    def to_dict(self):
        return {
            'EventTime': str(self.time),
            'EventName': str(self.eventName),
            'EventValue': str(self.eventValue),
        }



