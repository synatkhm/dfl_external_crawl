

from src.controllers.controller import Controller
from fastapi import APIRouter, Request, Response, Depends, FastAPI, status
from starlette.responses import JSONResponse, Response
import requests
from src.utils.api import Api
from src.utils.request import Request
from src.models.city_model import CityModel, CitiesModel
from src.models.area_model import AreaModel , AreasModel
import os


class DataController(Controller):
    
    user=''
    def __init__(self, user) -> None:
        super().__init__()
        self.user=user

    def index(self, request):
        
        # get prefictur information
        pre_info=Request(Api.prefecture_info, user=self.user).get()
        
        cities = CitiesModel().from_json(pre_info['data']['city'])
        areas = AreasModel().from_json(pre_info['data']['area'])
        city_list = CitiesModel().array_to_json(cities)
        area_list = AreasModel().array_to_json(areas)
        return super().templates.TemplateResponse("home.html", {"request": request,'email':self.user["user"]['email'],'area_list': area_list, 'city_list': city_list})

    def crawl_new_aid(self, request, area_id):
        # os.system(f'python {os.getcwd()}/src/scrapy_crawl/scrapy_loader.py {area_id} { self.user["token"].split("|")[1]}')
        return JSONResponse(status_code=status.HTTP_200_OK, content={'status': True, 'message': 'Crawl new aid success.'})
    
    def get_crawl_new_aid_log(self, request, area_id):
        return super().templates.TemplateResponse("logs.html", {"request": request,'area_id': area_id})
    
    def post_crawl_new_aid_log(self, request, area_id):

        try:
            filepath=f'{os.getcwd()}/storage/logs/log_{area_id}_crawl_new_aid.log'
            f = open(filepath, "r")
            log=f.read()
            return log
        except:
            return ''
        
    def post_crawl_new_aid(self, request, area_id):
        try:
            filepath=f'{os.getcwd()}/storage/crawl_new_aid/result_{area_id}_crawl_new_aid.json'
            f = open(filepath, "r")
            data=f.read()
            return data
        except:
            return ''
        
    def upload_crawl_new_aid(self, request, area_id):
        try:
            filepath=f'{os.getcwd()}/storage/crawl_new_aid/result_{area_id}_crawl_new_aid.json'
            result=Request(Api.upload_file_crawl_new_aid, user=self.user).post_file(filepath)
        except:
            result={
                'status': False,
                'message': 'The selected area is data empty.'
            }
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)

