import pandas as pd
import matplotlib.pyplot as plt
data=pd.read_csv('C:/Users/Vamsi/Desktop/TPO/data/Sales_Product_Price_by_Store.csv')

#Data Creation
product=data[(data['Product']==1) & (data['Store']==1)]
product['Discount']=(product['Base Price']-product['Price'])/product['Base Price']
product['Revenue']=product['Price']*product['Weekly_Units_Sold']



fig,ax=plt.subplots()
ax.plot(product['Revenue'],c='green')
ax.set_ylabel("Revenue")
ax2=ax.twinx()
ax2.plot(product['Price'],c='red')
ax2.set_ylabel("Price")
plt.show()

fig,ax=plt.subplots()
ax.plot(product['Revenue'],c='green')
ax.set_ylabel("Revenue")
ax2=ax.twinx()
ax2.plot(product['Discount'],c='red')
ax2.set_ylabel("discount")
plt.show()



#Data Filtering
product=product[['Base Price','Price','Discount','Date', 'Weekly_Units_Sold','Revenue']]

plt.scatter(product['Weekly_Units_Sold'],product['Revenue'])
plt.show()
plt.scatter(product['Discount'],product['Revenue'])
plt.show()



prices=list(product['Price'].unique())

plt.plot(product[product['Price']==prices[0]]['Revenue'])
plt.plot(product[product['Price']==prices[1]]['Revenue'])
plt.plot(product[product['Price']==prices[2]]['Revenue'])
plt.plot(product[product['Price']==prices[3]]['Revenue'])
plt.legend(['7.99','9.99','10.99','8.79'])
plt.show()
ohe=pd.get_dummies(product,columns=['Price'])
ohe=ohe[['Date','Price_7.99','Price_9.99','Price_10.99','Price_8.79','Weekly_Units_Sold']]
ohe['Price_7.99']=ohe['Price_7.99']*ohe['Weekly_Units_Sold']
ohe['Price_8.79']=ohe['Price_8.79']*ohe['Weekly_Units_Sold']
ohe['Price_10.99']=ohe['Price_10.99']*ohe['Weekly_Units_Sold']
ohe['Price_9.99']=ohe['Price_9.99']*ohe['Weekly_Units_Sold']

plt.plot(ohe['Price_7.99'])
plt.plot(ohe['Price_9.99'])
plt.plot(ohe['Price_10.99'])
plt.plot(ohe['Price_8.79'])
plt.legend(['7.99','9.99','10.99','8.79'])
plt.show()
