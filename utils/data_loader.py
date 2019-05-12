import pandas as pd

from typing import List, Tuple
import os
from pathlib import Path


FUNDS_CSV = 'input/Quant_Invest_Fundusze.csv'
STOCKS_CSV = 'input/all_indices_close.csv'
COMMODITIES_CSV = 'input/all_commodities_close.csv'
RATES_CSV = 'input/policy_rates.csv'
FX_CSV = 'input/exchange_rates.csv'

STOOQ_DIR = Path('input/stooq_selected/')
STOOQ_CSVS = [
    STOOQ_DIR / fname 
    for fname in os.listdir(STOOQ_DIR)
    if fname[-3:] == 'csv'
]


def _load_indexed(path, index_col='Daty', sep=',') -> pd.DataFrame:
    df = pd.read_csv(path, index_col=index_col, sep=sep)
    df.index = pd.to_datetime(df.index)
    return df.sort_index()


def load_funds() -> pd.DataFrame:
    return _load_indexed(FUNDS_CSV, sep=';')


def load_stocks() -> pd.DataFrame:
    return _load_indexed(STOCKS_CSV, index_col='Data')


def load_commodities() -> pd.DataFrame:
    return _load_indexed(COMMODITIES_CSV, index_col='Data')


def load_rates() -> pd.DataFrame:
    policy_rates = pd.read_csv(RATES_CSV, index_col = 0)
    policy_rates = policy_rates.pivot(index='date', columns='reference_area', values='obs_value')
    policy_rates.index = pd.to_datetime(policy_rates.index)
    return policy_rates.iloc[:(-42)]  # keep only years 2000-2018


def load_fx() -> pd.DataFrame:
    exchange_rates = pd.read_csv(FX_CSV, index_col=0)
    exchange_rates.index = pd.to_datetime(exchange_rates['Date'])
    shortnames={}
    for col in exchange_rates.columns[1:]:
        start = col.index('(')
        end = col.index(')')
        shortnames[col] = col[(start+1):end]
    return exchange_rates.rename(columns = shortnames).drop(columns=['Date'])


def load_all() -> pd.DataFrame:
    return pd.concat([
        load_funds(),
        load_stocks(),
        load_commodities(),
        load_rates(),
        load_fx()
    ], axis='columns')


def load_stooq() -> List[Tuple[pd.DataFrame, str]]:
    return [
        (_load_indexed(csv, index_col='Data', sep=';'), csv.stem)
        for csv in STOOQ_CSVS
    ]
