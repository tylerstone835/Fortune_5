import pandas as pd
import streamlit as st

from Static.company import company_dict

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

# Body layout
st.title('Fortune 5', text_alignment='center')
st.subheader(
    body='Visualizing price action for the five largest companies.',
    text_alignment='center',
    divider='grey'
)
st.dataframe(df, hide_index=True)
