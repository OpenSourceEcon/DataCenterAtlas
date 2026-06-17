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
# Import csv file as Pandas DataFrame
county_df = pd.read_csv(
    os.path.join(data_dir, "PropTaxGenPropTaxLevies.csv"),
    header=0, names = [
        "county", "net_txbl_assessed_val", "tot_prop_tax_alloc_levies",
        "avg_eff_prop_tax_pct"
    ],
    usecols=[2, 3, 8, 9], nrows=58,
    dtype={
        'county': str, 'net_txbl_assessed_val': np.float32,
        'tot_prop_tax_alloc_levies': np.float32,
        'avg_eff_prop_tax_pct': np.float32
    }
)

# Create avg_eff_prop_tax_rate column as a decimal fraction or
# avg_eff_prop_tax_pct / 100. Then reorder the last two columns
# avg_eff_prop_tax_rate then avg_eff_prop_tax_pct.
county_df["avg_eff_prop_tax_rate"] = county_df["avg_eff_prop_tax_pct"] / 100
county_df = county_df[
    ["county", "net_txbl_assessed_val", "tot_prop_tax_alloc_levies",
     "avg_eff_prop_tax_rate", "avg_eff_prop_tax_pct"]
]

print("DETAILS FOR county_df")
print(county_df.dtypes)
print(county_df.keys())
print(county_df.head(10))
print(county_df.tail(10))
print(county_df.describe())

# Save this DataFrame as a csv file cnty_prop_tax_rates_ca_2025.csv in the
# data/CA directory
county_df.to_csv(
    os.path.join(data_dir, "cnty_prop_tax_rates_ca_2025.csv"), index=False
)

# %%
# Create dynamic data viz of California county average effective property tax
# rates

# California county FIPS codes are the 2-digit state code "06" followed by 3-
# digit county codes that are the odd numbers "001", "003", "005", ..."113",
# "115" in alphabetical order: FIPS = 6000 + 2*i - 1 for i=1,2,...58.
rate_by_fips = {
    f"0{6000 + 2 * i + 1}": county_df[
        "avg_eff_prop_tax_pct"
    ].iloc[i] for i in range(58)
}
counties = gpd.read_file(os.path.join(data_dir,  "CA_Counties.geojson"))
counties["rate_pct"] = counties["FIPS"].map(rate_by_fips) * 100

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
