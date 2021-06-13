
import numpy as np
import pandas as pd
import time

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool, BoxAnnotation, CustomJS, BoxSelectTool
from bokeh.plotting import figure, show
from bokeh.events import SelectionGeometry

df = pd.read_csv('../cv2/data.csv')

source = ColumnDataSource(data=dict(x=np.arange(0, len(df)), y=df['score'], image_path=df['path'], frame=df['frame']))
selected_data = ColumnDataSource(data=dict(frame=[], y=[], image_path=[]))


TOOLTIPS = """ """
with open('hover.html', 'r') as f:
    TOOLTIPS = f.read()

# create new plot
p = figure(plot_width=1100, plot_height=500, 
           tools="xpan, save, zoom_in, zoom_out, ypan", 
           x_range=(0, 100), tooltips=TOOLTIPS)
p.y_range.flipped = True
# add renderers
p.line(x='x', y='y', source=source, color="blue", line_width=1, line_alpha=0.4)
### range tool ###
peek = figure(plot_height=70, plot_width=1100, y_range=p.y_range, x_axis_type='linear', y_axis_type=None,
                tools="", toolbar_location=None, background_fill_color="white")

callback = CustomJS(args=dict(source=source, selected_data=selected_data), code="""
    console.log("selection event");
    
    var g = cb_obj['geometry'];
    
    var start = Math.round(g['x0']);
    var end = Math.round(g['x1']);
    
    var d = source.data;
    var sf = selected_data;
    
    var f = sf['frame'];
    var y = sf['y'];
    var i = sf['image_path']
    
    frame = [];
    y = [];
    image_path = [];
    
    var selected_frame = d['frame'].slice(start, end);
    var selected_y = d['y'].slice(start, end);
    var selected_image_path = d['image_path'].slice(start, end);

    frame.push(selected_frame);
    y.push(selected_y);
    image_path.push(selected_image_path);
    
    console.log(frame);
    console.log(y);
    console.log(image_path);
     
""")



p.js_on_event('selectiongeometry', callback)




box_select = BoxSelectTool(dimensions="width")
box_select.overlay.line_dash =  "solid"
box_select.overlay.line_width = 1
box_select.overlay.fill_color = "green"
box_select.overlay.fill_alpha = 0.2
p.add_tools(box_select)


range_tool = RangeTool(x_range=p.x_range)
range_tool.overlay.fill_color = "white"
range_tool.overlay.fill_alpha = 0.1
range_tool.overlay.line_dash = 'solid'
range_tool.overlay.line_width = 1

peek.line('x', 'y', source=source, color="grey", line_alpha=0.4)
peek.add_tools(range_tool)
peek.toolbar.active_multi = range_tool

peek.ygrid.grid_line_color = 'whitesmoke'
peek.ygrid.line_color = 'whitesmoke'

p.ygrid.minor_grid_line_color = 'navy'
p.ygrid.minor_grid_line_alpha = 0.1



# show the results
layout = column(p, peek)

show(layout)
