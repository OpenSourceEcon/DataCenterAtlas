"""
Read in four Texas Comptroller 2025 workbooks and calculate the average
effective property tax rate by county, then visualize it on a map. Texas county
property tax rates from the Comptroller's 2025 Tax Ratesand Levies workbooks
https://comptroller.texas.gov/taxes/property-tax/rates/.

A county's taxing units (county, school districts, cities, special districts)
only partially overlap, so you can't simply add up their nominal rates.
Instead we compute the average effective rate actually paid in each county:

    rate = (sum of CALCULATED LEVY of every unit in the county)
           / (county taxable value)

This is the levy-weighted sum of each parcel's overlapping unit rates.
Texas appraises at 100% of market value, so the result is an effective rate.
"""
# %%
# Import packages
import os
from pathlib import Path
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# %%
# Set up some directory paths
proj_dir = Path(__file__).resolve().parent.parent.parent
data_dir = os.path.join(proj_dir, "data", "TX")
images_dir = os.path.join(proj_dir, "images", "TX")

# %%
# Import workbooks as Pandas DataFrames
county_df = pd.read_excel(
    os.path.join(data_dir, "2025-county-rates-levies.xlsx"),
    header=2, names = [
        "cad_id", "cad_name","county_id", "county_name", "tax_unit_id",
        "mkt_val", "txbl_val_gen_rd_br", "txbl_val_fmfc", "tot_cnty_tax_rate",
        "calculated_levy"
    ],
    usecols="A:E,H:J,V:W",
    dtype={"county_id": str}
).astype(
    {
        "cad_id": str,
        "cad_name": str,
        "county_id": str,
        "county_name": str,
        "tax_unit_id": str,
        "mkt_val": float,
        "txbl_val_gen_rd_br": float,
        "txbl_val_fmfc": float,
        "tot_cnty_tax_rate": float,
        "calculated_levy": float
    }
)
print("DETAILS FOR county_df")
print(county_df.dtypes)
print(county_df.keys())
print(county_df.head(10))

school_df = pd.read_excel(
    os.path.join(data_dir, "2025-school-district-rates-levies.xlsx"),
    header=2, names = [
        "cad_id", "cad_name","county_id", "county_name", "tax_unit_id",
        "tax_unit_name", "mkt_val", "txbl_val_mo", "txbl_val_is",
        "tot_tax_rate", "calculated_levy"
    ],
    usecols="A:F,J:L,Q:R",
    dtype={"county_id": str}
).astype(
    {
        "cad_id": str,
        "cad_name": str,
        "county_id": str,
        "county_name": str,
        "tax_unit_id": str,
        "tax_unit_name": str,
        "mkt_val": float,
        "txbl_val_mo": float,
        "txbl_val_is": float,
        "tot_tax_rate": float,
        "calculated_levy": float
    }
).assign(tax_unit_name=lambda df: df["tax_unit_name"].str.strip())
print("")
print("DETAILS FOR school_df")
print(school_df.dtypes)
print(school_df.keys())
print(school_df.head(10))

city_df = pd.read_excel(
    os.path.join(data_dir, "2025-city-rates-levies.xlsx"),
    header=2, names = [
        "cad_id", "cad_name","county_id", "county_name", "tax_unit_id",
        "tax_unit_name", "mkt_val", "txbl_val", "tot_tax_rate",
        "calculated_levy"
    ],
    usecols="A:F,J:K,P:Q",
    dtype={"county_id": str}
).astype(
    {
        "cad_id": str,
        "cad_name": str,
        "county_id": str,
        "county_name": str,
        "tax_unit_id": str,
        "tax_unit_name": str,
        "mkt_val": float,
        "txbl_val": float,
        "tot_tax_rate": float,
        "calculated_levy": float
    }
)
print("")
print("DETAILS FOR city_df")
print(city_df.dtypes)
print(city_df.keys())
print(city_df.head(10))

