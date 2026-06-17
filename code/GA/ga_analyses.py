"""
Code for replicating analyses for Georgia (GA) in DataCenterAtlas.org
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
data_dir = os.path.join(proj_dir, "data", "GA")
images_dir = os.path.join(proj_dir, "images", "GA")

# %%
# Import the total levies by county data as a Pandas DataFrame
# I extracted the data in the "/data/GA/county_tot_levies_ga_2025.csv" file
# from the PDF file
# "/data/GA/2025 Summary of Ad Valorem Taxes Levied Report.pdf" using ChatGPT
# https://chatgpt.com/share/6a32ee08-9950-83ea-9bff-2a3e7a19ab2a
tot_levies_df = pd.read_csv(
    os.path.join(data_dir, "county_tot_levies_ga_2025.csv"),
    header=0, names=["county_name", "tot_levies"],
    dtype={"county": str, "tot_levies": np.float32}
)
print("DETAILS FOR tot_levies_df")
print(tot_levies_df.dtypes)
print(tot_levies_df.keys())
print(tot_levies_df.head(10))
print(tot_levies_df.tail(10))
print(tot_levies_df.describe())

# %%
# Calculate total taxable value by county, then inflate it from 40% to 100% in
# order to calculate the average effective property tax rates
tot_txbl_val_df = pd.read_excel(
    os.path.join(data_dir, "Digest Export 4.6.26.xlsx"), header=0,
    names=[
        "cnty_name", "cnty_code", "dist_name", "dist_code", "tax_year",
        "tot_assess_val_mo", "tot_assess_val_bnd"
    ],
    usecols="A:E,PD:PE",
    dtype={
        "cnty_name": str, "cnty_code": int, "dist_name": str, "dist_code": int,
        "tax_year": int, "tot_assess_val_mo": np.float32,
        "tot_assess_val_bnd": np.float32
    }
)
# Fix typos in cnty_name column. Change any instances of "ATKINS" to "ATKINSON"
# in "county_name" variable
tot_txbl_val_df["cnty_name"] = tot_txbl_val_df["cnty_name"].replace(
    "ATKINS", "ATKINSON"
)
tot_txbl_val_df["cnty_name"] = tot_txbl_val_df["cnty_name"].replace(
    "HEARD KA", "HEARD"
)
tot_txbl_val_df["cnty_name"] = tot_txbl_val_df["cnty_name"].replace(
    "JONES KA", "JONES"
)
tot_txbl_val_df["cnty_name"] = tot_txbl_val_df["cnty_name"].replace(
    "POLK KA", "POLK"
)
tot_txbl_val_df["cnty_name"] = tot_txbl_val_df["cnty_name"].replace(
    "WHEELE", "WHEELER"
)
# Change all the cnty_name values to uppercase first letter of each word and
# lowercase for the rest. Then change "Dekalb" to "DeKalb", "Mcduffie" to
# "McDuffie", and "Mcintosh" to "McIntosh"
tot_txbl_val_df["cnty_name"] = tot_txbl_val_df["cnty_name"].str.title()
tot_txbl_val_df["cnty_name"] = tot_txbl_val_df["cnty_name"].replace(
    {"Dekalb": "DeKalb", "Mcduffie": "McDuffie", "Mcintosh": "McIntosh"}
)
print("DETAILS FOR tot_txbl_val_df")
print(tot_txbl_val_df.dtypes)
print(tot_txbl_val_df.keys())
print(tot_txbl_val_df.head(20))
print(tot_txbl_val_df.tail(10))
print(tot_txbl_val_df.describe())

# %%
# Create property tax rate variables
# Add tot_txbl_val column to tot_levies_df
tot_txbl_val_cnty_df = tot_txbl_val_df[tot_txbl_val_df["dist_code"]==0][
    ["cnty_name", "cnty_code", "dist_name", "dist_code", "tot_assess_val_mo"]
]
# Make a new DataFrame called tot_levies_txbl_val_df that merges all the
# variables from tot_levies_df with tot_txbl_val from tot_txbl_val_cnty_df
tot_levies_txbl_val_df = pd.merge(
    tot_levies_df, tot_txbl_val_cnty_df[["cnty_name", "tot_assess_val_mo"]],
    left_on="county_name", right_on="cnty_name", how="left"
)
# Make sure all entries in "county_name" equal the entries in "cnty_name" in
# tot_levies_txbl_val_df, then delete the "cnty_name" variable
assert (
    tot_levies_txbl_val_df["county_name"] ==
    tot_levies_txbl_val_df["cnty_name"]
).all()
tot_levies_txbl_val_df = tot_levies_txbl_val_df.drop(columns=["cnty_name"])
tot_levies_txbl_val_df["avg_prop_tax_rate"] = (
    tot_levies_txbl_val_df["tot_levies"] /
    tot_levies_txbl_val_df["tot_assess_val_mo"]
)
tot_levies_txbl_val_df["avg_prop_tax_pct"] = (
    tot_levies_txbl_val_df["avg_prop_tax_rate"] * 100
)
# Create avg_eff_prop_tax_rate that accounts for the homestead exemption and
# the 40% assessment ratio. We assume that 60% of the assessed property values
# are residential and therefore the homestead exemption reduces the assessment
# ratio for those properties to 39%
tot_levies_txbl_val_df["avg_eff_prop_tax_rate"] = (
    tot_levies_txbl_val_df["tot_levies"] / (
        0.4 * (tot_levies_txbl_val_df["tot_assess_val_mo"] / 0.4) +
        0.6 * (tot_levies_txbl_val_df["tot_assess_val_mo"] / 0.39)
    )
)
tot_levies_txbl_val_df["avg_eff_prop_tax_pct"] = (
    tot_levies_txbl_val_df["avg_eff_prop_tax_rate"] * 100
)

print("DETAILS FOR tot_levies_txbl_val_df")
print(tot_levies_txbl_val_df.dtypes)
print(tot_levies_txbl_val_df.keys())
print(tot_levies_txbl_val_df.head(20))
print(tot_levies_txbl_val_df.tail(10))
print(tot_levies_txbl_val_df.describe())

# Save this DataFrame as a csv file cnty_prop_tax_rates_ga_2025.csv in the
# data/GA directory
tot_levies_txbl_val_df.to_csv(
    os.path.join(data_dir, "cnty_prop_tax_rates_ga_2025.csv"), index=False
)

# %%
# Create dynamic data viz of Georgia county average effective property tax
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
