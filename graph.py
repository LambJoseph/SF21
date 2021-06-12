import numpy as np
import pandas as pd

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool, BoxAnnotation, HoverTool, BoxSelectTool
from bokeh.plotting import figure, show

df = pd.read_csv('../cv2/data.csv')

source = ColumnDataSource(data=dict(
    x=np.arange(0, len(df)), 
    y=df['score'],
    imgs=df['path'], 
    name=df['frame']
    ))

TOOLTIPS = """ """
with open('hover.html', 'r') as f:
    TOOLTIPS = f.read()

# create new plot
p = figure(plot_width=1100, plot_height=500, 
           tools="xpan, save, zoom_in, zoom_out, ypan", 
           x_range=(0, 100), tooltips=TOOLTIPS)
p.y_range.flipped = True
p.add_tools(
    BoxSelectTool(dimensions="width"),
    )
# add renderers
p.line(x='x', y='y', source=source, color="blue", line_width=1, line_alpha=0.4)

### range tool ###
select = figure(plot_height=70, plot_width=1100, y_range=p.y_range, x_axis_type='linear', y_axis_type=None,
                tools="", toolbar_location=None, background_fill_color="white")

range_tool = RangeTool(x_range=p.x_range)
range_tool.overlay.fill_color = "white"
range_tool.overlay.fill_alpha = 0.1
range_tool.overlay.line_dash = 'solid'
range_tool.overlay.line_width = 1

select.line('x', 'y', source=source, color="grey", line_alpha=0.4)
select.add_tools(range_tool)
select.toolbar.active_multi = range_tool

select.ygrid.grid_line_color = 'whitesmoke'
select.ygrid.line_color = 'whitesmoke'

p.ygrid.minor_grid_line_color = 'navy'
p.ygrid.minor_grid_line_alpha = 0.1


# show the results
layout = column(p, select)

show(layout)