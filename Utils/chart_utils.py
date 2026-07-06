import matplotlib.pyplot as plt
import pandas as pd

from Static.layout import layout_kwargs
from Utils.df_utils import is_green_day, get_bom

_GRID_ALPHA = .1
_GREEN = (.03, .53, .04, 1)
_RED = (.72, .23, .24, 1)
_Y_LABEL_GREY = (.5, .5, .5, 1)
_SPINE_WIDTH = .1


def plot_ohlc(
    axes: plt.axes,
    df: pd.DataFrame,
    xticks: pd.Series = pd.Series(),
) -> None:
    """
    Plot OHLC chart on child axes. Requires OHLC data

    :param axes: Child axes on matplotlib.pyplot.figure
    :param df: Source pd.DataFrame. Requires OHLC.
    :param xticks: Add a custom series of date xticks, else blank.
    """

    required_columns_set = {'date', 'open', 'high', 'low', 'close'}

    if not required_columns_set <= set(df.columns):
        raise ValueError('Missing necessary data to construct chart')

    marker_size = (len(df) * -1/125) + 3

    # Plot Data
    for row in df.itertuples(index=False):

        color = _GREEN if row.close >= row.open else _RED

        axes.plot([row.date, row.date], [row.low, row.high], marker=',', linestyle='-', color=color, linewidth=.75)
        axes.plot(row.date, row.open, marker=0, color=color, markersize=marker_size)
        axes.plot(row.date, row.close, marker=1, color=color, markersize=marker_size)

    # Style Settings
    axes.grid(visible=True, linestyle=':', alpha=_GRID_ALPHA, zorder=0)
    axes.set_xticks(xticks)
    axes.set_xticklabels([fdate.date().strftime('%b-%y') for fdate in xticks.astype('datetime64[ns]')])
    axes.tick_params(axis='x', direction='in', length=0, labelcolor=_Y_LABEL_GREY, labelsize='xx-small')
    axes.tick_params(axis='y', direction='out', length=1.5, labelcolor=_Y_LABEL_GREY, labelsize='xx-small', color=(0,0,0,0))
    axes.set_xbound(lower=-.5, upper=len(df) - .5)
    axes.set_facecolor((0,0,0,0))
    axes.spines[['left', 'right', 'top']].set_visible(False)
    axes.spines[['bottom']].set_visible(True)
    axes.spines[['bottom']].set_color(_Y_LABEL_GREY)
    axes.spines[['bottom']].set_linewidth(_SPINE_WIDTH)



def plot_candle(
    axes: plt.axes,
    df: pd.DataFrame,
    xticks: pd.Series = pd.Series(),
) -> None:
    """
    Plot Candle chart on child axes. Requires OHLC data

    :param axes: Child axes on matplotlib.pyplot.figure
    :param df: Source pd.DataFrame. Requires OHLC.
    :param xticks: Add a custom series of date xticks, else blank.
    """

    required_columns_set = {'date', 'open', 'high', 'low', 'close'}

    if not required_columns_set <= set(df.columns):
        raise ValueError('Missing necessary data to construct chart')

    candle_width = (len(df) * -2/125) + 5

    # Plot Data
    for row in df.itertuples(index=False):

        color = _GREEN if row.close >= row.open else _RED

        axes.plot([row.date, row.date], [row.open, row.close], linestyle='-', color=color, linewidth=candle_width)
        axes.plot([row.date, row.date], [row.low, row.high], linestyle='-', color=color, linewidth=.5)


    # Style Settings
    axes.grid(visible=True, linestyle=':', alpha=_GRID_ALPHA, zorder=0)
    axes.set_xticks(xticks)
    axes.set_xticklabels([fdate.date().strftime('%b-%y') for fdate in xticks.astype('datetime64[ns]')])
    axes.tick_params(axis='x', direction='in', length=0, labelcolor=_Y_LABEL_GREY, labelsize='xx-small')
    axes.tick_params(axis='y', direction='out', length=1.5, labelcolor=_Y_LABEL_GREY, labelsize='xx-small', color=(0, 0, 0, 0))
    axes.set_xbound(lower=-.5, upper=len(df) - .5)
    axes.set_facecolor((0, 0, 0, 0))
    axes.spines[['left', 'right', 'top']].set_visible(False)
    axes.spines[['bottom']].set_visible(True)
    axes.spines[['bottom']].set_color(_Y_LABEL_GREY)
    axes.spines[['bottom']].set_linewidth(_SPINE_WIDTH)


