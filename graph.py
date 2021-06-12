import numpy as np
import pandas as pd


from bokeh.models import NumeralTickFormatter, tools
from bokeh.plotting import figure, show

df = pd.read_csv('../sf21/data.csv')
x = np.arange(0,100)
y = df['score']

# create new plot
p = figure(plot_width=1400, plot_height=350, tools="xpan, save")
p.y_range.flipped = True
# add renderers
p.circle(x, y, size=8)
p.line(x, y, color="navy", line_width=1)

# format axes ticks
p.yaxis[0].formatter = NumeralTickFormatter(format="0.000")

# show the results
show(p)