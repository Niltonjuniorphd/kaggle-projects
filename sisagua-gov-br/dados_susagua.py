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

#%%
data['Parâmetro'].unique()
data['Valor'].unique()
data.head()



#%%
data_b = data.drop(
    columns=[
        'Região Geográfica',
        'UF',
        'Regional de Saúde',
        'Código IBGE',
        # 'Município',
        'Tipo da Instituição',
        'Sigla da Instituição',
        'Nome da Instituição',
        'CNPJ da Instituição',
        'Nome do escritório regional/local',
        'CNPJ do escritório regional/local',
        'Tipo da Forma de Abastecimento',
        'Código Forma de abastecimento',
        'Nome da Forma de Abastecimento',
        'Nome da ETA / UTA',
        'Tipo de Filtração',
        'Ano de referência',
        'Mês de referência',
        'Ponto de Monitoramento',
        # 'Parâmetro',
        'Campo',
        # 'Valor'
    ]
)


data_b['Valor'] = pd.to_numeric(data_b['Valor'], errors='coerce')
abt = (data_b
#  .query('`Ano de referência` == 2026').head(50)
 .dropna(subset=['Valor'])
 .groupby(['Município', 'Parâmetro'])['Valor']
    .mean()
    .unstack(1)
)

abt


