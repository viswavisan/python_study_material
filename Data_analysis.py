#data analysis
#basic:

import csv
import statistics
from collections import Counter

class data_analysis_basic:
    def __init__(self):
        pass

    def read_csv(self,file_path):
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]

    def analyze_numerical(self,data, columns):
        result = {}
        for col in columns:
            values = [float(row[col]) for row in data if row[col]]
            result[col] = {
                'mean': statistics.mean(values),
                'median': statistics.median(values),
                'mode': statistics.mode(values),
                'min': min(values),
                'max': max(values)
            }
        return result

    def analyze_categorical(self,data, columns):
        result = {}
        for col in columns:
            values = [row[col] for row in data if row[col]]
            result[col] = dict(Counter(values))
        return result

    def run(self):
        file_path = 'sample.csv'  # Replace with your actual file path
        data = self.read_csv(file_path)

        numerical_columns = ['age', 'salary']
        categorical_columns = ['gender', 'department']

        numerical_stats = self.analyze_numerical(data, numerical_columns)
        categorical_counts = self.analyze_categorical(data, categorical_columns)

        print("Numerical Analysis:")
        for col, stats in numerical_stats.items():
            print(f"{col}: {stats}")

        print("\nCategorical Analysis:")
        for col, counts in categorical_counts.items():
            print(f"{col}: {counts}")

#data_analysis_basic().run()

#Pandas:
'''
Pandas is a powerful and widely-used open-source Python library for data manipulation and analysis. 
It provides easy-to-use data structures and functions that make working with structured data (like tables and time series) 
fast and intuitive.
'''

import pandas as pd

#read datafram from json file
import json
def json_handling():
    with open('sample.json') as f:
        data=json.load(f)
    # print(data.keys())
    # print(data['fields'])
    # print(data['data'])
    
    fields=pd.DataFrame(data['fields'])
    # print(fields['label'])
    df=pd.DataFrame(data['data'],columns=fields['label'])
    # print(df)
    
# json_handling()

#Series:
'''
A Pandas Series is a one-dimensional labeled array in Python, capable of holding any data type (integers, strings, floats, Python objects, etc.)
'''

def series_demo():
    s1=pd.Series([1,2,3,5]) 
    s2=pd.Series({'A':1,'B':2,'C':3,'D':5})
    s3=pd.Series([1,2,3,5],index=['A','B','C','D'])
    # print(s1,'\n',s2)
    # s3.append(pd.Series([6,7],index=['E','F']))
    s4=s3.drop(['A']) # remove value 1 and assign to s4
    s3.drop('A', inplace=True) #remove value 1 and overwrite in original series s3
    #print(s3)
    #print(s2.add(s3))
    # print(s2.sub(s3))
    #access
    # print(s2.iloc[0:10])
    # print(s2.iloc[[1,2,3]])
    # print(s2.loc['B':'D'])

# series_demo()

#Data frame:
'''
In Pandas, a DataFrame is a two-dimensional, labeled data structure that is similar to a table in a database, an Excel spreadsheet, or a data frame in R.
'''

def datafram_demo():
    data={'name':['n1','n2','n3','X1','X2','N3'],'age':[20,21,21,22,24,24]}
    df1=pd.DataFrame(data)
    #print(df1)
    df2=pd.DataFrame(data,index=['e1','e2','e3','e4','e5','e6'])
    #print(df2)
    #print(df2.age)
    #print(df2['age'])
    data2=[[1,2,3],[1,2,3]]
    df3=pd.DataFrame(data2)
    # print(df2)
    # print(df2.loc['e1':'e2',['name']]) #rows, columns
    # print(df2.iloc[0:2,[0,1]])
    # print(df1.loc[df1['age']==21])
    # print(df1.loc[(df1['age']==21) & (df1['name']=='n2')])
    # print(df1.loc[df1.name.str.contains('X')])
    # print(df1.query('age==21'))
    # print(df1.filter(like='nam'))
    
