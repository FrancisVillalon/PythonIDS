import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.models import *
from src.db import *
from datetime import datetime, timedelta

def activityEngine(base_day,days):
		# Set Daytime
		print(f"Generate Events for {datetime.now().date()}")
		print(f"Start Date: {base_day}, End Date: {base_day + timedelta(days=days)}")
		daysLogged = [base_day + timedelta(days=i) for i in range(days)]

		# Generate 
		with shelve.open('csci262asgn3') as db:
			 for key in db['EventStats']:
					print(f"\n===> Generating {key} Events")
					EventStats = get_from_shelve('EventStats', key)
					EventData = get_from_shelve('Event', key)
					print(f"{key} Generator initiated with mean: {EventStats.mean}, stdDev: {EventStats.stdDev}, min: {EventData.min}, max: {EventData.max}")
					generator = EventGenerator(
						key,
						EventData.type,
						EventStats.mean,
						EventStats.stdDev,
						EventData.min,
						EventData.max,
						days
						)
					Events = generator.generate()
					for i, day in enumerate(daysLogged):
						if not os.path.exists(f"./logs/{day}"):
							os.makedirs(f"./logs/{day}")
						file_path = f"./logs/{day}/{day}_{key}.json"
						eventLogs = [EventLog(key,day,Events[i],).to_dict()]
						with open(file_path, 'w') as file:
							json.dump(eventLogs, file,indent=4)

						print(f"=> {key} Events generated for {day} and stored in {file_path}")# 
					print(f"===> {key} Events generated for {days} days")
			