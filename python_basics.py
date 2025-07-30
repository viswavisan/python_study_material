## Python Basics and Advanced Concepts

#what is python?
'''
Python is a high-level, interpreted programming language known for its simplicity and readability.
It supports multiple programming paradigms, including procedural, object-oriented, and functional programming.
Python is widely used for web development, data analysis, artificial intelligence, scientific computing, and more.
'''

# data types:
'''
Python has several built-in data types, including:
1. Numeric Types:
   - int: Integer values (e.g., 1, 42, -7)
   - float: Floating-point numbers (e.g., 3.14, -0.001)
   - complex: Complex numbers (e.g., 2 + 3j)
2. Sequence Types:
   - str: String (e.g., "Hello, World!")
   - list: Ordered, mutable collection (e.g., [1, 2, 3])
   - tuple: Ordered, immutable collection (e.g., (1, 2, 3))
3. Mapping Type:
   - dict: Key-value pairs (e.g., {'name': 'Alice', 'age': 30})
4. Set Types:
    - set: Unordered collection of unique elements (e.g., {1, 2, 3})
    - frozenset: Immutable version of a set
5. Boolean Type:
   - bool: Represents True or False values
6. None Type:
   - NoneType: Represents the absence of a value (None)
'''
#functions and modules:
'''
Functions are reusable blocks of code that perform a specific task. They can take inputs (arguments) and return outputs (return values).
Modules are files containing Python code that can define functions, classes, and variables. They allow you to organize your code into separate files for better maintainability and reusability.
'''
#lambda functions:
'''
Lambda functions are small, anonymous functions defined using the lambda keyword. 
They can take any number of arguments but can only have one expression. They are often used for short, throwaway functions.
'''
#Exceptions:
'''
Exceptions are events that occur during the execution of a program that disrupt the normal flow of instructions.
Python provides a robust exception handling mechanism using try, except, else, and finally blocks to catch and handle errors gracefully.
'''
def divide(a, b):
    """    Divides a by b.
    """
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")
        return None
    except TypeError:
        print("Error: Both arguments must be numbers.")
        return None
    else:
        return result

#DOC string
'''
In Python, a docstring is a special string used to document a module, class, method, or function. It’s placed right after the definition line and is enclosed in triple quotes .
There are several popular formats for writing docstrings. Here are the most common ones:
'''
def greet(name: str) -> None:
    """
    Greet a person by name.

    Args:
        name (str): The name of the person to greet.

    Returns:
        None
    """
    print(f"Hello, {name}!")

#decorators:
'''
Decorators are a way to modify or enhance the behavior of functions or methods without changing their code.
A decorator is a function that takes another function as an argument and returns a new function that adds some functionality.
'''
import time
from functools import wraps
def my_decorator(func):
    @wraps(func) # This preserves the original function's metadata
    def wrapper(*args, **kwargs):
        t1=time.time()
        response=func(*args, **kwargs)
        print(time.time()-t1)
        return response
    return wrapper
@my_decorator
def greet():print("Hello!")
# print(greet.__name__) # Output: greet
# print(greet.__doc__) # Output: This function greets the user

#oops
'''
Object-Oriented Programming (OOP) is a programming paradigm that uses objects to represent data and methods to manipulate that data.
OOP allows for encapsulation, inheritance, and polymorphism, making it easier to model real-world entities and relationships.
'''
#pillors of oops:
'''
1. Encapsulation: Bundling data and methods that operate on that data within a single unit (class).
2. Inheritance: Creating new classes based on existing classes, allowing for code reuse and the creation of hierarchical relationships.
3. Polymorphism: Allowing different classes to be treated as instances of the same class through a common interface.
4. Abstraction: Hiding complex implementation details and exposing only the necessary parts of an object.
'''
#superclass/inheritance/over ridding(polymorph)/encapsulation
class parent:               #parent class
    x='parent value'        #class variable / public variable
    __x='restricted value1' #private variable
    def __init__(self):     #constructor
        self.__y='private value' #instance variable / private variable
    def parent_method(self): #parent method
        return 'parent method called'

