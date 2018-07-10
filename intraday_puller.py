import csv,datetime,requests,time
import matplotlib.pyplot as plt
import numpy as np

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

ticker = 'NFLX' # example ticker (Netflix)
period = 60 # data every 60 seconds
days = 10 # 10 days worth of data
exchange = 'NASD' # NASDAQ exchange

url,data,names = numpy_stock(exchange,ticker,period,days)
