
from fastapi import FastAPI, Depends, HTTPException, status,APIRouter,Request
from fastapi.responses import RedirectResponse, JSONResponse,HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from jose import JWTError, jwt
from passlib.context import CryptContext
import datetime
from dotenv import load_dotenv


#Authendication
'''Authentication is the process of verifying the identity of a user or system.
In web applications, authentication typically involves checking credentials like usernames and passwords'''

#what is OAuth2?
'''OAuth2 is an authorization framework that enables third-party applications to obtain limited access to a web
service on behalf of a user, without sharing the user's credentials.
It allows users to grant access to their resources on one site to another site without sharing their credentials
and provides a way to manage access tokens that can be used to authenticate API requests.
OAuth2 is widely used for securing APIs and enabling single sign-on (SSO) across different applications.
'''

#single sign-on (SSO):
'''
Single Sign-On (SSO) is an authentication process that allows a user to access multiple applications with one set of login credentials.
In FastAPI, SSO can be implemented using OAuth2 or OpenID Connect, where the user logs in once and receives a token that can be used to access multiple services without needing to log in again.
'''

#configure sso with GitHub:
'''GitHub OAuth2 is a popular method for implementing SSO in web applications.
It allows users to log in using their GitHub account, providing a seamless authentication experience.
This is done by redirecting the user to GitHub's authorization page, where they can grant access to your application.
After the user authorizes the application, GitHub redirects back to your application with an authorization code,
which can be exchanged for an access token.
This access token can then be used to authenticate API requests and access user information from GitHub.

steps to implement GitHub OAuth2 in FastAPI:
1. Register your application on GitHub to obtain a client ID and client secret.
    github:settings--> developers settings --> OAuth Apps
2. Create an endpoint to redirect users to GitHub's authorization page.
3. Create a callback endpoint to handle the redirect from GitHub after authorization.
4. Exchange the authorization code for an access token.
'''


app = APIRouter()

class Sso():
    def __init__(self, redirect_url: str):
        load_dotenv()
        self.redirect_url = redirect_url
        self.oauth = OAuth(Config())
        self.oauth.register(
            name='github',
            access_token_url='https://github.com/login/oauth/access_token',
            access_token_params=None,
            authorize_url='https://github.com/login/oauth/authorize',
            authorize_params=None,
            api_base_url='https://api.github.com/',
            client_kwargs={'scope': 'user:email'},
        )
        app.add_route("/login_with_git_hub", self.login, methods=["GET"])
        app.add_route("/github/callback", self.auth_github_callback, methods=["GET"], name="github_callback")
      
    async def login(self, request: Request):
        try:
            redirect_uri = request.url_for('github_callback')
            return await self.oauth.github.authorize_redirect(request, redirect_uri)
        except Exception as e:
            return HTMLResponse(f"<h1>GitHub Login Failed</h1><p>{str(e)}</p>", status_code=500)

    async def auth_github_callback(self, request: Request):
        try:
            token = await self.oauth.github.authorize_access_token(request)
            user_data = await self.oauth.github.get('user', token=token)
            profile = user_data.json()
            request.session['user'] = profile
            return RedirectResponse(url=self.redirect_url)
        except Exception as e:
            return HTMLResponse(f"<h1>GitHub Login Failed</h1><p>{str(e)}</p>", status_code=500)

@app.get("/home")
def home():
    return JSONResponse(content={"message": "Welcome to the home page!"})
Sso(redirect_url="/home")



#Authorization?
''' Authorization is the process of determining whether a user or system has permission to perform a specific action,
such as accessing a resource or executing a command. authorization involves checking user roles or permissions against the requested resource or action.
'''

#what is JWT?
'''JWT (JSON Web Token) is a compact, URL-safe means of representing claims to be transferred between two parties.
The claims in a JWT are encoded as a JSON object that is used as the payload of a JSON Web Signature (JWS) structure or as the plaintext of a JSON Web Encryption (JWE) structure,
allowing the claims to be digitally signed or integrity protected with a Message Authentication Code (MAC),
and/or encrypted.'''


#what is API key?
'''An API key is a unique identifier used to authenticate a client or application making requests to an
API. It is typically a long string of characters that is passed in the request header or as a query parameter.
API keys are used to control access to the API, track usage, and enforce rate limits.
In FastAPI, API keys can be implemented using dependency injection,
where the API key is checked against a predefined list or database before allowing access to the endpoint.
'''

class AuthService:
    def __init__(self, secret_key: str="a_random_secret_key", algorithm: str="HS256", access_token_expire_minutes: int=30):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.fake_users_db = {"john": {
                "username": "john",
                "hashed_password": "$2b$12$78H88O/uQIzD4HqzdDIjF.7M6PywheWt/UfYA.9SyjP2DpQwgdgee",  # hashed 'secret'
            }}

    def create_access_token(self, username: str, password: str):
        if not self.pwd_context.verify(password, self.fake_users_db[username]["hashed_password"]): 
            raise HTTPException(status_code=400, detail="Invalid credentials")
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=self.access_token_expire_minutes)
        to_encode = {"sub": username, "exp": expire.timestamp()}
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_access_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")     
auth_service = AuthService()

@app.post("/token_class")
async def login_class(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token=auth_service.create_access_token(form_data.username,form_data.password)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me_class")
async def read_users_me_class(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token_class"))):
    payload = auth_service.decode_access_token(token)
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": username}
