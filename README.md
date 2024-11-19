## Usage
### Training the IDS
To train the IDS, the user must have a "Events.txt" file and a "Stats.txt" file.
The first line in every file must be an integer representing the amount of events being monitored.
- Events.txt : A file containing the definition of events (EventName:EventType:min:max:weight:)
- Stats.txt : A file containing the statistics of each event (EventName:mean:stddev)

The system then reads these files and loads them into the shelve database saving them under 
- Events
- EventStats

The activityEngine is then called to generate data that is consistent with the EventStats as well as 
adhering to the constraints defined in Events.

The generation of values is done through numpy and scipy and just takes random values from a normal distribution defined by the event's mean and std dev.

The user has to input the following files as well as the following command to generate the data for training.
```sh
python IDS.py {path_to_Events.txt} {path_to_Stats.txt} {days}
```
The user must then input the following command to set the baseline statistics which would be used for the alert engine later.
```sh
python IDS.py analyse --baseline
```
This parses and consolidates the generated data loading it into a pandas dataframe where I can then calculate the std dev and mean of each event.
The --baseline flag makes it so that the statistics calculated here are used to updated "BaseLineEventStats" in the shelve database.
#### Special Considerations for Discrete and Continuous Events
In this application Events are labelled either
- C : Continuous 
- D : Discrete

Continuous events are of any value whereas Discrete events are of integer values and occur one at a time.
Therefore, generation for the events have to be specific to the event type.
In this project, the generation is as follows

- C : Selects a random value from a truncated normal distribution where the upper bound is defined as (max-mean)/std and the lower bound is defined as (min-mean)/std. The normal distribution is defined with the event's mean and std dev.

- D : Selects a random value from a normal distribution defined by the event's mean and std dev. The value is rounded down and coerced into integer data type.

### Using Alert Engine
After the IDS, has been trained.
The user can use the alert engine by inputting the following command,
```sh
python IDS.py alert
```
This shows a basic menu to the user to either run the alert engine or quit.
Running the alert engine prompts the user to input
- Path to Stats.txt file : This is a file that describes the statistics of "live data"
- Days to monitor : This is an integer value describing over how many days should the system generate "live data" consistent with the provided Stats.txt file

After the user inputs the required data, it generates data consistent with the provided stats file and then compares the "live data" with our base line statistics.

A dataframe showing the anomaly scores of each event and on each day, sum of scores across all events per day and a boolean telling the user if an "intrustion" was detected on that day (i.e. sum of anomaly scores exceeds threshold).
## Commands

### Setup

Run this first to generate some data:

```sh
python IDS.py {path_to_Events.txt} {path_to_Stats.txt} {days}
```

### Analysis

#### With Baseline

Running this command with `--baseline` takes the statistics of the current data and uses it as a baseline for what is normal

This is the training portion of the IDS.

```sh
python IDS.py analyse --baseline
```

#### Without Baseline

Running this command without `--baseline` calculates the statistics of the current data but does not update the baseline.

```sh
python IDS.py analyse
```

### Alert

Running this generates data across `{days}` inclusive consistent with the stats file provided. 

It then monitors the consistency between the "live data" and baseline stats to detect if the statistics of "live data" is such that it is far from the baseline:

```sh
python IDS.py alert {path_to_Stats.txt} {days}
```

## How to Setup

### Installation without venv

```sh
pip install -r requirements.txt
```

### macOS

```sh
python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
```

### Windows

```sh
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

