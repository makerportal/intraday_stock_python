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

    hovertext=[]
    for kk in range(len(data[0])):
        hovertext.append(ticker+\
                         '<br>'+str(data[0][kk])+\
                         '<br>----------------------------'+\
                         '<br>Open: '+str(data_open[kk])+\
                         '<br>Close: '+str(data_close[kk])+\
                         '<br>High: '+str(data_high[kk])+\
                         '<br>Low: '+str(data_low[kk])+\
                         '<br>Volume: '+str(data_volume[kk]))
            
    trace = go.Ohlc(x=datevec,
                open=data_open,
                high=data_high,
                low=data_low,
                close=data_close,
                text = hovertext,
                hoverinfo='text')

    layout = go.Layout(
        title='Open-High-Low-Close Plot for '+ticker,
        xaxis = dict(
            rangeslider = dict(
                visible = False
            )
        ),
        yaxis=dict(
            title='U.S. Dollar'
        )
    )

    data = [trace]

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='OHLC_'+ticker)

ticker = 'NFLX'
period = 60
days = 5
exchange = 'NASD'

url,data,names = numpy_stock(exchange,ticker,period,days)

plotter(ticker,names,data)
