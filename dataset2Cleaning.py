import pandas as pd

df = pd.read_json("dataset2.json", orient = 'index')
df = df.reset_index()
df = df.rename(columns={"index": "model"})
df['Full_Price'] = df['Release Price (USD)']
df['Full_Price'] = df['Full_Price'].fillna(df['MSRP (USD)'])
df['Full_Price'] = df['Full_Price'].astype(str)
df['Full_Price'] = df['Full_Price'].str.replace('$', '', regex=False)
df['Full_Price'] = pd.to_numeric(df['Full_Price'], errors='coerce')
df['Date'] = pd.to_datetime(df['Launch'], errors='coerce')
df['Year'] = df['Date'].dt.year
df_clean = df.dropna(subset=['Full_Price', 'Year'])
df_clean['Year'] = df_clean['Year'].astype(int)
df_clean = df_clean.sort_values(by='Year')
cols_to_keep = ['model', 'Year', 'Full_Price']
df_clean.to_csv('dataset2_cleaned.csv', index=False)
df_clean.to_excel('dataset2_cleaned.xlsx', index=False)