def plot_line(
    axes: plt.axes,
    df: pd.DataFrame,
    xticks: pd.Series = pd.Series(),
) -> None:
    """
    Plot Line chart on child axes. Requires date and close data

    :param axes: Child axes on matplotlib.pyplot.figure
    :param df: Source pd.DataFrame. Requires date and close.
    :param xticks: Add a custom series of date xticks, else blank.
    """

    required_columns_set = {'date', 'close'}

    if not required_columns_set <= set(df.columns):
        raise ValueError('Missing necessary data to construct chart')

    # Plot Data
    color = _GREEN if is_green_day(df) else _RED
    axes.plot(df['date'], df['close'], color=color, linewidth=1)
    y_bounds = axes.get_ybound()
    axes.fill_between(df['date'], df['close'], color=(*color[0:3], .05), edgecolor=None)
    axes.set_ybound(y_bounds)

    # Style Settings
    axes.grid(visible=True, linestyle=':', alpha=_GRID_ALPHA, zorder=0)
    axes.set_xticks(xticks)
    axes.set_xticklabels([fdate.date().strftime('%b-%y') for fdate in xticks.astype('datetime64[ns]')])
    axes.tick_params(axis='x', direction='in', length=0, labelcolor=_Y_LABEL_GREY, labelsize='xx-small')
    axes.tick_params(axis='y', direction='out', length=1.5, labelcolor=_Y_LABEL_GREY, labelsize='xx-small', color=(0, 0, 0, 0))
    axes.set_xbound(lower=-.5, upper=len(df) - .5)
    axes.set_facecolor((0,0,0,0))
    axes.spines[['left', 'right', 'top']].set_visible(False)
    axes.spines[['bottom']].set_visible(True)
    axes.spines[['bottom']].set_color(_Y_LABEL_GREY)
    axes.spines[['bottom']].set_linewidth(_SPINE_WIDTH)


def plot_volume(
    axes: plt.axes,
    df: pd.DataFrame,
    xticks: pd.Series = pd.Series(),
) -> None:
    """
    Plot bar chart on child axes. Requires date and volume data

    :param axes: Child axes on matplotlib.pyplot.figure
    :param df: Source pd.DataFrame. Requires date and volume.
    :param xticks: Add a custom series of date xticks, else blank.
    """

    required_columns_set = {'date', 'volume'}

    if not required_columns_set <= set(df.columns):
        raise ValueError('Missing necessary data to construct chart')

    # Plot Data
    axes.bar(
        x=df['date'],
        height=df['volume'],
        color=(*_RED[0:3], .8),
        width=.5
    )

    # Style Settings
    axes.grid(visible=True, linestyle=':', alpha=_GRID_ALPHA, zorder=0)
    axes.set_xticks(xticks)
    axes.set_xticklabels([fdate.date().strftime('%b-%y') for fdate in xticks.astype('datetime64[ns]')])
    axes.tick_params(axis='x', direction='in', length=0, labelcolor=_Y_LABEL_GREY, labelsize='xx-small')
    axes.tick_params(axis='y', direction='out', length=1.5, labelcolor=_Y_LABEL_GREY, labelsize='xx-small', color=(0, 0, 0, 0))
    axes.set_xbound(lower=-.5, upper=len(df) - .5)
    axes.yaxis.get_offset_text().set_fontsize('xx-small')
    axes.set_facecolor((0,0,0,0))
    axes.spines[['left', 'right', 'top']].set_visible(False)
    axes.spines[['bottom']].set_visible(True)
    axes.spines[['bottom']].set_color(_Y_LABEL_GREY)
    axes.spines[['bottom']].set_linewidth(_SPINE_WIDTH)


