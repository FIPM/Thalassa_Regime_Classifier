import datetime
import numpy as np
import pandas as pd
from datetime import datetime
from websocket import create_connection
import json
import _thread
import time

class StreamingData():
    def __init__(self):
        self.depth = 20
        self.df_0 = None
        self.df = None
        # self.model = joblib.load('/Users/fipm/code/abefarkas/Thalassa_Regime_Classifier/model.joblib')
        self.symbol = 'BTCUSDT'
        self.socket = 'wss://stream.binance.com:9443/ws/{}@depth{}'.format(self.symbol.lower(),self.depth)
        self.ws = None
        
    def my_json(self, json_message):
        '''transforming the data to a dict type'''
        size = len(np.array(json_message['bids'])[:,0])
        return {
            **{'primary_key':[datetime.now()]},
            **{'bp'+str(key):[float(value)] for key,value in zip(np.arange(0,size)+1,np.array(json_message['bids'])[:,0])},
            **{'bs'+str(key):[float(value)] for key,value in zip(np.arange(0,size)+1,np.array(json_message['bids'])[:,1])},
            **{'ap'+str(key):[float(value)] for key,value in zip(np.arange(0,size)+1,np.array(json_message['asks'])[:,0])},
            **{'as'+str(key):[float(value)] for key,value in zip(np.arange(0,size)+1,np.array(json_message['asks'])[:,1])}}

    def my_json_0(self, size):
        '''transforming the data to a dict type'''
        return {
            **{'primary_key':[datetime.now()]},
            **{'bp'+str(key):[value] for key,value in zip(np.arange(0,size)+1,(np.arange(0,size)+1)*np.nan)},
            **{'bs'+str(key):[value] for key,value in zip(np.arange(0,size)+1,(np.arange(0,size)+1)*np.nan)},
            **{'ap'+str(key):[value] for key,value in zip(np.arange(0,size)+1,(np.arange(0,size)+1)*np.nan)},
            **{'as'+str(key):[value] for key,value in zip(np.arange(0,size)+1,(np.arange(0,size)+1)*np.nan)}}

    def preprocessing_streamed_data(self,df_ob):
        '''preprocessing of data for streamed data'''
        # aggregating by seconds
        df_agg = df_ob.groupby(pd.Grouper(key='primary_key', axis=0, freq='S')).mean()        
        # moving the index as a column
        df_agg.reset_index(inplace=True)
        # keeping the last 50 rows (most recent information)
        df_agg = df_agg.dropna().tail(200)

        return df_agg
    
    def ws_stream_data(self):
        '''clean the stream data'''
        while True:
            df = pd.DataFrame.from_dict(self.my_json(json.loads(self.ws.recv())))
            self.df_0 = pd.concat([self.df_0, df], axis=0)
            # to keep in memory enough data to have 50 rows
            # after triggering preprocessing_streamed_data
            self.df_0 = self.df_0.tail(500)
            # first 29 rolling windows will have less than 29 obs when calculating the aggregation.
            # better than waiting 30 seconds to plot first observation in streamlit
            self.df = self.preprocessing_streamed_data(self.df_0).reset_index(drop=True)
            # print(self.df[['primary_key']])
            time.sleep(.5)
         
    def get_stream_data(self):
        return self.df
    
    def start(self):
        '''start the connection with the server'''
        self.df_0 = pd.DataFrame.from_dict(self.my_json_0(self.depth))
        self.ws = create_connection(self.socket)
        # Start a new thread for the WebSocket interface
        _thread.start_new_thread(self.ws_stream_data, ())


if __name__=='__main__':
    w = StreamingData()
    w.start()
    while True:        
        print(w.get_stream_data())
