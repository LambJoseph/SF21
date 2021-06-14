

from bokeh.core.property.visual import FontSize
import numpy as np
import pandas as pd
from bokeh import events
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, RangeTool, BoxSelectTool, PreText
from bokeh.plotting import figure, curdoc, show
df = pd.read_csv('../cv2/data.csv')

s1 = ColumnDataSource(data=dict(x=np.arange(0, len(df)), y=df['score'], image_path=df['path'], frame=df['frame']))
s2 = ColumnDataSource(data=dict(frame=[], y=[], image_path=[]))

TOOLTIPS = """ """
with open('hover.html', 'r') as f:
    TOOLTIPS = f.read()

# create new plot
p = figure(plot_width=1100, plot_height=500, tools="xpan, save, zoom_in, zoom_out, ypan", x_range=(0, 100), tooltips=TOOLTIPS)
p.y_range.flipped = True
p.line(x='x', y='y', source=s1, color="blue", line_width=1, line_alpha=0.4)
peek = figure(plot_height=70, plot_width=1100, y_range=p.y_range, x_axis_type='linear', y_axis_type=None, background_fill_color="white")

box_select = BoxSelectTool(dimensions="width")
box_select.overlay.line_dash =  "solid"
box_select.overlay.line_width = 1
box_select.overlay.fill_color = "green"
box_select.overlay.fill_alpha = 0.1
p.add_tools(box_select)

range_tool = RangeTool(x_range=p.x_range)
range_tool.overlay.fill_color = "white"
range_tool.overlay.fill_alpha = 0.1
range_tool.overlay.line_dash = 'solid'
range_tool.overlay.line_width = 1

peek.line('x', 'y', source=s1, color="grey", line_alpha=0.4)
peek.add_tools(range_tool)
peek.toolbar.active_multi = range_tool

peek.ygrid.grid_line_color = 'whitesmoke'
peek.ygrid.line_color = 'whitesmoke'

p.ygrid.minor_grid_line_color = 'navy'
p.ygrid.minor_grid_line_alpha = 0.1

stats = PreText(text="", width=500, FontSize="14px")

def update_stats():
    stats.text = pd.DataFrame(s2.data).to_string()

def selection_change(event):
    event_data = event.geometry
    start = round(event_data['x0'])
    end   = round(event_data['x1'])
    d1 = s1.data

    new_data = {
        'frame': d1['frame'][start:end], 
        'y': d1['y'][start:end],
        'image_path': d1['image_path'][start:end]
    }
    s2.stream(new_data, rollover=26)
    update_stats()
p.on_event('selectiongeometry', selection_change)

r1 = row(p, stats)
c1 = column(peek)
c2 = column(r1, c1)

curdoc().add_root(c2)
