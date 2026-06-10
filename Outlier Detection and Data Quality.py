# %%
import pandas as pd
import glob
import os

# %%
os.getcwd()

# %%
sold_residential_feature_engineered = pd.read_csv('sold_residential_feature_engineered.csv', low_memory=False)

# %%
sold_residential_feature_engineered

# %%
numeric_cols = ['ClosePrice', 'LivingArea', 'DaysOnMarket']

for col in numeric_cols:
    Q1 = sold_residential_feature_engineered[col].quantile(0.25)
    Q3 = sold_residential_feature_engineered[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    
    sold_residential_feature_engineered[f'{col}_outlier_flag'] = ((sold_residential_feature_engineered[col] < lower) | (sold_residential_feature_engineered[col] > upper))
    
no_outliers = sold_residential_feature_engineered[
    (~sold_residential_feature_engineered['ClosePrice_outlier_flag']) &
    (~sold_residential_feature_engineered['LivingArea_outlier_flag']) &
    (~sold_residential_feature_engineered['DaysOnMarket_outlier_flag'])
]

# %%
print('Dataset size BEFORE filtering:', len(sold_residential_feature_engineered))
print('Dataset size AFTER filtering:', len(no_outliers))

for col in numeric_cols:
    print(f'\n{col}:')
    print(f'Median BEFORE filtering {col}:', sold_residential_feature_engineered[col].median())
    print(f'Median AFTER filtering {col}:', no_outliers[col].median())

# %%
sold_residential_feature_engineered.to_csv('sold_residential_flagged_outliers.csv', index=False)
no_outliers.to_csv('sold_residential_no_outliers.csv', index=False)


