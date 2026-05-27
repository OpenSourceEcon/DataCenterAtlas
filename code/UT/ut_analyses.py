"""
Code for replicating analyses for Utah (UT) in DataCenterAtlas.org
"""
# %%
# Import packages
from pathlib import Path
import os
import json
import pickle
import time
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.palettes import Reds9
from bokeh.models import (
    GeoJSONDataSource, HoverTool, ColumnDataSource, Legend, LegendItem, Title
)

# %%
# Set up some directory paths
proj_dir = Path(__file__).resolve().parent.parent.parent
data_dir = proj_dir / "data" / "UT"
data_path = data_dir / "rates_ut_2025.csv"

# %%
# Load data/rates_ut_2025.csv as pandas DataFrame rates_ut_2025_df and create
# a new variable (rate_cnty_avg) that is the average property tax rate by
# county (cnty_name) using groupby. The data start on row 5 (python index 4)
# and the variable names are in that row. The data end in row `364 (python
# index 1363).
rates_ut_2025_df = pd.read_csv(data_path, skiprows=4, nrows=1360)
rates_ut_2025_df["rate_cnty_avg"] = (
    rates_ut_2025_df.groupby("cnty_name")["rate_final"].transform("mean")
)
# Save data from rates_ut_2025_df with new variable rate_cnty_avg to the same
# rows in the original rates_ut_2025.csv, preserving the header top 4 rows, but
# replacing the original data with this new data. The weighting here is equal
# across all rows. This would be better if we weighted by tax revenue in each
# tax area (row).
with open(data_path, "r") as f:
    header_rows = [next(f) for _ in range(4)]
with open(data_path, "w") as f:
    f.writelines(header_rows)
rates_ut_2025_df.to_csv(data_path, index=False, mode="a", header=True)

# %%
# Create a DataFrame that is just the county varible (cnty_name) and the
# average property tax rate by county (rate_cnty_avg) that is just the one
# value for each county. Reset the index and print the DataFrame. Save the
# DataFrame as a csv file avg_proptax_rate_by_cnty_ut_2025.csv in the data/UT
# directory
cnty_avg_df = rates_ut_2025_df[
    ["cnty_name", "rate_cnty_avg"]
].drop_duplicates().reset_index(drop=True)
print(cnty_avg_df)
cnty_avg_df.to_csv(
    data_dir / "avg_proptax_rate_by_cnty_ut_2025.csv", index=False
)

# %%
