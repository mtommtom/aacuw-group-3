import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import difflib
import os

base_path = r'C:\Users\peter\Coding\aacuw-group-3'
paths = {}

for root, dirs, files in os.walk(base_path):
    for f in files:
        if f == 'bitcoin.csv': paths['btc'] = os.path.join(root, f)
        if f == 'dataset1cleaned.csv': paths['perf'] = os.path.join(root, f)
        if f == 'dataset2_cleanedtoneeded.csv': paths['spec'] = os.path.join(root, f)

if 'btc' not in paths:
    if os.path.exists(os.path.join(base_path, 'cleaned datatsets', 'bitcoin.csv')):
        paths['btc'] = os.path.join(base_path, 'cleaned datatsets', 'bitcoin.csv')

df_performance = pd.read_csv(paths['perf'])
df_specs = pd.read_csv(paths['spec'])
df_btc = pd.read_csv(paths['btc'], delimiter=';')

df_btc['timeClose'] = pd.to_datetime(df_btc['timeClose'])
df_btc['Year'] = df_btc['timeClose'].dt.year
btc_yearly = df_btc.groupby('Year')['close'].mean().reset_index()

missing_data = [
    {'Model': 'GeForce GTX 980 Ti', 'MSRP': 649, 'Year Released': 2015},
    {'Model': 'GeForce GTX 1060', 'MSRP': 249, 'Year Released': 2016},
    {'Model': 'GeForce GTX 1070', 'MSRP': 379, 'Year Released': 2016},
    {'Model': 'GeForce GTX 1080', 'MSRP': 599, 'Year Released': 2016},
    {'Model': 'GeForce GTX 1080 Ti', 'MSRP': 699, 'Year Released': 2017},
    {'Model': 'GeForce RTX 2060', 'MSRP': 349, 'Year Released': 2019},
    {'Model': 'GeForce RTX 2070', 'MSRP': 499, 'Year Released': 2018},
    {'Model': 'GeForce RTX 2080', 'MSRP': 699, 'Year Released': 2018},
    {'Model': 'GeForce RTX 3070', 'MSRP': 499, 'Year Released': 2020},
    {'Model': 'GeForce RTX 3080', 'MSRP': 699, 'Year Released': 2020},
    {'Model': 'Radeon RX 580', 'MSRP': 229, 'Year Released': 2017},
    {'Model': 'Radeon RX 5700 XT', 'MSRP': 399, 'Year Released': 2019},
    {'Model': 'GeForce RTX 4090', 'MSRP': 1599, 'Year Released': 2022},
    {'Model': 'GeForce RTX 4080', 'MSRP': 1199, 'Year Released': 2022},
    {'Model': 'GeForce RTX 4070', 'MSRP': 599, 'Year Released': 2023},
    {'Model': 'GeForce RTX 4060', 'MSRP': 299, 'Year Released': 2023},
    {'Model': 'Radeon RX 7900 XTX', 'MSRP': 999, 'Year Released': 2022},
    {'Model': 'Radeon RX 7900 XT', 'MSRP': 899, 'Year Released': 2022},
]
df_specs = pd.concat([df_specs, pd.DataFrame(missing_data)], ignore_index=True)

df_performance['price_clean'] = pd.to_numeric(
    df_performance['price_usd'].astype(str).str.replace('$', '').str.replace(',', ''),
    errors='coerce'
)

def get_best_match(name, choices, cutoff=0.55):
    name = str(name).lower()
    choice_map = {c.lower(): c for c in choices}
    matches = difflib.get_close_matches(name, choice_map.keys(), n=1, cutoff=cutoff)
    if matches:
        return choice_map[matches[0]]
    return None

clean_names = df_specs['Model'].unique().tolist()
df_performance['Matched_Model'] = df_performance['video_card_name'].apply(
    lambda x: get_best_match(x, clean_names, cutoff=0.55)
)

merged_df = pd.merge(df_performance, df_specs, left_on='Matched_Model', right_on='Model', how='inner')

merged_df['Value_Score'] = merged_df['pasmark_gd3_mark'] / merged_df['MSRP']
merged_df['Price_Tier'] = (merged_df['MSRP'] / 500).round() * 500

fig1, ax1 = plt.subplots(figsize=(14, 8))

sns.scatterplot(
    data=merged_df,
    x='Year Released',
    y='Value_Score',
    hue='Price_Tier',
    size='Price_Tier',
    sizes=(50, 400),
    palette='viridis',
    legend='full',
    ax=ax1,
    zorder=3 
)

