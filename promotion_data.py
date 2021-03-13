import pandas as pd
import numpy as np

data=pd.read_csv('C:/Users/Vamsi/Desktop/TPO/data/Sales_Product_Price_by_Store.csv')

refined_data=data[(data['Product']==1) & (data['Store']==1)]
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

refined_data=refined_data[['Date','Base Price','Price','p1','p2','p3','Weekly_Units_Sold']]


'''
p1=25
p2=15
p3=30
p1 and p2= 45
p1 and p3= 50
p2 and p3=35
p1 and p2 and p3= 10
'''

def add_promotion_lift(data):
    lift=[]
    p1=data['p1']
    p2=data['p2']
    p3=data['p3']
    for i in range(len(data)):
        if p1[i]==1 and p2[i]==0 and p3[i]==0:
            lift.append(25+np.random.normal(0,3,1)[0])
        elif p1[i]==0 and p2[i]==1 and p3[i]==0:
            lift.append(15+np.random.normal(0,3,1)[0])
        elif p1[i]==0 and p2[i]==0 and p3[i]==1:
            lift.append(30+np.random.normal(0,3,1)[0])
        elif p1[i]==1 and p2[i]==1 and p3[i]==0:
            lift.append(45+np.random.normal(0,3,1)[0])
        elif p1[i]==1 and p2[i]==0 and p3[i]==1:
            lift.append(50+np.random.normal(0,3,1)[0])
        elif p1[i]==0 and p2[i]==1 and p3[i]==1:
            lift.append(35+np.random.normal(0,3,1)[0])
        elif p1[i]==1 and p2[i]==1 and p3[i]==1:
            lift.append(10+np.random.normal(0,3,1)[0])
        else:
            lift.append(0)
    data['Weekly_Units_Sold']=data['Weekly_Units_Sold']+np.round(lift).astype(int)

add_promotion_lift(refined_data)



# =============================================================================
# from sklearn.linear_model import LinearRegression
# 
# final_data=refined_data[['p1','p2','p3','Weekly_Units_Sold']]
# sales=np.log(final_data['Weekly_Units_Sold']/final_data[''])
# X = final_data.iloc[:,:-1].reset_index().values
# y = final_data.iloc[:,-1].values
# 
# model = LinearRegression()
# model.fit(X,y)
# 
# print(model.coef_)
# print(model.intercept_)
# 
# print(model.score(X,y))
# =============================================================================



def calc_promotion_lift(data):
    p1_lift=[]
    p2_lift=[]
    p3_lift=[]
    p12_lift=[]
    p13_lift=[]
    p23_lift=[]
    p123_lift=[]
    p1=data['p1']
    p2=data['p2']
    p3=data['p3']
    for i in range(1,len(data)):
        if p1[i]==1 and p2[i]==0 and p3[i]==0:
            p1_lift.append(data['Weekly_Units_Sold'][i]-data['Weekly_Units_Sold'][i-1])
        elif p1[i]==0 and p2[i]==1 and p3[i]==0:
            p2_lift.append(data['Weekly_Units_Sold'][i]-data['Weekly_Units_Sold'][i-1])
        elif p1[i]==0 and p2[i]==0 and p3[i]==1:
            p3_lift.append(data['Weekly_Units_Sold'][i]-data['Weekly_Units_Sold'][i-1])
        elif p1[i]==1 and p2[i]==1 and p3[i]==0:
            p12_lift.append(data['Weekly_Units_Sold'][i]-data['Weekly_Units_Sold'][i-1])
        elif p1[i]==1 and p2[i]==0 and p3[i]==1:
            p13_lift.append(data['Weekly_Units_Sold'][i]-data['Weekly_Units_Sold'][i-1])
        elif p1[i]==0 and p2[i]==1 and p3[i]==1:
            p23_lift.append(data['Weekly_Units_Sold'][i]-data['Weekly_Units_Sold'][i-1])
        elif p1[i]==1 and p2[i]==1 and p3[i]==1:
            p123_lift.append(data['Weekly_Units_Sold'][i]-data['Weekly_Units_Sold'][i-1])
    return p1_lift,p2_lift,p3_lift

#p1l,p2l,p3l=calc_promotion_lift(refined_data)


from fbprophet import Prophet

df=refined_data[['Date','Weekly_Units_Sold']]
df.columns=['ds','y']
p1=pd.DataFrame({
    'holiday':'p1',
    'ds': refined_data[refined_data['p1']==1]['Date']
    })
p2=pd.DataFrame({
    'holiday':'p2',
    'ds': refined_data[refined_data['p1']==1]['Date']
    })
p3=pd.DataFrame({
    'holiday':'p3',
    'ds': refined_data[refined_data['p1']==1]['Date']
    })
holidays=pd.concat([p1,p2,p3])

m=Prophet(holidays=holidays,yearly_seasonality=True)
m.fit(df)

future=m.make_future_dataframe(periods=2,freq='W')
forecast=m.predict(future)

fig = m.plot_components(forecast)
