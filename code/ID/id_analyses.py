"""
Code for replicating analyses for Idaho (ID) in DataCenterAtlas.org
"""
# %%
# Import packages
import numpy as np
import pandas as pd
import os
from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt

# %%
# Set up some directory paths
proj_dir = Path(__file__).resolve().parent.parent.parent
data_dir = os.path.join(proj_dir, "data", "ID")
images_dir = os.path.join(proj_dir, "images", "ID")

# %%
# Extract the average effective property tax rates by county from the
# "/data/ID/EPB00129_12-04-2025.csv file
county_df = pd.read_csv(
    os.path.join(data_dir, "EPB00129_12-04-2025.csv"),
    header=0, names = [
        "county_name", "avg_urb_prop_tax_pct", "avg_rur_prop_tax_pct",
        "avg_eff_prop_tax_pct_2025"
    ],
    dtype={
        'county_name': str, 'avg_urb_prop_tax_pct': np.float32,
        'avg_rur_prop_tax_pct': np.float32,
        'avg_eff_prop_tax_pct_2025': np.float32
    }
)

# Create "avg_eff_prop_tax_rate_2025" column and reorder columns to be
# "county_name", "avg_urb_prop_tax_pct", "avg_rur_prop_tax_pct",
# "avg_eff_prop_tax_rate_2025", "avg_eff_prop_tax_pct_2025"
county_df["avg_eff_prop_tax_rate_2025"] = (
    county_df["avg_eff_prop_tax_pct_2025"] / 100
)
# Reorder columns
county_df = county_df[
    [
        "county_name", "avg_urb_prop_tax_pct", "avg_rur_prop_tax_pct",
        "avg_eff_prop_tax_rate_2025", "avg_eff_prop_tax_pct_2025"
    ]
]
print("DETAILS FOR county_df")
print(county_df.dtypes)
print(county_df.keys())
print(county_df.head(10))
print(county_df.tail(10))
print(county_df.describe())

# Save this DataFrame as a csv file cnty_prop_tax_rates_id_2025.csv in the
# data/ID directory
county_df.to_csv(
    os.path.join(data_dir, "cnty_prop_tax_rates_id_2025.csv"), index=False
)

# %%
# Create dynamic data viz of Idaho county average effective property tax
# rates

# # California county FIPS codes are the 2-digit state code "06" followed by 3-
# # digit county codes that are the odd numbers "001", "003", "005", ..."113",
# # "115" in alphabetical order: FIPS = 6000 + 2*i - 1 for i=1,2,...58.
# rate_by_fips = {
#     f"0{6000 + 2 * i + 1}": county_df[
#         "avg_eff_prop_tax_pct"
#     ].iloc[i] for i in range(58)
# }
# counties = gpd.read_file(os.path.join(data_dir,  "CA_Counties.geojson"))
# counties["rate_pct"] = counties["FIPS"].map(rate_by_fips) * 100

# ax = counties.plot(
#     column="rate_pct",
#     cmap="YlOrRd",
#     edgecolor="white",
#     linewidth=0.3,
#     legend=True,
#     legend_kwds={"label": "Effective property tax rate (%)", "shrink": 0.6},
#     figsize=(12, 11),
# )
# ax.set_axis_off()
# ax.set_title(
#     "Texas county property tax rates, 2025\n"
#     "(all overlapping unit levies ÷ county taxable value)"
# )

# plt.savefig(
#     os.path.join(images_dir, "tx_county_rates.png"),
#     dpi=150, bbox_inches="tight"
# )
# print("Wrote images/TX/tx_county_rates.png")

# for county_id, r in sorted(
#     cnty_prop_tax_rates_tx_2025_df.set_index("county_id")[
#         "avg_eff_prop_tax_rate"
#     ].items(), key=lambda kv: -kv[1]
# )[:5]:
#     print(f"  highest: county id {county_id}  {r:.2%}")

# %%
