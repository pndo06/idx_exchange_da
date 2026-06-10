# %%
import pandas as pd
import glob
import os

# %%
os.getcwd()

# %%
sold_residential = pd.read_csv('sold_residential.csv', low_memory=False)
listing_residential = pd.read_csv('listing_residential.csv', low_memory=False)

# %%
sold_residential

# %%
listing_residential

# %%
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=['observation_date'])
mortgage.columns = ['date', 'rate_30yr_fixed']

mortgage['year_month'] = mortgage['date'].dt.to_period('M')
mortgage_monthly = (
    mortgage.groupby('year_month')['rate_30yr_fixed'].mean().reset_index()
)

sold_residential['year_month'] = pd.to_datetime(sold_residential['CloseDate']).dt.to_period('M')

listing_residential['year_month'] = pd.to_datetime(listing_residential['ListingContractDate']).dt.to_period('M')

sold_with_rates = sold_residential.merge(mortgage_monthly, on='year_month', how='left')
listings_with_rates = listing_residential.merge(mortgage_monthly, on='year_month', how='left')

print(sold_with_rates['rate_30yr_fixed'].isnull().sum())
print(listings_with_rates['rate_30yr_fixed'].isnull().sum())

print(sold_with_rates[['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed']].head())

# %%
# Step 1 – Fetch the mortgage rate data from FRED
import pandas as pd
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=['observation_date'])
mortgage.columns = ['date', 'rate_30yr_fixed']
# Step 2 – Resample weekly rates to monthly averages
mortgage['year_month'] = mortgage['date'].dt.to_period('M')
mortgage_monthly = (
mortgage.groupby('year_month')['rate_30yr_fixed']
.mean()
.reset_index()
)
# Step 3 – Create a matching year_month key on the MLS datasets
# Sold dataset — key off CloseDate
sold_residential['year_month'] = pd.to_datetime(sold_residential['CloseDate']).dt.to_period('M')
# Listings dataset — key off ListingContractDate
listing_residential['year_month'] = pd.to_datetime(
listing_residential['ListingContractDate']
).dt.to_period('M')
# Step 4 – Merge
sold_with_rates = sold_residential.merge(mortgage_monthly, on='year_month', how='left')
listings_with_rates = listing_residential.merge(mortgage_monthly, on='year_month', how='left')
# Step 5 – Validate the merge
# Check for any unmatched rows (rate should not be null)
print(sold_with_rates['rate_30yr_fixed'].isnull().sum())
print(listings_with_rates['rate_30yr_fixed'].isnull().sum())
# Preview
print(
sold_with_rates[
['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed']
].head()
)


