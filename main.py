import pandas as pd
import streamlit as st

from Static.company import company_dict


with st.sidebar:
    symbol = st.selectbox(
        label='**Company**',
        options=['Amazon', 'Walmart', 'UnitedHealth', 'Apple', 'McKesson'],
        index=0
    )
    st.write('# Indicators')
    volume = st.toggle(label='**Volume**', value=False)
    macd_hist = st.toggle(label='**MACD Histogram**', value=False)
    macd_lines = st.toggle(label='**MACD Lines**', value=False)
    sma = st.slider(label='**SMA**', min_value=0, max_value=100, value=0)
    ema = st.slider(label='**EMA**', min_value=0, max_value=100, value=0)



df = pd.read_csv(
    f'https://raw.githubusercontent.com/tylerstone835/Fortune_5/refs/heads/master/Assets/Data/Daily/{company_dict[symbol]}.csv'
)

if not volume:
    df = df.drop(columns=['volume'])

st.dataframe(df, hide_index=True)


