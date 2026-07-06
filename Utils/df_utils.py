from datetime import date

import pandas as pd

def is_green_day(
    df: pd.DataFrame,
) -> bool:
    """
    Determine if latest day closed higher.
    :param df: df containing stock data for eval.
    :return: boolean expression confirming if latest stock day was green.
    """

    is_green_df = (
        df
        .sort_values(by='date', ascending=False)
        .reset_index(drop=True)
        .head(2)
    )

    if len(is_green_df) == 2:
        return is_green_df.loc[0, 'close'] >= is_green_df.loc[1, 'close']

    return True


def get_bom(
    df: pd.DataFrame,
) -> pd.Series:
    """
    Get the smallest date at the beginning of each month in DataFrame.
    :param df:
    :return:
    """

    required_columns_set = {'date'}

    if not required_columns_set <= set(df.columns):
        raise ValueError('Missing necessary data to construct BOM')

    bom_df = (
        df
        [['date']].astype('datetime64[ns]')
        .assign(
            month=lambda df: df['date'].apply(lambda x: x.month),
            year=lambda df: df['date'].apply(lambda x: x.year)
        )
        .groupby(by=['month', 'year'], as_index=False)
        .min()
        ['date'].astype('string')
    )

    return bom_df


def calculate_macd(
    df: pd.DataFrame,
    short_window: int = 12,
    long_window: int = 26,
    signal_window: int = 9,
) -> None:
    """
    Calculate macd_histogram column for designated pd.DataFrame.

    :param df: Target pd.DataFrame
    :param short_window: Number of closing periods used to make the short window.
    :param long_window: Number of closing periods used to make the long window.
    :param signal_window: Number of (short_window - long_window) periods to make signal line.
    """

    required_columns_set = {'close'}

    if not required_columns_set <= set(df.columns):
        raise ValueError('Missing necessary data to construct MACD')

    df[f'ema_{short_window}'] = (
        df[['close']]
        .ewm(span=short_window, adjust=False, min_periods=short_window)
        .mean()
        .reset_index(drop=True)
    )

    df[f'ema_{long_window}'] = (
        df[['close']]
        .ewm(span=long_window, adjust=False, min_periods=long_window)
        .mean()
        .reset_index(drop=True)
    )

    df['fast_line'] = df[f'ema_{short_window}'] - df[f'ema_{long_window}']

    df['signal_line'] = (
        df[['fast_line']]
        .ewm(span=signal_window, adjust=False, min_periods=signal_window)
        .mean()
        .reset_index(drop=True)
    )

    df['macd_histogram'] = round(df['fast_line'] - df['signal_line'], 7)
    df[['fast_line', 'signal_line']] = df[['fast_line', 'signal_line']].round(7)

    df.drop(columns=[f'ema_{short_window}', f'ema_{long_window}'], inplace=True)


def calculate_ema(
    df: pd.DataFrame,
    window: int,
) -> None:
    """
    Calculate ema column for designated pd.DataFrame.

    :param df: Target pd.DataFrame
    :param window: Number of closing periods used in EMA calculation.
    """

    df[f'ema_{window}'] = (
        df['close']
        .ewm(span=window, adjust=False, min_periods=window)
        .mean()
        .round(2)
    )


def calculate_close_delta(df):
    """
    Get latest closing delta for date range for header KPI metric.

    :param df: Target df to obtain KPI from.
    """

    max_index = df.index.max()
    difference = (df.at[max_index, 'close'] - df.at[max_index - 1, 'close']) / df.at[max_index - 1, 'close']
    return f'{round(difference * 100, 2)}%'
