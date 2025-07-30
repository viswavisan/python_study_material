# django
'''Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.
It follows the model-template-views (MTV) architectural pattern and provides a robust set of features for building web applications.
Django includes an ORM (Object-Relational Mapping) system for database interactions, a built-in admin interface, and a templating engine for rendering HTML.
Django is known for its "batteries-included" philosophy, meaning it comes with many built-in features that make it easy to build complex web applications quickly.
'''

import os
import django
from django.http import HttpResponse
from django.urls import path
from django.conf import settings
from corsheaders.defaults import default_headers
from django.core.wsgi import get_wsgi_application
from django.views.decorators.http import require_GET,require_POST
from wsgiref.simple_server import make_server

settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=['*'],
    SECRET_KEY='dummy',
    TEMPLATES=[
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'DIRS': [os.path.join(os.path.dirname(__file__), 'templates')],
                    'APP_DIRS': True,
                    'OPTIONS': {'context_processors': [],},
                },
            ],

    MIDDLEWARE=[
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.gzip.GZipMiddleware',
    ],
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ],
    STATIC_URL='/static/',
    CORS_ALLOW_ALL_ORIGINS=True,
    CORS_ALLOW_CREDENTIALS=True,
    CORS_ALLOW_HEADERS=list(default_headers) + [
        'X-Process-Time',
        'X-Frame-options',
        'X-Content-Type-Options',
        'X-XSS-Protection',
        'Strict-Transport-Security',
        'Content-Security-Policy',
    ],
    CORS_ALLOW_METHODS=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
)



# Initialize Django
django.setup()

# Create the WSGI application
app = get_wsgi_application()

def start_server():
    make_server('127.0.0.1', 8000, app).serve_forever()


# Define a simple view
#both get and post methods
def home(request):
    return HttpResponse("Hello, Django!")

#get method
@require_GET
def get_method(request):
    return HttpResponse("This is a GET request.")

#post method
def post_method(request):
    if request.method == 'POST':
        return HttpResponse("This is a POST request.")
    return HttpResponse("This endpoint only accepts POST requests.")

#html response example
@require_GET
def html_response(request):
    return HttpResponse("<h1>Hello, Django!</h1>", content_type="text/html")

#render template with Django's built-in templating engine
from django.shortcuts import render
@require_GET
def render_django_template(request):
    return render(request, "index.html", {"title": "Django Template Example"})

# Define URL patterns
urlpatterns = [
    path('', home),
    path('get/', get_method),
    path('post/', post_method),
    path('html/', html_response),
    path('template/', render_django_template),
]
