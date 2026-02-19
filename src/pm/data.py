import pandas as pd
import yfinance as yf
import numpy as np

def download_prices(tickers, price_data, start_date, end_date):
    '''
    Downloads historical price data for multiple securities using Yahoo Finance.
    
    Parameters
    --------------------
        tickers : list[str]
            The list of securities from which we are going to obtain their closing prices.
        price_data: str
        	The type of pricing data to extract, the valid options are:
        	- 'Close'
        	- 'Open'
        	- 'High'
        	- 'Low'
        	- 'Volume'
        start_date : datetime.datetime
            Starting date for the historical prices
        end_date : datetime.datetime
            Final date for the historical prices

    Returns
    --------------------
        pd.DataFrame:
            DataFrame containing the adjusted closing prices of each security.
            Columns correspond to ticker symbols, index corresponds to dates.
    '''

    valid_price_data = ["Close","Open","Low","High","Volume"]
    if price_data not in valid_price_data:
        raise ValueError(f"price_data must be one of {valid_price_data}, instead got '{price_data}'")
    
    # Normalize tickers (Input normalization -> list)
    if isinstance(tickers, str):
        tickers_list = [tickers]
    else:
        tickers_list = list(tickers)
    
    # Single download call
    raw = yf.download(
        tickers_list,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
        group_by="column",  # keeps consistent structure across versions
    )

    if raw.empty:
        return pd.DataFrame()

    # When multiple tickers -> Columns are MultiIndex (Field, Ticker)
    # When single ticker -> Columns are single level (Field)
    if isinstance(raw.columns, pd.MultiIndex):
        if price_data not in raw.columns.get_level_values(0):
            return pd.DataFrame()
        prices = raw[price_data].copy()
    else:
        if price_data not in raw.columns:
            return pd.DataFrame()
        prices = raw[[price_data]].copy()
        prices.columns = tickers_list  # Rename columns to tickers

    # Ensure consistent column order & only requested tickers
    prices = prices.reindex(columns=tickers_list)

    return prices

def ath_summary(prices):
    '''
    Computes All-Time High (ATH) info per asset.

    Parameters
    ----------
    prices : pd.DataFrame
        Price series. Each column is an asset and index is datetime-like.

    Returns
    -------
    pd.DataFrame
        DataFrame summarizing each asset's All-Time High (ATH) information and its current percentage drawdown relative to the ATH. 
        Columns:
        - ath_price
        - ath_date
        - last_price
        - last_date
        - drop_from_ath (decimal)
        - drop_from_ath_pct (%)
    '''
    rows = []

    for col in prices.columns:
        s = prices[col].dropna()
        if s.empty:
            rows.append({
                "Ticker": col,
                "ath_price": np.nan,
                "ath_date": pd.NaT,
                "last_price": np.nan,
                "last_date": pd.NaT,
                "drop_from_ath": np.nan,
                "drop_from_ath_pct": np.nan,
            })
            continue

        ath_price = s.max()
        ath_date = s.idxmax()

        last_date = s.index[-1]
        last_price = s.iloc[-1]

        drop_from_ath = (last_price / ath_price) - 1.0  # Negative if the last price is below ATH, maximum possible value is 0.00 (last_price == ath_price)
        rows.append({
            "Ticker": col,
            "ath_price": round(ath_price,3),
            "ath_date": ath_date,
            "last_price": round(last_price,3),
            "last_date": last_date,
            # "drop_from_ath": drop_from_ath,
            "drop_from_ath_pct": round(100.0 * drop_from_ath,3),
        })

    out = pd.DataFrame(rows).set_index("Ticker")

    out = out.sort_values("drop_from_ath_pct", ascending=False)

    return out

def filter_min_obs(prices, min_obs):
    '''
    Filters the portfolio universe by a minimum number of observations since not all the tickers may start trading on the same date.

    Parameters
    --------------------
        prices : pd.DataFrame
            DataFrame containing price series (columns=tickers, index=dates).
        min_obs : int
            Minimum number of valid observations required (e.g., 252).

    Returns
    --------------------
        pd.DataFrame:
            DataFrame where columns with fewer than (min_obs) non-missing observations are entirely set to NaN..
            Tickers with enough data remain unchanged (full history kept).
    '''
    prices_filt = prices.copy()
    excluded = []

    for col in prices_filt.columns:
        n_obs = prices_filt[col].dropna().shape[0]

        if n_obs < min_obs:
            prices_filt[col] = np.nan
            excluded.append(col)
    
    if len(excluded) == 0:
        print(f"All tickers meet the minimum requirement of {min_obs} observations.")
    else:
        print(f"{len(excluded)} ticker(s) excluded (less than {min_obs} observations):")
        print(excluded)

    return prices_filt





