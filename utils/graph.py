import numpy as np
import matplotlib.pyplot as plt

"""
Helper functions for graph plotting in Jupyter notebooks.
"""

def show_values_on_bars(axs: plt.Axes, orient: str):
    """Display values in a barplot."""
    
    def _show_on_single_plot(ax: plt.Axes, orient: str):
        for p in ax.patches:
            # print(f'{p.get_x()}, {p.get_y()} - {p.get_width()}, {p.get_height()}')
            if orient == 'v':
                _x = p.get_x() + p.get_width() / 2
                _y = p.get_y() + p.get_height()
                value = '{:,.0f}'.format(p.get_height())
                ha = 'center'
                rotation = 30
            elif orient == 'h':
                _x = p.get_x() + p.get_width()
                _y = p.get_y() + p.get_height() * 0.75
                value = '{:,.0f}'.format(p.get_width())
                ha = 'left'
                rotation = 0

            ax.text(_x, _y, value, ha=ha, rotation=rotation)

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _show_on_single_plot(ax, orient)
    else:
        _show_on_single_plot(axs, orient)
