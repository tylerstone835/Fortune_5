import pandas as pd
import streamlit as st
from pandas import DataFrame
from pandas.io.parsers import TextFileReader

from Static.company import company_dict
from Utils.df_utils import customize_dataframe, calculate_close_delta
from Utils.chart_utils import draw_dashboard_figure


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

def configure_sidebar() -> st.session_state:
    """
    Draw sidebar elements and collect widget inputs into a dict struct.

    :return: st.session_state
    """


    with st.sidebar:
        st.space('xxsmall')

        st.write('# Chart Options')

        st.selectbox(
            label='**Company**',
            options=[company for company in company_dict],
            index=0,
            key='symbol'
        )

        st.space('xxsmall')

        st.segmented_control(
            label='**Timeframe**',
            options=['Daily', 'Weekly'],
            selection_mode='single',
            default='Daily',
            required=True,
            key='timeframe'
        )

        st.space('xxsmall')

        st.segmented_control(
            label='**Chart Style**',
            options=['Candle', 'Line', 'OHLC'],
            selection_mode='single',
            default='Candle',
            required=True,
            key='style'
        )

        # Retrieve pd.DataFrame based on sidebar input
        st.session_state['data'] = get_stock_data(
            timeframe=st.session_state['timeframe'],
            symbol=company_dict[st.session_state['symbol']]
        )


        st.space('xxsmall')

        st.select_slider(
            label='**Date Range**',
            options=st.session_state['data']['date'],
            value=(
                st.session_state['data']['date'][int(st.session_state['data'].index.max() / 2)],
                st.session_state['data']['date'].max()
            ),
            key='date_selection'
        )

        st.divider()
        st.write('# Indicators')
        st.toggle(label='**Volume**', value=False, key='volume')
        st.toggle(label='**MACD Histogram**', value=True, key='macd_hist')
        st.toggle(label='**MACD Lines**', value=False, key='macd_lines')
        st.space('xxsmall')
        st.slider(label='**EMA**', min_value=0, max_value=100, value=20, key='ema')

        # Customize dataframe with sidebar inputs
        customize_dataframe(st.session_state)

        return st.session_state


def draw_footer() -> None:
    """
    Draw footer elements.
    """

    with st.bottom:
        st.markdown(
            body='[Visit GitHub Repository](https://github.com/tylerstone835/Fortune_5)',
            text_alignment='right'
        )


def draw_body(
    session_state: st.session_state
) -> None:
    """
    Draw body of dashboard with data selection and input elements from sidebar.

    :param session_state: st.session_state
    """

    # Body layout
    st.title('Fortune 5 - Price Action Analysis', text_alignment='center')
    with st.container(border=True, horizontal_alignment='center'):

        with st.container(horizontal=True):

            with st.container(horizontal_alignment='left'):
                st.metric(
                    label='Close Price',
                    value=session_state['data'].loc[session_state['data'].index.max(), 'close'],
                    delta=calculate_close_delta(session_state['data']),
                    label_visibility='collapsed'
                )

            with st.container(vertical_alignment='top'):
                st.markdown(
                    body=f'## :grey[{company_dict[session_state['symbol']]}: {session_state['symbol']}]',
                    text_alignment='center'
                )

            with st.container(horizontal_alignment='right'):
                viz_output = st.segmented_control(
                    label='**Visualization Type**',
                    label_visibility='collapsed',
                    options=['Chart', 'DataFrame'],
                    selection_mode='single',
                    default='Chart',
                    required=True
                )

        if viz_output == 'Chart':
            st.pyplot(
                fig=draw_dashboard_figure(session_state),
                width='content'
            )

        elif viz_output == 'DataFrame':
            st.dataframe(
                session_state['data'].sort_values(by='date', ascending=False),
                height='content',
                hide_index=True
            )