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