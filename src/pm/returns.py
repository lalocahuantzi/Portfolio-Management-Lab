import pandas as pd
import numpy as np

def compute_returns(df,method="simple",dropna=None):
    '''
    Computes simple (arithmetic) or logarithmic returns using a DataFrame with closing prices of different securities.

    Parameters
    --------------------
    df : pd.DataFrame
        DataFrame of price series where each column represents a security.
    method : str
        The type of returns calculation method, the valid options are:
            - "simple"
            - "log"
    dropna : str
        Specifies how missing values should be removed after return computation, the valid options are:
            - "all"
            - "any"

    Returns
    --------------------
    pd.DataFrame
        DataFrame of simple (arithmetic) or logarithmic returns, aligned by date.
        Columns correspond to securities, index corresponds to dates.
    '''
    if method == "simple":
        ret = df.pct_change(fill_method=None)
    elif method == "log":
        ret = np.log(df/df.shift(1))
    else:
        raise ValueError("Method must be 'simple' or 'log'")

    if dropna in ["all","any"]:
        ret = ret.dropna(how=dropna)

    return ret

