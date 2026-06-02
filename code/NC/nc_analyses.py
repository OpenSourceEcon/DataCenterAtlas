"""
Code for replicating analyses for North Carolina (NC) in DataCenterAtlas.org
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
data_dir = os.path.join(proj_dir, "data", "NC")
rates_path = os.path.join(
    data_dir, "2025-2026_Tax_Rates_&_Effective_Tax_Rates.xlsx"
)

# %%
# [THE CODE ON THE NEXT 33 LINES AUGMENTS THE
# 2025-2026_Tax_Rates_&_Effective_Tax_Rates.xlsx FILE AND CREATES THE
# avg_proptax_rate_by_cnty_nc_2025_2026.csv file.]
# Load data/NC/2025-2026_Tax_Rates_&_Effective_Tax_Rates.xlsx as pandas
# DataFrame rates_nc_2025_2026_df and create a new variable (rate_cnty_avg)
# that is the average property tax rate by county (cnty_name) using groupby.
# The data start on row 2 (python index 1) and the variable names are in that
# row. The data end in row 812 (python index 811).
rates_nc_2025_2026_df = pd.read_excel(rates_path, skiprows=1, nrows=810)
# Rename the 11 columns
rates_nc_2025_2026_df.columns = [
    "cnty_name",
    "mncpl_name",
    "ratio_appr_cnty",
    "sales_asses_ratio_2025",
    "last_appr_year",
    "prop_tax_rate_cnty",
    "prop_tax_rate_mncpl",
    "prop_tax_rate_comb",
    "prop_tax_rate_eff_cnty",
    "prop_tax_rate_eff_mncpl",
    "prop_tax_rate_eff_comb",
]

# Make sure that columns prop_tax_rate_mncpl, prop_tax_rate_comb,
# prop_tax_rate_eff_mncpl, and prop_tax_rate_eff_comb are floats in which any
# value "none" is "np.nan"
for col in [
    "prop_tax_rate_mncpl",
    "prop_tax_rate_comb",
    "prop_tax_rate_eff_mncpl",
    "prop_tax_rate_eff_comb",
]:
    rates_nc_2025_2026_df[col] = pd.to_numeric(
        rates_nc_2025_2026_df[col], errors="coerce"
    )

# For municipalities (rows) for which the prop_tax_rate_mncpl variable is
# np.nan, set the prop_tax_rate_comb variable to be the same as the
# prop_tax_rate_cnty variable.
rates_nc_2025_2026_df.loc[
    rates_nc_2025_2026_df["prop_tax_rate_mncpl"].isna(), "prop_tax_rate_comb"
] = rates_nc_2025_2026_df.loc[
    rates_nc_2025_2026_df["prop_tax_rate_mncpl"].isna(), "prop_tax_rate_cnty"
]
# For municipalities (rows) for which the prop_tax_rate_eff_mncpl variable is
# np.nan, set the prop_tax_rate_eff_comb variable to be the same as the
# prop_tax_rate_eff_cnty variable.
rates_nc_2025_2026_df.loc[
    rates_nc_2025_2026_df["prop_tax_rate_eff_mncpl"].isna(),
    "prop_tax_rate_eff_comb"
] = rates_nc_2025_2026_df.loc[
    rates_nc_2025_2026_df["prop_tax_rate_eff_mncpl"].isna(),
    "prop_tax_rate_eff_cnty"
]

rates_nc_2025_2026_df["rate_cnty_avg"] = (
    rates_nc_2025_2026_df.groupby(
        "cnty_name"
    )["prop_tax_rate_comb"].transform("mean")
) / 100

# %%
# Create a DataFrame that is just the county varible (cnty_name) and the
# average property tax rate by county (rate_cnty_avg) that is just the one
# value for each county. Reset the index and print the DataFrame. Save the
# DataFrame as a csv file avg_proptax_rate_by_cnty_nc_2025_2026.csv in the
# data/NC directory
cnty_avg_df = rates_nc_2025_2026_df[
    ["cnty_name", "rate_cnty_avg"]
].drop_duplicates().reset_index(drop=True)
print(cnty_avg_df)
cnty_avg_df.to_csv(
    os.path.join(data_dir, "avg_proptax_rate_by_cnty_nc_2025_2026.csv"),
    index=False
)

# %%
