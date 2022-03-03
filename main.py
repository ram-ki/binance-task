import time
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *


class Logic():
    def __init__(self, api_key, api_secret, url):
        self.client = RequestClient(api_key=api_key,secret_key=api_secret,url='https://testnet.binancefuture.com',testnet=True)
        print(self.client)
        self.i = 12
        self.buy_newClientOrderId = 'ALGOINTERN_OID'+str(self.i)
        self.stop_loss_newClientOrderId = 'ALGOINTERN_SL_OID'+str(self.i)
    
    def buy_order(self):
        
        try:
            result1 = self.client.post_order(symbol="BTCUSDT", side=OrderSide.BUY, ordertype=OrderType.MARKET, quantity=0.001, newClientOrderId=self.buy_newClientOrderId)
            print("buy order successful")
            return 1
        except:
            print("buy order failed")
            return 0

    
    def get_buy_avgPrice(self):
        
        try:
            result2 = self.client.get_order(symbol="BTCUSDT", origClientOrderId=self.buy_newClientOrderId)
            self.stoplossprice = (0.995)*(result2.avgPrice)
            self.stoplossprice = round(self.stoplossprice,1)
            print("successfully fetched stoploss price")
            print("stoplossprice : ", self.stoplossprice)
            return 1
        except:
            print(Exception)
            print("failed to fetch stoploss price")
            return 0

    def stop_loss_order(self):
        
        try:
            result3 = self.client.post_order(symbol="BTCUSDT", side=OrderSide.SELL, ordertype=OrderType.STOP_MARKET, stopPrice=self.stoplossprice, quantity=0.001, newClientOrderId=self.stop_loss_newClientOrderId, closePosition=True)
            print("stop loss order successful")
            return 1
        except:
            print("stop loss order failed")
            return 0
    
    def run(self):
        
        t = 5
        buy_order_successful = 0
        while(t>0):        
            
            buy_order_successful = self.buy_order()
            if(buy_order_successful == 1):
                break
            else:
                time.sleep(5)
                t-=1        
        
        self.get_buy_avgPrice()
        
        t = 5
        stop_loss_successful = 0
        while(t>0):        
            
            stop_loss_successful = self.stop_loss_order()
            if(stop_loss_successful == 1):
                break
            else:
                time.sleep(5)
                t-=1
        if(buy_order_successful == 1 and stop_loss_successful == 1):
            print("order successful")






if __name__ == '__main__':
    api_key = '2332f4b24cb554f226e95a6a8402ff58531322903bc9b0b8383fb5c12a893c19'
    api_secret = 'a1e66fd721c47cd598e5b68b53f468bc7d10a659ebda5140d9871eb3e72d88c1'
    url = 'https://testnet.binancefuture.com'

    obj = Logic(api_key, api_secret, url)
    print("using binance testnet server")
    obj.run()