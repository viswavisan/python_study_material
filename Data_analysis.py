#data analysis
#basic:

import csv
import statistics
from collections import Counter

class data_analysis_basic:
    def read_csv(self,file_path):
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            return list(reader)
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

#--------------SQL--------------#
'''
Layers of RDBMS
1.logical layer: database,query language
2.application layer:application server,application language
3.physical layer:
'''

#basic
import sqlite3

def run_query(query):
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute(''' CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, salary REAL)''')
    cursor.executemany('INSERT INTO employees VALUES (?, ?, ?)', [(1, 'Alice', 70000),(2, 'Bob', 50000),(3, 'Charlie', 60000),(4, 'David', 80000),(5, 'Eve', 55000)])
    cursor.execute(query)
    results = [i[0] for i in cursor.fetchall()]
    conn.close()
    return results
# print(run_query(''' SELECT name FROM employees WHERE salary > ( SELECT AVG(salary) FROM employees) '''))

#ORM
'''
ORM: Object-Relational Mapping
ORMs map database tables to Python classes, and rows to instances (objects) of those classes.
Without ORM (Raw SQL):
cursor.execute("SELECT name FROM users WHERE age > 20")
With ORM:
session.query(User).filter(User.age > 20).all()

Benefits of Using an ORM:
Cleaner code: Work with Python objects instead of SQL strings.
Database abstraction: Easily switch between databases (e.g., SQLite → PostgreSQL).
Security: Reduces risk of SQL injection.
Productivity: Less boilerplate code, more focus on business logic.

    Use SQLAlchemy Core (engine.connect()) if:
        You need maximum performance.
        You're doing bulk operations or data pipelines.
        You prefer writing raw SQL.

    Use SQLAlchemy ORM (Session) if:
        You want clean, maintainable code.
        You're building web apps or APIs.
        You prefer working with Python objects instead of SQL.

    Use Meta Data for internediate (Auto Mapping)
'''

from sqlalchemy import create_engine, Column, Integer, String,text,Table,ForeignKey
from sqlalchemy.orm import sessionmaker,registry,aliased,relationship
mapper_registry = registry()
Base = mapper_registry.generate_base()

class SqlAlchemy:
    def __init__(self, db_url='sqlite:///:memory:'):
        self.engine = create_engine(db_url, echo=False) #echo=True to print sql log
        self.session = sessionmaker(bind=self.engine)() #session for ORM
    def execute_raw(self,query,params=None):
        with self.engine.begin() as conn: #begin() auto commit / connect() manual commit
            result = conn.execute(text(query), params or {})
            if query.strip().lower().startswith("select"):
                return [dict(row._mapping) for row in result]
            else: return 'executed successfully'
db=SqlAlchemy()
if __name__ == "__main__": 
    db.execute_raw('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)')
    data = [{"name": "Alice", "age": 30},{"name": "Bob", "age": 25},{"name": "Charlie", "age": 35},]
    db.execute_raw('INSERT INTO users (name, age) VALUES (:name, :age)', data)
    # print(db.run('select * from users'))

#add additional feature convert dict and print value instead of object (optional)
class DictMixin:
    def to_dict(self):
        return {column.name: getattr(self, column.name, None) for column in self.__table__.columns}
    def __repr__(self):
        return str(self.to_dict())
    
#table class from existing table Automap
@mapper_registry.mapped
class User(DictMixin):
    __table__ = Table("users", Base.metadata, autoload_with=db.engine)
 
#table class from existing/new table manual map
class User2(Base,DictMixin):
    __tablename__ = 'users2'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

if __name__ == "__main__":
    #User2.metadata.create_all(db.engine)#create table if not exist
    Base.metadata.create_all(db.engine)#create all declared tables if not exists
    data = [{"name": "Alice1", "age": 30},{"name": "Bob1", "age": 25},{"name": "Charlie1", "age": 35},]
    db.session.add_all([User2(**row) for row in data]) # insert many
    db.session.commit()
    # print(db.session.query(User).all()) #get all values from table
    # print(db.session.query(User2).filter_by(name="Alice1").first())#where and limit1
    # print(User.__table__.name)

