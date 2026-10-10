# https://www.kaggle.com/datasets/natanaelferran/river-water-parameters/data



#%% 

import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

PROJECT_ROOT = Path.cwd().parents[1]
DATA_DIR = PROJECT_ROOT / 'data'

#%%
data = pd.read_csv(
    DATA_DIR / 'archive' / 'River water parameters.csv'
)


#%%
data.columns = (
    data.columns
    .str.replace('\n', ' ', regex=False)
    .str.replace(r'\s+', ' ', regex=True)
    .str.strip()
    .str.lower()
    .str.replace(' ', '_', regex=False)
)

data = data.rename(columns={
    'date_(dd/mm/yyyy)': 'date',
    'time_(24_hrs_xx:xx)': 'time',
})
data.info()
# %%

#%%
data.describe(include='all').T

#%%
data['hardness_classification'].unique()

data_clean = data.copy()
data_clean = data_clean.drop(columns=['date', 'time', 'sampling_point'])
train_data = data_clean[data_clean['hardness_classification'].notna()].dropna(axis=0)
predict_data = data_clean[data_clean['hardness_classification'].isna()]

train_data.info()
predict_data.info()

#%%

X = train_data.drop(columns=['hardness_classification'])
y = train_data.pop('hardness_classification')

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
x_train.shape, x_test.shape, y_train.shape, y_test.shape

#%%
x_train.head()



# %%

model = RandomForestClassifier(
    n_estimators=10, 
    random_state=42,
    max_depth=5,
    
    )
model.fit(x_train, y_train)

y_pred = model.predict(x_test)

print(classification_report(y_test, y_pred))
print('score:', model.score(x_test, y_test))

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    # xticklabels=['Benign', 'Attack'],
    # yticklabels=['Benign', 'Attack']
)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()


print(model.predict(predict_data.drop(columns=['hardness_classification'])))



# %%
