import pandas as pd
from pathlib import Path

def load_dataset() -> pd.DataFrame:
    """
    Load the Global Power Plant Database from the local data directory.
    Expects: data/global_power_plant_database.csv
    """
    data_path = Path(__file__).resolve().parents[1] / "data" / "global_power_plant_database.csv"
    df = pd.read_csv(data_path, low_memory=False)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df