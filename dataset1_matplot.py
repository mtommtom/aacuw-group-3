import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('dataset1cleaned.csv')

# Clean the price column - remove $ and commas, convert to float
df['price_clean'] = df['price_usd'].str.replace('$', '', regex=False).str.replace(',', '').str.strip().astype(float)

def get_brand(name):
    name = str(name).lower()
    if any(x in name for x in ['geforce', 'titan', 'quadro', 'nvidia', 'rtx', 'gtx', 'tesla']):
        return 'NVIDIA'
    elif any(x in name for x in ['radeon', 'firepro', 'amd', 'rx', 'vega', 'ryzen', 'firegl']):
        return 'AMD'
    elif any(x in name for x in ['intel', 'arc', 'iris']):
        return 'Intel'     
    else:
        return 'Other'

df['Brand'] = df['video_card_name'].apply(get_brand)

plt.figure(figsize=(12, 8))

brand_colors = {'NVIDIA': '#76b900', 'AMD': '#ed1c24', 'Intel': '#0071c5'}

for brand in df['Brand'].unique():
    subset = df[df['Brand'] == brand]
    
    plt.scatter(subset['price_clean'], subset['pasmark_gd3_mark'], 
                c=brand_colors.get(brand, 'gray'), 
                label=brand,
                alpha=0.6, s=20) 
    

# Create a scatter plot of performance vs price

plt.xlabel('Price (USD)')
plt.ylabel('PassMark G3D Score')
plt.title('GPU Performance vs Price')
plt.grid(True, alpha=0.3)
plt.legend(title='GPU vendor')

# Add a tight layout and save/show the plot
plt.tight_layout()
plt.savefig('gpu_performance_plot.png', dpi=150)
plt.show()