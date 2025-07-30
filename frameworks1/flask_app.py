# Flask
'''Flask is a lightweight WSGI web application framework in Python. 
It is designed to make it easy to get started with web development,
while also being flexible enough to allow for complex applications.
Flask is often referred to as a micro-framework because it does not include many of the tools and libraries that larger frameworks do,
but it provides the essentials needed to build a web application.
Flask is built on top of Werkzeug, a WSGI utility library, and Jinja2, a templating engine.
Flask is known for its simplicity, ease of use, and flexibility, making it a popular choice for web developers.
'''
from flask import Flask, jsonify,g

import time
app = Flask(__name__)
@app.route("/sync")
def sync_endpoint():
    time.sleep(3)
    return {"method": "sync"}


# Flask with async
'''Flask can also be used with asynchronous programming, but it requires additional setup.
To use async in Flask, you need to use an ASGI server like Uvicorn or Hypercorn.
This allows Flask to handle asynchronous requests and responses.
To use async in Flask, you can define your route handlers as async functions and use the `await` keyword to call asynchronous operations.
Flask with async is still relatively new, and not all features of Flask are fully compatible with async.
Flask with async is useful for applications that require high concurrency and low latency, such as real-time applications or applications that make many I/O-bound requests.
'''

import asyncio
app_async = Flask(__name__)
@app_async.route("/async")
async def async_endpoint():
    await asyncio.sleep(3)
    return {"method": "async"}

@app.before_request
def start_timer():
    g.start_time = time.time()

@app.after_request
def add_security_headers(response):
    process_time = time.time() - g.start_time
    print(f"Process time: {process_time} seconds")

    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Frame-options"] = "deny"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "img-src 'self' data:; "
        "object-src 'none'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self';"
    )

    return response


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    return response

#path parameter example
#call by http://xxx/path/10
@app.route("/path/<int:x>")
def pathmethod(x: int) -> dict:
    return {"method": "path method", "response": x}

#query parameter example
#call by http://xxx/query?x=10
@app.route("/query")
def querymethod(x: int = 0) -> dict:
    return {"method": "query method", "response": x}

#post method example
#call by http://xxx/post
# with body {"x": 10}
@app.route("/post", methods=["POST"])
async def postmethod(request: dict) -> dict:
    x = request.get("x", 0)
    return {"method": "post method", "response": x}

#frontend example
@app.route("/renderhtml")
def render_html():
    html_content = """
    <html>
        <head>
            <title>Flask HTML Template</title>
        </head>
        <body>
            <h1>Welcome to Flask!</h1>
            <p>This is a simple HTML page rendered by Flask.</p>
        </body>
    </html>
    """
    return html_content

from flask import render_template

@app.route("/rendertemplate")
def render_template1():
    return render_template("index.html",title="Flask Template Example Jinja")