special_df = pd.read_excel(
    os.path.join(data_dir, "2025-special-district-rates-levies.xlsx"),
    header=3, names = [
        "cad_id", "cad_name", "county_id", "county_name", "tax_unit_id",
        "tax_unit_name", "mkt_val", "txbl_val", "tot_tax_rate",
        "calculated_levy"
    ],
    usecols="A:F,J:K,P:Q",
    dtype={"county_id": str}
).astype(
    {
        "cad_id": str,
        "cad_name": str,
        "county_id": str,
        "county_name": str,
        "tax_unit_id": str,
        "tax_unit_name": str,
        "mkt_val": float,
        "txbl_val": float,
        "tot_tax_rate": float,
        "calculated_levy": float
    }
)
print("")
print("DETAILS FOR special_df")
print(special_df.dtypes)
print(special_df.keys())
print(special_df.head(10))

# %%
# Add up total calculated levy for each county, then divide by total taxable
# valuation for each county
cnty_prop_tax_rates_tx_2025_df = county_df[
    ["county_id", "county_name", "txbl_val_gen_rd_br", "calculated_levy"]
]
# rename txbl_val_gen_rd_br to cnty_txbl_val and calculated_levy to
# cnty_calculated_levy
cnty_prop_tax_rates_tx_2025_df = cnty_prop_tax_rates_tx_2025_df.rename(
    columns={
        "txbl_val_gen_rd_br": "cnty_txbl_val",
        "calculated_levy": "cnty_calculated_levy"
    }
)
print("Counties with cnty_calculated_levy == None or 0.")
print(
    cnty_prop_tax_rates_tx_2025_df[
        (cnty_prop_tax_rates_tx_2025_df["cnty_calculated_levy"].isnull()) |
        (cnty_prop_tax_rates_tx_2025_df["cnty_calculated_levy"] == 0)
    ]
)
# Print any records that have the string " *" in the county_name variable.
print("Counties with ' *' in county_name.")
print(
    cnty_prop_tax_rates_tx_2025_df[
        cnty_prop_tax_rates_tx_2025_df["county_name"].str.contains(
            " *", regex=False
        )
    ]
)
# Get rid of the " *" in county_name == "Culberson *"
cnty_prop_tax_rates_tx_2025_df["county_name"] = cnty_prop_tax_rates_tx_2025_df[
    "county_name"
].str.replace(" *", "", regex=False)

# Sum the txbl_val_mo and calculated_levy variables in school_df by county_id
# and add those variables as schl_txbl_val and schl_calculated_levy to the
# cnty_prop_tax_rates_tx_2025_df DataFrame by county_id. Merge on county_id and
# make sure the merge is one-to-one, no missing values and no duplicates.
schl_tot_txbl_val_by_cnty = school_df.groupby("county_id")["txbl_val_mo"].sum()
schl_tot_calculated_levy_by_cnty = school_df.groupby("county_id")[
    "calculated_levy"
].sum()
cnty_prop_tax_rates_tx_2025_df = cnty_prop_tax_rates_tx_2025_df.merge(
    schl_tot_txbl_val_by_cnty.rename("schl_txbl_val"), on="county_id",
    how="left"
).merge(
    schl_tot_calculated_levy_by_cnty.rename("schl_calculated_levy"),
    on="county_id", how="left"
)
print(
    "Merge of schl_tot_txbl_val_by_cnty and schl_tot_calculated_levy_by_cnty" +
    " into cnty_prop_tax_rates_tx_2025_df\n resulted in " +
    f"{len(schl_tot_txbl_val_by_cnty)} rows and " +
    f"{len(schl_tot_calculated_levy_by_cnty)} rows versus the " +
    f"{len(cnty_prop_tax_rates_tx_2025_df)} rows in the county DataFrame."
)
print(
    "The number of missing or 0 values in schl_txbl_val variable after merge" +
    " is " +
    f"{cnty_prop_tax_rates_tx_2025_df['schl_txbl_val'].isnull().sum()}."
)
print(
    "The number of missing or 0 values in schl_calculated_levy variable " +
    "after merge is " +
    f"{cnty_prop_tax_rates_tx_2025_df['schl_calculated_levy'].isnull().sum()}."
)
print(
    "The number of duplicate county_id values in " +
    "cnty_prop_tax_rates_tx_2025_df after merge with school variables is " +
    f"{cnty_prop_tax_rates_tx_2025_df['county_id'].duplicated().sum()}."
)

