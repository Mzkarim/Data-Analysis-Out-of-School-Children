
# coding: utf-8

# In[1]:

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


# ##UN Sustainable Development Goals
# 
# https://sustainabledevelopment.un.org/?menu=1300
# 
# 4.1 By 2030, ensure that all girls and boys complete free, equitable and quality primary and secondary education leading to relevant and effective learning outcomes
# However...
# GLOBAL TEACHER SHORTAGE THREATENS EDUCATION 2030:
# UIS data show that 33 countries still won’t have enough teachers to provide every child with a primary education by 2030 if current trends continue.
# 
# http://www.uis.unesco.org/education/pages/world-teachers-day-2015.aspx?spslanguage=en
# 

# **First, let's take a look at how many 6-12 year old children on this planet are out of school**

# ###Data Source: UNESCO Institute for Statistics
# 
# http://data.uis.unesco.org/#
# 

# **Import the Pandas library in Python**

# In[3]:

import pandas as pd


# **Download data files and import in dataframe using pandas**

# In[4]:

df_outofschool = pd.read_csv("E:/Data Collection/outofschoolchildren.csv",skiprows = 2)


# In[5]:

df_outofschool.shape


# In[6]:

df_outofschool.head()


# In[7]:

df_outofschool.columns


# ### Some Initial Cleaning... without touch Excel!
# 1. Change column names
# 2. Move cells up
# 3. Drop the 3rd column
# 4. Remove rows
# 5. Fill coutry names

# **1. Change Column Names**
# 
# **Change Unnamed:1 to year**

# In[8]:

df_outofschool.head()


# In[9]:

df_outofschool.rename(columns={'Unnamed: 1':'year'}, inplace =True)


# In[10]:

df_outofschool.head()   # Double check the change


# **Change the column name Indicator to country**

# In[14]:

df_outofschool.rename(columns={'Indicator':'Country'}, inplace =True)


# In[15]:

df_outofschool.head()   # Double check the change


# In[13]:

df_outofschool.columns


# **To Change all names at once**

# In[16]:

df_outofschool.columns=['Country','Year','Empty','All_children','Female','Male','percentage_female']


# **2. Shift Cells Up**

# In[18]:

#shift up first column
df_outofschool.Country =df_outofschool.Country.shift(-1)


# **shift the year column up one cell**

# In[19]:

df_outofschool.Year =df_outofschool.Year.shift(-1)


# In[20]:

df_outofschool.head()


# **3. Drop The 3rd Column "Empty"**

# In[21]:

df_outofschool.drop('Empty',axis =1,inplace=True)


# In[22]:

df_outofschool.head()  # Double check the changing


# **4. Remove Rows**

# In[23]:

df_outofschool.tail(10)


# In[25]:

#removing bottom rows
df_outofschool.drop(df_outofschool.index[3893:3900],inplace= True)


# In[26]:

df_outofschool.tail(10)  # Double check the change


# ##Caution: We need to know what we removed!

# In[27]:

#alternative methods
#df_outofschool.drop(df_outofschool.tail(7).index)
#df_outofschool.drop(list(range(3894,3900)))


# In[28]:

df_outofschool.tail()


# **5. Fill Country Names**

# In[29]:

df_outofschool['Country']=df_outofschool['Country'].ffill()


# In[30]:

df_outofschool


# ## Lets do some more cleaning...
# **6. Replace .. with missing values**
# 
# **7. Split the country column into code and country name**
# 
# **8. Add regions to each country by merging the metadata file**
# 
# **9. Remove countries and years that have absolutely no data**
# 
# **10. Convert column types**

# In[31]:

import numpy as np


# **6. Replace .. with missing values**

# In[32]:

#fill the '..' cells with NaN
df_outofschool.replace('..',np.nan,inplace =True)


# In[33]:

df_outofschool.head()


# **7. Split The Country Column Into Code And Country Name**

# In[34]:

#first look at the string values
df_outofschool.loc[0,'Country']


# In[35]:

df_outofschool.loc[0,'Country'].split(':')


# **Get The Country Code**

# In[36]:

df_outofschool.loc[0,'Country'].split(':')[0]


# In[37]:

get_country_code = lambda string:string.split(':')[0]


# In[39]:

# to look at what it does
df_outofschool['Country'].apply(get_country_code)


# In[41]:

df_outofschool['country_code'] = df_outofschool['Country'].apply(get_country_code)


# In[42]:

df_outofschool.head()


# ###convert values in the country column to values only with country names

# In[43]:

get_country_name = lambda string: string.split(':')[1]


# In[44]:

df_outofschool['Country'].apply(get_country_name)


# In[45]:

df_outofschool['Country']= df_outofschool['Country'].apply(get_country_name)


# In[46]:

df_outofschool.head()


# **8. Add Regions To Each Country By Merging The Metadata File**

# In[47]:

df_metadata = pd.read_csv("E:/Data Collection/countries_metadata.csv", encoding ="utf-8")


# In[48]:

df_metadata.head()


# **Prepare To Merge**

# In[49]:

df_metadata.rename(columns={'Country Code' : 'country_code'}, inplace = True)


# In[51]:

df_metadata.head()


# In[52]:

len(df_outofschool.country_code.unique())


# In[53]:

len(df_metadata['country_code'])


# In[54]:

pd.merge(df_outofschool,df_metadata,on ='country_code', how = 'left')


# In[55]:

df_merge = pd.merge(df_outofschool,df_metadata, on = 'country_code', how = 'left')


# In[57]:

df_merge.head()


# In[58]:

#but how to access columns with "" in their names?
#iloc


# In[59]:

