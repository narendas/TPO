import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from datetime import timedelta

data=pd.read_csv('C:/Users/Vamsi/Desktop/TPO/data/Sales_Product_Price_by_Store.csv')

refined_data=data[(data['Product']==1) & (data['Store']==1)]
refined_data['Date']=pd.to_datetime(refined_data['Date'])
def promotion(n):
    p=[]
    for i in range(n):
        p.append(np.random.choice([0,1],replace=True,p=[0.8,0.2]))
    return p

p1=promotion(len(refined_data))
p2=promotion(len(refined_data))
p3=promotion(len(refined_data))

promotion_data=pd.DataFrame({'p1':p1,
                           'p2':p2,
                           'p3':p3})

refined_data=pd.concat([refined_data,promotion_data],axis=1)

refined_data=refined_data[['Date','p1','p2','p3','Weekly_Units_Sold']]


#datee=datetime.datetime.strptime(refined_data.Date[1], "%m/%d/%Y")

refined_data['Month']=pd.DatetimeIndex(refined_data['Date']).month
refined_data['Year']=pd.DatetimeIndex(refined_data['Date']).year

#yearly_sales=pd.DataFrame()

year10=list(refined_data[refined_data['Year']==2010]['Weekly_Units_Sold'].values)
for i in range(4):
    year10.insert(0,np.nan)
year10 = pd.Series(year10)
year11=pd.Series(refined_data[refined_data['Year']==2011]['Weekly_Units_Sold'].values)
year12=pd.Series(refined_data[refined_data['Year']==2012]['Weekly_Units_Sold'].values)

yearly_data=pd.concat([year10,year11,year12],axis=1)

yearly_data.columns=['2010','2011','2012']

plt.plot(yearly_data)
plt.legend(yearly_data.columns)


diff=[]
for i in range(52,len(refined_data)):
    difference=refined_data['Weekly_Units_Sold'][i]-refined_data['Weekly_Units_Sold'][i-52]
    diff.append(difference)