# Sum the txbl_val and calculated_levy variables in city_df by county_id and
# add those variables as city_txbl_val and city_calculated_levy to the
# cnty_prop_tax_rates_tx_2025_df DataFrame by county_id. Merge on county_id and
# make sure the merge is one-to-one, no missing values and no duplicates.
city_tot_txbl_val_by_cnty = city_df.groupby("county_id")["txbl_val"].sum()
city_tot_calculated_levy_by_cnty = city_df.groupby("county_id")[
    "calculated_levy"
].sum()
cnty_prop_tax_rates_tx_2025_df = cnty_prop_tax_rates_tx_2025_df.merge(
    city_tot_txbl_val_by_cnty.rename("city_txbl_val"), on="county_id",
    how="left"
).merge(
    city_tot_calculated_levy_by_cnty.rename("city_calculated_levy"),
    on="county_id", how="left"
)
# Replace NaN entries in city_txbl_val and city_calculated_levy with 0.
# Originally, 11 observations had NaN values in both variables.
cnty_prop_tax_rates_tx_2025_df[
    "city_txbl_val"
] = cnty_prop_tax_rates_tx_2025_df["city_txbl_val"].fillna(0)
cnty_prop_tax_rates_tx_2025_df[
    "city_calculated_levy"
] = cnty_prop_tax_rates_tx_2025_df["city_calculated_levy"].fillna(0)
print(
    "Merge of city_tot_txbl_val_by_cnty and city_tot_calculated_levy_by_cnty" +
    " into cnty_prop_tax_rates_tx_2025_df\n resulted in " +
    f"{len(city_tot_txbl_val_by_cnty)} rows and " +
    f"{len(city_tot_calculated_levy_by_cnty)} rows versus the " +
    f"{len(cnty_prop_tax_rates_tx_2025_df)} rows in the county DataFrame."
)
print(
    "The number of missing or 0 values in city_txbl_val variable after merge" +
    " is " +
    f"{cnty_prop_tax_rates_tx_2025_df['city_txbl_val'].isnull().sum()}."
)
print(
    "The number of missing or 0 values in city_calculated_levy variable " +
    "after merge is " +
    f"{cnty_prop_tax_rates_tx_2025_df['city_calculated_levy'].isnull().sum()}."
)
print(
    "The number of duplicate county_id values in " +
    "cnty_prop_tax_rates_tx_2025_df after merge with city variables is " +
    f"{cnty_prop_tax_rates_tx_2025_df['county_id'].duplicated().sum()}."
)

# Sum the txbl_val and calculated_levy variables in special_df by county_id and
# add those variables as spec_txbl_val and spec_calculated_levy to the
# cnty_prop_tax_rates_tx_2025_df DataFrame by county_id. Merge on county_id and
# make sure the merge is one-to-one, no missing values and no duplicates.
spec_tot_txbl_val_by_cnty = special_df.groupby("county_id")["txbl_val"].sum()
spec_tot_calculated_levy_by_cnty = special_df.groupby("county_id")[
    "calculated_levy"
].sum()
cnty_prop_tax_rates_tx_2025_df = cnty_prop_tax_rates_tx_2025_df.merge(
    spec_tot_txbl_val_by_cnty.rename("spec_txbl_val"), on="county_id",
    how="left"
).merge(
    spec_tot_calculated_levy_by_cnty.rename("spec_calculated_levy"),
    on="county_id", how="left"
)
# Replace NaN entries in spec_txbl_val and spec_calculated_levy with 0.
# Originally, 11 observations had NaN values in both variables.
cnty_prop_tax_rates_tx_2025_df[
    "spec_txbl_val"
] = cnty_prop_tax_rates_tx_2025_df["spec_txbl_val"].fillna(0)
cnty_prop_tax_rates_tx_2025_df[
    "spec_calculated_levy"
] = cnty_prop_tax_rates_tx_2025_df["spec_calculated_levy"].fillna(0)
print(
    "Merge of spec_tot_txbl_val_by_cnty and spec_tot_calculated_levy_by_cnty" +
    " into cnty_prop_tax_rates_tx_2025_df\n resulted in " +
    f"{len(spec_tot_txbl_val_by_cnty)} rows and " +
    f"{len(spec_tot_calculated_levy_by_cnty)} rows versus the " +
    f"{len(cnty_prop_tax_rates_tx_2025_df)} rows in the county DataFrame."
)
print(
    "The number of missing or 0 values in spec_txbl_val variable after merge" +
    " is " +
    f"{cnty_prop_tax_rates_tx_2025_df['spec_txbl_val'].isnull().sum()}."
)
print(
    "The number of missing or 0 values in spec_calculated_levy variable " +
    "after merge is " +
    f"{cnty_prop_tax_rates_tx_2025_df['spec_calculated_levy'].isnull().sum()}."
)
print(
    "The number of duplicate county_id values in " +
    "cnty_prop_tax_rates_tx_2025_df after merge with special variables is " +
    f"{cnty_prop_tax_rates_tx_2025_df['county_id'].duplicated().sum()}."
)

