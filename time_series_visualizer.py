import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv',
                 parse_dates = ['date'],
                 index_col = 'date')
df.rename(columns={'value' : 'views'}, inplace=True)

# Clean data
df = df[(df['views'] >= df['views'].quantile(0.025)) & (df['views'] <= df['views'].quantile(0.975))]


def draw_line_plot():
    fig = df.plot(kind ='line',
        use_index = True,
        y = 'views',
        xlabel = 'Date',
        ylabel = 'Page Views',
        title = 'Daily freeCodeCamp Forum Page Views 5/2016-12/2019',
       figsize = (16,9))
    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.groupby([df.index.year, df.index.month_name()])['views'].mean().unstack()
    df_bar = df_bar[calendar.month_name[1:]]
    df_bar.columns.names = ['Months']
    

    # Draw bar plot
    fig = df_bar.plot(kind = 'bar',
                 xlabel = 'Year',
                 ylabel = 'Average Page Views',
                 figsize = (14,10)).get_figure()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Draw box plots (using Seaborn)
    fig, axe = plt.subplots(1, 2, figsize = (14,10))

    sns.boxplot(data = df_box,
                x = 'Year',
                y = 'views',
                ax = axe[0]).set_title('Year-wise Box Plot (Trend)')

    axe[0].set_xlabel('Year')
    axe[0].set_ylabel('Page Views')

    sns.boxplot(data = df_box,
                x = 'Month',
                y = 'views',
                order = month_order,
                ax = axe[1]).set_title('Month-wise Box Plot (Seasonality)')

    axe[1].set_xlabel('Month')
    axe[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
