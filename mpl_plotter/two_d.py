import inspect
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib as mpl

from importlib import import_module

from matplotlib import cm
from matplotlib import font_manager as font_manager
from matplotlib.ticker import FormatStrFormatter

from mpl_plotter.resources.mock_data import MockData
from mpl_plotter.resources.functions import normalize
from mpl_plotter.resources.functions import print_color

# from matplotlib import rc
# from matplotlib import colors
# from matplotlib import dates as mdates
# from numpy import sin, cos
# from skimage import measure
# from matplotlib import ticker
# from pylab import floor


class plot:

    def method_setup(self):
        if isinstance(self.fig, type(None)):
            if not self.plt.get_fignums():
                self.method_figure()
            else:
                self.fig = self.plt.gcf()
                self.ax = self.plt.gca()

        if isinstance(self.ax, type(None)):
            self.ax = self.fig.add_subplot(self.shape_and_position, adjustable='box')

    def method_figure(self):
        if not isinstance(self.style, type(None)):
            self.plt.style.use(self.style)
        self.fig = self.plt.figure(figsize=self.figsize)

    def method_style(self):
        if self.light:
            self.workspace_color = 'black' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (193/256, 193/256, 193/256) if isinstance(self.workspace_color2, type(
                None)) else self.workspace_color2
            self.style = 'classic'
        elif self.dark:
            self.workspace_color = 'white' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (89 / 256, 89 / 256, 89 / 256) if isinstance(self.workspace_color2,
                                                                                 type(
                                                                                     None)) else self.workspace_color2
            self.style = 'dark_background'
        else:
            self.workspace_color = 'black' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (193 / 256, 193 / 256, 193 / 256) if isinstance(self.workspace_color2, type(
                None)) else self.workspace_color2
        self.ax.set_facecolor(self.background_color_plot)
        self.fig.patch.set_facecolor(self.background_color_figure)

        self.plt.rcParams["font.family"] = "serif"
        self.plt.rcParams["mathtext.fontset"] = "dejavuserif"

    def method_cb(self):
        if self.color_bar is True:
            if isinstance(self.norm, type(None)):
                return print_color("No norm selected for colorbar. Set norm=<parameter of choice>", "grey")

            # Obtain and apply limits
            if isinstance(self.cb_vmin, type(None)):
                self.cb_vmin = self.norm.min()
            if isinstance(self.cb_vmax, type(None)):
                self.cb_vmax = self.norm.max()
            self.graph.set_clim([self.cb_vmin, self.cb_vmax])

            # Normalization
            locator = np.linspace(self.cb_vmin, self.cb_vmax, self.cb_tick_number)

            # Colorbar
            cbar = self.fig.colorbar(self.graph,
                                     ax=self.ax,
                                     orientation=self.cb_orientation, shrink=self.shrink,
                                     ticks=locator, boundaries=locator if self.cb_hard_bounds is True else None,
                                     spacing='proportional',
                                     extend=self.extend,
                                     format='%.' + str(self.tick_ndecimals) + 'f',
                                     pad=self.cb_pad,
                                     )

            # Ticks
            #   Locator
            cbar.locator = locator
            #   Direction
            cbar.ax.tick_params(axis='y', direction='out')
            #   Tick label pad and size
            cbar.ax.yaxis.set_tick_params(pad=self.cb_axis_labelpad, labelsize=self.cb_ticklabelsize)

            # Colorbar title
            if self.cb_orientation == 'vertical':
                if not isinstance(self.cb_title,
                                  type(None)) and self.cb_y_title is False and self.cb_top_title is False:
                    print('Input colorbar title location with booleans: cb_y_title=True or cb_top_title=True')
                if self.cb_y_title is True:
                    cbar.ax.set_ylabel(self.cb_title, rotation=self.cb_title_rotation,
                                       labelpad=self.cb_ytitle_labelpad)
                    text = cbar.ax.yaxis.label
                    font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style,
                                                           size=self.cb_title_size,
                                                           weight=self.cb_title_weight)
                    text.set_font_properties(font)
                if self.cb_top_title is True:
                    cbar.ax.set_title(self.cb_title, rotation=self.cb_title_rotation,
                                      fontdict={'verticalalignment': 'baseline',
                                                'horizontalalignment': 'left'},
                                      pad=self.cb_top_title_pad)
                    cbar.ax.title.set_position((self.cb_top_title_x, self.cb_top_title_y))
                    text = cbar.ax.title
                    font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style,
                                                           weight=self.cb_title_weight,
                                                           size=self.cb_title_size)
                    text.set_font_properties(font)
            elif self.cb_orientation == 'horizontal':
                cbar.ax.set_xlabel(self.cb_title, rotation=self.cb_title_rotation, labelpad=self.cb_ytitle_labelpad)
                text = cbar.ax.xaxis.label
                font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style,
                                                       size=self.cb_title_size,
                                                       weight=self.cb_title_weight)
                text.set_font_properties(font)

            # Outline
            cbar.outline.set_edgecolor(self.workspace_color2)
            cbar.outline.set_linewidth(self.cb_outline_width)

    def method_legend(self):
        if self.legend is True:
            lines_labels = [ax.get_legend_handles_labels() for ax in self.fig.axes]
            lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
            legend_font = font_manager.FontProperties(family=self.font,
                                                      weight=self.legend_weight,
                                                      style=self.legend_style,
                                                      size=self.legend_size)
            self.fig.legend(lines, labels,
                            loc=self.legend_loc, prop=legend_font,
                            handleheight=self.legend_handleheight, ncol=self.legend_ncol)

    def method_resize_axes(self):

        # Bound definition
        if not isinstance(self.x_bounds, type(None)):
            if not isinstance(self.x_bounds[0], type(None)):
                self.x_lower_bound = self.x_bounds[0]
            if not isinstance(self.x_bounds[1], type(None)):
                self.x_upper_bound = self.x_bounds[1]
        if not isinstance(self.y_bounds, type(None)):
            if not isinstance(self.y_bounds[0], type(None)):
                self.y_lower_bound = self.y_bounds[0]
            if not isinstance(self.y_bounds[1], type(None)):
                self.y_upper_bound = self.y_bounds[1]

        if self.resize_axes is True:

            def bounds(d, u, l, up, lp, v):
                # Upper and lower bounds
                if isinstance(u, type(None)):
                    u = d.max()
                else:
                    up = 0
                if isinstance(l, type(None)):
                    l = d.min()
                else:
                    lp = 0
                # Bounds vector
                if isinstance(v, type(None)):
                    v = [self.x_lower_bound, self.x_upper_bound]
                if isinstance(v[0], type(None)):
                    v[0] = l
                if isinstance(v[1], type(None)):
                    v[1] = u
                return v, up, lp

            self.x_bounds, self.x_upper_resize_pad, self.x_lower_resize_pad = bounds(self.x,
                                                                                     self.x_upper_bound,
                                                                                     self.x_lower_bound,
                                                                                     self.x_upper_resize_pad,
                                                                                     self.x_lower_resize_pad,
                                                                                     self.x_bounds)
            self.y_bounds, self.y_upper_resize_pad, self.y_lower_resize_pad = bounds(self.y,
                                                                                     self.y_upper_bound,
                                                                                     self.y_lower_bound,
                                                                                     self.y_upper_resize_pad,
                                                                                     self.y_lower_resize_pad,
                                                                                     self.y_bounds)

            if self.demo_pad_plot is True:
                pad_x = 0.05 * (abs(self.x.max()) + abs(self.x.min()))
                self.x_upper_resize_pad = pad_x
                self.x_lower_resize_pad = pad_x
                pad_y = 0.05 * (abs(self.y.max()) + abs(self.y.min()))
                self.y_upper_resize_pad = pad_y
                self.y_lower_resize_pad = pad_y

            if not isinstance(self.aspect, type(None)):
                self.ax.set_aspect(self.aspect)

            self.ax.set_xbound(lower=self.x_bounds[0] - self.x_lower_resize_pad,
                               upper=self.x_bounds[1] + self.x_upper_resize_pad)
            self.ax.set_ybound(lower=self.y_bounds[0] - self.y_lower_resize_pad,
                               upper=self.y_bounds[1] + self.y_upper_resize_pad)

            self.ax.set_xlim(self.x_bounds[0] - self.x_lower_resize_pad,
                             self.x_bounds[1] + self.x_upper_resize_pad)
            self.ax.set_ylim(self.y_bounds[0] - self.y_lower_resize_pad,
                             self.y_bounds[1] + self.y_upper_resize_pad)

    def method_background_alpha(self):
        self.ax.patch.set_alpha(1)

    def method_title(self):
        if not isinstance(self.title, type(None)):

            self.ax.set_title(self.title,
                              fontname=self.font if isinstance(self.title_font, type(None)) else self.title_font,
                              weight=self.title_weight,
                              color=self.workspace_color if isinstance(self.title_color, type(None)) else self.title_color,
                              size=self.title_size)
            self.ax.title.set_position((0.5, self.title_y))

    def method_axis_labels(self):
        if not isinstance(self.x_label, type(None)):

            # Draw label
            self.ax.set_xlabel(self.x_label, fontname=self.font, weight=self.x_label_weight,
                               color=self.workspace_color, size=self.x_label_size, labelpad=self.x_label_pad,
                               rotation=self.x_label_rotation)

            # Custom coordinates if provided
            if not isinstance(self.x_label_coords, type(None)):
                self.ax.yaxis.set_label_coords(self.x_label_coords)

        if not isinstance(self.y_label, type(None)):

            # y axis label rotation
            if isinstance(self.y_label_rotation, type(None)):
                self.y_label_rotation = 90 if len(self.y_label) > 3 else 0

            # Draw label
            self.ax.set_ylabel(self.y_label, fontname=self.font, weight=self.y_label_weight,
                               color=self.workspace_color, size=self.y_label_size, labelpad=self.y_label_pad,
                               rotation=self.y_label_rotation)

            # Custom coordinates if provided
            if not isinstance(self.y_label_coords, type(None)):
                self.ax.yaxis.set_label_coords(self.y_label_coords)

    def method_spines(self):
        for spine in self.ax.spines.values():
            spine.set_color(self.workspace_color if isinstance(self.spine_color, type(None)) else self.spine_color)

        top = True
        right = True
        left = True
        bottom = True

        for spine in self.spines_removed:
            self.ax.spines[spine].set_visible(False)
            if spine == 'top':
                top = False
            if spine == 'bottom':
                bottom = False
            if spine == 'left':
                left = False
            if spine == 'right':
                right = False

        self.ax.tick_params(axis='both', which='both', top=top, right=right, left=left, bottom=bottom)

    def method_ticks(self):
        #   Tick-label distance
        self.ax.xaxis.set_tick_params(pad=0.1, direction='in')
        self.ax.yaxis.set_tick_params(pad=0.1, direction='in')
        #   Color
        if not isinstance(self.tick_color, type(None)):
            self.ax.tick_params(axis='both', color=self.tick_color)
        #   Label font and color
        for tick in self.ax.get_xticklabels():
            tick.set_fontname(self.font)
            tick.set_color(self.workspace_color)
        for tick in self.ax.get_yticklabels():
            tick.set_fontname(self.font)
            tick.set_color(self.workspace_color)
        #   Label size
        if not isinstance(self.tick_label_size_x, type(None)):
            self.ax.tick_params(axis='x', labelsize=self.tick_label_size_x)
        if not isinstance(self.tick_label_size_y, type(None)):
            self.ax.tick_params(axis='y', labelsize=self.tick_label_size_y)
        if not isinstance(self.tick_label_size, type(None)):
            self.ax.tick_params(axis='both', labelsize=self.tick_label_size)
        #   Number and custom position ---------------------------------------------------------------------------------
        if not isinstance(self.x_tick_number, type(None)):
            self.ax.set_xticks(np.linspace(
                self.x_tick_labels[0] if not isinstance(self.x_tick_labels, type(None)) else self.ax.get_xlim()[0],
                self.x_tick_labels[1] if not isinstance(self.x_tick_labels, type(None)) else self.ax.get_xlim()[1],
                self.x_tick_number))
        if not isinstance(self.y_tick_number, type(None)):
            self.ax.set_yticks(np.linspace(
                self.y_tick_labels[0] if not isinstance(self.y_tick_labels, type(None)) else self.ax.get_ylim()[0],
                self.y_tick_labels[1] if not isinstance(self.y_tick_labels, type(None)) else self.ax.get_ylim()[1],
                self.y_tick_number))
        #   Prune
        if not isinstance(self.prune, type(None)):
            self.ax.xaxis.set_major_locator(self.plt.MaxNLocator(prune=self.prune))
        if not isinstance(self.prune, type(None)):
            self.ax.yaxis.set_major_locator(self.plt.MaxNLocator(prune=self.prune))
        #   Float format
        float_format = '%.' + str(self.tick_ndecimals) + 'f'
        self.ax.xaxis.set_major_formatter(FormatStrFormatter(float_format))
        self.ax.yaxis.set_major_formatter(FormatStrFormatter(float_format))
        #   Custom tick labels
        if not isinstance(self.custom_x_tick_labels, type(None)):
            self.ax.set_xticklabels(np.round(np.linspace(self.custom_x_tick_labels[0],
                                                         self.custom_x_tick_labels[1],
                                                         self.x_tick_number),
                                             self.tick_ndecimals))
        if not isinstance(self.custom_y_tick_labels, type(None)):
            self.ax.set_yticklabels(np.round(np.linspace(self.custom_y_tick_labels[0],
                                                         self.custom_y_tick_labels[1],
                                                         self.y_tick_number),
                                             self.tick_ndecimals))
        #       Date tick labels
        if self.date_tick_labels_x is True:
            fmtd = pd.date_range(start=self.x[0], end=self.x[-1], periods=self.x_tick_number)
            fmtd = [dt.datetime.strftime(d, self.date_format) for d in fmtd]
            self.ax.set_xticklabels(fmtd)

        #   Tick-label pad ---------------------------------------------------------------------------------------------
        if not isinstance(self.tick_label_pad, type(None)):
            self.ax.tick_params(axis='both', pad=self.tick_label_pad)
        #   Rotation
        if not isinstance(self.x_tick_rotation, type(None)):
            self.ax.tick_params(axis='x', rotation=self.x_tick_rotation)
            for tick in self.ax.xaxis.get_majorticklabels():
                tick.set_horizontalalignment("right")
        if not isinstance(self.y_tick_rotation, type(None)):
            self.ax.tick_params(axis='y', rotation=self.y_tick_rotation)
            for tick in self.ax.yaxis.get_majorticklabels():
                tick.set_horizontalalignment("left")

    def method_grid(self):
        if self.grid is not False:
            self.plt.grid(linestyle=self.grid_lines, color=self.grid_color)

    def method_save(self):
        if self.filename:
            self.plt.savefig(self.filename, dpi=self.dpi)

    def method_show(self):
        if self.more_subplots_left is not True:
            self.fig.tight_layout()
            self.plt.show()
        else:
            print('Ready for next subplot')


