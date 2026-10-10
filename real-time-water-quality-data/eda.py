#%%

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

data_path = Path(__file__).resolve().parent / 'data' / 'Johnstone_river_coquette_point_joined.csv' if '__file__' in locals() else Path('data/Johnstone_river_coquette_point_joined.csv')
if not data_path.exists():
    data_path = Path('real-time-water-quality-data/data/Johnstone_river_coquette_point_joined.csv')

data = pd.read_csv(data_path)
data['log_Conductivity'] = np.log1p(data['Conductivity'])

# Reorder columns so log_Conductivity is right after Conductivity
cols = [col for col in data.columns if col != 'log_Conductivity']
cols.insert(cols.index('Conductivity') + 1, 'log_Conductivity')
data = data[cols]

#%%
data.info()

#%%
data.describe()


#%%
# Boxplot com Pandas

def plot(data, column, by, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    data.boxplot(column=column, by=by, grid=False)
    plt.title(title)
    plt.suptitle('')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

for col in data.columns:
    if data[col].dtype in ['float64', 'int64']:
        plot(data, col, 'Month', f'{col} by Month', 'Month', col)    
        plt.show()

#%%
for col in ['Conductivity', 'log_Conductivity']:
    sns.kdeplot(data=data[[col]])

    plt.show()



#%%
# Boxplot com Seaborn
# plt.figure(figsize=(10, 6))
# sns.boxplot(data=data, x='Month', y='Temp')
# plt.title('Temperature by Month')
# plt.xlabel('Month')
# plt.ylabel('Temperature (°C)')
# plt.show()


#%%
sns.pairplot(data=data, 
             vars=data.select_dtypes(include=[np.number]).columns, 
             hue='Month')
plt.show()