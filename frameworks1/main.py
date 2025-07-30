#Micro services
'''
Microservices is an architectural style used in software development where an application is structured as a collection of small,
 independent services that communicate over a network—usually via HTTP APIs or messaging queues.

api vs microservices:
APIs are the means of interaction, while microservices are the units of functionality.

api vs rest api:
API is a general concept — any interface that allows software to talk to each other.
REST API is a specific type of API that uses HTTP and follows REST principles like statelessness, 
resource-based URLs, and standard methods (GET, POST, etc.).
'''

#diffence between post and get
'''
GET is used to retrieve data from a server, while POST is used to send data to a server to create or update a resource. 
GET requests are idempotent and can be cached, while POST requests are not idempotent and are not cached by default. 
GET requests include parameters in the URL, while POST requests include parameters in the request body.
'''

#other methods used in fastapi
'''
FastAPI supports several HTTP methods, including:
- GET: Retrieve data from the server.
- POST: Send data to the server to create a new resource.
- PUT: Update an existing resource on the server.
- DELETE: Remove a resource from the server.
- PATCH: Partially update an existing resource on the server.
- OPTIONS: Describe the communication options for the target resource.
- HEAD: Retrieve the headers of a resource without the body.
- TRACE: Perform a message loop-back test along the path to the target resource.
'''

#difference between async method and normal method
'''
The main difference between an async method and a normal method is that async methods allow for asynchronous programming, 
enabling the program to perform other tasks while waiting for I/O operations to complete. 
This can lead to better performance and responsiveness, especially in applications that involve network requests or file I/O. 
Normal methods, on the other hand, block the execution until the operation is complete,
which can lead to inefficiencies in handling concurrent tasks.
'''

#Swagger
'''
Swagger is a set of tools and specifications that help developers design, build, document, and consume RESTful APIs.
It’s now part of the OpenAPI Specification (OAS), which is the industry standard for describing APIs.
'''


import os,uvicorn
import fast_api,django_app
from django.utils.autoreload import run_with_reloader
import sys
from django.core.management import execute_from_command_line

framework_name = 'fastapi'

if framework_name=='fastapi':app = fast_api.app


if __name__ == "__main__":
    if framework_name=='fastapi':
        filename=os.path.splitext(os.path.basename(__file__))[0]
        uvicorn.run(f"{filename}:app", host="127.0.0.1", port=8000, reload=True)
    elif framework_name=='flask':
        from flask_app import app
        app.run(host='127.0.0.1', port=8000, debug=True)
    elif framework_name=='django':
        sys.argv = ["manage.py", "runserver", "127.0.0.1:8000"]
        execute_from_command_line(sys.argv)
    else:
        print("Unsupported framework. Please choose 'fastapi', 'flask', or 'django'.")