class input_st():

    def init(self):
        if not isinstance(self.backend, type(None)):
            try:
                mpl.use(self.backend)
            except AttributeError:
                raise AttributeError('{} backend not supported with current Python configuration'.format(self.backend))

        # matplotlib.use() must be called *before* pylab, matplotlib.pyplot,
        # or matplotlib.backends is imported for the first time.

        self.plt = import_module("matplotlib.pyplot")

        """
        Run
        """

        self.run()

    def run(self):

        self.method_setup()

        self.method_style()

        # Mock plot
        self.mock()

        # Main
        self.main()

        # Colorbar
        self.method_cb()

        # Legend
        self.method_legend()

        # Resize axes
        self.method_resize_axes()

        # Makeup
        self.method_background_alpha()
        self.method_title()
        self.method_axis_labels()
        self.method_spines()
        self.method_ticks()
        self.method_grid()

        # Save
        self.method_save()

        self.method_show()

        return self.ax


class input_df:

    def init(self):
        if not isinstance(self.backend, type(None)):
            try:
                mpl.use(self.backend)
            except AttributeError:
                raise AttributeError('{} backend not supported with current Python configuration'.format(self.backend))

        # matplotlib.use() must be called *before* pylab, matplotlib.pyplot,
        # or matplotlib.backends is imported for the first time.

        self.plt = import_module("matplotlib.pyplot")

        """
        Run
        """

        self.run()

    def run(self):

        self.method_setup()

        self.method_style()

        # Mock plot
        self.mock()

        # Main
        self.main()

        # Colorbar
        self.method_cb()

        # Makeup
        self.method_background_alpha()
        self.method_title()
        self.method_axis_labels()
        self.method_spines()
        self.method_ticks()
        self.method_grid()

        # Save
        self.method_save()

        self.method_show()

        return self.ax

    def method_resize_axes_coordinates(self):
        if self.resize_axes is True:
            if isinstance(self.x_upper_bound, type(None)):
                self.x_upper_bound = self.x.max()
            else:
                self.x_upper_resize_pad = 0
            if isinstance(self.x_lower_bound, type(None)):
                self.x_lower_bound = self.x.min()
            else:
                self.x_lower_resize_pad = 0

            if isinstance(self.y_upper_bound, type(None)):
                self.y_upper_bound = self.y.max()
            else:
                self.y_upper_resize_pad = 0
            if isinstance(self.y_lower_bound, type(None)):
                self.y_lower_bound = self.y.min()
            else:
                self.y_lower_resize_pad = 0

            if isinstance(self.x_upper_resize_pad, type(None)):
                self.x_upper_resize_pad = 0.05*(self.x_upper_bound-self.x_lower_bound)
            if isinstance(self.x_lower_resize_pad, type(None)):
                self.x_lower_resize_pad = 0.05*(self.x_upper_bound-self.x_lower_bound)
            if isinstance(self.y_upper_resize_pad, type(None)):
                self.y_upper_resize_pad = 0.05*(self.y_upper_bound-self.y_lower_bound)
            if isinstance(self.y_lower_resize_pad, type(None)):
                self.y_lower_resize_pad = 0.05*(self.y_upper_bound-self.y_lower_bound)

            if not isinstance(self.aspect, type(None)):
                self.ax.set_aspect(self.aspect)

            self.ax.set_xbound(lower=self.x_lower_bound - self.x_lower_resize_pad,
                               upper=self.x_upper_bound + self.x_upper_resize_pad)
            self.ax.set_ybound(lower=self.y_lower_bound - self.y_lower_resize_pad,
                               upper=self.y_upper_bound + self.y_upper_resize_pad)

            self.ax.set_xlim(self.x_lower_bound - self.x_lower_resize_pad, self.x_upper_bound + self.x_upper_resize_pad)
            self.ax.set_ylim(self.y_lower_bound - self.y_lower_resize_pad, self.y_upper_bound + self.y_upper_resize_pad)

    def method_resize_axes_dataframe(self):
        if not isinstance(self.z, type(pd.DataFrame)):
            xmin = 0
            ymin = 0
            xmax = self.z.shape[0]
            ymax = self.z.shape[1]
            if self.resize_axes is True:
                if isinstance(self.x_upper_bound, type(None)):
                    self.x_upper_bound = xmax
                if isinstance(self.x_lower_bound, type(None)):
                    self.x_lower_bound = xmin
                if isinstance(self.y_upper_bound, type(None)):
                    self.y_upper_bound = ymax
                if isinstance(self.y_lower_bound, type(None)):
                    self.y_lower_bound = ymin


