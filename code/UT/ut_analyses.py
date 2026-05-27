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
from scipy.optimize import root_scalar
import matplotlib.pyplot as plt
from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.palettes import Reds9
from bokeh.models import (
    GeoJSONDataSource, HoverTool, ColumnD

# %%
# Load data/rates_ut_2025.csv as pandas DataFrame rates_ut_2025_df and create
# a new variable (rate_cnty_avg) that is the average property tax rate by
# county (cnty_name) using groupby. The data start on row 5 (python index 4)
# and the variable names are in that row. The data end in row `364 (python
# index 1363).
data_path = Path("data/rates_ut_2025.csv")
rates_ut_2025_df = pd.read_csv(data_path, skiprows=4, nrows=1360)
rates_ut_2025_df["rate_cnty_avg"] = (
    rates_ut_2025_df.groupby("cnty_name")["rate"].transform("mean")
)
rates_ut_2025_df
