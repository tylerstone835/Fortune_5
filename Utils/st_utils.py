import pandas as pd
import streamlit as st
from pandas import DataFrame
from pandas.io.parsers import TextFileReader


@st.cache_data(scope='session')
def get_stock_data(
        timeframe: str,
        symbol: str
) -> TextFileReader | DataFrame:
    """
    A cached data retrieval function for the visualized stock data.
    :param timeframe:
    :param symbol:
    :return: pd.DataFrame contain stock data from UI selection.
    """

    try:
        return pd.read_csv(
            f'Assets/Data/{timeframe}/{symbol}.csv'
        )
    except FileNotFoundError:
        return pd.read_csv(
            f'https://raw.githubusercontent.com/tylerstone835/Fortune_5/refs/heads/master/Assets/Data/{timeframe}/{symbol}.csv'
        )


def set_dashboard_style() -> None:
    """
    Configure the global layout and tweak the default CSS settings.
    """

    st.set_page_config(layout='wide', page_title='Fortune 5')
    st.markdown(
        """
            <style>
                   .block-container {
                        padding-top: 1rem;
                        padding-bottom: 0rem;
                        padding-left: 4rem;
                        padding-right: 4rem;
                    }
    
                    [data-testid="stMetricValue"] {
                        font-size: 20px;
                    }
            </style>
            """,
        unsafe_allow_html=True
    )
