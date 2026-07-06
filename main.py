from Static.company import company_dict
from Static.layout import layout_kwargs
from Utils.chart_utils import *
from Utils.df_utils import *
from Utils.st_utils import *


set_dashboard_style()
sb_config = configure_sidebar()
draw_footer()


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
        st.pyplot(
            fig=draw_dashboard_figure(sb_config),
            width='content'
        )

    elif viz_output == 'DataFrame':
        st.dataframe(
            sb_config['data'].sort_values(by='date', ascending=False),
            height='content',
            hide_index=True
        )
