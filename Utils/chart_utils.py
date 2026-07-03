import matplotlib.pyplot as plt
import pandas as pd

_GRID_ALPHA = .1
_GREEN = '#07880b'
_RED = '#b73b3d'


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
    axes.tick_params(axis='x', direction='in', length=0)
    axes.tick_params(axis='y', direction='out', length=1.5, labelcolor=(.9, .9, .9, .65), labelsize='xx-small', color=(0,0,0,0))
    axes.set_xbound(lower=-.5, upper=len(df) - .5)
    axes.set_frame_on(False)
