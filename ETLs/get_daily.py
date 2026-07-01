from datetime import date, timedelta
import logging
import os
import pandas as pd

import requests

POLYGON_API_KEY = os.environ.get('POLYGON_API_KEY')
START_DATE = date.today() - timedelta(days=365)
END_DATE = date.today()

logger = logging.getLogger(__name__)
logging.basicConfig(filename='daily.log', level=logging.INFO)


def get_daily_price_action(
        from_: date,
        to: date,
        *tickers: str,
) -> None:
    """
    Leverage the polygon/massive api endpoint to retrieve daily aggregations for designated symbols.

    :param from_: Start of desired date period. Default to Unix start time to capture all.
    :param to: End of desired date period.
    :param tickers: Any number of ticker symbols for a publicly traded stock.
    """

    for ticker in tickers:

        path = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{from_}/{to}?apiKey={POLYGON_API_KEY}'
        response = requests.get(path)

        if response.status_code != 200:
            logger.error('GET Request failed: %s', path)

        try:
            daily_df = (
                pd.DataFrame((response.json())['results'])
                .assign(
                    symbol=ticker,
                    date=lambda x: pd.to_datetime(x['t'], unit='ms').dt.strftime('%Y-%m-%d'),
                    o=lambda x: x['o'].round(2),
                    h=lambda x: x['h'].round(2),
                    l=lambda x: x['l'].round(2),
                    c=lambda x: x['c'].round(2),
                    v=lambda x: x['v'].astype('int'),
                )
                .filter(['date', 'ticker', 'o', 'h', 'l', 'c', 'v'])
                .rename(columns={'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume'})
            )

        except:
            logger.error('Daily DataFrame failed to parse for %s', path)

        daily_df.to_csv(f'../Assets/Data/Daily/{ticker}.csv', index=False)


if __name__ == '__main__':
    get_daily_price_action(
        START_DATE,
        END_DATE,
        'AMZN',
        'WMT',
        'UNH',
        'AAPL',
        'MCK'
    )