# # Create tot_txbls_val variable as the maximum of the cnty_txbl_val, schl_txbl_val,
# # city_txbl_val, and spec_txbl_val variables.
# cnty_prop_tax_rates_tx_2025_df["tot_txbl_val"] = cnty_prop_tax_rates_tx_2025_df[[
#     "cnty_txbl_val", "schl_txbl_val", "city_txbl_val", "spec_txbl_val"
# ]].max(axis=1)

# Create tot_calculated_levy variable as the sum of the cnty_calculated_levy,
# schl_calculated_levy, city_calculated_levy, and spec_calculated_levy
# variables.
cnty_prop_tax_rates_tx_2025_df["tot_calculated_levy"] = (
    cnty_prop_tax_rates_tx_2025_df["cnty_calculated_levy"] +
    cnty_prop_tax_rates_tx_2025_df["schl_calculated_levy"] +
    cnty_prop_tax_rates_tx_2025_df["city_calculated_levy"] +
    cnty_prop_tax_rates_tx_2025_df["spec_calculated_levy"]
)
# Create avg_eff_prop_tax_rate variable as tot_calculated_levy divided by
# cnty_txbl_val.
cnty_prop_tax_rates_tx_2025_df["avg_eff_prop_tax_rate"] = (
    cnty_prop_tax_rates_tx_2025_df["tot_calculated_levy"] /
    cnty_prop_tax_rates_tx_2025_df["cnty_txbl_val"]
)
cnty_prop_tax_rates_tx_2025_df["avg_eff_prop_tax_rate_pct"] = (
    cnty_prop_tax_rates_tx_2025_df["avg_eff_prop_tax_rate"] * 100
)

print(cnty_prop_tax_rates_tx_2025_df.dtypes)
print(cnty_prop_tax_rates_tx_2025_df.keys())
print(cnty_prop_tax_rates_tx_2025_df.head(10))
print(cnty_prop_tax_rates_tx_2025_df.describe())

# Save this DataFrame as a csv file cnty_prop_tax_rates_tx_2025.csv in the
# data/TX directory
cnty_prop_tax_rates_tx_2025_df.to_csv(
    os.path.join(data_dir, "cnty_prop_tax_rates_tx_2025.csv"), index=False
)

# %%
# Create dynamic data viz of Texas county average effective property tax rates

# County IDs are 1..254 in alphabetical order, and Texas FIPS codes are
# exactly the odd numbers in alphabetical order: FIPS = 48000 + 2*id - 1.
rate_by_fips = {
    f"{48000 + 2 * int(county) - 1}": r for county, r in
    cnty_prop_tax_rates_tx_2025_df.set_index("county_id")["avg_eff_prop_tax_rate"].items()
}

counties = gpd.read_file(os.path.join(data_dir,  "Texas_Counties.geojson"))
counties["rate_pct"] = counties["FIPS"].map(rate_by_fips) * 100

ax = counties.plot(
    column="rate_pct",
    cmap="YlOrRd",
    edgecolor="white",
    linewidth=0.3,
    legend=True,
    legend_kwds={"label": "Effective property tax rate (%)", "shrink": 0.6},
    figsize=(12, 11),
)
ax.set_axis_off()
ax.set_title(
    "Texas county property tax rates, 2025\n"
    "(all overlapping unit levies ÷ county taxable value)"
)

plt.savefig(
    os.path.join(images_dir, "tx_county_rates.png"),
    dpi=150, bbox_inches="tight"
)
print("Wrote images/TX/tx_county_rates.png")

for county_id, r in sorted(
    cnty_prop_tax_rates_tx_2025_df.set_index("county_id")[
        "avg_eff_prop_tax_rate"
    ].items(), key=lambda kv: -kv[1]
)[:5]:
    print(f"  highest: county id {county_id}  {r:.2%}")

# %%
