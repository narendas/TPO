import pandas as pd
import numpy as np
from fbprophet import Prophet

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data=pd.read_csv('C:/Users/Vamsi/Desktop/TPO/data/tpodata.csv')
data['date2']=pd.to_datetime(data['date2'],format='%d-%m-%Y')
data=data.set_index('date2')

refined_data=data[(data['Product']=='100 ML Butterscotch') & (data['location ']=='Banjara hills')]



final_data=refined_data['Base Volume']+refined_data['SeasonalVolume']

