from pydantic import BaseModel
from datetime import datetime

class CityModel(BaseModel):
    id: int
    city_name: str
    search_keyword: list[str]
    abstract: list[str]
    support_detail: list[str]
    target: list[str]
    application_period: list[str]
    created_at: datetime
    updated_at: datetime
    code: None

class CitiesModel(BaseModel):
    cities: list[CityModel]=[]
    def from_json(self, json):
        
        for j in json:
            self.cities.append(CityModel.parse_obj(j))
        return self.cities
    
    def array_to_json(self, cities):
        return [{'city_id':c.id, 'name': c.city_name, } for c in cities]
         

        


    