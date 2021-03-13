from fbprophet import Prophet
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
data=pd.read_csv('C:/Users/Vamsi/Desktop/TPO/data/Sales_Product_Price_by_Store.csv')

refined_data=data[(data['Product']==1) & (data['Store']==1)][['Date','Weekly_Units_Sold']]
refined_data.columns=['ds','y']
refined_data1=refined_data.iloc[:-23,:]
m=Prophet(yearly_seasonality=True)
m.fit(refined_data1)

future=m.make_future_dataframe(periods=2,freq='W')


forecast=m.predict(future)

fig1=m.plot(forecast)

fig2=m.plot_components(forecast)
plt.show()
list0=list(refined_data['y'].iloc[:-22])
plt.plot(list0)
list1 = list(refined_data1['y'].values)
list1.append(170.40)
plt.plot(forecast['yhat'],c='red')
plt.plot(list1, c = 'green')
plt.show()