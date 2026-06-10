# %%
import pandas as pd
import glob
import os

# %%
os.getcwd()

# %%
sold_residential = pd.read_csv('sold_residential.csv', low_memory=False)
sold_residential

# %%
sold_missing_count = sold_residential.isna().sum()
missing_percent = (sold_missing_count / len(sold_residential)) * 100

missing_df = pd.DataFrame({
    'missing_percent': missing_percent
})

high_missing_cols = missing_df[missing_df['missing_percent'] > 90]

numeric_cols = ['ClosePrice', 'LivingArea', 'DaysOnMarket']
distribution_summary = sold_residential[numeric_cols].describe()
print(distribution_summary)


