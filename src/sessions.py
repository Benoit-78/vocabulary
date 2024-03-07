from fastapi import FastAPI, Depends, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.session import Session

app = FastAPI()


@app.middleware("http")
async def add_custom_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["custom-header"] = "custom-value"
    return response


@app.get("/")
async def read_item(session: Session = Depends(get_session)):
    return {"message": "Hello World"}


def get_session(request: Request):
    return Session(request=request)


# Include a secret key for session cookies
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")



# ==============================================================================

# In the router

from fastapi import FastAPI, Depends, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.session import Session

app = FastAPI()

@app.get("/")
async def read_item(session: Session = Depends(get_session)):
    # Check the session for user-specific data
    user_data = session.get("user_data", None)
    if not user_data:
        # Initialize user-specific data
        user_data = initialize_user_data()
        session["user_data"] = user_data
    return {"message": "Hello World", "user_data": user_data}

def get_session(request: Request):
    return Session(request=request)


# ==============================================================================


from fastapi import FastAPI, Depends, Request, Response
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_db = {}

@app.post("/token")
async def login(form_data: OAuthFlowsModel.password, response: Response):
    token = "fake-access-token"
    response.set_cookie(key="access_token", value=token, httponly=True)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    return {"message": "This is a protected resource"}




# ==============================================================================

# In JavaScript
// Storing in session storage
sessionStorage.setItem('userName', data.userName);

// Retrieving in another function or page
var storedUserName = sessionStorage.getItem('userName');



.then(data => {
    if (data && data.message === "User account created successfully") {
        // Use sessionStorage to store userName
        sessionStorage.setItem('userName', data.userName);
        // Redirect to user-space with userName as a query parameter
        window.location.href = `/user-space?userName=${data.userName}?userPassword=${data.userPassword}`;
    }

# ==============================================================================

# Cookies

from fastapi import Cookie

@app.get("/user-space", response_class=HTMLResponse)
def user_main_page(request: Request, user_name: str = Cookie(default=None)):
    """Call the base page of user space"""
    global cred_checker
    
    # Check credentials if provided in the Cookie
    if user_name:
        cred_checker.check_credentials(user_name)
    
    return templates.TemplateResponse(
        "user/user_space.html",
        {
            "request": request,
            "userName": user_name
        }
    )
