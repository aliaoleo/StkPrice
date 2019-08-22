
# coding: utf-8

# In[81]:


import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

def symbol_to_path(symbol):
    """Return CSV file path given ticker symbol."""
    base_dir="/Users/hh/Document_lc/PythonWorkspace/Input/"
    return os.path.join(base_dir, "{}.txt".format(str(symbol)))

symbols=["2330","2317"]

end=datetime.date(2015,12,30)
start=end-datetime.timedelta(days=30)
dates=pd.date_range(start,end)
df_temp=pd.DataFrame(index=dates)

for symbol in symbols:
    path= symbol_to_path(str(symbol))
    df=pd.read_csv(path,usecols=["date","close"],index_col="date")
    df=df.rename(columns={"close":symbol})
    df_temp=df_temp.join(df)
    df_temp=df_temp.dropna()
print(df_temp.head())

n=len(symbols)
w=np.ones(n)/n
df_temp=df_temp/df_temp.ix[0,:]
print(df_temp.head())
equalweight=df_temp*w
print(equalweight.head())
df_temp["summ"]=equalweight.sum(axis=1)
df_temp["Daily_R_Port"]=df_temp.summ-df_temp.summ.shift(1)
df_temp["Daily_Rollingmean"]=pd.rolling_mean(df_temp["Daily_R_Port"],window=120)
df_temp["Daily_Rollingstd"]=pd.rolling_std(df_temp["Daily_R_Port"],window=120)
df_temp["Sharp"]=252**0.5*(df_temp["Daily_Rollingmean"]/df_temp["Daily_Rollingstd"])


print(df_temp.head())
df_temp["summ"].plot(title="Portfolio")
plt.show()
df_temp["Sharp"].plot(title="Portfolio_Rolling_Sharp")
plt.show()
