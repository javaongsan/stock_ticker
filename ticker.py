import ystockquote, datetime, time, os
from termcolor import colored
    
stocks = []
prices = []
prevsma = []
prevema = []
period = 30

def stocklist():
    stocks.append(('STI', '^STI', 3280))
    stocks.append(('INFORMATICS','I03.SI', 0.131))
    stocks.append(('Wilmar', 'F34.SI', 3.55))
    stocks.append(('Rowsley','A50.SI',  0.405))
    stocks.append(('OSIM', 'O23.SI', 1.83))
    stocks.append(('UNI-ASIA', 'C3T.SI', 0.23))
    stocks.append(('AUS_GRP', '5GJ.SI', 0.55))
    stocks.append(('TAT HONG', 'T03.SI', 1.5))
    stocks.append(('Genting SP', 'G13.SI', 1.6))
    stocks.append(('MIDAS', '5EN.SI', 0.525))
    stocks.append(('GEO Energy', 'RE4.SI', 0.63))
    stocks.append(('UPP', 'U09.SI', 0.31))
    stocks.append(('CMZ(1:01@26/08/13)', 'K2N.SI', 0.53))

def Color_It(price, bought):
    color = "blue"
    if float(bought)==float(price):
        color="white"
    elif float(price) >= float(bought * 1.3):
        color = "green"
    elif float(price)  <= float(bought * 0.90):
        color="red"
    elif float(price)  <= float(bought * 0.75):
        color="yellow"
    return color

def get_ticks():        
    print "%(1)s %(2)s %(3)s %(4)s %(5)s %(6)s" % {"1" : "SYMBOLS".ljust(12), "2" : "Price".rjust(8), "3" : "Change".rjust(8), "4" : "Bought".rjust(8), "5" : "Vol(%)".rjust(8), "6" : "Action".ljust(5)}
    for stock in stocks:
        data= ystockquote.get_all(stock[1])
        prices.append((stock[0], data['price']))
        thisprices = []
        for price in prices:
            if price[0] == stock[0]:
                thisprices.append(float(price[1]))

        thisprevsma = data['price']        
        for price in prevsma:
            if price[0] == stock[0]:
                thisprevsma=price[1]

        thisprevema = data['price']        
        for price in prevema:
            if price[0] == stock[0]:
                thisprevema=price[1]
        bar =len(thisprices)-1
        currentsma = running_sma(bar, thisprices, 3, float(thisprevsma))
        currentema = ema(bar, thisprices, period, float(thisprevema), smoothing=None)

        Hit = False
        for i,value in enumerate(prevsma):
            if prevsma[i] == stock[0]:
                Hit=True
                prevsma[i] = currentsma

        if Hit==False:
             prevema.append((stock[0], currentsma))

        Hit = False
        for i,value in enumerate(prevema):
            if prevema[i] == stock[0]:
                Hit=True
                prevema[i] = currentema

        if Hit==False:
             prevema.append((stock[0], currentema))
        action = ""
        if float(currentsma) > float(currentema) :
            action = "long"
        elif float(currentema) > float(currentsma) :
            action = "short"
        
        vol=0
        
        if float(data['volume']) > 0 and float(data['avg_daily_volume']) > 0:
            vol = "{0:.2f}".format((float(data['volume']) /float(data['avg_daily_volume']))*100)

        color=Color_It(data['price'], stock[2])
        print colored("%(1)s %(2)s %(3)s %(4)s %(5)s %(6)s" % {"1" : stock[0].ljust(12), "2" : data['price'].rjust(8), "3" : data['change'].rjust(8), "4" : str(stock[2]).rjust(8), "5" : str(vol).rjust(8), "6" : action.ljust(5)}, color)

def running_sma(bar, series, period, prevma):
    """
    Returns the running simple moving average - avoids sum of series per call.
 
    Keyword arguments:
    bar     --  current index or location of the value in the series
    series  --  list or tuple of data to average
    period  --  number of values to include in average
    prevma  --  previous simple moving average (n - 1) of the series
    """
    if period < 1:
        raise ValueError("period must be 1 or greater")
 
    if bar <= 0:
        return series[0]
 
    elif bar < period:
        return cumulative_sma(bar, series, prevma)
 
    return prevma + ((series[bar] - series[bar - period]) / float(period))
 
def cumulative_sma(bar, series, prevma):
    """
    Returns the cumulative or unweighted simple moving average.
    Avoids sum of series per call.
 
    Keyword arguments:
    bar     --  current index or location of the value in the series
    series  --  list or tuple of data to average
    prevma  --  previous average (n - 1) of the series.
    """
 
    if bar <= 0:
        return series[0]
 
    else:
        return prevma + ((series[bar] - prevma) / (bar + 1.0))

def ema(bar, series, period, prevma, smoothing=None):
    '''Returns the Exponential Moving Average of a series.
     
    Keyword arguments:
    bar         -- currrent index or location of the series
    series      -- series of values to be averaged
    period      -- number of values in the series to average
    prevma      -- previous exponential moving average
    smoothing   -- smoothing factor to use in the series.
        valid values: between 0 & 1.
        default: None - which then uses formula = 2.0 / (period + 1.0)
        closer to 1 to gives greater weight to recent values - less smooth
        closer to 0 gives greater weight to older values -- more smooth
    '''
    if period < 1:
        raise ValueError("period must be 1 or greater")
     
    if smoothing:
        if (smoothing < 0) or (smoothing > 1.0):
            raise ValueError("smoothing must be between 0 and 1")
             
    else:
         smoothing = 2.0 / (period + 1.0)
     
    if bar <= 0:
        return series[0]
     
    elif bar < period:
        return cumulative_sma(bar, series, prevma)
     
    return prevma + smoothing * (series[bar] - prevma)
     
 
def cumulative_sma(bar, series, prevma):
    """
    Returns the cumulative or unweighted simple moving average.
    Avoids averaging the entire series on each call.
     
    Keyword arguments:
    bar     --  current index or location of the value in the series
    series  --  list or tuple of data to average
    prevma  --  previous average (n - 1) of the series.
    """
     
    if bar <= 0:
        return series[0]
         
    else:
        return prevma + ((series[bar] - prevma) / (bar + 1.0))


def main():
    stocklist()
    d = datetime.datetime.now() 
    while 1:
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        get_ticks()
        print "----------------------------------------------------------------------";
        d = datetime.datetime.now()
        if not d.hour in range(9, 18):
            print 'Trading End'
            break
        if not d.isoweekday() in range(1, 6):
            print 'None Trading Day'
            break
        time.sleep(60)
        
if __name__ == "__main__": 
    os.system('clear')
    main()

