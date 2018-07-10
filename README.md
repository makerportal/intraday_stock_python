# intraday_stock_python
Intraday Python Stock Puller Using Google Finance

Google Finance requires the following convention when requesting historic stock data:

https://finance.google.com/finance/getprices?q=GOOG&i=60&p=10d&x=NASD&f=d,o,h,l,c,v

KEY: 

q=GOOG - The 'q' denotes the selection of the stock ticker (GOOGLE in this case) 

i=60 - The 'i' denotes the period (in seconds) between data

p=10d - The 'p' denotes amount of days

x=NASD - The 'x' denotes selection of stock exchange

f=d,o,h,l,c,v - The 'f' denotes the desired data (d ≡ date, o ≡ open price, h ≡ high, l ≡ low, c ≡ close, v ≡ volume)
