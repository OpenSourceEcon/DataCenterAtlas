# /// script
# requires-python = ">=3.11"
# dependencies = ["openpyxl", "geopandas", "matplotlib"]
# ///
"""Texas county property tax rates from the Comptroller's 2025 Tax Rates
and Levies workbooks (https://comptroller.texas.gov/taxes/property-tax/rates/).

A county's taxing units (county, school districts, cities, special districts)
only partially overlap, so you can't simply add up their nominal rates.
Instead we compute the average effective rate actually paid in each county:

    rate = (sum of CALCULATED LEVY of every unit in the county)
           / (county taxable value)

This is the levy-weighted sum of each parcel's overlapping unit rates.
Texas appraises at 100% of market value, so the result is an effective rate.

Run:  uv run scripts/tx_county_rates.py
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import openpyxl

WORKBOOKS = [
    "data/TX/2025-county-rates-levies.xlsx",
    "data/TX/2025-school-district-rates-levies.xlsx",
    "data/TX/2025-city-rates-levies.xlsx",
    "data/TX/2025-special-district-rates-levies.xlsx",
]


def read_rows(path):
    """
    Yield each data row of a workbook as a {column name: value} dict.
    """
    sheet = openpyxl.load_workbook(path, read_only=True).active
    header = None
    for row in sheet.iter_rows(values_only=True):
        if row[0] == "CAD ID":  # the title rows above this differ per workbook
            header = row
        elif header and row[0] is not None:
            yield dict(zip(header, row))


def number(value):
    """
    Levy/value cells are mostly numeric but occasionally '$1,234.56' text.
    """
    if isinstance(value, str):
        value = value.replace("$", "").replace(",", "").strip() or 0
    return float(value or 0)


# --- The calculation -----------------------------------------------------

# 1. Sum every taxing unit's levy into its county (units that span several
#    counties appear once per county as SPLIT rows, so each county gets
#    exactly its share).
levy = {}  # county id "001".."254" -> total levy ($)
for path in WORKBOOKS:
    for row in read_rows(path):
        county = row["COUNTY ID"]
        levy[county] = levy.get(county, 0) + number(row["CALCULATED LEVY"])

# 2. Divide by each county's taxable value (from the county workbook).
rate = {}  # county id -> effective rate (decimal, e.g. 0.018 = 1.8%)
for row in read_rows(WORKBOOKS[0]):
    county = row["COUNTY ID"]
    taxable = number(row["TAXABLE VALUE FOR GENERAL/ROAD AND BRIDGE FUNDS"])
    rate[county] = levy[county] / taxable

# 3. County IDs are 1..254 in alphabetical order, and Texas FIPS codes are
#    exactly the odd numbers in alphabetical order: FIPS = 48000 + 2*id - 1.
rate_by_fips = {
    f"{48000 + 2 * int(county) - 1}": r for county, r in rate.items()
}

# --- The visualization ---------------------------------------------------

counties = gpd.read_file("data/TX/Texas_Counties.geojson")
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
ax.set_title("Texas county property tax rates, 2025\n"
             "(all overlapping unit levies ÷ county taxable value)")

plt.savefig("tx_county_rates.png", dpi=150, bbox_inches="tight")
print("Wrote tx_county_rates.png")

for county_id, r in sorted(rate.items(), key=lambda kv: -kv[1])[:5]:
    print(f"  highest: county id {county_id}  {r:.2%}")
