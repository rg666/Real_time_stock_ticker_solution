#!/usr/bin/env python
# coding: utf-8

#Imports
import pandas as pd

#Set the input variable
sample_input1 = '''8
2017-01-03,16:18:50,AAPL,142.64
2017-01-03,16:25:22,AMD,13.86
2017-01-03,16:25:25,AAPL,141.64
2017-01-03,16:25:28,AMZN,845.61
2017-01-03,16:28:50,AAPL,140.64
2017-01-03,16:29:59,FB,140.34
2017-01-04,16:29:32,AAPL,143.64
2017-01-04,16:30:50,AAPL,141.64'''

sample_input2 = '''10
2017-01-03,16:18:50,AAPL,142.64
2017-01-03,16:25:22,AMD,13.80
2017-01-03,16:25:22,AMD,13.88
2017-01-03,16:25:22,AMD,13.86
2017-01-03,16:25:25,AAPL,141.64
2017-01-03,16:25:28,AMZN,845.61
2017-01-03,16:28:50,AAPL,140.64
2017-01-03,16:29:59,FB,140.34
2017-01-04,16:29:32,AAPL,143.64
2017-01-04,16:30:50,AAPL,141.64'''

def pre_process_to_df(input_text):
    #Drop the first line which is not required
    sample_input_trimmed = input_text[input_text.find('\n')+1:]
    df = pd.DataFrame([x.split(',') for x in sample_input_trimmed.split('\n')])
    df.columns = ['Date','Time','Symbol','Price']
    df['DateTime'] = df['Date'] + ' ' + df['Time']
    df['DateTime'] =  pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H:%M:%S')
    df.drop(columns=['Date', 'Time'])    
    #Drop the transactions out of 09:30:00 hrs and 16:30:00 trading window
    df = (df.set_index('DateTime')
            .between_time('09:30:00', '16:30:00')
            .reset_index()
            .reindex(columns=df.columns))
    df = df.sort_values(by=['DateTime'])
    return df        

def calculate_day_wise_ticker(df):
    day_wise_transactions = [v for k, v in df.groupby(pd.Grouper(key='DateTime',freq='D'))]
    for i in day_wise_transactions:
        i = i.sort_values(by=['Symbol'])        
        print('Trading Day = ',str(i.DateTime.max())[:10])
        print('Last Quote Time = ',str(i.DateTime.max())[11::])
        print('Number of valid quotes = ',i.shape[0])
        print('Most active hour = ', i.DateTime.dt.hour.mode()[0])
        print('Most active symbol = ',i.Symbol.mode()[0])        
        day_symbol_wise_transactions = [v for k, v in i.groupby(pd.Grouper(key='Symbol'))]
        for j in day_symbol_wise_transactions:
            print(', '.join(str(x) for x in [j.DateTime.max().strftime("%Y-%m-%d %H:%M:%S"),j.Symbol.unique()[0],j.Price.max(),j.Price.min()]))


if __name__ == "__main__":
    df_processed = pre_process_to_df(sample_input1)
    calculate_day_wise_ticker(df_processed)