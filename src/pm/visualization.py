import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_universe_dispersion(
    prices: pd.DataFrame,
    *,
    normalize: str = "first_valid",   # "first_valid" | "first_row"
    ffill: bool = True,
    title: str = "Universe Dispersion (Min–Max Band)",
    figsize=(12, 5),
    mean_label: str = "Universe Mean",
    max_label: str = "Max Performer",
    min_label: str = "Min Performer",
    band_alpha: float = 0.15,
):
    '''
    Plot normalized cumulative paths dispersion for a universe of assets.

    Parameters
    --------------------
    prices : pd.DataFrame
        Price series (columns=tickers, index=dates).
    normalize : str
        - "first_valid": each asset is normalized by its first non-NaN value (suitable for dynamic universes where assets enter at different dates).
        - "first_row": all assets normalized by the first row after optional ffill (common-start view).
    ffill : bool
        Forward-fill prices before normalization, this helps avoid gaps for the "first_row" mode.
    '''

    if prices is None or prices.empty:
        raise ValueError("prices is empty")

    px = prices.copy()

    if ffill:
        px = px.ffill()

    if normalize == "first_row":
        base = px.iloc[0]
        cum = px.divide(base, axis=1)

    elif normalize == "first_valid":
        # Divide each column by its first valid value
        base = px.apply(lambda s: s.loc[s.first_valid_index()] if s.first_valid_index() is not None else np.nan)
        cum = px.divide(base, axis=1)

    else:
        raise ValueError("normalize must be 'first_valid' or 'first_row'")

    mean_path = cum.mean(axis=1, skipna=True)
    max_path = cum.max(axis=1, skipna=True)
    min_path = cum.min(axis=1, skipna=True)

    plt.figure(figsize=figsize)

    plt.plot(mean_path, label=mean_label, linewidth=2)
    plt.plot(max_path, linestyle="--", label=max_label)
    plt.plot(min_path, linestyle="--", label=min_label)

    plt.fill_between(mean_path.index, min_path, max_path, alpha=band_alpha)

    plt.title(title)
    plt.ylabel("Normalized Price")
    plt.legend()
    plt.show()

