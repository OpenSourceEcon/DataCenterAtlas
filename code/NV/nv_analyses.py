"""
Code for replicating analyses for Nevada (NV) in DataCenterAtlas.org
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
data_dir = os.path.join(proj_dir, "data", "NV")
images_dir = os.path.join(proj_dir, "images", "NV")

# %%
# Hard code the average effective property tax rates for Nevada's 17 counties
# from Property Tax Explorer website: https://propertytaxexplorer.com/us/nevada
# These look like the same rates that Tax Foundation used.
pte_proptax_rates_df = pd.DataFrame({
    "county_name": [
        "Carson City", "Churchill", "Clark", "Douglas", "Elko", "Esmeralda",
        "Eureka", "Humboldt", "Lander", "Lincoln", "Lyon", "Mineral",
        "Nye", "Pershing", "Storey", "Washoe", "White Pine"
    ],
    "avg_eff_prop_tax_rate_2025": [
        0.0046, 0.0052, 0.0052, 0.0045, 0.0056, 0.0052, 0.0034, 0.0056, 0.0073,
        0.0054, 0.0050, 0.0073, 0.0051, 0.0068, 0.0042, 0.0046, 0.0055
    ]
})
pte_proptax_rates_df["avg_eff_prop_tax_pct_2025"] = (
    pte_proptax_rates_df["avg_eff_prop_tax_rate_2025"] * 100
)

print("DETAILS FOR pte_proptax_rates_df")
print(pte_proptax_rates_df.dtypes)
print(pte_proptax_rates_df.keys())
print(pte_proptax_rates_df.head(10))
print(pte_proptax_rates_df.tail(10))
print(pte_proptax_rates_df.describe())

# Save this DataFrame as a csv file cnty_prop_tax_rates_or_2025.csv in the
# data/OR directory
pte_proptax_rates_df.to_csv(
    os.path.join(data_dir, "cnty_prop_tax_rates_nv_2025.csv"), index=False
)

# %%
# Create dynamic data viz of Nevada county average effective property tax
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
