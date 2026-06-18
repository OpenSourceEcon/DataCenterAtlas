# Georgia data
Georgia has the second most number of counties at 159, trailing only Texas which has 254 counties.

Georgia property taxes are county-, municipality-, and special-district-based (no state property tax). The taxes are specified in mill rates or dollar of tax liability for $1,000 of taxable assessed value. The  See the Georgia Department of Revenue "[Property Tax Millage Rates](https://dor.georgia.gov/local-government-services/digest-compliance/property-tax-millage-rates)" page. All land, buildings, and business personal property (e.g., servers, networking equipment, cooling systems) are assessed at 40% of fair market value, and the business personal property is depreciated annually at specified schedules.

The University of Georgia Institute of Government found that "local jurisdictions may offer incentives to encourage data centers to locate in a specific county or city." See Georgia Department of Audits and Accounts, "[Georgia Data Center Sales & Use Tax Exemption: DOAA summary of report prepared by the University of Georgia’s Carl Vinson Institute of Government (Institute)](https://www.audits2.ga.gov/reports/summaries/georgia-data-center-sales-use-tax-exemption)," (Dec. 24, 2025).

Most residences in Georgia can qualify for and receive the homestead exemption, which is a $2,000 deduction from the assessed taxable value of the property. Residents over the age of 65 can get a $4,000 deduction from their assessed taxable value. There are some other smaller exemptions for residents under the homestead exemption. See Georgia Department of Revenue's "[Property Tax Homestead Exemptions](https://dor.georgia.gov/property-tax-homestead-exemptions)" page, accessed June 17, 2026. We estimate that this reduces residential property assessed taxable values to 39% of fair market value, a one-percentage-point decrease from the 40% ratio without the exemption.

Let $L_{i,j}$ be the property tax liability for a particular property $i$ in county $j, and let $FMV_{i,j}$ be the fair market value of that property. The effective property tax rate $\tau_{eff,i,j}$ for a particular property $i$ in county $j$ is the following equation:

$$
\tau_{eff,i,j} = \frac{L_{i,j}}{FMV_{i,j}} \quad\text{for all}\quad i,j
$$

The effective property tax rate might differ from the statutory tax rate for a number of reasons, many of which are present in Georgia property tax policy.
- Different property tax juridictions add taxes on top of each other.
- Property tax rates vary within counties and across counties.
- Different taxable assessed values might apply to different industries and to residential versus commercial properties.
- Business tangible personal property might have different exemptions based on industry.
- Business properties might be assessed more aggressively and more often than residential properties.

Given these issues, the most reliable way to calculate an average effective property tax rate $\tau_{avg,eff,j}$ with in a county $j$ is usually to add up all the property tax levies ($\sum_i L_{i,j}$) and add up all the fair market values of the properties ($\sum_i FMV_{i,j}$).

$$
\tau_{avg,eff,j} = \frac{\sum_i L_{i,j}}{\sum_i FMV_{i,j}} \quad\text{for all}\quad j
$$

We calculate the total taxes levied by county from the Georgia Department of Revenue "[`2025 Summary of Ad Valorem Taxes Levied Report.pdf`](https://dor.georgia.gov/document/document/2025-summary-ad-valorem-taxes-levied-reportpdf/download)", which we have also stored as [`2025 Summary of Ad Valorem Taxes Levied Report.pdf`](https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/data/GA/2025%20Summary%20of%20Ad%20Valorem%20Taxes%20Levied%20Report.pdf) in this directory of the open source GitHub repository for the DataCenterAtlas.org web tool. We extracted the data from this PDF table using ChatGPT (see [this thread](https://chatgpt.com/share/6a32ee08-9950-83ea-9bff-2a3e7a19ab2a)), saving the output as [`/data/GA/county_tot_levies_ga_2025.csv`](https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/data/GA/county_tot_levies_ga_2025.csv). For each Georgia county, these are our values for the numerator on the right-hand-side of the average effective property tax rate by county $\tau_{avg,eff,j}$ equation.

The Georgia Departmet of Revenue also publishes a detailed spreadsheet of assessed taxable property values each year, "[2025 Digest.xls](https://dor.georgia.gov/media/34621/download)", accessed July 16, 2026, on their "[Digest Consolidated Summaries](https://dor.georgia.gov/local-government-services/digest-compliance/digest-consolidated-summaries)" web page. We have also posted this file [`Digest Export 4.6.26.xlsx`](https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/data/GA/Digest%20Export%204.6.26.xlsx) in this folder the open source GitHub repository for the DataCenterAtlas.org web tool. We use the county, "District Code = 0", "TotalAssessed Value-M&O" value as our taxable assessed value. However, this is not yet the value we need for the denominator on the right-hand-side of the average effective property tax rate by county $\tau_{avg,eff,j}$ equation.

Because Georgia assesses taxable value for both commercial and residential properties at 40% of fair market value, we have to adjust the total taxable assessed values $TAV_j$ for county $j$ in order to get total county assessed fair market values. Most residential properties in Georgia have the homestead exemption, which is a $2,000 deduction from taxable assessed values. We assume this is an extra 1 percentage point reduction of taxable assessed values, from 40\% to 39\%. Because residential properties are about 60\% of all assessed properties in Georgia (commercial properties are 40\%), we adjust the total taxable assessed values by county $TAV_j$ back up to total fair market value $FMV_j$ for county $j$ by the following equation.

$$
FMV_j = 0.6\left(\frac{TAV_j}{0.39}\right) + 0.4\left(\frac{TAV_j}{0.4}\right)
$$

With those total fair market values by county $FMV_j$ and the total tax levies $\sum_i L_i$ from above, we calculate the average effective property tax rate in each county $j$ using the equation for $\tau_{avg,eff,j}$.

The average effective property tax rate data from this computation is stored as [`/data/GA/cnty_prop_tax_rates_ga_2025.csv`](https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/data/GA/cnty_prop_tax_rates_ga_2025.csv) in the open source GitHub repository for the DataCenterAtlas.org web tool. All the code that used the source data above to calculate the average effective property tax rates by county in Georgia is available as [`/code/GA/ga_analyses.py`](https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/code/GA/ga_analyses.py).

## What we did not use
The Georgia Department of Revenue has a webpage on "[Property Tax Millage Rates](https://dor.georgia.gov/local-government-services/digest-compliance/property-tax-millage-rates)". This page describes the statutory property tax rates in Georgia and how they add up across county, municipality, and special district rates. The page has a PDF file of the "[2025 Georgia County Ad Valorem Tax Digest Millage Rates](https://dor.georgia.gov/document/document/2025-georgia-county-ad-valorem-tax-digest-millage-ratespdf/download)", which we have stored as [`2025 Georgia County Ad Valorem Tax Digest Millage Rates.pdf`](https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/data/GA/2025%20Georgia%20County%20Ad%20Valorem%20Tax%20Digest%20Millage%20Rates.pdf) in this directory of the open source GitHub repository for the DataCenterAtlas.org web tool.

We didn't use this file because it was hard to know which rates applied to which geographies. Some of the rates should be additively summed. Others should be averaged in order to calculate the county average millage rate. We also had no good way to weight the various interest rates. For this reason, we did not use the millage rates file to calculate the average effective property tax rate by county in Georgia.
