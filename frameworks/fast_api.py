#Fast API
#what is Fast API
'''
fastapi is a modern, fast (high-performance), 
web framework for building APIs with Python 3.6+ based on standard Python type hints.
It is built on top of Starlette for the web parts and Pydantic for the data parts.
FastAPI is designed to be easy to use, while also being powerful and flexible.
It allows for automatic generation of OpenAPI documentation,
and it supports asynchronous programming, which can lead to better performance in I/O-bound applications.
'''

#what is uvicorn?
'''
Uvicorn is a lightning-fast ASGI (Asynchronous Server Gateway Interface) server implementation, built on top of uvloop and httptools. 
It's commonly used to serve Python web applications that are built using asynchronous frameworks like FastAPI and Starlette.
'''


from fastapi import FastAPI
import time,os,asyncio
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import authentication

app = FastAPI()

app.include_router(authentication.app, prefix="", tags=["Authentication"])

#what is middleware?
'''Middleware is a way to process requests globally before they reach the endpoint or after the response is returned.
It can be used for tasks such as logging, authentication, and modifying requests or responses.'''

from starlette.middleware.sessions import SessionMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
app.add_middleware(SessionMiddleware, secret_key="!secret")

@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Process time: {process_time} seconds")

    response.headers["X-Process-Time"] = str(process_time) # Add process time to response headers
    response.headers["X-Frame-options"]= "deny"# Prevents the page from being displayed in a frame
    response.headers["X-Content-Type-Options"] = "nosniff" #This helps prevent certain attacks (like MIME type confusion), making your API more secure
    response.headers["X-XSS-Protection"] = "1; mode=block" # Enables the cross-site scripting (XSS) filter built into most browsers
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains" # Enforces secure (HTTPS) connections to the server
    response.headers["Content-Security-Policy"] = "default-src 'self'; " \
                                                    "script-src 'self'; " \
                                                    "style-src 'self'; " \
                                                    "img-src 'self' data:; " \
                                                    "object-src 'none'; " \
                                                    "frame-ancestors 'none'; " \
                                                    "base-uri 'self'; " \
                                                    "form-action 'self';" 
        # get source data only from the mentioned sources,
        # script-src allows scripts from the same origin,

    return response

@app.get("/sync")
def sync_endpoint():
    time.sleep(3)
    return {"method": "sync"}

@app.get("/async")
async def async_endpoint():
    await asyncio.sleep(3)
    return {"method": "async"}

#path parameter example
#call by http://xxx/path/10
@app.get("/path/{x}")
async def pathmethod(x: int) -> dict:
    await asyncio.sleep(3)
    return {"method": "path method", "response": x}

#query parameter example
#call by http://xxx/query?x=10
@app.get("/query")
async def querymethod(x: int = 0) -> dict:
    await asyncio.sleep(3)
    return {"method": "query method", "response": x}


#post method example
##call by http://xxx/post
# with body {"x": 10}
@app.post("/post")
async def postmethod(request: dict)-> dict:
    x=request.get("x", 0)
    await asyncio.sleep(3)
    return {"method": "post method","response":x}


#frontend example
from fastapi.responses import HTMLResponse
@app.get("/renderhtml",response_class=HTMLResponse)
async def render_html():
    html_content = """
    <html>
        <head>
            <title>FastAPI HTML Example</title>
        </head>
        <body>
            <h1>Welcome to FastAPI!</h1>
            <p>This is a simple HTML page served by FastAPI.</p>
        </body>
    </html>
    """
    return html_content

from fastapi.templating import Jinja2Templates
from fastapi import Request
@app.get("/rendertemplate",response_class=HTMLResponse)
async def render_template(request: Request):
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("index.html", {"request": request, "title": "FastAPI Template Example Jinja"})


