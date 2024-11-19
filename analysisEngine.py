import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import numpy as np
import os 

def analysisEngine():
  print("\n---------------------------------")
  print("Analysis Engine")
  masterDf = pd.DataFrame(columns=["EventTime","EventName","EventCount","EventValues"])
  for day in os.listdir("./logs"):
      if not (os.path.isdir(f"./logs/{day}")): continue

      df = pd.DataFrame(columns=["EventTime","EventName","EventCount","EventValues"])
      for logFile in os.listdir(f"./logs/{day}"):
          eventName = logFile.split("_")[1]
          logData = pd.read_json(f"./logs/{day}/{logFile}")
          df.loc[df.shape[0]] = {
              "EventTime": day,
              "EventName": eventName,
              "EventCount": len(logData["EventValue"]),
              "EventValues": logData["EventValue"].tolist()
          }
      masterDf = pd.concat([masterDf,df])
  masterDf = masterDf.reset_index(drop=True)

  for EventName in masterDf["EventName"].unique():
      targetDf = masterDf.loc[masterDf["EventName"]==EventName]
      print(f"------ Daily count for {EventName} ------")
      print(targetDf.sort_values("EventTime")[[ "EventTime","EventCount"]])
      if all(isinstance(i, float) for i in targetDf["EventValues"].explode()):
          print(f"Mean: {targetDf['EventValues'].explode().mean()}, StdDev: {targetDf['EventValues'].explode().std()}")
      else:
          print(f"Mean: {targetDf['EventCount'].mean()}, StdDev: {targetDf['EventCount'].std()}")
      print("\n")
          

          
      
      
        