def plot_macd(
    axes: plt.axes,
    df: pd.DataFrame,
    plot_hist: bool,
    plot_lines: bool,
    xticks: pd.Series = pd.Series(),
) -> None:
    """
    Plot bar chart on child axes. Requires date and macd data

    :param axes: Child axes on matplotlib.pyplot.figure
    :param df: Source pd.DataFrame. Requires date and macd data.
    :param plot_hist: Flag for drawing MACD histogram.
    :param plot_lines: Flag for drawing MACD lines.
    :param xticks: Add a custom series of date xticks, else blank.
    """

    # Plot Data
    if plot_hist:
        color = (
            (df['macd_histogram'] >= 0)
            .map({True: (*_GREEN[0:3], .8), False: (*_RED[0:3], .8)})
        )

        axes.bar(
            x=df['date'],
            height=df['macd_histogram'],
            width=.5,
            color=color,
            zorder=3
        )

        axes.grid(visible=True, linestyle=':', alpha=_GRID_ALPHA, zorder=0)
        axes.set_xticks(xticks)
        axes.set_xticklabels([fdate.date().strftime('%b-%y') for fdate in xticks.astype('datetime64[ns]')])
        axes.tick_params(axis='x', direction='in', length=0, labelcolor=_Y_LABEL_GREY, labelsize='xx-small')
        axes.tick_params(axis='y', direction='out', length=1.5, labelcolor=_Y_LABEL_GREY, labelsize='xx-small', color=(0, 0, 0, 0))
        axes.set_xbound(lower=-.5, upper=len(df) - .5)
        axes.set_facecolor((0, 0, 0, 0))
        axes.spines[['left', 'right', 'top']].set_visible(False)
        axes.spines[['bottom']].set_visible(True)
        axes.spines[['bottom']].set_color(_Y_LABEL_GREY)
        axes.spines[['bottom']].set_linewidth(_SPINE_WIDTH)

    if plot_lines:

        line_axes = axes if not plot_hist else axes.twinx()

        line_axes.plot(
            df['date'],
            df['fast_line'],
            linestyle='-',
            color=_Y_LABEL_GREY,
            linewidth=.4
        )

        line_axes.plot(
            df['date'],
            df['signal_line'],
            linestyle='-',
            color=_Y_LABEL_GREY,
            linewidth=1
        )

        line_axes.grid(visible=True, linestyle=':', alpha=_GRID_ALPHA, zorder=0)
        line_axes.set_xticks(xticks)
        line_axes.set_xticklabels([fdate.date().strftime('%b-%y') for fdate in xticks.astype('datetime64[ns]')])
        line_axes.tick_params(axis='x', direction='in', length=0, labelcolor=_Y_LABEL_GREY, labelsize='xx-small')
        line_axes.tick_params(axis='y', direction='out', length=1.5, labelcolor=_Y_LABEL_GREY, labelsize='xx-small', color=(0, 0, 0, 0))
        line_axes.set_xbound(lower=-.5, upper=len(df) - .5)
        line_axes.set_facecolor((0, 0, 0, 0))
        line_axes.spines[['left', 'right', 'top', 'bottom']].set_visible(False)

        if plot_hist and plot_lines:
            line_axes.set_yticks([])
        else:
            line_axes.spines[['bottom']].set_visible(True)
            line_axes.spines[['bottom']].set_color(_Y_LABEL_GREY)
            line_axes.spines[['bottom']].set_linewidth(_SPINE_WIDTH)


def plot_ema(
    axes: plt.axes,
    df: pd.DataFrame,
    window: int,
    xticks: pd.Series = pd.Series(),
) -> None:
    """
    Plot EMA on child axes. Requires date and EMA data

    :param axes: Child axes on matplotlib.pyplot.figure
    :param df: Source pd.DataFrame. Requires date and EMA.
    :param window: EMA window that's being plotted.
    :param xticks: Add a custom series of date xticks, else blank.
    """

    required_columns_set = {'date', f'ema_{window}'}

    if not required_columns_set <= set(df.columns):
        raise ValueError('Missing necessary data to construct EMA')

    x_bounds = axes.get_xbound()
    y_bounds = axes.get_ybound()

    axes.plot(df['date'], df[f'ema_{window}'], color=_Y_LABEL_GREY, linewidth=1)

    axes.set_xticks(xticks)
    axes.set_xticklabels([fdate.date().strftime('%b-%y') for fdate in xticks.astype('datetime64[ns]')])
    axes.set_xbound(x_bounds)
    axes.set_ybound(y_bounds)


def draw_dashboard_figure(
        sb_config: dict,
) -> plt.figure:
    """
    Determine what charts should be drawn in accordance with the sidebar
    configuration and pick out the proper layout ratio for the number
    of charts included.

    :param sb_config:
    :return: pyplot.figure with fully drawn child axes.
    """

    number_of_charts = 1 + sb_config['volume'] + (sb_config['macd_hist'] or sb_config['macd_lines'])

    fig, ax = plt.subplots(**layout_kwargs[number_of_charts])
    fig.set_facecolor((0, 0, 0, 0))
    plt.tight_layout()

    if number_of_charts == 1:
        ax = [ax]
    
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
            axes=ax[number_of_charts - 1],
            df=sb_config['data'],
            plot_hist=sb_config['macd_hist'],
            plot_lines=sb_config['macd_lines'],
            xticks=bom
        )

    return fig
