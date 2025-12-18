import pandas as pd
import numpy as np
import plotly.express as px

def preprocess_data(df: pd.DataFrame):
    """
    Clean, prepare, and aggregate the dataset exactly as in the Milestone 2 notebook.
    Returns a dictionary with cleaned data and visualization constants.
    """

    # Clean and prepare
    df = df.drop_duplicates()
    df = df.dropna(subset=['capacity_mw', 'primary_fuel'])

    df['primary_fuel'] = df['primary_fuel'].astype(str).str.strip().str.title()
    df['country_long'] = df['country_long'].astype(str).str.strip().str.title()

    df['estimated_generation_gwh_2017'] = df['estimated_generation_gwh_2017'].fillna(0)

    # Define renewables
    renewables = {"Hydro", "Solar", "Wind", "Geothermal", "Biomass", "Wave And Tidal", "Storage"}

    # Label plants
    df['energy_category'] = np.where(df['primary_fuel'].isin(renewables), 'Renewable', 'Non-Renewable')
    df['renewable_flag'] = np.where(df['primary_fuel'].isin(renewables), 'Renewable', 'Nonrenewable')

    # Remove extreme outliers
    cap_limit = df['capacity_mw'].quantile(0.999)
    df = df[df['capacity_mw'] <= cap_limit]

    # Trimmed version for visuals
    y_max = df['capacity_mw'].quantile(0.95)
    df_filtered = df[df['capacity_mw'] <= y_max].copy()

    # Aggregated data
    capacity_by_category = (
        df.groupby('energy_category', as_index=False)['capacity_mw']
          .sum()
          .sort_values('capacity_mw', ascending=False)
    )

    capacity_by_fuel = (
        df.groupby('primary_fuel', as_index=False)['capacity_mw']
          .sum()
          .sort_values('capacity_mw', ascending=False)
    )

    # Visualization constants
    data_note = "Data reflects global installed capacity as of 2017 (Global Power Plant Database)."
    fuel_palette = px.colors.qualitative.Safe
    numeric_palette = "Viridis"
    energy_colors = {
        "Renewable": "#1f77b4",
        "Non-Renewable": "#d62728"
    }

    print("Columns ready for visualization:", [c for c in df.columns if 'energy' in c or 'renewable' in c])

    return {
        "df": df,
        "df_filtered": df_filtered,
        "capacity_by_category": capacity_by_category,
        "capacity_by_fuel": capacity_by_fuel,
        "fuel_palette": fuel_palette,
        "numeric_palette": numeric_palette,
        "energy_colors": energy_colors,
        "data_note": data_note
    }