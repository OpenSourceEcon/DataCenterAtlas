"""
Code for replicating analyses for Texas (TX) in DataCenterAtlas.org
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
data_dir = os.path.join(proj_dir, "data", "TX")
rates_path = os.path.join(data_dir, "2025-total-rates-levies.xlsx")

# %%
# Read in the data/TX/2025-total-rates-levies.xlsx file as a pandas DataFrame
# rates_tx_2025_df.
rates_tx_2025_df = pd.read_excel(
    rates_path, header=2,
    names=["tax_unit_name", "tax_unit_id", "prop_tax_rate"]
)
# Sort rates_tx_2025_df by tax_unit_id ascending
rates_tx_2025_df = rates_tx_2025_df.sort_values(by="tax_unit_id")
# Fix typos
rates_tx_2025_df.loc[
    rates_tx_2025_df["tax_unit_id"] == "055-000-00", "tax_unit_name"
] = "Culberson"
rates_tx_2025_df.loc[
    rates_tx_2025_df["tax_unit_id"] == "062-000-00", "tax_unit_name"
] = "DeWitt"
rates_tx_2025_df.loc[
    rates_tx_2025_df["tax_unit_id"] == "064-000-00", "tax_unit_name"
] = "Dimmitt"
rates_tx_2025_df.loc[
    rates_tx_2025_df["tax_unit_id"] == "064-201-11", "tax_unit_name"
] = "Dimmitt County Regional Hospital District"


# %%
# Create dictionary of Texas county names as strings as keys and the 3-digit
# county code as strings from the website
# https://comptroller.texas.gov/taxes/property-tax/county-directory/
# in the "Select your county below:" section.
tx_county_code_dict = {
    "Anderson": "001",
    "Andrews": "002",
    "Angelina": "003",
    "Aransas": "004",
    "Archer": "005",
    "Armstrong": "006",
    "Atascosa": "007",
    "Austin": "008",
    "Bailey": "009",
    "Bandera": "010",
    "Bastrop": "011",
    "Baylor": "012",
    "Bee": "013",
    "Bell": "014",
    "Bexar": "015",
    "Blanco": "016",
    "Borden": "017",
    "Bosque": "018",
    "Bowie": "019",
    "Brazoria": "020",
    "Brazos": "021",
    "Brewster": "022",
    "Briscoe": "023",
    "Brooks": "024",
    "Brown": "025",
    "Burleson": "026",
    "Burnet": "027",
    "Caldwell": "028",
    "Calhoun": "029",
    "Callahan": "030",
    "Cameron": "031",
    "Camp": "032",
    "Carson": "033",
    "Cass": "034",
    "Castro": "035",
    "Chambers": "036",
    "Cherokee": "037",
    "Childress": "038",
    "Clay": "039",
    "Cochran": "040",
    "Coke": "041",
    "Coleman": "042",
    "Collin": "043",
    "Collingsworth": "044",
    "Colorado": "045",
    "Comal": "046",
    "Comanche": "047",
    "Concho": "048",
    "Cooke": "049",
    "Coryell": "050",
    "Cottle": "051",
    "Crane": "052",
    "Crockett": "053",
    "Crosby": "054",
    "Culberson": "055",
    "Dallam": "056",
    "Dallas": "057",
    "Dawson": "058",
    "Deaf Smith": "059",
    "Delta": "060",
    "Denton": "061",
    "DeWitt": "062",
    "Dickens": "063",
    "Dimmitt": "064",
    "Donley": "065",
    "Duval": "066",
    "Eastland": "067",
    "Ector": "068",
    "Edwards": "069",
    "Ellis": "070",
    "El Paso": "071",
    "Erath": "072",
    "Falls": "073",
    "Fannin": "074",
    "Fayette": "075",
    "Fisher": "076",
    "Floyd": "077",
    "Foard": "078",
    "Fort Bend": "079",
    "Franklin": "080",
    "Freestone": "081",
    "Frio": "082",
    "Gaines": "083",
    "Galveston": "084",
    "Garza": "085",
    "Gillespie": "086",
    "Glasscock": "087",
    "Goliad": "088",
    "Gonzales": "089",
    "Gray": "090",
    "Grayson": "091",
    "Gregg": "092",
    "Grimes": "093",
    "Guadalupe": "094",
    "Hale": "095",
    "Hall": "096",
    "Hamilton": "097",
    "Hansford": "098",
    "Hardeman": "099",
    "Hardin": "100",
    "Harris": "101",
    "Harrison": "102",
    "Hartley": "103",
    "Haskell": "104",
    "Hays": "105",
    "Hemphill": "106",
    "Henderson": "107",
    "Hidalgo": "108",
    "Hill": "109",
    "Hockley": "110",
    "Hood": "111",
    "Hopkins": "112",
    "Houston": "113",
    "Howard": "114",
    "Hudspeth": "115",
    "Hunt": "116",
    "Hutchinson": "117",
    "Irion": "118",
    "Jack": "119",
    "Jackson": "120",
    "Jasper": "121",
    "Jeff Davis": "122",
    "Jefferson": "123",
    "Jim Hogg": "124",
    "Jim Wells": "125",
    "Johnson": "126",
    "Jones": "127",
    "Karnes": "128",
    "Kaufman": "129",
    "Kendall": "130",
    "Kenedy": "131",
    "Kent": "132",
    "Kerr": "133",
    "Kimble": "134",
    "King": "135",
    "Kinney": "136",
    "Kleberg": "137",
    "Knox": "138",
    "Lamar": "139",
    "Lamb": "140",
    "Lampasas": "141",
    "La Salle": "142",
    "Lavaca": "143",
    "Lee": "144",
    "Leon": "145",
    "Liberty": "146",
    "Limestone": "147",
    "Lipscomb": "148",
    "Live Oak": "149",
    "Llano": "150",
    "Loving": "151",
    "Lubbock": "152",
    "Lynn": "153",
    "Madison": "154",
    "Marion": "155",
    "Martin": "156",
    "Mason": "157",
    "Matagorda": "158",
    "Maverick": "159",
    "McCulloch": "160",
    "McLennan": "161",
    "McMullen": "162",
    "Medina": "163",
    "Menard": "164",
    "Midland": "165",
    "Milam": "166",
    "Mills": "167",
    "Mitchell": "168",
    "Montague": "169",
    "Montgomery": "170",
    "Moore": "171",
    "Morris": "172",
    "Motley": "173",
    "Nacogdoches": "174",
    "Navarro": "175",
    "Newton": "176",
    "Nolan": "177",
    "Nueces": "178",
    "Ochiltree": "179",
    "Oldham": "180",
    "Orange": "181",
    "Palo Pinto": "182",
    "Panola": "183",
    "Parker": "184",
    "Parmer": "185",
    "Pecos": "186",
    "Polk": "187",
    "Potter": "188",
    "Presidio": "189",
    "Rains": "190",
    "Randall": "191",
    "Reagan": "192",
    "Real": "193",
    "Red River": "194",
    "Reeves": "195",
    "Refugio": "196",
    "Roberts": "197",
    "Robertson": "198",
    "Rockwall": "199",
    "Runnels": "200",
    "Rusk": "201",
    "Sabine": "202",
    "San Augustine": "203",
    "San Jacinto": "204",
    "San Patricio": "205",
    "San Saba": "206",
    "Schleicher": "207",
    "Scurry": "208",
    "Shackelford": "209",
    "Shelby": "210",
    "Sherman": "211",
    "Smith": "212",
    "Somervell": "213",
    "Starr": "214",
    "Stephens": "215",
    "Sterling": "216",
    "Stonewall": "217",
    "Sutton": "218",
    "Swisher": "219",
    "Tarrant": "220",
    "Taylor": "221",
    "Terrell": "222",
    "Terry": "223",
    "Throckmorton": "224",
    "Titus": "225",
    "Tom Green": "226",
    "Travis": "227",
    "Trinity": "228",
    "Tyler": "229",
    "Upshur": "230",
    "Upton": "231",
    "Uvalde": "232",
    "Val Verde": "233",
    "Van Zandt": "234",
    "Victoria": "235",
    "Walker": "236",
    "Waller": "237",
    "Ward": "238",
    "Washington": "239",
    "Webb": "240",
    "Wharton": "241",
    "Wheeler": "242",
    "Wichita": "243",
    "Wilbarger": "244",
    "Willacy": "245",
    "Williamson": "246",
    "Wilson": "247",
    "Winkler": "248",
    "Wise": "249",
    "Wood": "250",
    "Yoakum": "251",
    "Young": "252",
    "Zapata": "253",
    "Zavala": "254",
}

# %%
# Create two new variables in rates_tx_2025_df called cnty_name and cnty_code
# that is the county name and county code from the dictionary
# tx_county_code_dict that corresponds to the first three digits of the
# tax_unit_id in rates_tx_2025_df.
rates_tx_2025_df["cnty_code"] = rates_tx_2025_df[
    "tax_unit_id"
].astype(str).str[:3]
rates_tx_2025_df["cnty_name"] = rates_tx_2025_df["cnty_code"].map(
    {v: k for k, v in tx_county_code_dict.items()}
)
print(rates_tx_2025_df.head(20))

# %%
# Run the big loop
# Create a new empty DataFrame rates_tx_2025_units_df that has the following
# four variables: tax_area (string), cnty_code (string), cnty_name (string),
# tot_prop_tax_rate (float).
rates_tx_2025_units_df = pd.DataFrame(
    columns=["tax_area", "cnty_code", "cnty_name", "tot_prop_tax_rate"]
).astype(
    {
        "tax_area": str,
        "cnty_code": str,
        "cnty_name": str,
        "tot_prop_tax_rate": float
    }
)
print(rates_tx_2025_units_df.dtypes)
# Loop through each county in rates_tx_2025_df
for cnty_code in rates_tx_2025_df["cnty_code"].unique():
    # Create a sample of the DataFrame that includes all the rows for that
    # county
    cnty_sample_df = rates_tx_2025_df[
        rates_tx_2025_df["cnty_code"] == cnty_code
    ]
    # If the size of the sample is zero, report an error that the county code
    # is not found in the data
    if cnty_sample_df.shape[0] == 0:
        print(f"Error: County code {cnty_code} not found in data.")
    # If the size of the sample is 1, report the values of each variable in the
    # single row of the sample.
    if cnty_sample_df.shape[0] == 1:
        print(f"County code {cnty_code} has only one row in the data.")
        print(cnty_sample_df.iloc[0])
    # Test if the last six digits of the first row of the tax_unit_id variable in the sample are "000-00".
    if cnty_sample_df.iloc[0]["tax_unit_id"][-6:] != "000-00":
        print(
            f"Error: County code {cnty_code} does not have a first row with " +
            "tax_unit_id ending in 000-00."
        )
    # Test if the tax_unit_name variable in the first row of the sample is the
    # same as the cnty_name variable in that row.
    if cnty_sample_df.iloc[0]["tax_unit_name"] != cnty_sample_df.iloc[0][
        "cnty_name"
    ]:
        print(
            f"Error: County code {cnty_code} does not have a first row with " +
            "tax_unit_name that matches the cnty_name variable in that row."
        )
        print(cnty_sample_df.iloc[0])
    obs_name_list = []
    for i in range(cnty_sample_df.shape[0]):
        # If the last six digits of tax_unit_id variable in the i-th row of the
        # sample are "000-00", and another tax_unit_name in the sample equals
        # the tax_unit_name variable in the ith row, then set the first_word
        # variable equal to the first word plus "UnInc".
        if (
            (cnty_sample_df.iloc[i]["tax_unit_id"][-6:] == "000-00") and
            (
                cnty_sample_df['tax_unit_name'].eq(
                    cnty_sample_df.iloc[i]["tax_unit_name"]
                ).sum() > 1
            )
        ):
            cnty_code = cnty_sample_df.iloc[i]["cnty_code"]
            print(
                f"Number of first_word matches for county {cnty_code}:",
                cnty_sample_df['tax_unit_name'].eq(
                    cnty_sample_df.iloc[i]["tax_unit_name"]
                ).sum()
            )
            first_word = (
                cnty_sample_df.iloc[i]["tax_unit_name"].split()[0] + " UnInc"
            )
            obs_name_list.append(first_word)
            tot_prop_tax_rate = cnty_sample_df.iloc[i][
                "prop_tax_rate"
            ]
            # Append a new row to rates_tx_2025_units_df with the tax_area
            # variable equal to the first word, the cnty_code variable, the
            # cnty_name variable, and the tot_prop_tax_rate variable.
            rates_tx_2025_units_df = pd.concat(
                [
                    rates_tx_2025_units_df,
                    pd.DataFrame([{
                        "tax_area": first_word,
                        "cnty_code": cnty_sample_df.iloc[i]["cnty_code"],
                        "cnty_name": cnty_sample_df.iloc[i]["cnty_name"],
                        "tot_prop_tax_rate": tot_prop_tax_rate,
                    }]),
                ],
                ignore_index=True,
            )
            print(
                f"Total property tax rate for area {first_word} in county " +
                f"{cnty_code} {cnty_sample_df.iloc[i]['cnty_name']} is " +
                f"{tot_prop_tax_rate}."
            )
        elif (
            (cnty_sample_df.iloc[i]["tax_unit_id"][-6:] == "000-00") and
            (
                cnty_sample_df['tax_unit_name'].eq(
                    cnty_sample_df.iloc[i]["tax_unit_name"]
                ).sum() == 1
            )
        ):
            first_word_init = cnty_sample_df.iloc[i][
                "tax_unit_name"
            ].split()[0]
            tot_prop_tax_rate = cnty_sample_df[
                cnty_sample_df["tax_unit_name"].str.startswith(first_word_init)
            ]["prop_tax_rate"].sum()
            first_word = first_word_init + " UnInc"
            obs_name_list.append(first_word)
            # Append a new row to rates_tx_2025_units_df with the tax_area
            # variable equal to the first word, the cnty_code variable, the
            # cnty_name variable, and the tot_prop_tax_rate variable.
            rates_tx_2025_units_df = pd.concat(
                [
                    rates_tx_2025_units_df,
                    pd.DataFrame([{
                        "tax_area": first_word,
                        "cnty_code": cnty_sample_df.iloc[i]["cnty_code"],
                        "cnty_name": cnty_sample_df.iloc[i]["cnty_name"],
                        "tot_prop_tax_rate": tot_prop_tax_rate,
                    }]),
                ],
                ignore_index=True,
            )
            print(
                f"Total property tax rate for area {first_word} in county " +
                f"{cnty_code} {cnty_sample_df.iloc[i]['cnty_name']} is " +
                f"{tot_prop_tax_rate}."
            )
        # else:
        #     if cnty_sample_df.iloc[i]["tax_unit_name"] == "Archer City":
        #         first_word = "Archer City"
        #     else:
        #         first_word = cnty_sample_df.iloc[i]["tax_unit_name"].split()[0]
        #     if first_word not in obs_name_list:
        #         obs_name_list.append(first_word)
        #         tot_prop_tax_rate = (
        #             cnty_sample_df[
        #                 cnty_sample_df[
        #                     "tax_unit_name"
        #                 ].str.startswith(first_word) &
        #                 (
        #                     cnty_sample_df[
        #                         "tax_unit_name"
        #                     ] != first_word + " UnInc"
        #                 )
        #             ]["prop_tax_rate"].sum() +
        #             cnty_sample_df.iloc[0]["prop_tax_rate"]
        #         )
        #         # Append a new row to rates_tx_2025_units_df with the tax_area
        #         # variable equal to the first word, the cnty_code variable, the
        #         # cnty_name variable, and the tot_prop_tax_rate variable.
        #         rates_tx_2025_units_df = pd.concat(
        #             [
        #                 rates_tx_2025_units_df,
        #                 pd.DataFrame([{
        #                     "tax_area": first_word,
        #                     "cnty_code": cnty_sample_df.iloc[i]["cnty_code"],
        #                     "cnty_name": cnty_sample_df.iloc[i]["cnty_name"],
        #                     "tot_prop_tax_rate": tot_prop_tax_rate,
        #                 }]),
        #             ],
        #             ignore_index=True,
        #         )
        #         print(
        #             f"Total property tax rate for area {first_word} in " +
        #             f"county {cnty_code} " +
        #             f"{cnty_sample_df.iloc[i]['cnty_name']} is " +
        #             f"{tot_prop_tax_rate}."
        #         )

# %%
# Print the descriptive statistics for rates_tx_2025_units_df.
print(rates_tx_2025_units_df.describe())

# %%
# Save and List the rows of rates_tx_2025_units_df where the tot_prop_tax_rate variable
# is greater than 3.0.
big_rates = rates_tx_2025_units_df[
    rates_tx_2025_units_df["tot_prop_tax_rate"] > 3.0
]
big_rates.to_csv(
    os.path.join(data_dir, "big_prop_tax_rates_tx_2025.csv"), index=False
)
print(big_rates)

# %%
# [THE CODE ON THE NEXT 33 LINES AUGMENTS THE rates_ut_2025.csv FILE AND
# CREATES THE avg_proptax_rate_by_cnty_ut_2025.csv file.]
# Load data/rates_ut_2025.csv as pandas DataFrame rates_ut_2025_df and create
# a new variable (rate_cnty_avg) that is the average property tax rate by
# county (cnty_name) using groupby. The data start on row 5 (python index 4)
# and the variable names are in that row. The data end in row `364 (python
# index 1363).
rates_ut_2025_df = pd.read_csv(rates_path, skiprows=4, nrows=1360)
rates_ut_2025_df["rate_cnty_avg"] = (
    rates_ut_2025_df.groupby("cnty_name")["rate_final"].transform("mean")
)
# Save data from rates_ut_2025_df with new variable rate_cnty_avg to the same
# rows in the original rates_ut_2025.csv, preserving the header top 4 rows, but
# replacing the original data with this new data. The weighting here is equal
# across all rows. This would be better if we weighted by tax revenue in each
# tax area (row).
with open(rates_path, "r") as f:
    header_rows = [next(f) for _ in range(4)]
with open(rates_path, "w") as f:
    f.writelines(header_rows)
rates_ut_2025_df.to_csv(rates_path, index=False, mode="a", header=True)

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
