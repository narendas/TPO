from bayes_opt import BayesianOptimization
import pandas as pd

data = pd.read_csv('C:/Users/Vamsi/Desktop/TPO/data/Sales_Product_Price_by_Store.csv')

refined_data= data[(data['Product']==1)&(data['Store']==1)].iloc[:-23,:]


refined_data['Discount'] = refined_data['Base Price']-refined_data['Price']

def obj_func(price, discount):
    return (price-discount)*(-20.48*price-2.56*discount+375.003)

pbounds = {'price':(min(refined_data['Base Price']), max(refined_data['Base Price'])), 'discount': (min(refined_data['Discount']), max(refined_data['Discount']))}

optimizer= BayesianOptimization(f = obj_func, pbounds = pbounds, verbose = 2, random_state = 1)

optimizer.maximize(init_points = 5, n_iter = 25)

print(optimizer.max)
print('Optimum number of units to be sold:',optimizer.max['target']/optimizer.max['params']['price'])