len(df_merge.iloc[:,-5].unique())


# In[60]:

df_merge.drop(['Unnamed: 5'],axis=1)


# In[61]:

df_merge.drop(['Unnamed: 5'],axis =1,inplace = True)


# **9. Remove Countries and Years That Have Absolutely No Data**

# In[63]:

# Remove rows with no data
df_merge.dropna(axis =0,how = 'all',subset = df_merge.columns[2:6])


# In[64]:

df_merge.dropna(axis =0,how = 'all',subset = df_merge.columns[2:6],inplace = True)


# In[65]:

by_country = df_merge.groupby('Country')


# In[66]:

type(by_country)


# In[67]:

by_country.count()


# In[68]:

by_country.count().iloc[:,1:5]


# In[69]:

df_merge.columns[2:6]


# In[70]:

by_year = df_merge.groupby('Year')


# In[71]:

df_merge.dtypes


# In[72]:

df_merge.columns[2:6]


# In[73]:

df_merge[df_merge.columns[2:6]].astype(float)


# In[74]:

df_merge[df_merge.columns[2:6]] = df_merge[df_merge.columns[2:6]].astype(float)


# In[75]:

df_merge[df_merge.columns[1]] = df_merge[df_merge.columns[1]].astype(int)


# In[76]:

df_merge.columns


# In[77]:

df_merge['percentage_male'] = 100 - df_merge['percentage_female']


# In[80]:

by_region = df_merge.groupby('Region')


# In[84]:

by_region['All_children'].sum()


# In[85]:

by_region['All_children'].mean()


# In[86]:

by_region['All_children'].max()


# In[87]:

by_region['All_children'].min()


# ### which country has the highest number out of scholl children in the Middle East?

# In[88]:

df_merge[df_merge['All_children'] == 1338154]


# In[89]:

df_merge.groupby(['Region','Year'])['All_children'].mean()


# In[90]:

df_merge.groupby(['Region','Year'])['All_children'].mean().unstack()


# ## Pivot Table is much easier to write

# In[91]:

df_merge.pivot_table('All_children',index = 'Year', columns = 'Region',aggfunc = 'mean')


# In[92]:

pivot_year_region = df_merge.pivot_table('All_children',
                    index ='Year',columns='Region',aggfunc= 'mean')


# In[93]:

type(pivot_year_region)


# ## Rounding off Decimal Places

# In[94]:

np.round(pivot_year_region,0)


# In[95]:

pivot_year_region_rounded = np.round(pivot_year_region,0)


# In[97]:

pivot_year_region_rounded


# ** Now we build a pivot table with year as rows and income group as columns, showing Out-of-school children of primary school age, percentage female (%) round if off to no decimal place**

# In[100]:

pivot_female_percent_year_income = df_merge.pivot_table('percentage_female',
          index='Year',columns= 'IncomeGroup',aggfunc='mean')


# In[101]:

pivot_female_percent_year_income.plot()


# In[102]:

average_children_by_region = by_region['All_children'].mean()


# In[103]:

average_children_by_region


# In[104]:

type(average_children_by_region)


# In[105]:

import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')


# In[106]:

pivot_female_percent_year_income.plot()


# In[107]:

average_children_by_region.plot(kind ='bar')


# In[108]:

from matplotlib import style


# In[109]:

style.use('ggplot')


# In[110]:

average_children_by_region.plot(kind='bar')


# In[111]:

average_children_by_region.plot(kind='bar')
plt.title('Average # of out of school Children of Primary School Age')
plt.ylabel('# of Children')
plt.xlabel('World Bank regions')


# In[112]:

average_children_by_region.plot(kind='bar', color = 'black')
plt.title('Average # of out of school Children of Primary School Age')
plt.ylabel('# of Children')
plt.xlabel('World Bank regions')
plt.xticks(rotation = 30)


# In[113]:

average_children_by_region.plot(kind='bar', color = 'black',figsize =(15,5))
plt.title('Average # of out of school Children of Primary School Age')
plt.ylabel('# of Children')
plt.xlabel('World Bank regions')
plt.xticks(rotation = 30)


# In[115]:

average_children_by_region.plot(kind='bar')
plt.title('Average # of out of school Children of Primary School Age')
plt.ylabel('# of Children')
plt.xlabel('World Bank regions')
plt.xticks(rotation = 30)


# **Bar Graph of Total Number of Out-of-School Children by Year**

# In[117]:

df_merge.columns


# In[119]:

total_children_by_year = by_year['All_children'].sum()


# In[120]:

total_children_by_year.plot(kind='bar',color='black',figsize=(15,5))


# In[121]:

#### To save the plot


# In[122]:

total_children_by_year.plot(kind='bar',color='black',figsize=(15,5))
plt.title('Average # of Out of School Children at Primary School Age ')
plt.ylabel('# of Children')
plt.xlabel('Year')
plt.xticks(rotation=30)
plt.savefig('total_children_by_year.pdf')


# In[123]:

total_children_by_year.plot(kind = 'barh',color='black')


# In[124]:

df_merge['percentage_female'].hist()


# In[126]:

df_merge['All_children'].hist()


# In[127]:

pivot_female_percent_year_income


# In[128]:

pivot_female_percent_year_income.plot(kind='box',figsize =(15,10))


# In[129]:

pivot_year_region


# In[130]:

pivot_year_region.plot(figsize=(15,10))


# In[131]:

pivot_female_percent_year_income.plot(figsize=(15,10))


# In[132]:

total_female=df_merge[['All_children','percentage_female']]


# In[134]:

total_female.plot(kind='scatter',x = 'All_children',y = 'percentage_female',
                 figsize=(15,10))

