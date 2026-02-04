import pandas as pd
import numpy as np

df = pd.read_json("dataset2.json", orient = 'index')
df = df.reset_index()
df = df.rename(columns={"index": "model"})
df['Full_Price'] = df['Release Price (USD)']
df['Full_Price'] = df['Full_Price'].fillna(df['MSRP (USD)'])
df['Full_Price'] = df['Full_Price'].astype(str)
df['Full_Price'] = df['Full_Price'].str.replace('$', '', regex=False)
df['Full_Price'] = pd.to_numeric(df['Full_Price'], errors='coerce')
df['Year'] = pd.to_datetime(df['Launch'], errors='coerce').dt.year
df_clean = df.dropna(subset=['Full_Price', 'Year']).copy()
df_clean = df_clean.replace(['nan', 'NaN', 'None', ''], np.nan)
df_clean = df_clean.replace(r'^\s*$', np.nan, regex=True)
df_clean['Year'] = df_clean['Year'].astype(int)
df_clean = df_clean.sort_values(by='Year')
priority_cols = [
    'Model', 
    'Model name', 
    'Model (Codename)',                       
    'Branding and Model Branding and Model.1', 
    'Branding and Model',                     
    'model',                                   
    'Code name'
]
existing_cols = [c for c in priority_cols if c in df_clean.columns]
df_clean['Final_Model'] = df_clean[existing_cols].bfill(axis=1).iloc[:, 0]
amd_cols = [c for c in df_clean.columns if "Model" in c and "Codename" in c]
intel_cols = [c for c in df_clean.columns if "Branding" in c]
priority_cols = ['Model', 'Model name'] + amd_cols + intel_cols + ['Code name', 'model']
existing_cols = [c for c in priority_cols if c in df_clean.columns]
df_clean['Final_Model'] = df_clean[existing_cols].bfill(axis=1).iloc[:, 0]
df_final = df_clean[['Final_Model', 'Full_Price', 'Year']].copy()
df_final.columns = ['Model', 'MSRP', 'Year Released']
df_final.to_csv('dataset2_cleanedtoneeded.csv', index=False)