class child(parent):        #child class
    x='child value'         #overriding parent class variable (polymorphism)
    def super_c(self):
        #print(self.__x)     #AttributeError: 'child' object has no attribute '_child__x'
        return super().x    #accessing parent class variable

print('inheritance (accesing):',child().parent_method())
print('polymorph (over ridding):',child.x)
print('super class (retain parent object):',child().super_c())
try:print(child.__x)
except Exception as e: print('encapsulated :',str(e))
#Abstact class

#difference between deep copy and shallow copy:
'''Shallow Copy:
A shallow copy creates a new object, but it does not create copies of nested objects. Instead, it copies references to the nested objects.
Changes made to nested objects in the original will be reflected in the shallow copy.
Deep Copy:
A deep copy creates a new object and recursively copies all nested objects, creating entirely new instances.
'''
import copy
original = {'a': 1, 'b': [2, 3]}
shallow_copied = copy.copy(original)  # Shallow copy
deep_copied = copy.deepcopy(original)  # Deep copy
original['b'].append(4)  # Modify the nested list
print("Original:", original)  # {'a': 1, 'b': [2, 3, 4]}
print("Shallow Copied:", shallow_copied)  # {'a': 1, 'b': [2, 3, 4]}
print("Deep Copied:", deep_copied)  # {'a': 1, 'b': [2, 3]}

#what is list comprehension?
'''List comprehension is a concise way to create lists in Python. It allows you to generate a new list by applying an expression to each item in an existing iterable (like a list or range) and optionally filtering items based on a condition.
'''

#what is iterators and generators?
'''Iterators are objects that allow you to iterate over a collection (like a list or tuple) one element at a time. 
They implement the iterator protocol, which consists of the __iter__() and __next__() methods.

Generators are a special type of iterator that are defined using functions with the yield statement. 
When called, a generator function returns an iterator object that can be iterated over, producing values one at a time and maintaining its state between iterations.
'''
def simple_generator():
    yield 1
    yield 2
    yield 3
gen = simple_generator()
print(next(gen))  # Output: 1
print(next(gen))  # Output: 2
print(next(gen))  # Output: 3

#what is map, filter, reduce?
'''Map, filter, and reduce are higher-order functions in Python that allow you to apply operations to collections of data.
1. Map: Applies a function to each item in an iterable and returns a new iterable with the results.
2. Filter: Applies a function to each item in an iterable and returns a new iterable containing only the items for which the function returns True.
3. Reduce: Applies a function cumulatively to the items in an iterable, reducing it to a single value.
'''
from functools import reduce
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))  # Map
filtered = list(filter(lambda x: x % 2 == 0, numbers))  # Filter
reduced = reduce(lambda x, y: x + y, numbers)  # Reduce
print("Squared:", squared)  # Output: [1, 4, 9, 16, 25]
print("Filtered:", filtered)  # Output: [2, 4]
print("Reduced:", reduced)  # Output: 15

#what is context manager?
'''Context managers are a way to manage resources in Python, ensuring that they are properly acquired and released.
They are typically used with the with statement, which ensures that resources are cleaned up automatically, even if an error occurs.
A context manager is defined using the __enter__() and __exit__() methods.
'''
class MyContextManager:
    def __enter__(self):
        print("Entering the context")
        return self  # Return the resource to be used within the context

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting the context")
        # Handle any cleanup here
        if exc_type:
            print(f"An error occurred: {exc_value}")
with MyContextManager() as cm:
    print("Inside the context")
    # You can use cm here

#what is multithreading and multiprocessing?
'''Multithreading and multiprocessing are two techniques for achieving concurrent execution in Python.
1. Multithreading: Involves running multiple threads (smaller units of a process) within a single process. 
Threads share the same memory space, which allows for efficient communication.
2. Multiprocessing: Involves running multiple processes, each with its own memory space. 
This can lead to better performance for CPU-bound tasks, as it bypasses the Global Interpreter Lock (GIL) in Python.
'''


#----------best practices------------#
#split odd, even numbers
even,odd=[i   for i in range(100) if i%2==0],[i  for i in range(100) if i%2!=0 ]