class line(plot, input_st):

    def __init__(self,
                 # Specifics
                 x=None, y=None,
                 line_width=3,
                 # Base
                 backend='Qt5Agg', plot_label="Line", font='serif',
                 # Figure, axis
                 fig=None, ax=None, figsize=None, shape_and_position=111,
                 # Setup
                 prune=None, resize_axes=True, aspect=None,
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white',
                 style=None, light=None, dark=None,
                 # Spines
                 spine_color=None, spines_removed=('top', 'right'),
                 # Bounds
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 # Pads
                 demo_pad_plot=False,
                 x_upper_resize_pad=0, x_lower_resize_pad=0,
                 y_upper_resize_pad=0, y_lower_resize_pad=0,
                 # Grid
                 grid=False, grid_color='black', grid_lines='-.',
                 # Color
                 color='darkred', cmap='RdBu_r', alpha=None, norm=None,
                 # Title
                 title=None, title_size=12, title_y=1.025, title_weight=None, title_font=None, title_color=None,
                 # Labels
                 x_label=None, x_label_size=12, x_label_pad=10, x_label_rotation=None, x_label_weight=None,
                 y_label=None, y_label_size=12, y_label_pad=10, y_label_rotation=None, y_label_weight=None,
                 # Ticks
                 x_tick_number=5, x_tick_labels=None,
                 y_tick_number=5, y_tick_labels=None,
                 x_tick_rotation=None, y_tick_rotation=None, x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5, tick_ndecimals=1,
                 # Tick labels
                 tick_label_size=None, tick_label_size_x=None, tick_label_size_y=None,
                 custom_x_tick_labels=None, custom_y_tick_labels=None, date_tick_labels_x=False, date_format='%Y-%m-%d',
                 # Color bar
                 color_bar=False, cb_pad=0.2, extend='neither',
                 cb_title=None, cb_orientation='vertical', cb_axis_labelpad=10, cb_tick_number=5, shrink=0.75,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, cb_top_title_x=0, cb_vmin=None, cb_vmax=None,
                 cb_ticklabelsize=10, cb_hard_bounds=False,
                 # Legend
                 legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 more_subplots_left=True, zorder=None,
                 # Save
                 filename=None, dpi=None,
                 ):
        """
        Line plot class
        mpl_plotter - 2D
        :param backend: Interactive plotting backends. Working with Python 3.7.6: Qt5Agg, QT4Agg, TkAgg.
                        Backend error:
                            pip install pyqt5
                            pip install tkinter
                            pip install tk
                            ... stackoverflow
                        Plotting window freezes even if trying different backends with no backend error: python configuration problem
                            backend=None
        """

        # Turn all instance arguments to instance attributes
        for item in inspect.signature(line).parameters:
            setattr(self, item, eval(item))

        self.init()

    def main(self):

        if isinstance(self.norm, type(None)):
            self.graph = self.ax.plot(self.x, self.y, label=self.plot_label, linewidth=self.line_width, color=self.color,
                                      zorder=self.zorder,
                                      alpha=self.alpha,
                                      )
        else:
            # Create a set of line segments so that we can color them individually
            # This creates the points as a N x 1 x 2 array so that we can stack points
            # together easily to get the segments. The segments array for line collection
            # needs to be (numlines) x (points per line) x 2 (for x and y)
            points = np.array([self.x, self.y]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)

            # Create a continuous norm to map from data points to colors
            _norm = self.norm(self.x) if hasattr(self.norm, '__call__') else self.norm
            norm = self.plt.Normalize(_norm.min(), _norm.max())
            lc = mpl.collections.LineCollection(segments, cmap=self.cmap, norm=norm)

            # Set the values used for colormapping
            lc.set_array(self.norm)
            lc.set_linewidth(self.line_width)
            self.graph = self.ax.add_collection(lc)

    def mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.x, self.y = MockData().spirograph()


