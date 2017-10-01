"""PIPlot.

Provide functions for plotting data obtained from PI.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('white')
sns.set_style({
    'lines.linewidth': 2.5,
    'axes.grid': True,
    'axes.linewidth': 0.1,
    'grid.color': '.9',
    'grid.linestyle': '--',
    'legend.frameon': True,
    'legend.framealpha': 0.2
    })


def PI_plot(tags, df, PIAttributes, ax=None,
            savefig=False, folder=None, figname=None):
    """Plot PI values.

    Parameters
    ----------
    tags : str
        String with the tags (e.g.: 'VI290003X VI290003Y')
    df : pd.DataFrame
        DataFrame with PI data.
    PIAttributes : dict
        Dictionary with PI tags metadata.
    ax : matplotlib.axes, optional
        Matplotlib axes where data will be plotted.
        If None creates a new.

    returns
    ax : matplotlib.axes
        Matplotlib axes with plotted data.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(16, 8))
    tags = tags.split(' ')
    tagunits = {}

    # checke how many units/axes
    for tag in tags:
        # check if unit is already in tagunits
        if not PIAttributes[tag]['engunits'] in tagunits.values():
            # create unit
            tagunits[tag] = PIAttributes[tag]['engunits']

    n_units = len(tagunits)
    units = [i for i in tagunits.values()]

    if n_units > 3:
        raise Exception('Cannot plot more than 3 units')

    if n_units == 1:
        for tag in tags:
            series = getattr(df, tag)
            ax.plot(series, label=tag)
            ax.set_ylabel(units[0])
            ax.set_xlabel('Time')
            ax.legend()
    else:
        axes = [ax.twinx() for i in range(len(tagunits) - 1)]
        axes.insert(0, ax)

    if n_units == 2:
        # set the labels
        for _ax, unit in zip(axes, tagunits.values()):
            _ax.set_ylabel(unit)

        # check unit for each tag and plot to the correct axes
        lines = []
        labels = []
        for tag in tags:
            unit = PIAttributes[tag]['engunits']
            idx = units.index(unit)
            series = getattr(df, tag)
            # Make solid lines for lines in ax0
            if idx == 0:
                line, = axes[idx].plot(series, label=tag)
                axes[idx].set_xlabel('Time')
            else:
                line, = axes[idx].plot(series, linestyle='--', alpha=0.3, label=tag)
                axes[idx].grid(False)
            lines.append(line)
            labels.append(line.get_label())
        ax = axes[0]
        box = ax.get_position()
        ax.legend(lines, labels, loc='center left', bbox_to_anchor=(1.1, 0.5))

    if n_units == 3:
        # set the labels
        for _ax, unit in zip(axes, tagunits.values()):
            _ax.set_ylabel(unit)

        # check unit for each tag and plot to the correct axes
        lines = []
        labels = []
        for tag in tags:
            unit = PIAttributes[tag]['engunits']
            idx = units.index(unit)
            series = getattr(df, tag)
            # Make solid lines for lines in ax0 and keep one color cycle
            next_color = axes[0]._get_lines.get_next_color()
            if idx == 0:
                line, = axes[idx].plot(series, label=tag, color=next_color)
                axes[idx].set_xlabel('Time')
            else:
                line, = axes[idx].plot(series, linestyle='--', color=next_color, alpha=0.5, label=tag)
                axes[idx].grid(False)
            lines.append(line)
            labels.append(line.get_label())
        ax = axes[0]
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(lines, labels, loc='center left', bbox_to_anchor=(1.2, 0.5))

        # Make some space on the right side for the extra y-axis.
        fig.subplots_adjust(right=0.75)

        # Move the last y-axis spine over to the right by 20% of the width of the axes
        axes[-1].spines['right'].set_position(('axes', 1.1))

        # To make the border of the right-most axis visible, we need to turn the frame
        # on. This hides the other plots, however, so we need to turn its fill off.
        axes[-1].set_frame_on(True)
        axes[-1].patch.set_visible(False)

    if savefig is True:
        if figname is None:
            start, end = (df.index[0], df.index[-1])
            if not start.day == end.day:
                start_hour, end_hour = ('', '')
            else:
                start_hour, end_hour = (('-' + str(start.hour)), ('-' + str(end.hour)))
            figname = (str(start.day) + '-' + str(start.month) + '-' + str(start.year) + start_hour
                       + '-' + str(end.day) + '-' + str(end.month) + '-' + str(end.year) + end_hour
                       + '-' + '_'.join(tags))
            fignamepdf = figname + '.pdf'
            fignamepng = figname + '.png'

        print(f'Saving figure as {folder + figname}')
        plt.tight_layout()
        plt.savefig(folder + fignamepdf, bbox_inches='tight')
        plt.savefig(folder + fignamepng, bbox_inches='tight')

    if n_units > 1:
        return axes
    else:
        return ax


def create_pi_attributes(tag, **kwargs):
    """Create PI attributes dictionary

    This function can be used to fake a PI attributes when the data
    is not available.

    Parameters
    ----------
    tag : str
        String with the tag name

    """
    keys = ['descriptor', 'exdesc', 'typicalvalue', 'engunits', 'zero', 'span',
            'pointtype', 'pointsource', 'scan', 'excmin', 'excmax', 'excdev',
            'shutdown', 'archiving', 'compressing', 'step', 'compmin',
            'compmax', 'compdev', 'creationdate', 'creator', 'changedate',
            'changer', 'displaydigits', 'location1', 'location2', 'location3',
            'location4', 'location5', 'filtercode', 'squareroot', 'totalcode',
            'convers', 'srcptid', 'instrumenttag', 'userint1', 'userint2',
            'userreal1', 'userreal2', 'ptowner', 'ptgroup', 'ptaccess',
            'ptsecurity', 'dataowner', 'datagroup', 'dataaccess',
            'datasecurity', 'pointid', 'recno', 'ptclassname', 'ptclassid',
            'ptclassrev', 'tag', 'sourcetag', 'digitalset', 'compdevpercent',
            'excdevpercent']

    piattr = {k: '' for k in keys}

    for k, v in kwargs.items():
        piattr[k] = v

    return piattr
