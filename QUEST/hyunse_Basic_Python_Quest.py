#클래스 연습문제

class stock_analysis:
   try:
       def __init__(self,code):
           self.df = pd.read_csv('Desktop\\Python & Data Anal\\q3\\'+code+'.csv', engine='python')
           self.latest_close = self.df[-1:]['종가']
           self.latest_open = self.df[-1:]['시가']
           self.latest_low = self.df[-1:]['저가']
           self.latest_high = self.df[-1:]['고가']

       def close_mean(self):
           return self.df['종가'].mean()
       def close_variance(self):
           return self.df['종가'].var()
       def close_std(self):
           return self.df['종가'].std()
       def volume_mean(self):
           return self.df['거래량'].mean()
       def MA5(self):
           d={}
           for i in range(4,len(self.df)):
               d[self.df.loc[i,'일자']]=self.df['종가'][i-4:i].mean()
           return d
   except FileNotFoundError:
       print('파일명 혹은 경로가 잘못되었습니다.')


#판다스 연습문제

from datetime import datetime

naver_data = pd.read_csv('Desktop\\Python & Data Anal\\q3\\네이버_new.csv', engine='python')
naver_data['종가'] = naver_data['종가'] * (-1) #1
naver_data['variation']=naver_data['종가']-naver_data['시가'] #2
naver_data['datetime'] = naver_data['일자'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d'))
std=naver_data[(datetime(year=2013,month=3,day=1)<=naver_data['datetime']) & (naver_data['datetime']<=datetime(year=2013,month=6,day=1))]['variation'].std() #3
naver_data['yrs']=naver_data['datetime'].apply(lambda x: x.year)
for i in set(naver_data['yrs']):
   naver_data['yravg'] = naver_data[naver_data['yrs']==i]['거래량'].mean()
avg_above_avg = naver_data[naver_data['거래량']>=naver_data['yravg']]['종가'].mean() #4
