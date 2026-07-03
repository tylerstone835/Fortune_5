import pandas as pd

def is_green_day(
    df: pd.DataFrame,
) -> bool:
    """
    Determine if latest day in stock df was green.
    :param df: df containing stock data for eval.
    :return: boolean expression confirming if latest stock day was green.
    """

    latest_row = df.loc[df['date'] == df['date'].max(), ['open', 'close']].to_dict(orient='list')

    return latest_row['close'][0] >= latest_row['open'][0]