import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data=pd.read_csv('C:/Users/Vamsi/Desktop/TPO/data/tpodata.csv')
data['date2']=pd.to_datetime(data['date2'],format='%d-%m-%Y')
data=data.set_index('date2')

refined_data=data[(data['Product']=='100 ML Butterscotch') & (data['location ']=='Banjara hills')]
refined_data=refined_data.drop(['Product','Unnamed: 0','Unnamed: 0.1','period1','location ','Feature Only_Grouped','Display Only_Grouped','Fea & Disp_Grouped'],axis=1)
refined_data=refined_data.drop(['BaseVolume%','Seasonality %','TPR %','Display Only %','Fea & Disp%','Feature Only%','PRICE DISCOUNT %'],axis=1)
refined_data=refined_data.drop(['date','Season_Summer','Season_Winter','TotalFactor'],axis=1)
refined_data=refined_data.drop(['Level','LocatHierachyNode','productcatogery','TotFactoredVolume'],axis=1)

#refined_data.reset_index(inplace=True)


#Add placeholder values to empty cells in Seasonality
refined_data['seasonality']=refined_data['seasonality'].replace(np.nan,'No Seasonal Effects')


#handling negative promotional lift values
promotions=['TPR','Display Only','Fea & Disp','Feature Only']
for promotion in promotions:
    refined_data.loc[refined_data[promotion]<0,promotion]=0

#calculate sum of base and lift to get total sales to get errors
refined_data['Total Volume']=refined_data['Base Volume']+refined_data['SeasonalVolume']+refined_data['TPR']+refined_data['Display Only']+refined_data['Fea & Disp']+refined_data['Feature Only']
refined_data['Total Volume']=np.round(refined_data['Total Volume'],2)

refined_data['Total Lift']=refined_data['SeasonalVolume']+refined_data['TPR']+refined_data['Display Only']+refined_data['Fea & Disp']+refined_data['Feature Only']
refined_data['Total Lift']=np.round(refined_data['Total Lift'],2)

refined_data['Promotional Lift']=refined_data['TPR']+refined_data['Display Only']+refined_data['Fea & Disp']+refined_data['Feature Only']
refined_data['Promotional Lift']=np.round(refined_data['Promotional Lift'],2)
# =============================================================================
# sales_data=refined_data[['Base Volume','SeasonalVolume','TPR','Display Only','Fea & Disp','Feature Only','sold units','To2tFactoredVolume']]
# sales_data['Total Volume']=sales_data['Base Volume']+sales_data['SeasonalVolume']+sales_data['TPR']+sales_data['Display Only']+sales_data['Fea & Disp']+sales_data['Feature Only']
# sales_data['Total Volume']=np.round(sales_data['Total Volume'],2)
# sales_data['To2t']=sales_data['To2tFactoredVolume']==sales_data['Total Volume']
# =============================================================================


#Error handling
refined_data.loc[refined_data['To2tFactoredVolume']!=refined_data['Total Volume'],'To2tFactoredVolume']=refined_data['Total Volume']

#Plots
fig,ax=plt.subplots(3,1,figsize=(15,15))
ax[0].plot(refined_data['Base Volume'])
ax[0].set_title('Base Sales')
ax[1].plot(refined_data['Base Volume']+refined_data['SeasonalVolume'])
ax[1].set_title('Baseline Sales')
ax[2].plot(refined_data['To2tFactoredVolume'])
ax[2].set_title('Total Factored Sales')
plt.show()

plot_data=refined_data[100:]
plt.bar(range(len(plot_data.index)),plot_data['Base Volume'],color='#f3e151')
plt.bar(range(len(plot_data.index)),plot_data['Promotional Lift'], bottom=plot_data['Base Volume'], color="#6c3378")
plt.plot(range(len(plot_data.index)),plot_data['Base Volume']+plot_data['SeasonalVolume'])
plt.legend(['Baseline Sales','Base Sales','Promotional Lift'],loc='lower right')
plt.show()


#Final data to be used for forecasting and analysis
final_data=refined_data.copy()
final_data['Baseline Volume']=final_data['Base Volume']+final_data['SeasonalVolume']
final_data=final_data.drop(['seasonality','WINTER ','SUMMER','FESTIVAL','Base Volume','SeasonalVolume','Total Volume','Total Lift','liftfactor'],axis=1)
final_data=final_data[['YEAR','period','Baseline Volume','TPR','Display Only','Feature Only','Fea & Disp','Promotional Lift','sold units','To2tFactoredVolume','MSRP','PRICE DISCOUNT','Average unit price','total sales']]


grouped_data=final_data.groupby('PRICE DISCOUNT').mean()['TPR']
plt.scatter(grouped_data.index,grouped_data)
plt.title('TPR vs Discount')
plt.show()

grouped_data=final_data[['Baseline Volume', 'Average unit price']].groupby('Average unit price').mean()
plt.scatter(grouped_data.index[:4], grouped_data['Baseline Volume'].values[:4])
plt.title('Baseline Volume vs Average unit price')
plt.show()


#Linear Regression fitting

from sklearn.linear_model import LinearRegression
model = LinearRegression()
X=grouped_data.index.values[:4]
X=X.reshape([len(X),1])
Y=grouped_data.values[:4]
model.fit(X,Y)

print(model.coef_)
print(model.intercept_)