@my_decorator
def shape_pattern(x):
    for i in range(1,x):
        print(' '*(x-i),''.join([str(y) for y in range (1,i)])+''.join([str(y) for y in range (i,0,-1)]),' '*(x-i))

def flatten_list(nested_list):
    return [item for sublist in nested_list for item in (flatten_list(sublist) if isinstance(sublist, list) else [sublist])]

#print(flatten_list([1,[2,[3,4],5],6]))

def flatten_dict(d,parent_key=''):
    final={}
    for key,v in d.items():
        key=f'{parent_key}.{key}' if parent_key!='' else key
        if isinstance(v, dict):final.update(flatten_dict(v,key))
        else:final[key]=v
    return final
# print(flatten_dict({'a':1, 'b':{'b1':2}, 'c':[1,2,3], 'd':{'d1':{'d2':3}} }))

from collections import defaultdict
def group_anagrams(words):
    grouped = defaultdict(list)
    [grouped[''.join(sorted(word))].append(word) for word in words]    
    return list(grouped.values())

print(group_anagrams(words=['eat','tea','tan','ate','nat','bat']))

def number_multiplier(x):return ''.join([t*int(n) for t,n in zip(x[::2],x[1::2])])
#print(number_multiplier('a3b2c4'))

def verify_number_count(x):return all([x[n+1:n+1+int(i)].isalpha() for n,i in enumerate(x) if i.isdigit()])
#print(verify_number_count('1a2xy3eee'))

# Lambda
verify_number_count_l = lambda x: all([x[n+1:n+1+int(i)].isalpha() for n,i in enumerate(x) if i.isdigit()])
#print(verify_number_count_l('1a2xy3eee'))


#return type hint:
'''
The -> in the function definition is called a return type hint in Python. 
It tells you (and tools like linters or IDEs) what type of value the function is expected to return.
These hints don't enforce types at runtime — they’re just suggestions unless you use a type checker.
'''
def hint_type()->int:
    return '0'

#if __name__ == "__main__":
'''
it is a common Python idiom used to control the execution of code when a file is run directly versus when it is imported as a module.
To prevent certain code from running when the file is imported.
'''



#lint
'''
    In programming, lint (or linter) refers to a tool that analyzes your code for potential errors, 
    bugs, stylistic issues, or suspicious constructs.
    A linter checks your code for:

        Syntax errors
        Code style violations (e.g., indentation, naming conventions)
        Potential bugs (e.g., unused variables, unreachable code)
        Best practices (e.g., avoiding deprecated functions)
    Python	pylint, flake8, black (formatter)
    
    flake8 my_script.py
    my_script.py:3:1: F401 'os' imported but unused
    my_script.py:5:80: E501 line too long (82 > 79 characters)

'''

#code coverage
'''
    In SonarQube, code coverage refers to the percentage of your source code that is tested by automated tests (like unit tests). It helps you understand how much of your code is being exercised during testing, which is a key indicator of code quality and test effectiveness.

    What Code Coverage Measures:
    Lines covered: How many lines of code were executed during tests.
    Branches covered: Whether all possible paths (like if/else conditions) were tested.
    Conditions covered: Whether all boolean expressions were evaluated both true and false.'''



#test case
def add(a, b):
    return a + b

#1. Unit test
import unittest
# Test case class
class TestMathFunctions(unittest.TestCase):
    
    def test_add_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative_numbers(self):
        self.assertEqual(add(-1, -1), -2)

    def test_add_zero(self):
        self.assertEqual(add(0, 5), 6,'error message')
    # assertEqual(a, b)
    # assertNotEqual(a, b)
    # assertTrue(x)
    # assertFalse(x)
    # assertIsNone(x)
    # assertIsInstance(x, type)

#unittest.main()
#pytest

def test_multiply_positive():
    assert add(2, 3), 5 == 6

#pytest test_math_utils.py (run in terminal)
#tests all functions starts with test

