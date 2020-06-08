#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


data = pd.read_csv('gamesDataSet_original.csv')
data.head()


# In[3]:


data = data[data['Add-on'].isnull()]
data.isnull().sum()  / data.shape[0] * 100


# In[4]:


data = data[['GameTittle','Genre','Platforms','Published by','Released','Platform','Developed by','Gameplay','Perspective']]


# In[5]:


platformNN = data[~data['Platform'].isnull()].shape[0]
platformNNandPlatformsN = data[~data['Platform'].isnull() & data['Platforms'].isnull()].shape[0]

print (platformNN,platformNNandPlatformsN)


# In[6]:


data.loc[~data['Platform'].isnull(), 'Platforms'] = data.loc[~data['Platform'].isnull(), 'Platform']
data = data.drop(['Platform'], axis=1)
data.isnull().sum() 


# In[7]:


data[data['GameTittle'].isnull()]


# In[8]:


data = data[~data['GameTittle'].isnull()]
data = data[~data['Platforms'].isnull()]
data.isnull().sum() 


# In[9]:


(data=='Unknown').sum() 


# In[10]:


data = data[data['Released'] != 'Unknown']
data = data.fillna('Unknown')


# In[11]:


data.shape


# In[12]:


data.head()


# In[13]:


data.Released


# In[14]:


def getYearIfCompleteDate(date):
    if len(date) > 4:
        date = date[-4:]
    return date


# In[15]:


data.Released = data.Released.apply(getYearIfCompleteDate)
data.Released.unique()


# In[16]:


plt.boxplot(pd.to_numeric(data.Released))


# In[17]:


data.head()


# In[18]:


lst_col = 'Platforms'
data = data.assign(**{lst_col:data[lst_col].str.split(',')})


# In[19]:


data = pd.DataFrame({
          col:np.repeat(data[col].values, data[lst_col].str.len())
          for col in data.columns.difference([lst_col])
}).assign(**{lst_col:np.concatenate(data[lst_col].values)})[data.columns.tolist()]


# In[20]:


data = data.rename(columns={"Platforms": "Platform"})
data.head()


# In[21]:


data.shape


# In[22]:


data.Platform  = data.Platform.apply(lambda x: x.strip())
data.Released = pd.to_numeric(data.Released)
data.to_csv ('gamesDataSet_final.csv', index = False, header=True)   


# In[ ]:


####ANÀLISI


# In[58]:


platformList = data.Platform.value_counts()
platformList = platformList[platformList > 1000]
print(platformList)
platformList = platformList[platformList > 1000].index.tolist()
data2 = data[data.Platform.isin(platformList)]


# In[24]:


print(data.shape)
print(data2.shape)


# In[63]:


varName = 'Platform'

print(data2[varName].nunique())

data2 = data2.sort_values(by=varName, ascending=True)

plt.figure(figsize=(20,5))
plt.xticks(rotation='vertical')
sns.countplot(data = data2, x = varName)
plt.show()

plt.figure(figsize=(20,5))
plt.xticks(rotation='vertical')
sns.countplot(data = data2[data2.Platform != 'Windows'], x = varName)
plt.show()

plt.figure(figsize=(20,5))
plt.xticks(rotation='vertical')
sns.boxplot(data = data2, x=varName, y='Released',showfliers=False)
plt.show()


# In[64]:


plt.plot(data2['Released'].value_counts().sort_index())


# In[26]:


dataPlays = data2[data2.Platform.str.contains('PlayStation')]
dataPlays.Platform.value_counts()


# In[56]:


def createPlots ():
    plays = ['PlayStation','PlayStation 2', 'PlayStation 3','PlayStation 4']
    colors = ['yellow', 'red', 'green','blue']
    colorIndex = 0

    for target in plays:
        x = dataPlays[dataPlays['Platform']==target].Released
        legend = target
        legend = '%s σ = %s' % (target, round(x.std(),2))
        plt.hist(x, facecolor=colors[colorIndex], alpha=0.5, label = legend)
        plt.axvline(x.mean(), color=colors[colorIndex], linestyle='dashed', linewidth=1)
        colorIndex=(colorIndex+1) % 4
    plt.legend()
    plt.show()

    sns.boxplot(data = dataPlays, x=varName, y='Released',showfliers=False)
    
createPlaystationPlots()


# In[49]:


dataNintendos = data2[data2.Platform.str.contains('Nintendo')]
dataNintendos.Platform.value_counts()


# In[55]:


def createNintendoPlots ():
    plays = ['Nintendo DS','Nintendo 3DS', 'Nintendo Switch']
    colors = ['red', 'green','blue']
    colorIndex = 0

    for target in plays:
        x = dataNintendos[dataNintendos['Platform']==target].Released
        legend = target
        legend = '%s σ = %s' % (target, round(x.std(),2))
        plt.hist(x, facecolor=colors[colorIndex], alpha=0.5, label = legend)
        plt.axvline(x.mean(), color=colors[colorIndex], linestyle='dashed', linewidth=1)
        colorIndex=(colorIndex+1) % 3
    plt.legend()
    plt.show()

    sns.boxplot(data = dataNintendos, x=varName, y='Released',showfliers=False)
    
createNintendoPlots()

