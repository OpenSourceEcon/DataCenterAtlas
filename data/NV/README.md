# Nevada data
Navade has a 35% assessment ratio across all properties, including commercial and residential. As such, assessed value = 35% of taxable value. And taxable value is not equal to the fair market value. This makes it difficult to calculate Nevada's average effective property tax rates by county.

Nevada is a state that treats data centers differently than other commercial properties in terms of property taxation. Since 2015, Nevada has offered special tax abatements for qualifying data centers that meet investment and employment requirements. Eligible data centers can receive the following tax incentives.
- Up to 75% abatement of personal property taxes for 10 or 20 years. Business tangible personal property is often a large portion of a data center's value.
- Major sales and use tax reductions to a minimum of 2%
The requirements to receive the 10-year abatements are:
- Within 5 years employ 10 full-time employees who are Nevada residents.
- Pay at least 100% of the statewide average wage.
- Within 5 years invest at least $25 million in cumulative capital expenditures between the applicant and tenants.
The requirements to receive the 20-year abatements are:
- Within 5 years employ 50 full-time employees who are Nevada residents.
- Pay at least 100% of the statewide average wage.
- Within 5 years invest at least $100 million in cumulative capital expenditures between the applicant and tenants.
There are some other basic requirements for both lengths of abatement, like maintaining the business in Nevada for 10 years. See Nevada Governor's Office of Economic Development, "[Business Incentives](https://goed.nv.gov/incentives)" page, then the section on "Data Center Abatements". Looking at the business incentives page, Nevada has a lot of exemptions, abatements, and credits for businesses. They clearly are price differentiating the taxes on their businesses. This data center tax abatement program means that data centers will face a significantly lower effective property tax rate than other businesses because tangible personal property is such a large portion of their value.

Nevada also has a property tax abatement system that caps the growth in assessed valuations at:
- 3% annual assessment value growth per year for owner-occupied residential property
- Up to 8% annually fo rother property classes, including commercial property.
See Nevada Governor's Office of Economic Development, "[Tax Abatements Overview](https://goed.nv.gov/wp-content/uploads/2024/03/Tax-Abatements-Overview-MAR2024.pdf)," Mar. 2024.

Because of the different abatements available to Nevada data centers, other commercial industries, and residential properties, Nevada is a hard state for which to calculate average effective property tax rates by county. The Property Tax Explorer website has a [Nevada page](https://propertytaxexplorer.com/us/nevada) that lists effective property tax rates by county, which includes both commercial and residential properties. It looks like these Property Tax Explorer effective tax rates are the same ones that Tax Foundation uses in their [county property tax rates map](https://taxfoundation.org/data/all/state/property-taxes-by-state-county/). But in neither case can I see how they calculated these effective tax rates.

To calculate the average effective property tax rates on data centers by county, we use the State of Nevada, Department of Taxation, Division of Government Services, "[Local Government Finance Revenue Projections, Fiscal Year 2025-2026, Final](https://tax.nv.gov/wp-content/uploads/2025/03/Final-Revenue-Projections-FY25.26.pdf)," Mar. 15, 2025. The table on page A-1 gives the FY 2026 total property final assessed value including net proceeds projection by county. To get to the fair market values in each county we have to inflate those valuations by the 35% assessment ratio and by the average amount of exemptions across the state.

$$
FMV_i = ExempRatio_i\left(AssessValue_i / 0.35\right) \quad\text{for all}\quad i
$$

$FMV_i$ is the fair market value for county $i$, $ExempRatio_i$ is the ratio of total county-$i$ valuations before exemptions to total valuations after exemptions, and $AssessValue_i$ is the final assessed blue including net proceeeds projection. We calculate the $ExempRatio_i$ using the statewide total assessed valuation by property classes before examptions and after exemptions from the two tables on page 72 of the State of Nevada Department of Taxation "[Annual Report: Fiscal Year 2025 (2024-2025)](https://tax.nv.gov/wp-content/uploads/2026/01/FY25_AnnualReport_FINAL.pdf)", Jan. 2026. Our computed values of total property fair market value by county $FMV_i$ represents the denominator in our calculation of average effective property tax rates by county $i$.

$$
\tau_{avg,eff,i} = \frac{PropTaxRev_i}{FMV_i} \quad\text{for all}\quad i
$$

We use the table "Assessed Valuation by Counties after Exemptions" FY 2024-25 variable (p. 72) from the State of Nevada Department of Taxation "[Annual Report: Fiscal Year 2025 (2024-2025)](https://tax.nv.gov/wp-content/uploads/2026/01/FY25_AnnualReport_FINAL.pdf)", Jan. 2026, to get baseline after-exemption valuation totals for each county. Then we use the percent difference between the total row from the table "Assessed Valuation by Property Classes before Exemptions" versus the total row from the "Assessed Valuation by Counties after Exemptions" to get the average percent increase to get to fair market value. We increase the valuation totals by county from the "Assessed Valuation by Counties after Exemptions" by this percentage to get assessed valuation by county before exemption.



<!-- We used [ChatGPT](https://chatgpt.com/share/6a3abab6-93c0-83ea-a054-0d15d587030a) to convert Chart VIII "[2025 Average Property Tax Rates Based on Levied Amounts](https://tax.idaho.gov/wp-content/uploads/reports/EPB00129/EPB00129_12-04-2025.pdf)" to a `.csv` file, which we saved as [`/data/ID/EPB00129_12-04-2025.csv`](https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/data/ID/EPB00129_12-04-2025.csv) in the open source GitHub repository for the DataCenterAtlas.org web tool. Our code for extracting and calculating the average effective property tax rates by county in Idaho for 2025 is in the [`/code/ID/id_analyses.py`](https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/code/ID/id_analyses.py) file in the open source GitHub repository for the DataCenterAtlas.org web tool. The data for Idah average effective property tax rates by county for the year 2025 is saved as [`/data/ID/cnty_prop_tax_rates_id_2025.csv`](https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/data/ID/cnty_prop_tax_rates_id_2025.csv). -->