class scatter(plot, input_st):

    def __init__(self,
                 # Specifics
                 point_size=5, marker='o',
                 # Base
                 x=None, y=None,
                 backend='Qt5Agg', plot_label="Scatter plot", font='serif',
                 # Figure, axis
                 fig=None, ax=None, figsize=None, shape_and_position=111,
                 # Setup
                 prune=None, resize_axes=True, aspect=None,
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white',
                 style=None, light=None, dark=None,
                 # Spines
                 spine_color=None, spines_removed=('top', 'right'),
                 # Bounds
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 # Pads
                 demo_pad_plot=False,
                 x_upper_resize_pad=0, x_lower_resize_pad=0,
                 y_upper_resize_pad=0, y_lower_resize_pad=0,
                 # Grid
                 grid=False, grid_color='black', grid_lines='-.',
                 # Color
                 color="C0", cmap='RdBu_r', alpha=None, norm=None,
                 # Title
                 title=None, title_size=12, title_y=1.025, title_weight=None, title_font=None, title_color=None,
                 # Labels
                 x_label=None, x_label_size=12, x_label_pad=10, x_label_rotation=None, x_label_weight=None,
                 y_label=None, y_label_size=12, y_label_pad=10, y_label_rotation=None, y_label_weight=None,
                 # Ticks
                 x_tick_number=5, x_tick_labels=None,
                 y_tick_number=5, y_tick_labels=None,
                 x_tick_rotation=None, y_tick_rotation=None, x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5, tick_ndecimals=1,
                 # Tick labels
                 tick_label_size=None, tick_label_size_x=None, tick_label_size_y=None,
                 custom_x_tick_labels=None, custom_y_tick_labels=None, date_tick_labels_x=False, date_format='%Y-%m-%d',
                 # Color bar
                 color_bar=False, cb_pad=0.2, extend='neither',
                 cb_title=None, cb_orientation='vertical', cb_axis_labelpad=10, cb_tick_number=5, shrink=0.75,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, cb_top_title_x=0, cb_vmin=None, cb_vmax=None,
                 cb_ticklabelsize=10, cb_hard_bounds=False,
                 # Legend
                 legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 more_subplots_left=True, zorder=None,
                 # Save
                 filename=None, dpi=None,
                 ):
        """
        Scatter plot class
        mpl_plotter - 2D
        :param backend: Interactive plotting backends. Working with Python 3.7.6: Qt5Agg, QT4Agg, TkAgg.
                        Backend error:
                            pip install pyqt5
                            pip install tkinter
                            pip install tk
                            ... stackoverflow
                        Plotting window freezes even if trying different backends with no backend error: python configuration problem
                            backend=None
        """

        # Turn all instance arguments to instance attributes
        for item in inspect.signature(scatter).parameters:
            setattr(self, item, eval(item))

        self.init()

    def main(self):

        if not isinstance(self.norm, type(None)):
            self.graph = self.ax.scatter(self.x, self.y, label=self.plot_label, s=self.point_size, marker=self.marker,
                                         c=self.norm, cmap=self.cmap,
                                         zorder=self.zorder,
                                         alpha=self.alpha)
        else:
            self.graph = self.ax.scatter(self.x, self.y, label=self.plot_label, s=self.point_size, marker=self.marker,
                                         color=self.color,
                                         zorder=self.zorder,
                                         alpha=self.alpha)

    def mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.x, self.y = MockData().spirograph()
            self.norm = self.y


