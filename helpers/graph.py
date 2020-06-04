import numpy as np
import matplotlib.pyplot as plt

"""
Helper functions for graph plotting in Jupyter notebooks.
"""

def show_values_on_bars(axs: plt.Axes, orient: str):
    """Display values in a barplot."""
    
    def _show_on_single_plot(ax: plt.Axes, orient: str):        
        for p in ax.patches:
            if orient == 'v':
                _x = p.get_x() + p.get_width() / 2
                _y = p.get_y() + p.get_height()
                value = '{:,.0f}'.format(p.get_height())
                rotation = 30
            elif orient == 'h':
                _x = p.get_x() + p.get_width() + 2.5
                _y = p.get_y() + p.get_height()
                value = '{:,.0f}'.format(p.get_width())
                rotation = 0

            ax.text(_x, _y, value, ha='center', rotation=rotation)

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _show_on_single_plot(ax, orient)
    else:
        _show_on_single_plot(axs, orient)
