import pandas as pd
import numpy as np

def simple_returns(df):
    '''
    Calculates simple (arithmetic) returns using a DataFrame with closing prices of different securities.

    Parameters
    --------------------
    df : pd.DataFrame
        DataFrame of price series where each column represents a security. 

    Returns
    --------------------
    pd.DataFrame
        DataFrame of arithmetic returns, aligned by date.
        Columns correspond to securities, index corresponds to dates.
    '''
    rend = pd.DataFrame()
    lista_rend = df.columns.tolist()
    for i in range(len(lista_rend)):
        nombre_col = str(lista_rend[i])
        rend[nombre_col] = df[lista_rend[i]] / df[lista_rend[i]].shift(1) - 1
    rend = rend.dropna(how='all')
    return rend

def log_returns(df):
    '''
    Calculates logarithmic returns using a DataFrame with closing prices of different securities.

    Parameters
    --------------------
    df : pd.DataFrame
        DataFrame of price series where each column represents a security. 

    Returns
    --------------------
    pd.DataFrame
        DataFrame of logarithmic returns, aligned by date.
        Columns correspond to securities, index corresponds to dates.
    '''
    rend = pd.DataFrame()
    lista_rend = df.columns.tolist()
    for i in range(len(lista_rend)):
        nombre_col = str(lista_rend[i])
        rend[nombre_col] = np.log(df[lista_rend[i]] / df[lista_rend[i]].shift(1))
    rend = rend.dropna(how='all')
    return rend
