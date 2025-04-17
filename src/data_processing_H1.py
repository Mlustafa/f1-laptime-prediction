import fastf1
import pandas as pd
import numpy as np
import pickle
from tqdm import tqdm
import os



def fetch_Race_gp_data(Race="Bahrain", years=range(2018, 2025)):
    """
    Fetch Race GP data for specified years and return a dictionary of sessions.
    Key: year, Value: fastf1 Session object
    """
    print(f"Fetching {Race} GP data for years: {list(years)}")

    # Initialize a dictionary to store sessions by year
    sessions = {}

    for year in tqdm(years, desc="Loading sessions"):
        try:
            # Load the race session for the given year
            sess = fastf1.get_session(year, Race, 'R')
            sess.load()
            sessions[year] = sess
            print(f"Successfully loaded {year} {Race} GP.")
        except Exception as e:
            print(f"Error loading {year} {Race} GP: {e}")

    return sessions


def save_all_laps_unfiltered(sessions, output_csv="all_unfiltered_laps.csv"):
    """
    Combine lap data from all sessions (all years) into one DataFrame
    and save it to a CSV (unfiltered).
    """
    # Collect data from each year into a list
    dfs = []

    for year, session_obj in sessions.items():
        laps = session_obj.laps 
        laps = laps.pick_not_deleted().pick_wo_box()
        laps = laps.reset_index(drop=True)
        weather_data = laps.get_weather_data()
        weather_data = weather_data.reset_index(drop=True)
        joined = pd.concat([laps, weather_data.loc[:, ~(weather_data.columns == 'Time')]], axis=1)
        if joined.empty:
            continue
        
        # add a column indicating the year or race name
        joined['Year'] = year

        # Append to list for concatenation
        dfs.append(joined)

    # Concatenate all laps into one big DataFrame
    if dfs:
        all_laps_df = pd.concat(dfs, ignore_index=True)
    else:
        print("No laps data found.")
        return
    
    # Save to CSV unfiltered
    all_laps_df.to_csv(output_csv, index=False)
    print(f"Saved unfiltered laps data to: {output_csv}")


def main():
    Race = "Abudhabi"
    print(f"Fetching {Race} data...")
    
    # 1. Fetch sessions
    sessions = fetch_Race_gp_data(Race=Race, years=range(2018, 2025))
    
    # 2. Save all laps to a single CSV (unfiltered)
    save_all_laps_unfiltered(sessions, output_csv="Abudhabi_unfiltered_laps_with_weather.csv")


if __name__ == "__main__":
    print("Starting data processing...")
    main()
    print("Data processing complete!")
