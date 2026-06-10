# %%
import pandas as pd
import glob
import os

# %%
os.getcwd()

# %%
sold_residential = pd.read_csv('sold_residential.csv', low_memory=False)

# %%
sold_residential

# %%
print('Sold residential BEFORE cleaning:', len(sold_residential))

# %%
sold_residential = sold_residential.copy()

# %%
date_cols = ['CloseDate', 'PurchaseContractDate', 'ListingContractDate', 'ContractStatusChangeDate']
for col in date_cols:
    sold_residential[col] = pd.to_datetime(sold_residential[col], errors='coerce')
    

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
    sold_residential[col] = pd.to_numeric(sold_residential[col], errors='coerce')


sold_residential = sold_residential[(sold_residential['ClosePrice'] > 0) &
                                    (sold_residential['LivingArea'] > 0) &
                                    (sold_residential['DaysOnMarket'] >= 0) &
                                    (sold_residential['BedroomsTotal'] >= 0) &
                                    (sold_residential['BathroomsTotalInteger'] >= 0)]


sold_residential['listing_after_close_flag'] = sold_residential['ListingContractDate'] > sold_residential['CloseDate']
sold_residential['purchase_after_close_flag'] = sold_residential['PurchaseContractDate'] > sold_residential['CloseDate']
sold_residential['negative_timeline_flag'] = ((sold_residential['ListingContractDate'] > sold_residential['PurchaseContractDate']) |
                                              (sold_residential['PurchaseContractDate'] > sold_residential['CloseDate']) | 
                                              (sold_residential['ListingContractDate'] > sold_residential['CloseDate']))

print('Listing after close:', sold_residential['listing_after_close_flag'].sum())
print('Purchase after close:', sold_residential['purchase_after_close_flag'].sum())
print('Negative timeline:', sold_residential['negative_timeline_flag'].sum())


sold_residential['missing_coordinates'] = sold_residential['Latitude'].isna() | sold_residential['Longitude'].isna()
sold_residential['sentinel_null_values'] = (sold_residential['Latitude'] == 0) | (sold_residential['Longitude'] == 0)
sold_residential['positive_longitude'] = sold_residential['Longitude'] > 0
sold_residential['out_of_state_coordinates'] = ((sold_residential['Latitude'] < 32) | 
                                               (sold_residential['Latitude'] > 42) | 
                                               (sold_residential['Longitude'] < -124) | 
                                               (sold_residential['Longitude'] > -114))


print()
print('Missing coordinates:', sold_residential['missing_coordinates'].sum())
print('Sentinel null values:', sold_residential['sentinel_null_values'].sum())
print('Positive longitude:', sold_residential['positive_longitude'].sum())
print('Out-of-state coordinates:', sold_residential['out_of_state_coordinates'].sum())

# %%
print('Sold residential AFTER cleaning:', len(sold_residential))

# %%
sold_residential.to_csv('sold_residential_cleaned.csv', index=False)


