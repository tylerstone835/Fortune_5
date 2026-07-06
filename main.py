from Static.company import company_dict
from Static.layout import layout_kwargs
from Utils.chart_utils import *
from Utils.df_utils import *
from Utils.st_utils import *


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

            [data-testid="stMetricValue"] {
                font-size: 20px;
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
        options=['Candle', 'Line', 'OHLC'],
        selection_mode='single',
        default='Candle',
        required=True
    )

    # Data Config
    df = get_stock_data(timeframe=timeframe, symbol=company_dict[symbol])
    bom = get_bom(df)

    st.space('xxsmall')

    date_selection = st.select_slider(
        label='**Date Range**',
        options=df['date'],
        value=(df['date'][int(df.index.max() / 2)], df['date'].max())
    )

    st.divider()
    st.write('# Indicators')
    volume = st.toggle(label='**Volume**', value=False)
    macd_hist = st.toggle(label='**MACD Histogram**', value=True)
    macd_lines = st.toggle(label='**MACD Lines**', value=False)
    st.space('xxsmall')
    ema = st.slider(label='**EMA**', min_value=0, max_value=100, value=20)

chart_number = 1 + volume + (macd_hist or macd_lines)

# Footer layout
with st.bottom:
    st.markdown(
        body='[Visit GitHub Repository](https://github.com/tylerstone835/Fortune_5)',
        text_alignment='right'
    )


if not volume:
    df.drop(columns=['volume'], inplace=True)

if not macd_hist:
    df.drop(columns=['macd_histogram'], inplace=True)

if not macd_lines:
    df.drop(columns=['fast_line', 'signal_line'], inplace=True)

if ema:
    calculate_ema(df, ema)

# Filter date selection
df = (
    df
    .loc[
        (df['date'] >= date_selection[0]) &
        (df['date'] <= date_selection[1])
    ]
    .reset_index(drop=True)
)


fig, ax = plt.subplots(**layout_kwargs[chart_number])
if chart_number == 1:
    ax = [ax]

fig.set_facecolor((0, 0, 0, 0))
plt.tight_layout()

if style == 'OHLC':
    plot_ohlc(
        axes=ax[0],
        df=df,
        xticks=bom
    )

elif style == 'Candle':
    plot_candle(
        axes=ax[0],
        df=df,
        xticks=bom
    )

else:
    plot_line(
        axes=ax[0],
        df=df,
        xticks=bom
    )

if ema:
    plot_ema(
        axes=ax[0],
        df=df,
        window=ema,
        xticks=bom
    )

if volume:
    plot_volume(
        axes=ax[1],
        df=df,
        xticks=bom
    )

if macd_hist or macd_lines:
    plot_macd(
        axes=ax[chart_number - 1],
        df=df,
        plot_hist=macd_hist,
        plot_lines=macd_lines,
        xticks=bom
    )

# Body layout
st.title('Fortune 5 - Price Action Analysis', text_alignment='center')
with st.container(border=True, horizontal_alignment='center'):
    # with st.container(horizontal_alignment='right'):
    with st.container(horizontal=True):

        with st.container(horizontal_alignment='left', vertical_alignment='top'):
            st.metric(
                label='Close Price',
                value=df.loc[df.index.max(), 'close'],
                delta=calculate_close_delta(df),
                label_visibility='collapsed'
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
        st.pyplot(fig=fig, width='content')
    elif viz_output == 'DataFrame':
        st.dataframe(df.sort_values(by='date', ascending=False), height='content', hide_index=True)
