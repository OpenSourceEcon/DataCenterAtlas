# Georgia data
Georgia has the second most number of counties at 159, trailing only Texas which has 254 counties.

Georgia property taxes are county-, municipality-, and special-district-based (no state property tax). The taxes are specified in mill rates or dollar of tax liability for $1,000 of taxable assessed value. The  See the Georgia Department of Revenue "[Property Tax Millage Rates](https://dor.georgia.gov/local-government-services/digest-compliance/property-tax-millage-rates)" page. All land, buildings, and business personal property (e.g., servers, networking equipment, cooling systems) are assessed at 40% of fair market value, and the business personal property is depreciated annually at specified schedules.

The University of Georgia Institute of Government found that "local jurisdictions may offer incentives to encourage data centers to locate in a specific county or city." See Georgia Department of Audits and Accounts, "[Georgia Data Center Sales & Use Tax Exemption: DOAA summary of report prepared by the University of Georgia’s Carl Vinson Institute of Government (Institute)](https://www.audits2.ga.gov/reports/summaries/georgia-data-center-sales-use-tax-exemption)," (Dec. 24, 2025).

Most residences in Georgia can qualify for and receive the homestead exemption, which is a $2,000 deduction from the assessed taxable value of the property. Residents over the age of 65 can get a $4,000 deduction from their assessed taxable value. There are some other smaller exemptions for residents under the homestead exemption. See Georgia Department of Revenue's "[Property Tax Homestead Exemptions](https://dor.georgia.gov/property-tax-homestead-exemptions)" page, accessed June 17, 2026. We estimate that this reduces residential property assessed taxable values to 39% of fair market value, a one-percentage-point decrease from the 40% ratio without the exemption.

Let $L_i$ be the property tax liability for a particular property $i$, and let $FMV_i$ be the fair market value of that property. The effective property tax rate $\tau_{eff,i}$ for a particular property $i$ is the following equation:

$$
\tau_{eff,i} = \frac{L_i}{FMV_i}
$$

given county is equal to... [TODO: the total property taxes levied divided by the fair market value]

We calculate the total taxes levied by county from the "[`2025 Summary of Ad Valorem Taxes Levied Report.pdf`](https://dor.georgia.gov/document/document/2025-summary-ad-valorem-taxes-levied-reportpdf/download)", which we have also stored as [`2025 Summary of Ad Valorem Taxes Levied Report.pdf`](https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/data/GA/2025%20Summary%20of%20Ad%20Valorem%20Taxes%20Levied%20Report.pdf) in this directory of the open source GitHub repository for the DataCenterAtlas.org web tool. We extracted the data from this PDF table using ChatGPT (see [this thread](https://chatgpt.com/share/6a32ee08-9950-83ea-9bff-2a3e7a19ab2a)), saving the output as [`/data/GA/county_tot_levies_ga_2025.csv`](https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/data/GA/county_tot_levies_ga_2025.csv).

[Define how we get the total assessed value by county]

[Define how we get the effective property tax rate by dividing by 0.40 and 0.39, respectively]

The average effective property tax rate data from this computation is stored as [`/data/GA/cnty_prop_tax_rates_ga_2025.csv`](https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/data/GA/cnty_prop_tax_rates_ga_2025.csv) in the open source GitHub repository for the DataCenterAtlas.org web tool. All the code that used the source data above to calculate the average effective property tax rates by county in Georgia is available as [`/code/GA/ga_analyses.py`](https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/code/GA/ga_analyses.py).

## What we did not use
The Georgia Department of Revenue has a webpage on "[Property Tax Millage Rates](https://dor.georgia.gov/local-government-services/digest-compliance/property-tax-millage-rates)". This page describes the statutory property tax rates in Georgia and how they add up across county, municipality, and special district rates. The page has a PDF file of the "[2025 Georgia County Ad Valorem Tax Digest Millage Rates](https://dor.georgia.gov/document/document/2025-georgia-county-ad-valorem-tax-digest-millage-ratespdf/download)", which we have stored as [`2025 Georgia County Ad Valorem Tax Digest Millage Rates.pdf`](https://github.com/OpenSourceEcon/DataCenterAtlas/blob/main/data/GA/2025%20Georgia%20County%20Ad%20Valorem%20Tax%20Digest%20Millage%20Rates.pdf) in this directory of the open source GitHub repository for the DataCenterAtlas.org web tool.

We didn't use this file because it was hard to know which rates applied to which geographies. Some of the rates should be additively summed. Others should be averaged in order to calculate the county average millage rate. We also had no good way to weight the various interest rates. For this reason, we did not use the millage rates file to calculate the average effective property tax rate by county in Georgia.