#querry to get 3rd highest marks from students table

#problem:1
class students(Base,DictMixin):
    __tablename__='students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    mark = Column(Integer)

students.metadata.create_all(db.engine)
data = [{"name": "Grace", "mark": 98},{"name": "Alice", "mark": 100},{"name": "Charlie", "mark": 99},{"name": "Bob", "mark": 100},{"name": "Tony", "mark": 98},{"name": "steve", "mark": 97},]
db.session.add_all([students(**row) for row in data]) # insert many
db.session.commit()

#ORM (prefered)
third_highest_mark = db.session.query(students.mark).distinct().order_by(students.mark.desc()).limit(1).offset(2).scalar()
students_with_third_highest = db.session.query(students).filter(students.mark == third_highest_mark).all()
# print(students_with_third_highest)

#core
from sqlalchemy import select, distinct, desc
query = select(students).where(students.mark == ((select(distinct(students.mark)).order_by(desc(students.mark)).limit(1).offset(2)).scalar_subquery()))
# print(db.session.execute(query).scalars().all())

#raw query
students_with_third_highest=db.execute_raw("SELECT name FROM students WHERE mark = (SELECT DISTINCT mark FROM students ORDER BY mark DESC LIMIT 1 OFFSET 2);")
# print(students_with_third_highest)

#problem2

class Employee(Base,DictMixin):
    __tablename__ = 'employees'   
    id = Column(Integer, primary_key=True)
    name = Column(String)
    salary = Column(Integer)
    manager_id = Column(Integer, ForeignKey('employees.id'))

Employee.metadata.create_all(db.engine)
data = [
    {"id": 1, "name": "Alice", "salary": 9000, "manager_id": None},    # CEO
    {"id": 2, "name": "Bob", "salary": 7000, "manager_id": 1},
    {"id": 3, "name": "Charlie", "salary": 8000, "manager_id": 1},     # Earns more than manager's other subordinates
    {"id": 4, "name": "David", "salary": 9500, "manager_id": 2},       # Earns more than Bob (his manager)
    {"id": 5, "name": "Eve", "salary": 6000, "manager_id": 3},
]
db.session.add_all([Employee(**row) for row in data])
db.session.commit()

#raw query
highpaid=db.execute_raw("""
SELECT e.name AS employee_name, e.salary AS employee_salary,m.name AS manager_name, m.salary AS manager_salary
FROM employees e JOIN employees m ON e.manager_id = m.id WHERE e.salary > m.salary;""")
# print(highpaid)

#ORM
employee = aliased(Employee)
manager = aliased(Employee)
#Because joining the Employee table to itself (employee and manager), and both need different references.

result=(db.session.query( employee)
        .join(manager, employee.manager_id==manager.id)
        .filter(employee.salary > manager.salary)
        .all())
# print(result)
    
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
    print(df)
    
# json_handling()

# Series:
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



#handling big data
'''
Handling Big Data in Python (Short Version)
Use Dask or PySpark for large-scale data processing.
Read data in chunks with Pandas if it's too big for memory.
Store data in efficient formats like Parquet or HDF5.
Use cloud tools (like BigQuery or AWS) for massive datasets.
'''

#-----------------pyspark--------------------#
'''
PySpark is the Python API for Apache Spark, a powerful distributed computing framework. 
It allows you to write Spark applications using Python, combining the simplicity of Python
with the scalability of Spark.
'''

def spark_test():
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col

    # Create a Spark session
    spark = SparkSession.builder.appName("PySpark Example")\
        .config("spark.driver.extraJavaOptions", "--enable-native-access=ALL-UNNAMED") \
        .getOrCreate()

    # Sample data
    data = [("Alice", 25),("Bob", 30),("Charlie", 35)]
    columns = ["Name", "Age"]
    df = spark.createDataFrame(data, columns)
    df.show()
    df_filtered = df.filter(col("Age") > 28)
    df_filtered.show()
    spark.stop()