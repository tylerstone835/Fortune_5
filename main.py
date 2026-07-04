import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from Static.company import company_dict
from Static.layout import layout_kwargs
from Utils.chart_utils import *
from Utils.df_utils import *


# Initial page configuration and default pad settings.
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
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar layout
with st.sidebar:
    st.space('xxsmall')

    st.write('# Chart Options')

    symbol = st.selectbox(
        label='**Company**',
        options=[company for company in company_dict],
        index=0
    )

    st.space('xxsmall')

    timeframe = st.segmented_control(
        label='**Timeframe**',
        options=['Daily', 'Weekly'],
        selection_mode='single',
        default='Daily',
        required=True
    )

    st.space('xxsmall')

    style = st.segmented_control(
        label='**Chart Style**',
        options=['OHLC', 'Candle', 'Line'],
        selection_mode='single',
        default='OHLC',
        required=True
    )

    st.divider()
    st.write('# Indicators')
    volume = st.toggle(label='**Volume**', value=False)
    macd_hist = st.toggle(label='**MACD Histogram**', value=False)
    macd_lines = st.toggle(label='**MACD Lines**', value=False)
    st.space('xxsmall')
    sma = st.slider(label='**SMA**', min_value=0, max_value=100, value=0)
    ema = st.slider(label='**EMA**', min_value=0, max_value=100, value=0)

chart_number = 1 + volume + (macd_hist or macd_lines)

# Footer layout
with st.bottom:
    st.markdown(
        body='[Visit GitHub Repository](https://github.com/tylerstone835/Fortune_5)',
        text_alignment='right'
    )

# Data Config
df = pd.read_csv(
    f'https://raw.githubusercontent.com/tylerstone835/Fortune_5/refs/heads/master/Assets/Data/Daily/{company_dict[symbol]}.csv'
)

if not volume:
    df = df.drop(columns=['volume'])

df = df.tail(125).reset_index(drop=True)

fig, ax = plt.subplots(**layout_kwargs[chart_number])
if chart_number == 1:
    ax = [ax]

fig.set_facecolor((0, 0, 0, 0))
plt.tight_layout()

if style == 'OHLC':
    plot_ohlc(
        axes=ax[0],
        df=df
    )

elif style == 'Candle':
    plot_candle(
        axes=ax[0],
        df=df
    )

else:
    plot_line(
        axes=ax[0],
        df=df
    )

if volume:
    plot_volume(
        axes=ax[1],
        df=df
    )

# Body layout
st.title('Fortune 5 - Price Action for the Five Largest Companies', text_alignment='center')
with st.container(border=True, horizontal_alignment='center'):
    st.pyplot(fig=fig, width='content')
