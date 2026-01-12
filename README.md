# Portfolio Management Lab

This repository contains a personal portfolio management project focused on market data extraction and return construction as inputs for quantitative analysis.

## Current scope

At this stage, the project includes:

- Downloading historical price data using Yahoo Finance
- Construction of simple (arithmetic) and logarithmic returns
- An initial Jupyter notebook combining data extraction with conceptual notes

## Repository structure

    portfolio-management-lab/
    ├── notebooks/
    │   └── 01_data_and_returns.ipynb
    ├── src/
    │   └── pm/
    │       ├── data.py
    │       └── returns.py
    ├── pyproject.toml
    ├── setup.cfg
    └── README.md

## Usage

1. Install the project in editable mode:

   pip install -e .

2. Open and run the notebook:

   notebooks/01_data_and_returns.ipynb

The notebook is intended to be run sequentially from top to bottom.