#doc test
def divide(a, b):
    """
    Divides a by b.
    test cases

    >>> divide(6, 2)
    3.0
    >>> divide(5, 2)
    2.5
    >>> divide(1, 0)
    Traceback (most recent call last):
        ...
    ZeroDivisionError: division by zero

    completed
    """
    return a / b

#pydantic model
'''
    Pydantic is a data validation and settings management library that uses Python type hints to validate and parse data.
'''

from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str
def pydantic_test():
    # Create a user instance
    user = User(name="Alice", age=25, email="alice@example.com")

    # Access fields
    print(user.name)

    # Automatic validation
    try:
        invalid_user = User(name="Bob", age="twenty", email="bob@example.com")
        # Raises a validation error because age is not an integer
    except Exception as e:print(e)

#--------------SQL--------------#

'''
Layers of RDBMS
1.logical layer: database,query language
2.application layer:application server,application language
3.physical layer:
'''

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
'''



#basic
import pymysql

# Connect to the database
connection = pymysql.connect(host='localhost',user='root',password='root',database='employee',cursorclass=pymysql.cursors.DictCursor)

def pymysql_test():
    try:
        with connection.cursor() as cursor:
            # Create a new table
            cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(100),email VARCHAR(100))""")

            # Insert a new record
            cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", ("Alice", "20"))

            # Commit the transaction
            connection.commit()

            # Query the table
            cursor.execute("SELECT * FROM users")
            result = cursor.fetchall()
            for row in result:
                print(row)

    finally:
        connection.close()

#ORM model

from sqlalchemy import create_engine, Column, Integer, String,text,MetaData,select
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('mysql+pymysql://root:root@localhost/employee')

'''
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
def alchemy_test():
# Use raw SQL (sql injection risk but faster)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM database.table WHERE age > 20"))
        for row in result: print(f"{row.name} is {row.age} years old.")

#use meta data (avoid sql injection risk)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    users_table = metadata.tables['users']

    with engine.connect() as conn:
        result = conn.execute(select(users_table).where(users_table.c.age > 20))
        for row in result:print(f"{row.name} is {row.age} years old.")

#use ORM MODEL (avoid sql injection risk little slow)
    Base = declarative_base()
    class User(Base):
        __tablename__ = 'table' 
        id = Column(Integer, primary_key=True)
        name = Column(String(100))
        age = Column(Integer)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    users = session.query(User).all()

    # new_user = User(name="Alice", age=25)
    # session.add(new_user)
    # session.commit()

    for user in users:print(f"{user.name}, {user.age}")

    # Fetch users older than 20
    older_users = session.query(User).filter(User.age > 20).all()
    for user in older_users:print(f"{user.name} is {user.age} years old.")


#querry to get second highest marks from students table
#Raw Query
"SELECT name FROM students WHERE marks = (SELECT DISTINCT marks FROM students ORDER BY marks DESC LIMIT 1 OFFSET 1);"


from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    name = Column(String)
    marks = Column(Integer)

from sqlalchemy import select, distinct, desc
subquery = (select(distinct(Student.marks)).order_by(desc(Student.marks)).limit(1).offset(1)).scalar_subquery()

query = select(Student.name).where(Student.marks == subquery)

from sqlalchemy.orm import Session
with Session(engine) as session:
    result = session.execute(query).scalars().all()
    print(result)



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


#stages in development:
'''
Planning - Define goals, scope, and requirements.
Design - Create architecture, UI/UX, and system models.
Development - Write and build the actual code.
Testing - Verify functionality, performance, and security.
Deployment - Release the application to users or production.
Maintenance - Fix bugs, update features, and ensure stability.
'''

#create environment:
'''
python -m venv venv
venv\Scripts\ activate

'''

#async program
''' 
In Python, an async method (or asynchronous function) is a function that allows you to perform non-blocking operations,
such as I/O tasks (like reading files, making network requests, or querying databases), without freezing the entire program.
'''



#handling big data
'''
Handling Big Data in Python (Short Version)
Use Dask or PySpark for large-scale data processing.
Read data in chunks with Pandas if it's too big for memory.
Store data in efficient formats like Parquet or HDF5.
Use cloud tools (like BigQuery or AWS) for massive datasets.
'''


