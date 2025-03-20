import fastf1
import pandas as pd

# Enable FastF1 caching
#fastf1.Cache.enable_cache('cache')

# Load a session (Example: Monza 2024 Qualifying)
session = fastf1.get_session(2024, 'Monza', 'Q')
session.load()

# Get lap data
laps = session.laps

df = laps[['Driver', 'LapTime', 'Compound', 'LapNumber']]

# Save to CSV !(Change to data folder)!
df.to_csv('/Users/mustafa/Desktop/f1-lap-time-prediction/data/lap_times.csv', index=False)

print("Lap time data saved!")