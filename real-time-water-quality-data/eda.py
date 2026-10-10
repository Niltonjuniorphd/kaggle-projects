#%%

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data_path = Path(__file__).resolve().parent / 'data' / 'Johnstone_river_coquette_point_joined.csv' if '__file__' in locals() else Path('data/Johnstone_river_coquette_point_joined.csv')
if not data_path.exists():
    data_path = Path('real-time-water-quality-data/data/Johnstone_river_coquette_point_joined.csv')

data = pd.read_csv(data_path)

data.info()

#%%
# Boxplot com Pandas
data.boxplot(column='Temp', by='Month', grid=False, figsize=(10, 6))
plt.title('Temperature by Month')
plt.suptitle('')
plt.xlabel('Month')
plt.ylabel('Temperature (°C)')
plt.show()

#%%
# Boxplot com Seaborn
plt.figure(figsize=(10, 6))
sns.boxplot(data=data, x='Month', y='Temp')
plt.title('Temperature by Month')
plt.xlabel('Month')
plt.ylabel('Temperature (°C)')
plt.show()
#%%