ax1.set_ylabel('GPU Value (Performance per $1)', fontsize=12, color='darkblue')
ax1.set_title('GPU Performance Value vs. Bitcoin Market Cycles (2005-2024)', fontsize=16)
ax1.grid(True, alpha=0.3)

ax2 = ax1.twinx() 
color_btc = 'orange'
ax2.fill_between(btc_yearly['Year'], btc_yearly['close'], color=color_btc, alpha=0.15, label='Bitcoin Price')
ax2.plot(btc_yearly['Year'], btc_yearly['close'], color=color_btc, linestyle='--', alpha=0.5)
ax2.set_ylabel('Average Bitcoin Price (USD)', color=color_btc, fontsize=12)
ax2.tick_params(axis='y', labelcolor=color_btc)

def get_brand(name):
    name = str(name).lower()
    if any(x in name for x in ['geforce', 'titan', 'quadro', 'nvidia', 'rtx', 'gtx']):
        return 'NVIDIA'
    elif any(x in name for x in ['radeon', 'firepro', 'amd', 'rx', 'vega']):
        return 'AMD'
    elif 'intel' in name or 'arc' in name:
        return 'Intel'
    return 'Other'

merged_df['Brand'] = merged_df['Matched_Model'].apply(get_brand)

brand_colors = {'NVIDIA': '#76b900', 'AMD': '#ed1c24', 'Intel': '#0071c5', 'Other': 'gray'}

fig2, ax3 = plt.subplots(figsize=(14, 8))

sns.scatterplot(
    data=merged_df,
    x='Year Released',
    y='Value_Score',
    hue='Brand',
    style='Brand',
    size='MSRP',
    sizes=(50, 400),
    palette=brand_colors,
    alpha=0.7,
    ax=ax3
)

ax3.set_ylabel('GPU Value (Performance per $1)', fontsize=12, fontweight='bold')
ax3.set_title('The Brand War: NVIDIA vs. AMD Value (2005-2024)', fontsize=16, fontweight='bold')
ax3.grid(True, alpha=0.3)

plt.show()

def clean_gpu_name(name):
    return name.replace('GeForce', '').replace('Radeon', '').replace('NVIDIA', '').replace('AMD', '').strip()

merged_df['Short_Name'] = merged_df['Matched_Model'].apply(clean_gpu_name)

grouped_df = merged_df.groupby('Short_Name').agg({
    'price_clean': 'mean',
    'MSRP': 'mean',
    'Year Released': 'max',
    'Matched_Model': 'first'  
}).reset_index()

grouped_df['Markup_Percentage'] = ((grouped_df['price_clean'] - grouped_df['MSRP']) / grouped_df['MSRP']) * 100

ignore_list = ['GeForce GTX 1060', 'GeForce GTX 1070', 'GeForce GTX 1080', 'GeForce GTX 1080 Ti', 'GeForce GT 1030', 'GeForce GT 710']

scalper_df = grouped_df[
    (grouped_df['Year Released'] >= 2017) & 
    (grouped_df['MSRP'] > 0) & 
    (~grouped_df['Matched_Model'].isin(ignore_list))
].sort_values('Markup_Percentage', ascending=False).head(10)

fig3, ax = plt.subplots(figsize=(12, 8))

ax.hlines(y=range(len(scalper_df)), xmin=0, xmax=scalper_df['Markup_Percentage'], color='gray', alpha=0.6, linewidth=2)
ax.scatter(scalper_df['Markup_Percentage'], range(len(scalper_df)), color='#d62728', s=150, zorder=3)

ax.set_yticks(range(len(scalper_df)))
ax.set_yticklabels(scalper_df['Short_Name'], fontsize=12, fontweight='bold')

for i in range(len(scalper_df)):
    pct = scalper_df.iloc[i]['Markup_Percentage']
    ax.text(pct + 5, i, f"+{pct:.0f}%", va='center', fontsize=11, fontweight='bold', color='#d62728')

ax.set_xlabel('Average Price Markup (%)', fontsize=12, fontweight='bold')
ax.set_title('The Scalper Tax: Top 10 Most Overpriced GPUs (Averaged)', fontsize=16, fontweight='bold')
ax.grid(axis='x', linestyle='--', alpha=0.3)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.tight_layout()
print("Displaying Scalper Tax Lollipop Chart...")
plt.show()