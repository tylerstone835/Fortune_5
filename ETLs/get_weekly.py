from datetime import date, timedelta
import logging
import os
import pandas as pd

import requests

from Utils.df_utils import calculate_macd

POLYGON_API_KEY = os.environ.get('POLYGON_API_KEY')
START_DATE = date.today() - timedelta(days=730)
CUTOFF_DATE = date.today() - timedelta(days=365)
END_DATE = date.today()

logger = logging.getLogger(__name__)
logging.basicConfig(filename='weekly.log', level=logging.INFO)


def get_weekly_price_action(
        from_: date,
        to: date,
        *tickers: str,
) -> None:
    """
    Leverage the polygon/massive api endpoint to retrieve weekly aggregations for designated symbols.

    :param from_: Start of desired date period. Default to Unix start time to capture all.
    :param to: End of desired date period.
    :param tickers: Any number of ticker symbols for a publicly traded stock.
    """

    for ticker in tickers:

        path = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/week/{from_}/{to}?apiKey={POLYGON_API_KEY}'
        response = requests.get(path)

        if response.status_code != 200:
            logger.error('GET Request failed: %s', path)

        try:
            weekly_df = (
                pd.DataFrame((response.json())['results'])
                .assign(
                    symbol=ticker,
                    date=lambda x: (pd.to_datetime(x['t'], unit='ms') + timedelta(days=1)).dt.strftime('%Y-%m-%d'),
                    o=lambda x: x['o'].round(2),
                    h=lambda x: x['h'].round(2),
                    l=lambda x: x['l'].round(2),
                    c=lambda x: x['c'].round(2),
                    v=lambda x: x['v'].astype('int'),
                )
                .filter(['date', 'ticker', 'o', 'h', 'l', 'c', 'v'])
                .rename(columns={'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume'})
            )

            calculate_macd(weekly_df)

        except:
            logger.error('Weekly DataFrame failed to parse for %s', path)
            return

        (
            weekly_df
            .loc[weekly_df['date'] >= CUTOFF_DATE.strftime('%Y-%m-%d')]
            .to_csv(f'../Assets/Data/Weekly/{ticker}.csv', index=False)
        )


if __name__ == '__main__':
    get_weekly_price_action(
        START_DATE,
        END_DATE,
        'AMZN',
        'WMT',
        'UNH',
        'AAPL',
        'MCK'
    )