class heatmap(plot, input_df):

    def __init__(self,
                 # Specifics
                 x=None, y=None, z=None, normvariant='SymLog',
                 # Base
                 backend='Qt5Agg', plot_label="Heatmap", font='serif',
                 # Figure, axis
                 fig=None, ax=None, figsize=None, shape_and_position=111,
                 # Setup
                 prune=None, resize_axes=True, aspect=None,
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white',
                 style=None, light=None, dark=None,
                 # Spines
                 spine_color=None, spines_removed=('top', 'right'),
                 # Bounds
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 # Pads
                 demo_pad_plot=False,
                 x_upper_resize_pad=0, x_lower_resize_pad=0,
                 y_upper_resize_pad=0, y_lower_resize_pad=0,
                 # Grid
                 grid=False, grid_color='black', grid_lines='-.',
                 # Color
                 color=None, cmap='RdBu_r', alpha=None, norm=None,
                 # Title
                 title=None, title_size=12, title_y=1.025, title_weight=None, title_font=None, title_color=None,
                 # Labels
                 x_label=None, x_label_size=12, x_label_pad=10, x_label_rotation=None, x_label_weight=None,
                 y_label=None, y_label_size=12, y_label_pad=10, y_label_rotation=None, y_label_weight=None,
                 # Ticks
                 x_tick_number=5, x_tick_labels=None,
                 y_tick_number=5, y_tick_labels=None,
                 x_tick_rotation=None, y_tick_rotation=None, x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5, tick_ndecimals=1,
                 # Tick labels
                 tick_label_size=None, tick_label_size_x=None, tick_label_size_y=None,
                 custom_x_tick_labels=None, custom_y_tick_labels=None, date_tick_labels_x=False, date_format='%Y-%m-%d',
                 # Color bar
                 color_bar=False, cb_pad=0.2, extend='neither',
                 cb_title=None, cb_orientation='vertical', cb_axis_labelpad=10, cb_tick_number=5, shrink=0.75,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, cb_top_title_x=0, cb_vmin=None, cb_vmax=None,
                 cb_ticklabelsize=10, cb_hard_bounds=False,
                 # Legend
                 legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 more_subplots_left=True, zorder=None,
                 # Save
                 filename=None, dpi=None,
                 ):
        """
        Heatmap plot class
        mpl_plotter - 2D
        :param backend: Interactive plotting backends. Working with Python 3.7.6: Qt5Agg, QT4Agg, TkAgg.
                        Backend error:
                            pip install pyqt5
                            pip install tkinter
                            pip install tk
                            ... stackoverflow
                        Plotting window freezes even if trying different backends with no backend error: python configuration problem
                            backend=None
        """
        # Turn all instance arguments to instance attributes
        for item in inspect.signature(heatmap).parameters:
            setattr(self, item, eval(item))

        self.init()

    def main(self):

        if not isinstance(self.x, type(None)) and not isinstance(self.y, type(None)):
            self.graph = self.ax.pcolormesh(self.x, self.y, self.z, cmap=self.cmap,
                                            zorder=self.zorder,
                                            alpha=self.alpha,
                                            label=self.plot_label,
                                            )
            # Resize axes
            self.method_resize_axes_coordinates()

        else:
            self.graph = self.ax.pcolormesh(self.z, cmap=self.cmap, norm=self.norm,
                                            zorder=self.zorder,
                                            alpha=self.alpha,
                                            label=self.plot_label,)
            # Resize axes
            self.method_resize_axes_dataframe()

    def mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.z = MockData().waterdropdf()


