import pandas as pd
import yfinance as yf

def download_prices(tickers, price_data, start_date, end_date):
    '''
    Extracts the adjusted prices for multiple securities using Yahoo Finance.
    
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
    
    portfolio = pd.DataFrame()
    
    for i in range(len(tickers)):
        col_name = str(tickers[i])
        df = yf.download(tickers[i],
            start=start_date,
            end=end_date,
            auto_adjust=True,
            progress=False)

        if df.empty or price_data not in df.columns:
        	continue

        portfolio[col_name] = df[price_data]
        
    return portfolio





