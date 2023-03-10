from fastapi import FastAPI, Request

from src.router import data
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse, HTMLResponse
from fastapi import FastAPI, Depends, Request, status
from fastapi.staticfiles import StaticFiles
from src.utils.api import Api
import requests
import json
from src.utils.exception import NotAuthenticatedException
from src.utils.custom_login_manager import manager, DB
from src.utils.templates import templates

app = FastAPI()

@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    """
    Redirect the user to the login page if not logged in
    """
    return RedirectResponse(url='/login')

app.include_router(data.router, prefix="/data", dependencies=[Depends(manager)])

# init html rendering
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post('/login')
def login(request: Request, data: OAuth2PasswordRequestForm = Depends()):
    param = {
        "email": data.username,
        "password": data.password,
    }
    try:
        result=requests.post(Api.login, json=param)
        dict_result= json.loads(str(result.text))
        if dict_result['status']:
            global DB
            DB['users'][data.username]=dict_result
            token = manager.create_access_token(data={'sub': data.username})
            response = RedirectResponse(url="/",status_code=status.HTTP_302_FOUND)
            manager.set_cookie(response, token)
            return response
        else:
            return templates.TemplateResponse("login.html", {"request": request, 'message': 'Invalid credentials.'})
    
    except:
        return templates.TemplateResponse("login.html", {"request": request, 'message': 'Can not connect to API.'})
    

@app.post('/logout')
def logout(user=Depends(manager)):
    response = RedirectResponse(url="/login",status_code=status.HTTP_302_FOUND)
    manager.set_cookie(response, None)
    return response

@app.get("/")
def read_root(user=Depends(manager)):
    return RedirectResponse(url="/data",status_code=status.HTTP_302_FOUND)

@app.get("/favicon.ico")
def favicon(user=Depends(manager)):
    return ''