class quiver(plot, input_st):

    def __init__(self,
                 # Specifics
                 x=None, y=None, u=None, v=None,
                 rule=None, custom_rule=None, vector_width=0.01, vector_min_shaft=2, vector_length_threshold=0.1,
                 # Base
                 backend='Qt5Agg', plot_label="Quiver", font='serif',
                 # Figure, axis
                 fig=None, ax=None, figsize=None, shape_and_position=111,
                 # Setup
                 prune=None, resize_axes=True, aspect=None,
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white',
                 style=None, light=None, dark=None,
                 # Spines
                 spine_color=None, spines_removed=('top', 'right'),
                 # Bounds
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 # Pads
                 demo_pad_plot=False,
                 x_upper_resize_pad=0, x_lower_resize_pad=0,
                 y_upper_resize_pad=0, y_lower_resize_pad=0,
                 # Grid
                 grid=False, grid_color='black', grid_lines='-.',
                 # Color
                 color=None, cmap='RdBu_r', alpha=None, norm=None,
                 # Title
                 title=None, title_size=12, title_y=1.025, title_weight=None, title_font=None, title_color=None,
                 # Labels
                 x_label=None, x_label_size=12, x_label_pad=10, x_label_rotation=None, x_label_weight=None,
                 y_label=None, y_label_size=12, y_label_pad=10, y_label_rotation=None, y_label_weight=None,
                 # Ticks
                 x_tick_number=5, x_tick_labels=None,
                 y_tick_number=5, y_tick_labels=None,
                 x_tick_rotation=None, y_tick_rotation=None, x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5, tick_ndecimals=1,
                 # Tick labels
                 tick_label_size=None, tick_label_size_x=None, tick_label_size_y=None,
                 custom_x_tick_labels=None, custom_y_tick_labels=None, date_tick_labels_x=False, date_format='%Y-%m-%d',
                 # Color bar
                 color_bar=False, cb_pad=0.2, extend='neither',
                 cb_title=None, cb_orientation='vertical', cb_axis_labelpad=10, cb_tick_number=5, shrink=0.75,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, cb_top_title_x=0, cb_vmin=None, cb_vmax=None,
                 cb_ticklabelsize=10, cb_hard_bounds=False,
                 # Legend
                 legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 more_subplots_left=True, zorder=None,
                 # Save
                 filename=None, dpi=None,
                 ):
        """
        Quiver plot class
        mpl_plotter - 2D
        :param backend: Interactive plotting backends. Working with Python 3.7.6: Qt5Agg, QT4Agg, TkAgg.
                        Backend error:
                            pip install pyqt5
                            pip install tkinter
                            pip install tk
                            ... stackoverflow
                        Plotting window freezes even if trying different backends with no backend error: python configuration problem
                            backend=None
        """
        # Turn all instance arguments to instance attributes
        for item in inspect.signature(quiver).parameters:
            setattr(self, item, eval(item))

        self.init()

    def main(self):

        # Color rule
        self.method_rule()

        self.graph = self.ax.quiver(self.x, self.y, self.u, self.v,
                                    color=self.color, cmap=self.cmap,
                                    width=self.vector_width,
                                    minshaft=self.vector_min_shaft,
                                    minlength=self.vector_length_threshold,
                                    label=self.plot_label,
                                    zorder=self.zorder,
                                    alpha=self.alpha
                                    )

    def mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.x = np.random.random(100)
            self.y = np.random.random(100)
            self.u = np.random.random(100)
            self.v = np.random.random(100)
            self.norm = np.sqrt(self.u**2+self.v**2)

    def method_rule(self):
        # Rule
        if isinstance(self.custom_rule, type(None)):
            if isinstance(self.rule, type(None)):
                self.rule = lambda u, v: (u ** 2 + v ** 2)
            self.rule = self.rule(u=self.u, v=self.v)
        else:
            self.rule = self.custom_rule

        # Color determined by rule function
        c = self.rule
        # Flatten and normalize
        c = (c.ravel() - c.min()) / c.ptp()
        # Repeat for each body line and two head lines
        c = np.concatenate((c, np.repeat(c, 2)))
        # Colormap
        cmap = mpl.cm.get_cmap(self.cmap)
        self.color = cmap(c)


