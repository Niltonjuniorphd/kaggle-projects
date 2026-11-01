#%%
import pandas as pd


#%%
URL = 'https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SISAGUA/controle_mensal_parametros_basicos_2026_csv.zip'

def load_data_from_gov():
    """
    Load the SISAGUA data from the provided URL.

    Returns:
        pd.DataFrame: A DataFrame containing the SISAGUA data.
    """
    # Read the CSV file directly from the ZIP file
    df = pd.read_csv(URL, compression='zip', encoding='latin1', sep=';', low_memory=False)
    
    return df

# data = load_data_from_gov()
# data.info()

# data.to_parquet('data/data.parquet', index=False)  # Save the DataFrame as a Parquet file

# %%

data = pd.read_parquet('data/data.parquet')
data.info()  # Load the DataFrame from the Parquet file  

# %%
data.head(50)

#%%
data['Parâmetro'].unique()
data['Valor'].unique()

#%%
data['Valor'] = pd.to_numeric(data['Valor'], errors='coerce')
(data
 .query('`Ano de referência` == 2026').head(50)
 .dropna(subset=['Valor'])
 .groupby(['Município', 'Parâmetro'])['Valor'].mean().unstack(1)
)

#%%
