import pandas as pd
import matplotlib.pyplot as plt
from fbprophet import Prophet
from sklearn.linear_model import LinearRegression
from bayes_opt import BayesianOptimization


data = pd.read_csv('C:/Users/Vamsi/Desktop/TPO/data/Sales_Product_Price_by_Store.csv')

refined_data= data[(data['Product']==1)&(data['Store']==1)].iloc[:-23,:]
backup_data = data[(data['Product']==1)&(data['Store']==1)].iloc[-23:,:]
backup_data1 = data[(data['Product']==1)&(data['Store']==1)].iloc[:-22,:]

plt.plot(refined_data['Weekly_Units_Sold'])
plt.title('Trend of weekly units sold')
plt.xlabel('Time')
plt.ylabel('Weekly units sold')
plt.show()
#plt.plot(backup_data['Weekly_Units_Sold'])
#plt.show()

#len(refined_data)

refined_data['Discount'] = refined_data['Base Price']-refined_data['Price']
final_data = refined_data[['Weekly_Units_Sold','Price']].groupby('Price').mean()

plt.scatter(final_data.index,final_data['Weekly_Units_Sold'])
plt.title('Price v/s Mean of Weekly units sold plot for store 1, product 1 (grouped)')
plt.xlabel('Price')
plt.ylabel('Mean of Weekly units sold')
plt.show()



X = final_data.iloc[:,:-1].reset_index().values
y = final_data.iloc[:,-1].values

model = LinearRegression()
model.fit(X,y)

print(model.coef_)
print(model.intercept_)

print(model.score(X,y))

def obj_func(price):
    return (price)*(model.coef_[0]*price+model.intercept_)



pbounds = {'price':(min(refined_data['Price']), max(refined_data['Price']))}

optimizer= BayesianOptimization(f = obj_func, pbounds = pbounds, verbose = 2, random_state = 1)

optimizer.maximize(init_points = 5, n_iter = 25)

print(optimizer.max)


#data=pd.read_csv('C:/Users/Vamsi/Desktop/TPO/data/Sales_Product_Price_by_Store.csv')

refined_data_1=refined_data[['Date', 'Weekly_Units_Sold']]
refined_data_1.columns = ['ds','y']
m=Prophet()
m.fit(refined_data_1)

future=m.make_future_dataframe(periods=2,freq='W')


forecast=m.predict(future)

fig1=m.plot(forecast)

fig2=m.plot_components(forecast)
plt.show()
list0=list(backup_data1['Weekly_Units_Sold'].values[-15:])
plt.plot(list0)
list1 = list(refined_data_1['y'].values[-14:])
list1.append(optimizer.max['target']/optimizer.max['params']['price'])
plt.plot(forecast['yhat'].values[-15:],c='red')
plt.plot(list1, c = 'green')
plt.legend(['Actual Sales', 'Predicted by fbprophet', 'Bayesian Optimized'])
plt.show()