class streamline(plot, input_st):

    def __init__(self,
                 # Specifics
                 x=None, y=None, u=None, v=None, line_width=1, line_density=2,
                 # Base
                 backend='Qt5Agg', plot_label="Streamline", font='serif',
                 # Figure, axis
                 fig=None, ax=None, figsize=None, shape_and_position=111,
                 # Setup
                 prune=None, resize_axes=True, aspect=None,
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white',
                 style=None, light=None, dark=None,
                 # Spines
                 spine_color=None, spines_removed=('top', 'right'),
                 # Bounds
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 # Pads
                 demo_pad_plot=False,
                 x_upper_resize_pad=0, x_lower_resize_pad=0,
                 y_upper_resize_pad=0, y_lower_resize_pad=0,
                 # Grid
                 grid=False, grid_color='black', grid_lines='-.',
                 # Color
                 color=None, cmap='RdBu_r', alpha=None, norm=None,
                 # Title
                 title=None, title_size=12, title_y=1.025, title_weight=None, title_font=None, title_color=None,
                 # Labels
                 x_label=None, x_label_size=12, x_label_pad=10, x_label_rotation=None, x_label_weight=None,
                 y_label=None, y_label_size=12, y_label_pad=10, y_label_rotation=None, y_label_weight=None,
                 # Ticks
                 x_tick_number=5, x_tick_labels=None,
                 y_tick_number=5, y_tick_labels=None,
                 x_tick_rotation=None, y_tick_rotation=None, x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5, tick_ndecimals=1,
                 # Tick labels
                 tick_label_size=None, tick_label_size_x=None, tick_label_size_y=None,
                 custom_x_tick_labels=None, custom_y_tick_labels=None, date_tick_labels_x=False, date_format='%Y-%m-%d',
                 # Color bar
                 color_bar=False, cb_pad=0.2, extend='neither',
                 cb_title=None, cb_orientation='vertical', cb_axis_labelpad=10, cb_tick_number=5, shrink=0.75,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, cb_top_title_x=0, cb_vmin=None, cb_vmax=None,
                 cb_ticklabelsize=10, cb_hard_bounds=False,
                 # Legend
                 legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 more_subplots_left=True, zorder=None,
                 # Save
                 filename=None, dpi=None,
                 ):
        """
        Streamline class
        mpl_plotter - 2D
        :param backend: Interactive plotting backends. Working with Python 3.7.6: Qt5Agg, QT4Agg, TkAgg.
                        Backend error:
                            pip install pyqt5
                            pip install tkinter
                            pip install tk
                            ... stackoverflow
                        Plotting window freezes even if trying different backends with no backend error: python configuration problem
                            backend=None
        """

        # Turn all instance arguments to instance attributes
        for item in inspect.signature(streamline).parameters:
            setattr(self, item, eval(item))

        self.init()

    def main(self):

        # Color rule
        self.method_rule()

        # Plot
        self.graph = self.ax.streamplot(self.x, self.y, self.u, self.v,
                                        color=self.color,
                                        cmap=self.cmap,
                                        linewidth=self.line_width,
                                        density=self.line_density,
                                        zorder=self.zorder,
                                        ).lines

    def mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.x = np.linspace(0, 10, 100)
            self.y = np.linspace(0, 10, 100)
            self.x, self.y = np.meshgrid(self.x, self.y)
            self.u = np.random.random(100)
            self.v = np.random.random(100)
            self.u, self.v = np.meshgrid(self.u, self.v)

    def method_rule(self):
        if isinstance(self.color, type(None)):
            rule_color = lambda u: np.sqrt(self.u**2+self.v**2)/np.sqrt(self.u.max()**2+self.v.max()**2)
            self.color = rule_color(self.u)