# datafram_demo()

#read dataframe from csv

import numpy as np
def csv_handling():
    #read
    CSV=pd.read_csv('sample.csv')
    #preview
    #print(CSV) #This prints entire sheet data.
    # print(CSV.head()) #This prints only the first 5 rows of the DataFrame by default.
    # print(CSV.head(10)) #This prints only the first 10 rows of the DataFrame.
    # print(CSV.tail())#This prints only the last 5 rows of the DataFrame by default.
    # print(CSV.columns())#This prints only headers of the DataFrame.
    # print(CSV.index)#This prints only index of the DataFrame.
    # print(CSV.axes) #This prints both index and headers of the DataFrame.
    # print(CSV.shape) #rows,columns
    # print(CSV.size) #rows x columns
    # print(CSV.values) print as list of list
    # print(CSV.describe())
    # print(CSV.age.describe())
    # print(CSV.department.describe())

    #updation
    CSV['new']=np.arange(0,6) #add new column
    # print(CSV.head())
    newdf=CSV.drop_duplicates()# drop existing duplicate rows
    # print(newdf.head())
    newdf.drop(columns=['Marks'],inplace=True) #drop column
    newdf.set_index('Name',inplace=True) #set index
    newdf.set_index(['Name','Age'],inplace=True) #set multiple index
# csv_handling()


import matplotlib.pyplot as plt
def plots():
    df=pd.DataFrame({'Eng':[50,51,60],'Maths':[80,70,85],'sceince':[72,77,70]},index=['s1','s2','s3'])
    #print(df)
    # df.plot.bar()
    # df.plot.barh()
    # df.plot.bar(stacked=True)
    df2=pd.DataFrame(np.random.binomial(10,.5,1000))
    # df2.hist()
    plt.scatter(x=df.index, y=df['Eng'])
    plt.show()
# plots()

# encoding
def encode():
    df=pd.DataFrame({'Name':['Tom','Bob','Mary','Jhon'],'Age':[11,'?',13,'""'],'Marks':[100,'NO',12,21],
                     'Score':[10.0,20.0,'NaN',40.0],'Gender':['M','M','F','M']})
    #binary encoding
    df["Num_Gender"]=np.where(df.Gender=='M',0,1)
    # print(df)
    #Label encoding
# encode()

# Data manipulation:
def data_manipulation():
    df=pd.DataFrame({'Name':['Tom    ','Bob Abc','Mary','Jhon'],'Age':[11,'10',13,"8"],'Marks':[100,'NO',12,21],
                     'Score':[10.0,20.0,'NaN',40.0],'Gender':['Male','M','Female','male']})
    # df.Gender.replace(['male','M','m'],'Male',inplace=True) #replace values
    # print(df)
    df.Age=df.Age.replace('\'','') #replace value
    df.Age=df.Age.replace('"','') #replace value
    # print(df.dtypes) #check data types
    df.Age=df.Age.astype(int) #convert to int
    print(df.dtypes) #check data types again
    df.Name=df.Name.str.strip() #remove leading and trailing spaces
    
# data_manipulation()

#merge dataframes:
df1 = pd.DataFrame({'id': [1, 2, 3], 'name': ['Alice', 'Bob', 'Charlie']})
df2 = pd.DataFrame({'id': [2, 3, 4], 'age': [24, 30, 22], 'name': ['Bob', 'Charlie', 'David']})

# Merge dataframes one below one
df_merged = pd.concat([df1, df2], ignore_index=True)  # ignore_index to reset index
# Merge dataframes side by side
df_side_by_side = pd.concat([df1, df2], axis=1)  # axis=1 for side by side
# Merge based on a common column
merged_df = pd.merge(df1, df2, on='id', how='inner')  # Options: 'inner', 'outer', 'left', 'right'
# Merge based on multiple columns
merged_df_multi = pd.merge(df1, df2, on=['id', 'name'], how='outer')  # Merge on multiple columns