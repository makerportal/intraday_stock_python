import csv,datetime,requests,time
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go

def numpy_stock(exchange,ticker,interval,days):
    url = 'https://finance.google.com/finance/getprices?q=%s&i=%d&p=%dd&x=%s&f=d,o,h,l,c,v' %\
          (ticker,interval,days,exchange)
    
    with requests.Session() as ses:
        file = ses.get(url)
        csv_reader = csv.reader(file.text.splitlines(),delimiter=',')
        header_pass = 0
        for row in csv_reader:

            if row[0].split('=')[0]=='COLUMNS':
                column_names = [row[0].split('=')[1]]+row[1:]
                data = [[] for ii in range(0,len(column_names))]
            if row[0].split('=')[0]=='TIMEZONE_OFFSET':
                t_offset = float(row[0].split('=')[1])
                header_pass = 1
                continue
            if header_pass==1:
                if row[0][0]=='a':
                    new_day = datetime.datetime.fromtimestamp(int(row[0][1:]))
                    curr_datetime = new_day
                else:
                    curr_datetime = new_day+datetime.timedelta(seconds=period*int(row[0]))
                for ii in range(0,len(column_names)):
                    if ii==0:
                        data[ii].extend([curr_datetime])
                    else:
                        data[ii].extend([np.double(row[ii])])
    return url,data,column_names

def plotter(ticker,names,data):

    for ii,jj in zip(range(0,len(names)),names):
        if jj=='DATE':
            datevec = data[ii]
        elif jj=='OPEN':
            data_open = data[ii]
        elif jj=='HIGH':
            data_high = data[ii]
        elif jj=='LOW':
            data_low = data[ii]
        elif jj=='CLOSE':
            data_close = data[ii]
        elif jj=='VOLUME':
            data_volume = data[ii]

    data_row_1 = 1
    data_row_2 = 5
    
    date_hover1 = [ticker+'<br>'+str(data[0][mm])+\
                   '<br>'+names[data_row_1]+': '+str(data[data_row_1][mm]) for mm in range(0,len(datevec))]
    date_hover2 = [names[data_row_2]+': '+str(data[data_row_2][mm]) for mm in range(0,len(datevec))]
    
    trace1 = go.Scatter(
                x = np.linspace(0,len(datevec)-1,len(datevec)),
                y = data[data_row_1],
                name=names[data_row_1],
                text = date_hover1,
                hoverinfo='text',
                mode='markers'
                )
    
    trace2 = go.Scatter(
                x = np.linspace(0,len(datevec)-1,len(datevec)),
                y = data[data_row_2],
                name=names[data_row_2],
                text = date_hover2,
                hoverinfo='text',
                mode='markers',
                yaxis='y2'
                )    
    layout = go.Layout(
        title='Multi-Scatter Plot for '+ticker,
        xaxis = dict(
            rangeslider = dict(
                visible = False
            )
        ),
        yaxis=dict(
            title='U.S. Dollar'
        ),
        yaxis2=dict(
            title=names[data_row_2],
            overlaying='y',
            type='log',
            side='right'
        )
    )

    plot_data = [trace1,trace2]

    fig = go.Figure(data=plot_data, layout=layout)
    py.plot(fig, filename='High_Frequency_'+ticker)
    return date_hover1,data[data_row_1]

ticker = 'MSFT'
period = 60
days = 5
exchange = 'NASD'

url,data,names = numpy_stock(exchange,ticker,period,days)

x,y1 = plotter(ticker,names,data)