class fill_area(plot, input_st):

    def __init__(self,
                 # Specifics
                 z=None,
                 between=False,
                 below=False,
                 above=False,
                 # Base
                 x=None, y=None,
                 backend='Qt5Agg', plot_label=None, font='serif',
                 # Figure, axis
                 fig=None, ax=None, figsize=None, shape_and_position=111,
                 # Setup
                 prune=None, resize_axes=True, aspect=None,
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white',
                 style=None, light=None, dark=None,
                 # Spines
                 spine_color=None, spines_removed=('top', 'right'),
                 # Bounds
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 # Pads
                 demo_pad_plot=False,
                 x_upper_resize_pad=0, x_lower_resize_pad=0,
                 y_upper_resize_pad=0, y_lower_resize_pad=0,
                 # Grid
                 grid=False, grid_color='black', grid_lines='-.',
                 # Color
                 color=None, cmap='RdBu_r', alpha=None, norm=None,
                 # Title
                 title=None, title_size=12, title_y=1.025, title_weight=None, title_font=None, title_color=None,
                 # Labels
                 x_label=None, x_label_size=12, x_label_pad=10, x_label_rotation=None, x_label_weight=None,
                 y_label=None, y_label_size=12, y_label_pad=10, y_label_rotation=None, y_label_weight=None,
                 # Ticks
                 x_tick_number=5, x_tick_labels=None,
                 y_tick_number=5, y_tick_labels=None,
                 x_tick_rotation=None, y_tick_rotation=None, x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5, tick_ndecimals=1,
                 # Tick labels
                 tick_label_size=None, tick_label_size_x=None, tick_label_size_y=None,
                 custom_x_tick_labels=None, custom_y_tick_labels=None, date_tick_labels_x=False, date_format='%Y-%m-%d',
                 # Color bar
                 color_bar=False, cb_pad=0.2, extend='neither',
                 cb_title=None, cb_orientation='vertical', cb_axis_labelpad=10, cb_tick_number=5, shrink=0.75,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, cb_top_title_x=0, cb_vmin=None, cb_vmax=None,
                 cb_ticklabelsize=10, cb_hard_bounds=False,
                 # Legend
                 legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 more_subplots_left=True, zorder=None,
                 # Save
                 filename=None, dpi=None,
                 ):

        """
        Fill area class
        mpl_plotter - 2D
        :param backend: Interactive plotting backends. Working with Python 3.7.6: Qt5Agg, QT4Agg, TkAgg.
                        Backend error:
                            pip install pyqt5
                            pip install tkinter
                            pip install tk
                            ... stackoverflow
                        Plotting window freezes even if trying different backends with no backend error: python configuration problem
                            backend=None
        """

        # Turn all instance arguments to instance attributes
        for item in inspect.signature(fill_area).parameters:
            setattr(self, item, eval(item))

        self.init()

    def main(self):

        """
        Fill the region below the intersection of S and Z
        """
        if not isinstance(self.z, type(None)):
            if self.between is True:
                self.ax.fill_between(self.x, self.y, self.z, facecolor=self.color, alpha=self.alpha)
            if self.below is True:
                self.ax.fill_between(self.x, self.i_below(), np.zeros(self.y.shape), facecolor=self.color, alpha=self.alpha)
            if self.above is True:
                self.ax.fill_between(self.x, self.i_above(), np.zeros(self.y.shape), facecolor=self.color, alpha=self.alpha)
            if self.between is False and self.below is False and self.above is False:
                print_color('No area chosen to fill: specify whether to fill "between", "below" or "above" the curves',
                            'grey')
        else:
            self.ax.fill_between(self.x, self.y, np.zeros(self.y.shape), facecolor=self.color, alpha=self.alpha)

    def i_below(self):
        # Curve
        c = np.zeros(self.y.shape, dtype=np.float)
        for i in range(len(c)):
            c[i] = self.y[i] if self.y[i] <= self.z[i] else self.z[i]
        return c

    def i_above(self):
        # Curve
        c = np.zeros(self.y.shape, dtype=np.float)
        for i in range(len(c)):
            c[i] = self.y[i] if self.y[i] >= self.z[i] else self.z[i]
        return c

    def intersection(self):
        return np.nonzero(np.absolute(self.y - self.z) == min(np.absolute(self.y - self.z)))[0]

    def mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):

            self.x = np.arange(-6, 6, .01)
            self.y = MockData().boltzman(self.x, 0, 1)
            self.z = 1 - MockData().boltzman(self.x, 0.5, 1)
            line(x=self.x, y=self.y, color='darkred', more_subplots_left=True)
            line(x=self.x, y=self.z, color='darkred', more_subplots_left=True)
            self.below = True


class customize(plot):

    def __init__(self,
                 # Base
                 backend='Qt5Agg', font='serif',
                 # Figure, axis
                 fig=None, ax=None, figsize=None, shape_and_position=111,
                 # Setup
                 prune=None, resize_axes=False, aspect=None,
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white',
                 style=None, light=None, dark=None,
                 # Spines
                 spine_color=None, spines_removed=('top', 'right'),
                 # Bounds
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 # Pads
                 demo_pad_plot=False,
                 x_upper_resize_pad=0, x_lower_resize_pad=0,
                 y_upper_resize_pad=0, y_lower_resize_pad=0,
                 # Grid
                 grid=False, grid_color='black', grid_lines='-.',
                 # Color
                 color=None, cmap='RdBu_r', alpha=None, norm=None,
                 # Title
                 title=None, title_size=12, title_y=1.025, title_weight=None, title_font=None, title_color=None,
                 # Labels
                 x_label=None, x_label_size=12, x_label_pad=10, x_label_rotation=None, x_label_weight=None,
                 y_label=None, y_label_size=12, y_label_pad=10, y_label_rotation=None, y_label_weight=None,
                 # Ticks
                 x_tick_number=5, x_tick_labels=None,
                 y_tick_number=5, y_tick_labels=None,
                 x_tick_rotation=None, y_tick_rotation=None, x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5, tick_ndecimals=1,
                 # Tick labels
                 tick_label_size=None, tick_label_size_x=None, tick_label_size_y=None,
                 custom_x_tick_labels=None, custom_y_tick_labels=None, date_tick_labels_x=False, date_format='%Y-%m-%d',
                 # Color bar
                 color_bar=False, cb_pad=0.2, extend='neither',
                 cb_title=None, cb_orientation='vertical', cb_axis_labelpad=10, cb_tick_number=5, shrink=0.75,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, cb_top_title_x=0, cb_vmin=None, cb_vmax=None,
                 cb_ticklabelsize=10, cb_hard_bounds=False,
                 # Legend
                 legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 more_subplots_left=True, zorder=None,
                 # Save
                 filename=None, dpi=None,
                 ):

        """
        Customize plot class
        mpl_plotter - 2D
        :param backend: Interactive plotting backends. Working with Python 3.7.6: Qt5Agg, QT4Agg, TkAgg.
                        Backend error:
                            pip install pyqt5
                            pip install tkinter
                            pip install tk
                            ... stackoverflow
                        Plotting window freezes even if trying different backends with no backend error: python configuration problem
                            backend=None
        """

        # Turn all instance arguments to instance attributes
        for item in inspect.signature(customize).parameters:
            setattr(self, item, eval(item))

        self.plt = import_module("matplotlib.pyplot")

        self.run()

    def run(self):

        self.method_style()

        # Legend
        self.method_legend()

        # Resize axes
        self.method_resize_axes()

        # Makeup
        self.method_background_alpha()
        self.method_title()
        self.method_axis_labels()
        self.method_spines()
        self.method_ticks()
        self.method_grid()

        # Save
        self.method_save()

        self.method_show()

        return self.ax


class utils:

    def floating_text(self, ax, text, font="serif", x=0.5, y=0.5, size=20, weight='normal', color='darkred'):
        # Font
        font = {'family': font,
                'color': color,
                'weight': weight,
                'size': size,
                }
        # Floating text
        ax.text(x, y, text, size=size, weight=weight, fontdict=font)
