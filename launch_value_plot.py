import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_performance = pd.read_csv('dataset1cleaned.csv')
df_specs = pd.read_csv('dataset2_cleanedtoneeded.csv')

df_performance['price_clean'] = pd.to_numeric(
    df_performance['price_usd'].astype(str).str.replace('$', '').str.replace(',', ''),
    errors='coerce'
)

def normalize_name(name):
    name = str(name).lower()
    junk_words = ['radeon', 'geforce', 'gtx', 'rtx', 'amd', 'nvidia', 'series', 'edition']
    for word in junk_words:
        name = name.replace(word, '')
    return ''.join(char for char in name if char.isalnum())

df_performance['match_key'] = df_performance['video_card_name'].apply(normalize_name)
df_specs['match_key'] = df_specs['Model'].apply(normalize_name)

merged_df = pd.merge(
    df_specs, 
    df_performance[['match_key', 'pasmark_gd3_mark', 'price_clean']], 
    on='match_key', 
    how='inner'
)

merged_df['Value_Score'] = merged_df['pasmark_gd3_mark'] / merged_df['MSRP']

merged_df['Price_Tier'] = (merged_df['MSRP'] / 500).round() * 500

plt.figure(figsize=(12, 8))

plot = sns.scatterplot(
    data=merged_df,
    x='Year Released',
    y='Value_Score',
    hue='Price_Tier',       
    size='Price_Tier',      
    sizes=(50, 400),  
    palette='viridis',
    legend='full'
)

sns.move_legend(plot, "upper left", bbox_to_anchor=(1, 1), title='MSRP ($)', frameon=False)

plt.text(
    x=2014.2, y=3,        
    s="Titan Z ($3,000)", 
    color='black',
    weight='bold'
)

plt.tight_layout() 

plt.title('GPU Value: Performance per Dollar at Launch', fontsize=16)
plt.ylabel('Value (PassMark Points per $1)', fontsize=12)
plt.xlabel('Year Released', fontsize=12)
plt.grid(True, alpha=0.3)

plt.title('GPU Value: Performance per Dollar at Launch')
plt.ylabel('Value (PassMark Points per $1)')
plt.xlabel('Year Released')
plt.grid(True, alpha=0.3)

plt.show() 