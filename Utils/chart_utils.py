import matplotlib.pyplot as plt
import pandas as pd

from Utils.df_utils import is_green_day

_GRID_ALPHA = .1
_GREEN = (.03, .53, .04, 1)
_RED = (.72, .23, .24, 1)
_Y_LABEL_GREY = (.5, .5, .5, 1)


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

    # Plot Data
    for row in df.itertuples(index=False):

        color = _GREEN if row.close >= row.open else _RED

        axes.plot([row.date, row.date], [row.low, row.high], marker=',', linestyle='-', color=color, linewidth=.75)
        axes.plot(row.date, row.open, marker=0, color=color, markersize=2.5)
        axes.plot(row.date, row.close, marker=1, color=color, markersize=2.5)

    # Style Settings
    axes.grid(visible=True, linestyle=':', alpha=_GRID_ALPHA, zorder=0)
    axes.set_xticks(xticks)
    axes.set_xticklabels([fdate.date().strftime('%b-%y') for fdate in xticks.astype('datetime64[ns]')])
    axes.tick_params(axis='x', direction='in', length=0, labelcolor=_Y_LABEL_GREY, labelsize='xx-small')
    axes.tick_params(axis='y', direction='out', length=1.5, labelcolor=_Y_LABEL_GREY, labelsize='xx-small', color=(0,0,0,0))
    axes.set_xbound(lower=-.5, upper=len(df) - .5)
    axes.set_frame_on(False)


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

    # Plot Data
    for row in df.itertuples(index=False):

        color = _GREEN if row.close >= row.open else _RED

        axes.plot([row.date, row.date], [row.open, row.close], linestyle='-', color=color, linewidth=3)
        axes.plot([row.date, row.date], [row.low, row.high], linestyle='-', color=color, linewidth=.5)


    # Style Settings
    axes.grid(visible=True, linestyle=':', alpha=_GRID_ALPHA, zorder=0)
    axes.set_xticks(xticks)
    axes.set_xticklabels([fdate.date().strftime('%b-%y') for fdate in xticks.astype('datetime64[ns]')])
    axes.tick_params(axis='x', direction='in', length=0, labelcolor=_Y_LABEL_GREY, labelsize='xx-small')
    axes.tick_params(axis='y', direction='out', length=1.5, labelcolor=_Y_LABEL_GREY, labelsize='xx-small', color=(0, 0, 0, 0))
    axes.set_xbound(lower=-.5, upper=len(df) - .5)
    axes.set_frame_on(False)


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
    axes.fill_between(df['date'], df['close'], color=(*color[0:3], .1), edgecolor=None)
    axes.set_ybound(y_bounds)

    # Style Settings
    axes.grid(visible=True, linestyle=':', alpha=_GRID_ALPHA, zorder=0)
    axes.set_xticks(xticks)
    axes.set_xticklabels([fdate.date().strftime('%b-%y') for fdate in xticks.astype('datetime64[ns]')])
    axes.tick_params(axis='x', direction='in', length=0, labelcolor=_Y_LABEL_GREY, labelsize='xx-small')
    axes.tick_params(axis='y', direction='out', length=1.5, labelcolor=_Y_LABEL_GREY, labelsize='xx-small', color=(0, 0, 0, 0))
    axes.set_xbound(lower=-.5, upper=len(df) - .5)
    axes.set_frame_on(False)


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
    axes.set_frame_on(False)
    axes.yaxis.get_offset_text().set_fontsize('xx-small')


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
        axes.set_frame_on(False)

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
        axes.tick_params(axis='x', direction='in', length=0, labelcolor=_Y_LABEL_GREY, labelsize='xx-small')
        line_axes.tick_params(axis='y', direction='out', length=1.5, labelcolor=_Y_LABEL_GREY, labelsize='xx-small', color=(0, 0, 0, 0))
        line_axes.set_xbound(lower=-.5, upper=len(df) - .5)
        line_axes.set_frame_on(False)


