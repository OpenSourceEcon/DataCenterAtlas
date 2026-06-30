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
        "Carson City",
        "Churchill",
        "Clark",
        "Douglas",
        "Elko",
        "Esmeralda",
        "Eureka",
        "Humboldt",
        "Lander",
        "Lincoln",
        "Lyon",
        "Mineral",
        "Nye",
        "Pershing",
        "Storey",
        "Washoe",
        "White Pine"
    ],
    "avg_eff_prop_tax_rate_2025": [
        0.0046,
        0.0052,
        0.0052,
        0.0045,
        0.0056,
        0.0052,
        0.0034,
        0.0056,
        0.0073,
        0.0054,
        0.0050,
        0.0073,
        0.0051,
        0.0068,
        0.0042,
        0.0046,
        0.0055
    ]
}).astype({"avg_eff_prop_tax_rate_2025": np.float32})
pte_proptax_rates_df["avg_eff_prop_tax_pct_2025"] = (
    pte_proptax_rates_df["avg_eff_prop_tax_rate_2025"] * 100
)

# Save this DataFrame as a csv file cnty_prop_tax_rates_nv_2025.csv in the
# data/NV directory
pte_proptax_rates_df.to_csv(
    os.path.join(data_dir, "cnty_prop_tax_rates_nv_2025.csv"), index=False
)

print("DETAILS FOR pte_proptax_rates_df")
print(pte_proptax_rates_df.dtypes)
print(pte_proptax_rates_df.keys())
print(pte_proptax_rates_df.head(10))
print(pte_proptax_rates_df.tail(10))
print(pte_proptax_rates_df.describe())

# %%
# Read in FY 2026 after-exemptions assessment values from page A-1 and total
# allowed revenues (column 30) from the county tables in
# https://tax.nv.gov/wp-content/uploads/2025/03/Final-Revenue-Projections-FY25.26.pdf
nv_prop_tax_df = pd.DataFrame({
    "county_name": [
        "Carson City",
        "Churchill",
        "Clark",
        "Douglas",
        "Elko",
        "Esmeralda",
        "Eureka",
        "Humboldt",
        "Lander",
        "Lincoln",
        "Lyon",
        "Mineral",
        "Nye",
        "Pershing",
        "Storey",
        "Washoe",
        "White Pine"
    ],
    "aft_exemp_prop_val": [
        2_608_605_932,
        1_224_164_907,
        152_571_071_908,
        4_886_575_182,
        2_548_635_842,
        277_879_990,
        1_784_429_418,
        2_089_861_660,
        1_758_189_304,
        422_824_219,
        3_414_228_155,
        318_895_304,
        2_516_930_712,
        515_342_611,
        3_543_355_021,
        31_982_957_867,
        723_147_733
    ],
    "tot_allowed_rev": [
        81_509_167,
        53_143_317,
        1_663_269_999,
        67_052_397,
        109_535_916,
        47_983_748,
        804_911_279,
        72_144_573,
        707_344_075,
        24_613_799,
        120_831_520,
        32_925_783,
        345_098_805,
        159_412_949,
        302_688_356,
        1_236_841_840,
        186_714_837
    ],
    "tot_comb_tax_rate": [
        0.031246,
        0.044650,
        0.010902,
        0.013722,
        0.044507,

    ]
}).astype(
    {
        "aft_exemp_prop_val": np.float32,
        "tot_allowed_rev": np.float32
    }
)

# Calculated the before-exemptions / after-exemptions ratio of NV statewide
# assessed valuations using two tables on page 72 of
# https://tax.nv.gov/wp-content/uploads/2026/01/FY25_AnnualReport_FINAL.pdf
exemp_ratio = 288_392_802_369 / 213_655_703_485
print("Exemption ratio is:", exemp_ratio)
assess_ratio = 0.35

# Inflate the after-exemptions assessed property values to reflect the
# exemption ratio and the assessment ratio in order to get fair market value
nv_prop_tax_df["fmv_prop_val"] = (
    exemp_ratio * nv_prop_tax_df["aft_exemp_prop_val"] / assess_ratio
)
# Reorder variables
nv_prop_tax_df = nv_prop_tax_df[
    ["county_name", "aft_exemp_prop_val", "fmv_prop_val", "tot_allowed_rev"]
]
# Create average effective property tax rate
nv_prop_tax_df["avg_eff_prop_tax_rate"] = (
    nv_prop_tax_df["tot_allowed_rev"] / nv_prop_tax_df["fmv_prop_val"]
)
nv_prop_tax_df["avg_eff_prop_tax_pct"] = (
    nv_prop_tax_df["avg_eff_prop_tax_rate"] * 100
)


# # Save this DataFrame as a csv file cnty_prop_tax_rates_nv_2026.csv in the
# # data/NV directory
# nv_prop_tax_df.to_csv(
#     os.path.join(data_dir, "cnty_prop_tax_rates_nv_2026.csv"), index=False
# )

print("DETAILS FOR nv_prop_tax_df")
print(nv_prop_tax_df.dtypes)
print(nv_prop_tax_df.keys())
print(nv_prop_tax_df.head(10))
print(nv_prop_tax_df.tail(10))
print(nv_prop_tax_df.describe())

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
