from Static.company import company_dict
from Static.layout import layout_kwargs
from Utils.chart_utils import *
from Utils.df_utils import *
from Utils.st_utils import *


set_dashboard_style()
sb_config = configure_sidebar()
draw_footer()



if not sb_config['volume']:
    sb_config['data'].drop(columns=['volume'], inplace=True)

if not sb_config['macd_hist'] :
    sb_config['data'].drop(columns=['macd_histogram'], inplace=True)

if not sb_config['macd_lines']:
    sb_config['data'].drop(columns=['fast_line', 'signal_line'], inplace=True)

if sb_config['ema']:
    calculate_ema(sb_config['data'], sb_config['ema'])

# Filter date selection
sb_config['data'] = (
    sb_config['data']
    .loc[
        (sb_config['data']['date'] >= sb_config['date_selection'][0]) &
        (sb_config['data']['date'] <= sb_config['date_selection'][1])
    ]
    .reset_index(drop=True)
)


fig, ax = plt.subplots(**layout_kwargs[chart_number])
if chart_number == 1:
    ax = [ax]

fig.set_facecolor((0, 0, 0, 0))
plt.tight_layout()
bom = get_bom(sb_config['data'])

if sb_config['style'] == 'OHLC':
    plot_ohlc(
        axes=ax[0],
        df=sb_config['data'],
        xticks=bom
    )

elif sb_config['style'] == 'Candle':
    plot_candle(
        axes=ax[0],
        df=sb_config['data'],
        xticks=bom
    )

else:
    plot_line(
        axes=ax[0],
        df=sb_config['data'],
        xticks=bom
    )

if sb_config['ema']:
    plot_ema(
        axes=ax[0],
        df=sb_config['data'],
        window=sb_config['ema'],
        xticks=bom
    )

if sb_config['volume']:
    plot_volume(
        axes=ax[1],
        df=sb_config['data'],
        xticks=bom
    )

if sb_config['macd_hist'] or sb_config['macd_lines']:
    plot_macd(
        axes=ax[chart_number - 1],
        df=sb_config['data'],
        plot_hist=sb_config['macd_hist'],
        plot_lines=sb_config['macd_lines'],
        xticks=bom
    )

# Body layout
st.title('Fortune 5 - Price Action Analysis', text_alignment='center')
with st.container(border=True, horizontal_alignment='center'):

    with st.container(horizontal=True):

        with st.container(horizontal_alignment='left', vertical_alignment='top'):
            st.metric(
                label='Close Price',
                value=sb_config['data'].loc[sb_config['data'].index.max(), 'close'],
                delta=calculate_close_delta(sb_config['data']),
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
        st.dataframe(
            sb_config['data'].sort_values(by='date', ascending=False),
            height='content',
            hide_index=True
        )
