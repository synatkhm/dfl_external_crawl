
from pydantic import BaseModel
from datetime import datetime
from pydantic.schema import Optional

class AreaModel(BaseModel):
    id: int
    city_id: int
    area_name: str
    allowe_domain: str
    url: str
    tag_main_list: str
    tag_lists: str
    tag_detail_page: str
    tag_title: str
    tag_update_date: str
    tag_sub_lists: str
    tag_contact_detail: str
    tag_abstract: str
    tag_header: Optional[str]
    status: str
    crawl_status: Optional[str]
    is_deleted: str
    created_at: datetime
    updated_at: Optional[str]
    category_status: int
    dynamic_website: int
    time: int
    code: Optional[str]
    search_keyword: Optional[list[str]]
    tag_for_remove: Optional[str]
    check_tag_for_remove: int
    url_pattern: Optional[str]
    deny_url_pattern: Optional[int]


class AreasModel(BaseModel):
    areas: list[AreaModel]=[]
    def from_json(self, json):
        for j in json:
            self.areas.append(AreaModel.parse_obj(j))
        return self.areas
    
    def array_to_json(self, areas):
        return [{'id': a.id, 'city_id':a.city_id, 'name': a.area_name, } for a in areas]
         