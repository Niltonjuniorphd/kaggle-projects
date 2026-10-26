# https://www.kaggle.com/datasets/natanaelferran/river-water-parameters/data
#
# Modelling pipeline for 'hardness_classification'.
#   - 'hardness_(mg_caco3/l)' is excluded: the class is derived from it.
#   - The sampling date is not used: the 'date' column is dropped on load.
#   - Preprocessing is fitted inside each fold through a Pipeline.

# %%
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

try:
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
except NameError:
    # Interactive (VS Code / Jupyter) execution from src/scripts
    PROJECT_ROOT = Path.cwd().parents[1]

DATA_DIR = PROJECT_ROOT / 'data'
FIGURES_DIR = PROJECT_ROOT / 'reports' / 'figures'
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
TARGET = 'hardness_classification'
CATEGORICAL_FEATURES = ['sampling_point']
EXCLUDED_COLUMNS = [
    'time',
    TARGET,
    'hardness_(mg_caco3/l)',  # the target is a threshold of this value
    'tds_(mg/l)',  # computed from EC by the probe (r = 0.999)
]

# %%
data = pd.read_csv(DATA_DIR / 'archive' / 'River water parameters.csv')

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
data = data.drop(columns=['date'])
data['sampling_point'] = data['sampling_point'].str.replace('_', ' ', regex=False)

# %%
labelled = data[data[TARGET].notna()].reset_index(drop=True)
unlabelled = data[data[TARGET].isna()].reset_index(drop=True)

X = labelled.drop(columns=EXCLUDED_COLUMNS)
y = labelled[TARGET]


def build_model(X: pd.DataFrame) -> Pipeline:
    numeric = [c for c in X.columns if c not in CATEGORICAL_FEATURES]
    preprocess = ColumnTransformer([
        ('num', SimpleImputer(strategy='median'), numeric),
        ('cat', OneHotEncoder(handle_unknown='ignore'), CATEGORICAL_FEATURES),
    ])
    classifier = RandomForestClassifier(
        n_estimators=300,
        max_depth=5,
        class_weight='balanced',
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    return Pipeline([('preprocess', preprocess), ('model', classifier)])


# %%
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
fold_scores = []
fold_importances = []

for fold, (train_idx, test_idx) in enumerate(cv.split(X, y)):
    model = build_model(X)
    model.fit(X.iloc[train_idx], y.iloc[train_idx])

    score = balanced_accuracy_score(y.iloc[test_idx], model.predict(X.iloc[test_idx]))
    fold_scores.append(score)

    result = permutation_importance(
        model, X.iloc[test_idx], y.iloc[test_idx],
        scoring='balanced_accuracy', n_repeats=30, random_state=RANDOM_STATE,
    )
    fold_importances.append(result.importances_mean)
    print(f'Fold {fold}: balanced accuracy = {score:.3f}')

fold_importances = np.vstack(fold_importances)
importance = pd.DataFrame({
    'feature': X.columns,
    'mean': fold_importances.mean(axis=0),
    'std': fold_importances.std(axis=0),
})
print(f'Balanced accuracy: {np.mean(fold_scores):.3f} +/- {np.std(fold_scores):.3f}')

# %%
# Final model on all labelled rows; predict the unlabelled samples
final_model = build_model(X).fit(X, y)
X_unlabelled = unlabelled.drop(columns=EXCLUDED_COLUMNS)
print(unlabelled[['time', 'sampling_point']].assign(
    prediction=final_model.predict(X_unlabelled)
))

# %%
FEATURE_LABELS = {
    'ambient_temperature_(°c)': 'Ambient temperature (°C)',
    'ambient_humidity': 'Ambient humidity',
    'sample_temperature_(°c)': 'Sample temperature (°C)',
    'ph': 'pH',
    'ec_(µs/cm)': 'EC (µS/cm)',
    'tss_(ml_sed/l)': 'TSS (mL sed/L)',
    'do_(mg/l)': 'DO (mg/L)',
    'level_(cm)': 'Level (cm)',
    'turbidity_(ntu)': 'Turbidity (NTU)',
    'total_cl-_(mg_cl-/l)': 'Total Cl⁻ (mg/L)',
    'sampling_point': 'Sampling point',
}

COLORS = {
    'surface': '#fcfcfb',
    'text_primary': '#0b0b0b',
    'text_secondary': '#52514e',
    'grid': '#e4e3df',
    'series': '#2a78d6',
}

df = importance.sort_values('mean').reset_index(drop=True)
labels = df['feature'].map(FEATURE_LABELS).fillna(df['feature'])
positions = np.arange(len(df))

fig, ax = plt.subplots(figsize=(8, 5.5), facecolor=COLORS['surface'])
ax.barh(positions, df['mean'], height=0.6, color=COLORS['series'], zorder=2)
ax.errorbar(
    df['mean'], positions, xerr=df['std'], fmt='none',
    ecolor=COLORS['text_secondary'], elinewidth=1, capsize=0, zorder=3,
)
for pos, value, err in zip(positions, df['mean'], df['std']):
    ax.text(max(value, 0) + err, pos, f'  {value:.3f}', va='center',
            fontsize=8, color=COLORS['text_secondary'])

ax.set_yticks(positions, labels, fontsize=9, color=COLORS['text_primary'])
ax.axvline(0, color=COLORS['text_secondary'], linewidth=1, zorder=1)
ax.set_title(
    'Permutation feature importance - hardness classification\n'
    f'Stratified 5-fold CV, balanced accuracy '
    f'{np.mean(fold_scores):.2f} ± {np.std(fold_scores):.2f}',
    loc='left', fontsize=11, color=COLORS['text_primary'],
)
ax.set_xlabel('Drop in balanced accuracy when permuted',
              fontsize=9, color=COLORS['text_secondary'])
ax.grid(axis='x', color=COLORS['grid'], linewidth=0.8, zorder=0)
ax.tick_params(axis='x', colors=COLORS['text_secondary'], labelsize=8)
ax.tick_params(axis='y', length=0)
ax.set_facecolor(COLORS['surface'])
for spine in ax.spines.values():
    spine.set_visible(False)
ax.margins(x=0.15)

fig.text(
    0.01, -0.02,
    'Bars: mean drop in balanced accuracy across folds; whiskers: ±1 std.',
    fontsize=8, color=COLORS['text_secondary'],
)
fig.savefig(FIGURES_DIR / 'feature_importance.png', dpi=150,
            bbox_inches='tight', facecolor=COLORS['surface'])
plt.show()

# %%
