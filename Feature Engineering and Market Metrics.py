# %%
import pandas as pd
import glob
import os

# %%
os.getcwd()

# %%
sold_residential_cleaned = pd.read_csv('sold_residential_cleaned.csv', low_memory=False)

# %%
sold_residential_cleaned

# %%
date_cols = ['CloseDate', 'PurchaseContractDate', 'ListingContractDate', 'ContractStatusChangeDate']
for col in date_cols:
    sold_residential_cleaned[col] = pd.to_datetime(sold_residential_cleaned[col], errors='coerce')


numeric_cols = ['ClosePrice', 
                'ListPrice', 
                'OriginalListPrice', 
                'LivingArea', 
                'LotSizeAcres', 
                'BedroomsTotal', 
                'BathroomsTotalInteger', 
                'DaysOnMarket', 
                'YearBuilt']
for col in numeric_cols:
    sold_residential_cleaned[col] = pd.to_numeric(sold_residential_cleaned[col], errors='coerce')

# %%
sold_residential_cleaned['price_ratio'] = sold_residential_cleaned['ClosePrice'] / sold_residential_cleaned['OriginalListPrice']

sold_residential_cleaned['price_per_sq_ft'] = sold_residential_cleaned['ClosePrice'] / sold_residential_cleaned['LivingArea']

sold_residential_cleaned['year'] = sold_residential_cleaned['CloseDate'].dt.year
sold_residential_cleaned['month'] = sold_residential_cleaned['CloseDate'].dt.month
sold_residential_cleaned['yrmo'] = sold_residential_cleaned['CloseDate'].dt.to_period('M')

sold_residential_cleaned['close_to_original_list_ratio'] = sold_residential_cleaned['ClosePrice'] / sold_residential_cleaned['OriginalListPrice']

sold_residential_cleaned['listing_to_contract_days'] = (sold_residential_cleaned['PurchaseContractDate'] - sold_residential_cleaned['ListingContractDate']).dt.days

sold_residential_cleaned['contract_to_close_days'] = (sold_residential_cleaned['CloseDate'] - sold_residential_cleaned['PurchaseContractDate']).dt.days

# %%
sold_residential_cleaned[['price_ratio', 'price_per_sq_ft', 'year', 'month', 'yrmo', 'close_to_original_list_ratio', 'listing_to_contract_days', 'contract_to_close_days']]

# %%
sold_residential_cleaned.groupby(['PropertyType', 'PropertySubType'])[
    ['ClosePrice', 'DaysOnMarket', 'LivingArea', 'price_per_sq_ft', 'price_ratio']].mean()

# %%
sold_residential_cleaned.groupby(['CountyOrParish', 'MLSAreaMajor'])[
    ['ClosePrice', 'DaysOnMarket', 'LivingArea', 'price_per_sq_ft', 'price_ratio']].mean()

# %%
sold_residential_cleaned.groupby(['ListOfficeName', 'BuyerOfficeName'])[
    ['ClosePrice', 'DaysOnMarket', 'LivingArea', 'price_per_sq_ft', 'price_ratio']].mean()

# %%
sold_residential_cleaned.to_csv('sold_residential_feature_engineered.csv', index=False)


