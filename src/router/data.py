from typing import Union

from fastapi import APIRouter, Request, Response, Depends, FastAPI, status
from starlette.responses import JSONResponse, Response
from starlette.middleware.sessions import SessionMiddleware
from src.controllers.data_controller import DataController
from fastapi_login import LoginManager
from src.utils.custom_login_manager import *

router = APIRouter()

@router.get("/")
def data_root(request: Request, user=Depends(manager)):

    return DataController(user).index(request)

@router.post("/crawl-new-aid")
async def crawl_new_aid(request: Request, user=Depends(manager)):
    json_request = await request.json()
    return DataController(user).crawl_new_aid(request, json_request['area_id'])

@router.get("/crawl-new-aid/logs/{area_id}")
async def get_crawl_new_aid_log(area_id:str,request: Request, user=Depends(manager)):
    return DataController(user).get_crawl_new_aid_log(request, area_id)

@router.post("/crawl-new-aid/logs/{area_id}")
async def post_crawl_new_aid_log(area_id:str,request: Request, user=Depends(manager)):
    return DataController(user).post_crawl_new_aid_log(request, area_id)

@router.post("/crawl-new-aid/{area_id}")
async def post_crawl_new_aid(area_id:str,request: Request, user=Depends(manager)):
    return DataController(user).post_crawl_new_aid(request, area_id)

@router.post("/upload-crawl-new-aid/{area_id}")
async def upload_crawl_new_aid(area_id:str,request: Request, user=Depends(manager)):
    return DataController(user).upload_crawl_new_aid(request, area_id)


# fixe error load file svg
@router.get("/img/undraw_profile_3.svg")
def data_root(request: Request, user=Depends(manager)):
    return ''
@router.get("/img/undraw_profile_1.svg")
def data_root(request: Request, user=Depends(manager)):
    return ''
@router.get("/img/undraw_profile_2.svg")
def data_root(request: Request, user=Depends(manager)):
    return ''
@router.get("/img/undraw_profile.svg")
def data_root(request: Request, user=Depends(manager)):
    return ''

