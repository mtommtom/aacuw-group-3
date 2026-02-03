import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('dataset1cleaned.csv')

# Clean the price column - remove $ and commas, convert to float
df['price_clean'] = df['price_usd'].str.replace('$', '', regex=False).str.replace(',', '').str.strip().astype(float)

# Create a scatter plot of performance vs price
plt.figure(figsize=(12, 8))
plt.scatter(df['price_clean'], df['pasmark_gd3_mark'], alpha=0.5, s=20)

plt.xlabel('Price (USD)')
plt.ylabel('PassMark G3D Score')
plt.title('GPU Performance vs Price')
plt.grid(True, alpha=0.3)

# Add a tight layout and save/show the plot
plt.tight_layout()
plt.savefig('gpu_performance_plot.png', dpi=150)
plt.show()