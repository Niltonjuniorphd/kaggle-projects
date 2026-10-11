#%%

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

data_path = Path(__file__).resolve().parent / 'data' / 'all_stations.parquet' if '__file__' in locals() else Path('data/all_stations.parquet')
if not data_path.exists():
    data_path = Path('real-time-water-quality-data/data/all_stations.parquet')

# Consolidated dataset: all stations concatenated, with a 'station' column.
# Not every station has every sensor, so Q, Conductivity, NO3, Temp,
# Turbidity and Level contain NaN for stations missing that probe.
data = pd.read_parquet(data_path)
data['log_Conductivity'] = np.log1p(data['Conductivity'])
data['year'] = data['Timestamp'].dt.year

# Reorder columns so log_Conductivity is right after Conductivity
cols = [col for col in data.columns if col != 'log_Conductivity']
cols.insert(cols.index('Conductivity') + 1, 'log_Conductivity')
data = data[cols]

#%%
data.head()

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
# Sample rows for the pairplot: the consolidated dataset has ~295k rows
# across 11 stations, too many for pairplot to render in a reasonable time.
# pairplot_sample = data.sample(n=5000, random_state=0)
# sns.pairplot(data=pairplot_sample,
#              vars=pairplot_sample.select_dtypes(include=[np.number]).columns,
#              hue='Month')
# plt.show()