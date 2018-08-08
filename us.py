
# coding: utf-8

# In[ ]:


from colormap import rgb2hex
import matplotlib
import numpy as np
from bokeh.models import Label
import pandas as pd
from bokeh.sampledata import us_states
from bokeh.client import push_session, pull_session
from bokeh.plotting import *
import matplotlib.cm as cm
from bokeh.layouts import column, row, widgetbox
from bokeh.models import Select,ColorBar, LinearColorMapper


us_states = us_states.data.copy()
del us_states["HI"]
del us_states["AK"]
state_xs = [us_states[code]["lons"] for code in us_states]
state_ys = [us_states[code]["lats"] for code in us_states]
name=[us_states[code]["name"] for code in us_states]
lon=[np.nanmean(np.asarray(x)) for x in state_xs]
lat=[np.nanmean(np.asarray(x)) for x in state_ys]
p = figure(title="Carbon Monoxide AQI Level in US States, Year:2000",toolbar_location="left", plot_width=1000, plot_height=600, name="plot1")
for itr in range(0,len(lon)):
        lab=Label(x=lon[itr]-0.5,y=lat[itr]-0.5,text=name[itr], text_font_size="7.5pt",y_offset=1,text_font_style="bold",text_color="black")
        p.add_layout(lab)
p.patches(state_xs, state_ys, fill_alpha=0.0,line_color="black", line_width=1.5)



data=pd.read_csv("data.csv")
Year=2000
data_year=data[["Code","State", str(Year)]]
data_year=data_year.dropna()
df=data_year
df=df.reset_index()
df=df.drop("index",axis=1)
cmap = cm.get_cmap('OrRd') 
df[str(Year)]=(df[str(Year)]-df[str(Year)].min())/(df[str(Year)].max()-df[str(Year)].min())
for itr in range(0,len(data_year)):
    x=us_states[df["Code"][itr]]['lons']
    y=us_states[df["Code"][itr]]['lats']
    a=cmap((df[str(Year)][itr]))
    rgb = a[:3] 
    b=matplotlib.colors.rgb2hex(rgb)
    p.patch(x, y, fill_color=b,line_color="black")

    



colors=['#fff7ec', '#feebd0', '#fddcaf', '#fdca94', '#fdb27b', '#fc8c59','#f26d4b', '#e0442f', '#c91d13', '#a80000']
mapper = LinearColorMapper(palette=colors, low=0, high=1)

color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="5pt",
                     label_standoff=6, border_line_color=None, location=(0, 0))
p.add_layout(color_bar, 'right')

def update_plot(attrname, old, new):
    rootLayout = curdoc().get_model_by_name('mainLayout')
    listOfSubLayouts = rootLayout.children
    plotToRemove = curdoc().get_model_by_name('plot1')
    listOfSubLayouts.remove(plotToRemove)
    p = figure(title="Carbon Monoxide AQI Level in US States, Year:"+new,toolbar_location="left", plot_width=1000, plot_height=600, name="plot1")
    p.patches(state_xs, state_ys, fill_alpha=0.0,line_color="black", line_width=1.5)
    for itr in range(0,len(lon)):
        lab=Label(x=lon[itr]-0.5,y=lat[itr]-0.5,text=name[itr], text_font_size="7.5pt",y_offset=1,text_font_style="bold",text_color="black")
        p.add_layout(lab)
    Year=new
    data_year=data[["Code","State", str(Year)]]
    data_year=data_year.dropna()
    df=data_year
    df=df.reset_index()
    df=df.drop("index",axis=1)
    cmap = cm.get_cmap('OrRd') 
    df[str(Year)]=(df[str(Year)]-df[str(Year)].min())/(df[str(Year)].max()-df[str(Year)].min())
    for itr in range(0,len(data_year)):
        x=us_states[df["Code"][itr]]['lons']
        y=us_states[df["Code"][itr]]['lats']
        a=cmap((df[str(Year)][itr]))
        rgb = a[:3] 
        b=matplotlib.colors.rgb2hex(rgb)
        p.patch(x, y, fill_color=b,line_color="black")
    colors=['#fff7ec', '#feebd0', '#fddcaf', '#fdca94', '#fdb27b', '#fc8c59','#f26d4b', '#e0442f', '#c91d13', '#a80000']
    mapper = LinearColorMapper(palette=colors, low=0, high=1)

    color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="5pt",
                     label_standoff=6, border_line_color=None, location=(0, 0))
    p.add_layout(color_bar, 'right')

    
    listOfSubLayouts.append(p)
    
    
    
    
    
    
#menu
select = Select(options=["2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016"],title="Year")
select.on_change('value',update_plot)
# show results
mainLayout = row(row(p,name='mainLayout'),widgetbox(select))
curdoc().add_root(mainLayout)

# #create a session
session = push_session(curdoc())
session.loop_until_closed()

