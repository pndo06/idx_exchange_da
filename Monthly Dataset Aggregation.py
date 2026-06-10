# %%
import pandas as pd
import glob
import os

# %%
os.getcwd()

# %%
sold_files = glob.glob('CRMLSSold*.csv')

sold_dfs = []
for file in sold_files:
    df = pd.read_csv(file, encoding='latin1')
    sold_dfs.append(df)

sold_before_concat = sum(len(df) for df in sold_dfs)
print('Sold row count BEFORE concat:', sold_before_concat)
sold_df = pd.concat(sold_dfs, ignore_index=True)
print('Sold row count AFTER concat:', len(sold_df))


listing_files = glob.glob('CRMLSListing*.csv')

listing_dfs = []
for file in listing_files:
    df = pd.read_csv(file, encoding='latin1')
    listing_dfs.append(df)
    
listing_before_concat = sum(len(df) for df in listing_dfs)
print('Listing row count BEFORE concat:', listing_before_concat)
listing_df = pd.concat(listing_dfs, ignore_index=True)
print('Listing row count AFTER concat:', len(listing_df))


print('Sold BEFORE residential filter:', len(sold_df))
sold_residential = sold_df[sold_df['PropertyType'] == 'Residential'].copy()
print('Sold AFTER residential filter:', len(sold_residential))

print('Listing BEFORE residential filter:', len(listing_df))
listing_residential = listing_df[listing_df['PropertyType'] == 'Residential'].copy()
print('Listing AFTER residential filter:', len(listing_residential))

# %%
sold_residential.to_csv('sold_residential.csv', index=False)
listing_residential.to_csv('listing_residential.csv', index=False)


