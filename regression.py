import pandas as pd
import matplotlib.pyplot as plt
import os

data = pd.read_csv('C:/Users/Vamsi/Desktop/TPO/data/Sales_Product_Price_by_Store.csv')

refined_data= data[(data['Product']==1)&(data['Store']==1)].iloc[:-23,:]


refined_data['Discount'] = refined_data['Base Price']-refined_data['Price']


final_data = refined_data[['Base Price', 'Discount', 'Weekly_Units_Sold']].groupby('Base Price').mean()

plt.plot(final_data.index,final_data['Weekly_Units_Sold'])
plt.title('Price v/s Mean of Weekly units sold plot for store 1, product 1 (grouped)')
plt.xlabel('Base Price')
plt.ylabel('Mean of Weekly units sold')
plt.show()

plt.scatter(final_data['Discount'],final_data['Weekly_Units_Sold'])
plt.title('Discount v/s Mean of Weekly units sold plot for store 1, product 1 (grouped)')
plt.xlabel('Discount')

plt.ylabel('Mean of Weekly units sold')
plt.show()

from sklearn.linear_model import LinearRegression
from sklearn import metrics

X = final_data.iloc[:,:-1].reset_index().values
y = final_data.iloc[:,-1].values

model = LinearRegression()
model.fit(X,y)

print(model.coef_)
print(model.intercept_)

print(model.score(X,y))
