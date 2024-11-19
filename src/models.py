'''
Discrete events must take integer values and occur one at a time
Continuous events can take any real value and can occur multiple times
'''
import numpy as np 
import json

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
            # * Returns an array of integer values 
            # * each element is the number of events for that day
            values = np.random.normal(loc=self.mean, scale=self.std, size=self.days)
            values = [int(round(value)) for value in values]
        else:
            # * Returns an array of float values
            # * each element is the occurence of an event that day
            values = []
            current_sum = 0
            while current_sum < self.max:
                value = np.random.normal(loc=self.mean, scale=self.std)
                if current_sum + value > self.max:
                    break
                values.append(value)
                current_sum += value
            values = np.array(values)
            values = np.clip(values, self.min, self.max)
        return values


class EventLogDiscrete:
    def __init__(self, eventName, eventTime):
        self.eventName = eventName
        self.time = eventTime
        self.eventValue = 1

    def __repr__(self):
        return f'EventTime: {self.time}, EventName: {self.eventName}'
    
    def to_dict(self):
        return {
            'EventTime': str(self.time),
            'EventName': str(self.eventName),
            'EventValue': str(self.eventValue),
        }
    def to_json(self):
        return json.dumps(self.to_dict())


class EventLogContinuous:
    def __init__(self, eventName, eventTime,eventValue):
        self.eventName = eventName
        self.time = eventTime
        self.value = eventValue

    def __repr__(self):
        return f'EventTime: {self.time}, EventName: {self.eventName}, EventValue: {self.value}'
    
    def to_dict(self):
        return {
            'EventTime': str(self.time),
            'EventName': str(self.eventName),
            'EventValue': str(self.value),
        }
    def to_json(self):
        return json.dumps(self.to_dict())

