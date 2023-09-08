from fyers_api import fyersModel
import pandas as pd
import numpy as np
from datetime import datetime, date, time, timedelta
import time as t

class FyersTradingBot:
    def __init__(self, client_id, access_token,date):
        self.client_id = client_id
        self.access_token = access_token
        self.date = date
        self.fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")
        self.allowedSegment = [14]
        self.fno_url = 'http://public.fyers.in/sym_details/NSE_FO.csv'
        self.load_fno_symbols()

    def load_fno_symbols(self):
        fno_symbolList = pd.read_csv(self.fno_url, header=None)
        fno_symbolList.columns = ['FyersToken', 'Name', 'Instrument', 'lot', 'tick', 'ISIN',
                                  'TradingSession', 'Lastupdatedate', 'Expirydate', 'Symbol', 'Exchange', 'Segment',
                                  'ScripCode', 'ScripName', 'token', 'strike', 'type', 'tok2', 'None']
        fno_symbolList = fno_symbolList[fno_symbolList['Instrument'].isin(self.allowedSegment)]
        fno_symbolList['Expirydate'] = pd.to_datetime(fno_symbolList['Expirydate'], unit='s').apply(lambda x: x.date())
        fno_symbolList = fno_symbolList[(fno_symbolList['Expirydate'] == date(2023,8,10)) & (fno_symbolList['ScripName'] == 'BANKNIFTY')]
        self.atmdf = fno_symbolList.copy()
        self.lst = self.atmdf['strike'].tolist()
        self.lot = 1

    def closest(self, lst, K):
        return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]

    def get_token(self, name, exp, typ, strike):
        return name + exp + strike + typ

    def getLTP(self, symbol):
        data = {"symbols": symbol}
        res = self.fyers.quotes(data)
        return res['d'][0]['v']['lp']

    def placeOrder(self, symbol, buy_sell, quantity):
        data = {
            "symbol": symbol,
            "qty": quantity,
            "type": 2,
            "side": buy_sell,
            "productType": "MARGIN",
            "limitPrice": 0,
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": "False",
            "stopLoss": 0,
            "takeProfit": 0
        }
        self.fyers.place_order(data)

    def two_five(self):
        tday = self.date
        qty = self.lot * 15
        start = time(15, 0, 1)
        end = time(15, 25, 1)
        pt1 = datetime.now().time()
        while pt1 < start:
            pt1 = datetime.now().time()

        tick = 'NSE:NIFTYBANK-INDEX'
        try:
            atm = self.getLTP(tick)
        except Exception as e:
            pass

        #atm=46000

        atint = str(int(self.closest(self.lst, atm)))
        print(atint)
        
        tick = self.self.get_token('NSE:BANKNIFTY', '23810', 'CE', atint)
        print(tick)

        data = {"symbol": tick, "resolution": "5", "date_format": "1", "range_from": tday, "range_to": tday, "cont_flag": "1"}
        cf2 = pd.DataFrame(self.fyers.history(data)['candles'],
                           columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        cf2['date'] = pd.to_datetime(cf2['date'], unit='s', utc=True, )
        cf2['date'] = cf2['date'].dt.tz_convert('Asia/Kolkata')

        hh = cf2['high'].values[-1]
        lh = cf2['low'].values[-1]

        q = 0
        while q < 3:
            try:
                ltp = self.getLTP(tick)
            except Exception as e:
                pass
            q += 1
            t.sleep(1)

        pt1 = datetime.now().time()
        while ltp < hh and pt1 <= end:
            try:
                ltp = self.getLTP(tick)
            except Exception as e:
                pass

        pt1 = datetime.now().time()
        if ltp >= hh and pt1 <= end:
            print('buy')
            entry = ltp
            sl = ltp - 0.1 * ltp
            trg = ltp + 0.1 * ltp
            self.placeOrder(tick, 1, qty)

            pt1 = datetime.now().time()
            while pt1 < end:
                try:
                    ltp = self.getLTP(tick)
                except Exception as e:
                    pass
                if ltp >= trg:
                    print('target_hit')
                    print('profit is', ltp - entry)
                    sl = sl + 0.1 * entry
                    trg = trg + 0.1 * entry
                elif ltp <= sl:
                    self.placeOrder(tick, -1, qty)
                    print('sl hit')
                    print('profit is', ltp - entry)
                    break
                pt1 = datetime.now().time()

            if pt1 >= end:
                self.placeOrder(tick, -1, qty)
                print('sqareoff')
                try:
                    ltp = self.getLTP(tick)
                except Exception as e:
                    pass

                print('profit is', ltp - entry)

    def straddle(self):
        rr=2
        exip='23906'
        qty=self.lot*15

        start=time(9,50,1)
        pt1=datetime.now().time()
        while(pt1<start):
            pt1=datetime.now().time()


            
        tick='NSE:NIFTYBANK-INDEX'
        q=0
        while(q<3):
            try:
                ltp=self.getLTP(tick)
            except Exception as e:
                pass
            q+=1
            t.sleep(1)
            

        entry=ltp
        

        atint= str(int(self.closest(self.lst, entry)))


        tkk_CE=self.get_token('NSE:BANKNIFTY',exip,'CE',atint)
        tkk_PE=self.get_token('NSE:BANKNIFTY',exip,'PE',atint)

        # sell both
        print('sell tkk_CE and tkk_PE now')

        q=0
        while(q<3):
            try:
                ltp_CE=self.getLTP(tkk_CE)
            except Exception as e:
                pass
            q+=1
            t.sleep(1)
            
        q=0
        while(q<3):
            try:
                ltp_PE=self.getLTP(tkk_PE)
            except Exception as e:
                pass
            q+=1
            t.sleep(1)
        
        lis=[]
        sl_CE=ltp_CE+40
        sl_PE=ltp_PE+40
        print(datetime.now())
        print('sell '+tkk_CE+' at '+str(ltp_CE)+' with sl '+str(sl_CE))
        print('sell '+tkk_PE+' at '+str(ltp_PE)+' with sl '+str(sl_PE))
        entry_CE=ltp_CE
        entry_PE=ltp_PE

        self.placeOrder(tkk_CE,-1,qty)
        self.placeOrder(tkk_PE,-1,qty)

        profit=0
        prof=0
        cnt=0
        lis.append({'Strike':tkk_CE,'Entry':entry_CE,'Stop':sl_CE,'Entry_time':datetime.now()})
        lis.append({'Strike':tkk_PE,'Entry':entry_PE,'Stop':sl_PE,'Entry_time':datetime.now()})

        while(ltp_CE<sl_CE and ltp_PE<sl_PE):
            try:
                ltp_CE=self.getLTP(tkk_CE)
            except Exception as e:
                pass
            
            try:
                ltp_PE=self.getLTP(tkk_PE)
            except Exception as e:
                pass
            
            profit=prof+entry_CE-ltp_CE + entry_PE-ltp_PE
            tk=datetime.now().time()
            var=tk.minute
            if(var%15==0 and cnt==0):
                print(tkk_CE)
                print('Profit CE running',entry_CE-ltp_CE)
                print(tkk_PE)
                print('Profit PE running',entry_PE-ltp_PE)
                
                print('Net Profit', profit)
                cnt=1
                
            if(var%15!=0):
                cnt=0
            
        '''if(ltp_CE>sl_CE):
            reentry_ce(ltp_CE,sl_CE,tkk_CE,ltp_PE,sl_PE,tkk_PE)
            if(ltp_PE>sl_PE):
                    
                reentry_pe(ltp_CE,sl_CE,tkk_CE,ltp_PE,sl_PE,tkk_PE)
        elif(ltp_PE>sl_PE):
            reentry_pe(ltp_CE,sl_CE,tkk_CE,ltp_PE,sl_PE,tkk_PE)
            if(ltp_CE>sl_CE):
                    
                reentry_ce(ltp_CE,sl_CE,tkk_CE,ltp_PE,sl_PE,tkk_PE)'''
            
        if(ltp_CE>=sl_CE):
            self.placeOrder(tkk_CE,1,qty)
            #cost sl
            sl_PE=entry_PE
            print('sl hit for '+tkk_CE)
            #sell order
            prof+=entry_CE-ltp_CE
            # rentry
            #lis.append()
            q=0
            while(q<3):
                try:
                    ltp=self.getLTP(tick)
                except Exception as e:
                    pass
                q+=1
                t.sleep(1)
            
            
            atint= str(int(self.closest(self.lst, ltp)))

            tkk_CE=self.get_token('NSE:BANKNIFTY',exip,'CE',atint)
            # buy ce on rentry
            q=0
            while(q<3):
                try:
                    ltp_CE=self.getLTP(tkk_CE)
                except Exception as e:
                    pass
                q+=1
                t.sleep(1)
                
            sl_CE=ltp_CE+40
            print(datetime.now())
            print('sell '+tkk_CE+' at '+str(ltp_CE)+' with sl '+str(sl_CE))
            self.placeOrder(tkk_CE,-1,qty)
            entry_CE=ltp_CE
            lis.append({'Strike':tkk_CE,'Entry':entry_CE,'Stop':sl_CE,'Entry_time':datetime.now()})
            
            cnt=0
            while(ltp_CE<sl_CE and ltp_PE<sl_PE):
                try:
                    ltp_CE=self.getLTP(tkk_CE)
                except Exception as e:
                    pass
                
                try:
                    ltp_PE=self.getLTP(tkk_PE)
                except Exception as e:
                    pass
                
                profit=prof+entry_CE-ltp_CE + entry_PE-ltp_PE
                tk=datetime.now().time()
                
                var=tk.minute
                if(var%15==0 and cnt==0):
                    print(tkk_CE)
                    print('Profit CE running',entry_CE-ltp_CE)
                    print(tkk_PE)
                    print('Profit PE running',entry_PE-ltp_PE)
                    
                    print('Net Profit', profit)
                    cnt=1
                    
                if(var%15!=0):
                    cnt=0
                    
            if(ltp_CE>=sl_CE):
                self.placeOrder(tkk_CE,1,qty)
                # sl hit
                print('sl hit for '+tkk_CE)
                #exit order
                prof+=entry_CE-ltp_CE
                
                cnt=0    
                while(ltp_PE<sl_PE):
                    try:
                        ltp_PE=self.getLTP(tkk_PE)
                    except Exception as e:
                        pass
                    
                    profit=prof+entry_PE-ltp_PE
                    tk=datetime.now().time()
                    var=tk.minute
                    if(var%15==0 and cnt==0):
                        print(tkk_PE)
                        print('Profit PE running',entry_PE-ltp_PE)
                        
                        
                        print('Net Profit', profit)
                        cnt=1
                    if(var%15!=0):
                        cnt=0
                print('sl hit for '+tkk_PE)
                self.placeOrder(tkk_PE,1,qty)
                #exit order
                prof+=entry_PE-ltp_PE
                # rentry
                q=0
                while(q<3):
                    try:
                        ltp=self.getLTP(tick)
                    except Exception as e:
                        pass
                    q+=1
                    t.sleep(1)
                    
                atint= str(int(self.closest(self.lst, ltp)))

                tkk_PE=self.get_token('NSE:BANKNIFTY',exip,'PE',atint)
                # buy PE on rentry
                q=0
                while(q<3):
                    try:
                        ltp_PE=self.getLTP(tkk_PE)
                    except Exception as e:
                        pass
                    q+=1
                    t.sleep(1)
                    
                sl_PE=ltp_PE+40
                print(datetime.now())
                print('sell '+tkk_PE+' at '+str(ltp_PE)+' with sl '+str(sl_PE))
                self.placeOrder(tkk_PE,-1,qty)
                entry_PE=ltp_PE
                
                lis.append({'Strike':tkk_PE,'Entry':entry_PE,'Stop':sl_PE,'Entry_time':datetime.now()})
                
                cnt=0
                while(ltp_PE<sl_PE):
                    try:
                        ltp_PE=self.getLTP(tkk_PE)
                    except Exception as e:
                        pass
                    
                    profit=prof+entry_PE-ltp_PE 
                    tk=datetime.now().time()
                    var=tk.minute
                    if(var%15==0 and cnt==0):
                        print(tkk_PE)
                        print('Profit PE running',entry_PE-ltp_PE)
                        
                        
                        print('Net Profit', profit)
                        cnt=1
                    if(var%15!=0):
                        cnt=0
                        
                #sl hit
                self.placeOrder(tkk_PE,1,qty)
                print('sl hit for '+tkk_PE)
                # exit order
                prof+=entry_PE-ltp_PE
                
            elif(ltp_PE>=sl_PE):
                self.placeOrder(tkk_PE,1,qty)
                #cost sl
                sl_CE=entry_CE
                print('sl hit for '+tkk_PE)
                #sell order
                prof+=entry_PE-ltp_PE
                # rentry
                q=0
                while(q<3):
                    try:
                        ltp=self.getLTP(tick)
                    except Exception as e:
                        pass
                    q+=1
                    t.sleep(1)
                    
                atint= str(int(self.closest(self.lst, ltp)))

                tkk_PE=self.get_token('NSE:BANKNIFTY',exip,'PE',atint)
                # buy ce on rentry
                q=0
                while(q<3):
                    try:
                        ltp_PE=self.getLTP(tkk_PE)
                    except Exception as e:
                        pass
                    q+=1
                    t.sleep(1)
                    
                sl_PE=ltp_PE+40
                print(datetime.now())
                print('sell '+tkk_PE+' at '+str(ltp_PE)+' with sl '+str(sl_PE))
                self.placeOrder(tkk_PE,-1,qty)
                entry_PE=ltp_PE
                lis.append({'Strike':tkk_PE,'Entry':entry_PE,'Stop':sl_PE,'Entry_time':datetime.now()})
                
                
                cnt=0
                while(ltp_CE<sl_CE and ltp_PE<sl_PE):
                    try:
                        ltp_CE=self.getLTP(tkk_CE)
                    except Exception as e:
                        pass
                    
                    try:
                        ltp_PE=self.getLTP(tkk_PE)
                    except Exception as e:
                        pass
                    
                    profit=prof+entry_CE-ltp_CE + entry_PE-ltp_PE
                    tk=datetime.now().time()
                    
                    var=tk.minute
                    if(var%15==0 and cnt==0):
                        print(tkk_CE)
                        print('Profit CE running',entry_CE-ltp_CE)
                        print(tkk_PE)
                        print('Profit PE running',entry_PE-ltp_PE)
                        
                        print('Net Profit', profit)
                        cnt=1
                        
                    if(var%15!=0):
                        cnt=0
                        
                if(ltp_PE>=sl_PE):
                    prof+=entry_PE-ltp_PE
                    #exit order
                    self.placeOrder(tkk_PE,1,qty)
                    print('sl hit for '+tkk_PE)
                    # sl hit
                    cnt=0    
                    while(ltp_CE<sl_CE):
                        try:
                            ltp_CE=self.getLTP(tkk_CE)
                        except Exception as e:
                            pass
                        
                        profit=prof+entry_CE-ltp_CE 
                        tk=datetime.now().time()
                        
                        var=tk.minute
                        if(var%15==0 and cnt==0):
                            print(tkk_CE)
                            print('Profit CE running',entry_CE-ltp_CE)
                            
                            
                            print('Net Profit', profit)
                            cnt=1
                        if(var%15!=0):
                            cnt=0
                    print('sl hit for '+tkk_CE)
                    #exit order
                    self.placeOrder(tkk_CE,1,qty)
                    prof+=entry_CE-ltp_CE
                    
                elif(ltp_CE>=sl_CE):
                    self.placeOrder(tkk_CE,1,qty)
                    #cost sl
                    sl_PE=entry_PE
                    prof+=entry_CE-ltp_CE
                    #exit order
                    # sl hit
                    print('sl hit for '+tkk_CE)
                    cnt=0    
                    while(ltp_PE<sl_PE):
                        try:
                            ltp_PE=self.getLTP(tkk_PE)
                        except Exception as e:
                            pass
                        
                        profit=prof+entry_PE-ltp_PE 
                        tk=datetime.now().time()
                        var=tk.minute
                        if(var%15==0 and cnt==0):
                            print(tkk_PE)
                            print('Profit PE running',entry_PE-ltp_PE)
                            
                            
                            print('Net Profit', profit)
                            cnt=1
                        if(var%15!=0):
                            cnt=0
                    print('sl hit for '+tkk_PE)
                    #exit order
                    self.placeOrder(tkk_PE,1,qty)
                    prof+=entry_PE-ltp_PE
                    
                    
        elif(ltp_PE>=sl_PE):
            #cost sl
            sl_CE=entry_CE
            print('sl hit for '+tkk_PE)
            #exit order
            self.placeOrder(tkk_PE,1,qty)
            prof+=entry_PE-ltp_PE
            # rentry
            q=0
            while(q<3):
                try:
                    ltp=self.getLTP(tick)
                except Exception as e:
                    pass
                q+=1
                t.sleep(1)
                
            atint= str(int(self.closest(self.lst, ltp)))

            tkk_PE=self.get_token('NSE:BANKNIFTY',exip,'PE',atint)
            # sell pe on rentry
            q=0
            while(q<3):
                try:
                    ltp_PE=self.getLTP(tkk_PE)
                except Exception as e:
                    pass
                q+=1
                t.sleep(1)
                
            sl_PE=ltp_PE+40
            print(datetime.now())
            print('sell '+tkk_PE+' at '+str(ltp_PE)+' with sl '+str(sl_PE))
            entry_PE=ltp_PE
            self.placeOrder(tkk_PE,-1,qty)
            
            lis.append({'Strike':tkk_PE,'Entry':entry_PE,'Stop':sl_PE,'Entry_time':datetime.now()})
            
            
            cnt=0
            while(ltp_CE<sl_CE and ltp_PE<sl_PE):
                try:
                    ltp_CE=self.getLTP(tkk_CE)
                except Exception as e:
                    pass
                
                try:
                    ltp_PE=self.getLTP(tkk_PE)
                except Exception as e:
                    pass
                
                profit=prof+entry_CE-ltp_CE + entry_PE-ltp_PE
                tk=datetime.now().time()
                
                var=tk.minute
                if(var%15==0 and cnt==0):
                    print(tkk_CE)
                    print('Profit CE running',entry_CE-ltp_CE)
                    print(tkk_PE)
                    print('Profit PE running',entry_PE-ltp_PE)
                    
                    print('Net Profit', profit)
                    cnt=1
                    
                if(var%15!=0):
                    cnt=0
            
            if(ltp_PE>=sl_PE):
                print('sl hit for '+tkk_PE)
                #exit order
                self.placeOrder(tkk_PE,1,qty)
                prof+=entry_PE-ltp_PE
                # sl hit
                cnt=0    
                while(ltp_CE<sl_CE):
                    try:
                        ltp_CE=self.getLTP(tkk_CE)
                    except Exception as e:
                        pass
                    
                    profit=prof+entry_CE-ltp_CE
                    tk=datetime.now().time()
                    var=tk.minute
                    if(var%15==0 and cnt==0):
                        print(tkk_CE)
                        print('Profit CE running',entry_CE-ltp_CE)
                        
                        
                        print('Net Profit', profit)
                        cnt=1
                    if(var%15!=0):
                        cnt=0
                print('sl hit for '+tkk_CE)
                #exit order
                self.placeOrder(tkk_CE,1,qty)
                prof+=entry_CE-ltp_CE
                # rentry
                q=0
                while(q<3):
                    try:
                        ltp=self.getLTP(tick)
                    except Exception as e:
                        pass
                    q+=1
                    t.sleep(1)
                    
                atint= str(int(self.closest(self.lst, ltp)))

                tkk_CE=self.get_token('NSE:BANKNIFTY',exip,'CE',atint)
                # buy ce on rentry
                q=0
                while(q<3):
                    try:
                        ltp_CE=self.getLTP(tkk_CE)
                    except Exception as e:
                        pass
                    q+=1
                    t.sleep(1)
                    
                sl_CE=ltp_CE+40
                print(datetime.now())
                print('sell '+tkk_CE+' at '+str(ltp_CE)+' with sl '+str(sl_CE))
                self.placeOrder(tkk_CE,-1,qty)
                entry_CE=ltp_CE
                lis.append({'Strike':tkk_CE,'Entry':entry_CE,'Stop':sl_CE,'Entry_time':datetime.now()})
                
                
                cnt=0
                while(ltp_CE<sl_CE):
                    try:
                        ltp_CE=self.getLTP(tkk_CE)
                    except Exception as e:
                        pass
                    
                    profit=prof+entry_CE-ltp_CE
                    tk=datetime.now().time()
                    var=tk.minute
                    if(var%15==0 and cnt==0):
                        print(tkk_CE)
                        print('Profit CE running',entry_CE-ltp_CE)
                        
                        
                        print('Net Profit', profit)
                        cnt=1
                    if(var%15!=0):
                        cnt=0
                        
                #sl hit
                print('sl hit for '+tkk_CE)
                # exit order
                self.placeOrder(tkk_CE,1,qty)
                prof+=entry_CE-ltp_CE
                

            elif(ltp_CE>=sl_CE):
                #cost sl
                sl_PE=entry_PE
                print('sl hit for '+tkk_CE)
                #exit order
                self.placeOrder(tkk_CE,1,qty)
                prof+=entry_CE-ltp_CE
                # rentry
                q=0
                while(q<3):
                    try:
                        ltp=self.getLTP(tick)
                    except Exception as e:
                        pass
                    q+=1
                    t.sleep(1)
                    
                atint= str(int(self.closest(self.lst, ltp)))

                tkk_CE=self.get_token('NSE:BANKNIFTY',exip,'CE',atint)
                # sell ce on rentry
                q=0
                while(q<3):
                    try:
                        ltp_CE=self.getLTP(tkk_CE)
                    except Exception as e:
                        pass
                    q+=1
                    t.sleep(1)
                    
                sl_CE=ltp_CE+40
                print(datetime.now())
                print('sell '+tkk_CE+' at '+str(ltp_CE)+' with sl '+str(sl_CE))
                self.placeOrder(tkk_CE,-1,qty)
                entry_CE=ltp_CE
                lis.append({'Strike':tkk_CE,'Entry':entry_CE,'Stop':sl_CE,'Entry_time':datetime.now()})
                
                
                cnt=0
                while(ltp_CE<sl_CE and ltp_PE<sl_PE):
                    try:
                        ltp_CE=self.getLTP(tkk_CE)
                    except Exception as e:
                        pass
                    
                    try:
                        ltp_PE=self.getLTP(tkk_PE)
                    except Exception as e:
                        pass
                    
                    profit=prof+entry_CE-ltp_CE + entry_PE-ltp_PE
                    tk=datetime.now().time()
                    
                    var=tk.minute
                    if(var%15==0 and cnt==0):
                        print(tkk_CE)
                        print('Profit CE running',entry_CE-ltp_CE)
                        print(tkk_PE)
                        print('Profit PE running',entry_PE-ltp_PE)
                        
                        print('Net Profit', profit)
                        cnt=1
                        
                    if(var%15!=0):
                        cnt=0
                        
                if(ltp_PE>=sl_PE):
                    #cost sl
                    sl_CE=entry_CE
                    prof+=entry_PE-ltp_PE
                    #exit order
                    self.placeOrder(tkk_PE,1,qty)
                    print('sl hit for '+tkk_PE)
                    # sl hit
                    cnt=0    
                    while(ltp_CE<sl_CE):
                        try:
                            ltp_CE=self.getLTP(tkk_CE)
                        except Exception as e:
                            pass
                        
                        profit=prof+entry_CE-ltp_CE
                        tk=datetime.now().time()
                        var=tk.minute
                        if(var%15==0 and cnt==0):
                            print(tkk_CE)
                            print('Profit CE running',entry_CE-ltp_CE)
                            
                            
                            print('Net Profit', profit)
                            cnt=1
                        if(var%15!=0):
                            cnt=0
                    print('sl hit for '+tkk_CE)
                    #exit order
                    self.placeOrder(tkk_CE,1,qty)
                    prof+=entry_CE-ltp_CE
                    
                elif(ltp_CE>=sl_CE):
                    prof+=entry_CE-ltp_CE
                    #exit order
                    self.placeOrder(tkk_CE,1,qty)
                    # sl hit
                    print('sl hit for '+tkk_CE)
                    cnt=0    
                    while(ltp_PE<sl_PE):
                        try:
                            ltp_PE=self.getLTP(tkk_PE)
                        except Exception as e:
                            pass
                        
                        profit=prof+entry_PE-ltp_PE 
                        tk=datetime.now().time()
                        var=tk.minute
                        if(var%15==0 and cnt==0):
                            print(tkk_PE)
                            print('Profit PE running',entry_PE-ltp_PE)
                            
                            
                            print('Net Profit', profit)
                            cnt=1
                        if(var%15!=0):
                            cnt=0
                    print('sl hit for '+tkk_PE)
                    #exit order
                    self.placeOrder(tkk_PE,1,qty)
                    prof+=entry_PE-ltp_PE
            


if __name__ == "__main__":
    tday='2023-07-21'
    client_id = "###############"
    access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTAxMjI2MzgsImV4cCI6MTY5MDE1ODYzOCwibmJmIjoxNjkwMTIyNjM4LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa3ZUbU9ZMlA1VFpwYUktaVBrSkZrb0VmVkxwR0dQVGx0OGxKY3BOcUFPSmxwaTI4bzRXeUFnU19BNU9TZ1hvaVFqeWI3Rm82Q2JnYmltenFJc1Q0aUV4VzEwUDIta2VWRTcyWnc1ZU1hcThCRWxaST0iLCJkaXNwbGF5X25hbWUiOiJHQVVSQVYgS1VNQVIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI5ODRlMjgxNGY4MGFmZTNkNTZmNDMwOThjZTNiOWM5NWI1OTI5YzE4YzFjZmQxNDE5Y2NjYzQ5ZSIsImZ5X2lkIjoiWEcxMzk2NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.H05rCTUFxjkueNTTrG2XsrGIzn2Kr1Gdj1LJHU0uwNc'
    trading_bot = FyersTradingBot(client_id, access_token,tday)
    trading_bot.two_five()
