## Usage
```sh
# Setup: Run this first to generate some data
python IDS.py {path_to_Events.txt} {path_to_Stats.txt} {days}
# Analysis: Running this command WITH --baseline takes the statistics of the current data and uses it as a baseline for what is normal
# Analysis: Running this WITHOUT --baseline calculates the statistics of the current data but does not update the baseline
python IDS.py analyse --baseline
# Alert: Running this generates data across {days} INCLUSIVE consistent with the stats file provided -> It then monitors the consistency between the "live data" and baseline stats to detect if the statistics of "live data" is such that it is far from the baseline
python IDS.py alert {path_to_Stats.txt} {days}
```

## How to Setup

### Installation without venv
```sh
pip install -r requirements.txt
```

### MACOS
```sh
python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
```

### WINDOWS
```sh
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

