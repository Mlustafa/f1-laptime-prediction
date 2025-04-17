import pandas as pd
import numpy as np
from pathlib import Path

# ---------------------------
# CONFIG – adjust as desired
# ---------------------------
INPUT_FILE  = "/Users/mustafa/Desktop/f1-lap-time-prediction/data/Bahrain_unfiltered_laps.csv"     
OUTPUT_FILE = "/Users/mustafa/Desktop/f1-lap-time-prediction/data/Bahrain_ready_for_model.csv"   
CIRCUIT_NAME = "Bahrain"                      # will be stored in a new column 

# Which categorical columns to one‑hot encode
CATEGORICALS = ["Compound", "Team", "Driver", "TrackStatus"]

# Numeric columns we’ll keep as‑is
NUMERICS = [
    "LapNumber", "Stint", "TyreLife",
    "SpeedI1", "SpeedI2", "SpeedFL", "SpeedST",
    "Position", "Year",
]

# -------------------------------------------------
# 1. LOAD  (no parse_dates needed for LapTime now)
# -------------------------------------------------
df = pd.read_csv(INPUT_FILE)

# ----------------------------------------------
# 2. CONVERT LapTime (object ➜ float seconds)
# ----------------------------------------------
df = df[df["LapTime"].notna()]                # drop rows that are empty 
df["LapTime"] = pd.to_timedelta(df["LapTime"], errors="coerce").dt.total_seconds()


# ----------------------------------------------
# 3. ADD a 1‑lap‑ago feature per driver & year
# ----------------------------------------------
df = df.sort_values(["Year", "Driver", "LapNumber"])
df["LapTime_lag1"] = df.groupby(["Year", "Driver"])["LapTime"].shift(1)
df.dropna(subset=["LapTime_lag1"], inplace=True)

# ----------------------------------------------
# 4. DROP leak / meta columns we don’t want
# ----------------------------------------------
LEAK_COLS = [
    "Sector1Time", "Sector2Time", "Sector3Time",
    "Sector1SessionTime", "Sector2SessionTime", "Sector3SessionTime",
    "PitOutTime", "PitInTime",                 # you filtered but keep safe
    "IsPersonalBest", "Deleted", "DeletedReason",
    "FastF1Generated", "IsAccurate",
    "Time", "LapStartTime", "LapStartDate"
]
df.drop(columns=[c for c in LEAK_COLS if c in df.columns], inplace=True, errors="ignore")

# -------------------------------------------------
# 5. ONE‑HOT encode categoricals (Will not use since my H2 will compare static vs temporal models)
# -------------------------------------------------
# df = pd.get_dummies(df, columns=CATEGORICALS, drop_first=False)

# -------------------------------------------------
# 6. ADD circuit label (handy if you later concat)
# -------------------------------------------------
df["Circuit"] = CIRCUIT_NAME

# -------------------------------------------------
# 7. SELECT final columns order (optional)
# -------------------------------------------------
target = "LapTime"
feature_cols = NUMERICS + [c for c in df.columns if any(cat + "_" in c for cat in CATEGORICALS)] + ["LapTime_lag1", "Circuit"]
df = df[[target] + feature_cols]

# -------------------------------------------------
# 8. SAVE ready‑to‑model file
# -------------------------------------------------
# Path(OUTPUT_FILE).parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved cleaned file → {OUTPUT_FILE}  |  rows: {len(df)}  |  cols: {df.shape[1]}")