# from os import get_inheritable
from scrapy.utils.log import configure_logging
import logging
from logging.handlers import RotatingFileHandler
import scrapy
import requests
import os
from scrapy.http.request import Request
import time
from urllib.parse import urljoin
# from bs4 import BeautifulSoup
from lxml import html

import json, sys, re
sys.path.append(os.getcwd())
from src.models.area_model import AreaModel
from src.models.city_model import CityModel
from datetime import datetime

emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                "]+", flags=re.UNICODE)

class ScrapyCrawlNewAidSpider(scrapy.Spider):
    
    custom_settings = {
            'FEEDS' : {
                f'{os.getcwd()}/storage/crawl_new_aid/result_%(area_id)s_crawl_new_aid.json' : {
                    'format' : 'json',
                    'overwrite': True
                }
            }
        }
    
    log_file_path=f'{os.getcwd()}/storage/logs/'
    prefecture_info_by_area_id='http://127.0.0.1:8001/api/external_crawl/prefecture-info/'
    name            = 'ScrapyCrawlNewAid'

    allowed_domains = []
    start_urls = []
    baseUrl         = ''
    city_id         = ''
    area_id         = ''
    area            = ''
    title_tags      = ['h2', 'h3', 'h4']
    title           = ''
    contents        = ''
    keyword_title               = ''
    keyword_abstract            = ''
    keyword_support_detail      = ''
    keyword_target              = ''
    keyword_application_period  = ''
    keyword_in_content          = ''
    action                      = ''
    id                          = ''
    path_to_get_main_list   = ''
    path_to_get_sub_list    = ''
    path_to_get_title       = ''
    path_to_get_abstract    = ''
    path_to_get_content     = ''
    path_to_get_category    = ''
    check_contact_info      = ''
    update_date_info        = ''
    category_status         = ''
    time                    = ''
    act_message = 'False'
    log_file_name=''
    is_dynamic = 'True'
    keyword_by_area         = ''
    tag_for_remove          = ''
    check_tag_for_remove    = ''
    url_pattern             = ''
    deny_url_pattern        = ''

    IGNORED_EXTENSIONS = [
        'mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif', 'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg',
        'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',
        '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv', 'm4a',
        'css', 'pdf', 'doc', 'exe', 'bin', 'rss', 'zip', 'rar', 'dat'
    ]
    
    exist_urls=[]
    
    def __init__(self, area_id = None, token=None):
        self.area_id=area_id
        self.token=token
        self.setUplogs(f'log_{area_id}_crawl_new_aid.log')

        logging.log(logging.INFO, 'Initialize parameter')
        self.get_prefecture_info_by_area_id()

        
    def get_prefecture_info_by_area_id(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        result=requests.get(self.prefecture_info_by_area_id + self.area_id, headers=headers)
        dict_result= json.loads(str(result.text))
        if dict_result['status']:
            area=AreaModel.parse_obj(dict_result['data']['area'])
            city=CityModel.parse_obj(dict_result['data']['city'])
            self.exist_urls=[u['url'] for u in dict_result['data']['url']]
            
            self.city_id                     = city.id
            self.area_id                     = area.id
            self.area                        = city.city_name.split('|')[0]+'-'+area.area_name.split('|')[0]
            self.allowed_domains             = [area.allowe_domain]
            self.baseUrl                     = area.tag_lists
            self.start_urls                  = [area.url]
            self.path_to_get_main_list       = area.tag_main_list.split('&')
            self.path_to_get_sub_list        = area.tag_sub_lists.split('&')
            self.path_to_get_content         = area.tag_detail_page
            self.path_to_get_title           = area.tag_title .split('&')
            self.path_to_get_abstract        = area.tag_abstract
            self.path_to_get_category        = None
            self.update_date_info            = area.tag_update_date
            self.check_contact_info          = area.tag_contact_detail

            self.keyword_title               = city.search_keyword
            self.keyword_abstract            = city.abstract
            self.keyword_support_detail      = city.support_detail
            self.keyword_target              = city.target
            self.keyword_application_period  = city.application_period

            self.action                      = 'crawl_new_aid'
            self.id                          = area.id
            self.category_status             = area.category_status
            self.time                        = area.time
            self.keyword_by_area             = area.search_keyword
            self.tag_for_remove              = area.tag_for_remove
            self.check_tag_for_remove        = area.check_tag_for_remove
            self.url_pattern                 = area.url_pattern
            self.deny_url_pattern            = area.deny_url_pattern

            self.keyword_title=self.check_and_replace(self.keyword_title[0])
            self.keyword_by_area=self.check_and_replace(self.keyword_by_area[0])
            if self.keyword_by_area:
                self.keyword_title = self.keyword_title+"|"+self.keyword_by_area
            else:
                self.keyword_title = self.keyword_title

            self.keyword_abstract=self.check_and_replace(self.keyword_abstract[0])
            self.keyword_support_detail=self.check_and_replace(self.keyword_support_detail[0])
            self.keyword_target=self.check_and_replace(self.keyword_target[0])
            self.keyword_application_period=self.check_and_replace(self.keyword_application_period[0])

            self.keyword_in_content          = self.keyword_abstract+'|'+self.keyword_support_detail+'|'+self.keyword_target+'|'+self.keyword_application_period
            

        else:
            logging.log(logging.ERROR, 'Problem on get_prefecture_info_by_area_id')


    # Default callback method responsible for returning the scraped output and processing it.
    def parse(self, response):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        
        for get_main_link in self.path_to_get_main_list:
            for link in response.xpath(self.check_and_replace(get_main_link)):
                category = link.xpath('./text()').get()
                url = link.xpath('./@href').get()
                if self.check_url(url):
                    time.sleep(float(self.time))
                    yield Request(self.remov_duplicates(urljoin(response.url, url)), callback=self.parse_list, cb_kwargs={'category': category}, headers=headers)
                else:
                    logging.log(logging.WARNING,"Invalid URL: " + url)
    

    def parse_list(self, response, category):
        for get_sub_link in self.path_to_get_sub_list:
            for link in response.xpath(self.check_and_replace(get_sub_link)):
                url = link.xpath('./@href').get()
                if self.check_url(url):
                    time.sleep(float(self.time))
                    yield Request(self.remov_duplicates(urljoin(response.url, url)), callback=self.parse_list, cb_kwargs={'category': category})
                else:
                    logging.log(logging.WARNING,"Invalid URL: " + url)

        # contact = response.xpath(self.check_and_replace(self.check_contact_info))
        for get_title in self.path_to_get_title:
            if "|" in get_title:
                self.title = response.xpath(self.check_and_replace(get_title.split('|')[0]))[int(get_title.split('|')[1])]
            else:
                self.title = response.xpath(self.check_and_replace(get_title))
            if self.title:
                break
        if self.title:
            yield self.parse_data(response, category,'','')


    def parse_data(self, response, category, id, approve_id):
        if self.category_status == '1':
            get_category = self.check_and_replace(self.path_to_get_category).split('|')
            if len(get_category)==2:
                category = response.xpath(get_category[0])[int(get_category[1])].getall()
            else:
                category = response.xpath(self.check_and_replace(self.path_to_get_category)).getall()

        logging.log(logging.INFO,"check detail: " + response.url)
        updated_at = ''
        try:
            updated_at = response.xpath(self.check_and_replace(self.update_date_info)).getall()
        except Exception as e:
            logging.log(logging.ERROR,"<b>Error on XPATH update_at at url " + response.url+"</b>")
            logging.log(logging.ERROR,str(f"<b>{e=}, {type(e)=}</b>"))

        date = datetime.now()
        currentDate = date.strftime('%Y-%m-%d %H:%M:%S')
        abstract = None
        support_details = ""
        target = ""
        application_period = ""
        checkGetOrNot = self.check_get_or_not(response)
        contact_detail = ""

        try:
            contact_detail = response.xpath(self.check_and_replace(self.check_contact_info)).getall()
        except Exception as e:
            logging.log(logging.ERROR,"<b>Error on XPATH contact_detail at url " + response.url+"</b>")
            logging.log(logging.ERROR,str(f"<b>{e=}, {type(e)=}</b>"))

        try:
            abstract = response.xpath(self.check_and_replace(self.path_to_get_abstract)).getall()
        except Exception as e:
            logging.log(logging.ERROR,"<b>Error on XPATH abstract at url " + response.url+"</b>")
            logging.log(logging.ERROR,str(f"<b>{e=}, {type(e)=}</b>"))


        if checkGetOrNot:
            # logging.log(logging.INFO,self.title.getall())
            for i, tag in enumerate(self.contents):
                if abstract is None:
                    abstract = tag.xpath('.//p[2]//text()').getall()
                if tag.xpath('name()').get() in self.title_tags:
                    header = tag.xpath('.//text()')
                    if header is not None:
                        if abstract is None:
                            if re.search(r''+self.keyword_abstract, header.get()):
                                abstract = self.contents[i + 1].xpath('.//p//text()').get()
                            continue
                        if re.search(r''+self.keyword_support_detail, header.get()):
                            support_details = self.contents[i + 1].xpath('.//text()').getall()
                            continue
                        if re.search(r''+self.keyword_target, header.get()):
                            target = self.contents[i + 1].xpath('.//text()').getall()
                            continue
                        if re.search(r''+self.keyword_application_period, header.get()):
                            application_period = self.contents[i + 1].xpath('.//text()').getall()
                            continue
            
            #content detail
            content = ''.join(self.contents.getall())
            if self.tag_for_remove and self.check_tag_for_remove == "1":
                soup_content = BeautifulSoup(content,"lxml")
                tag = self.tag_for_remove.split("&")
                for lists in tag:
                    items = lists.split("|")
                    for  ex in soup_content.find_all(items[0], {items[1]: items[2]}):
                        ex.extract()
            else:
                soup_content = content

            soup_content = str(soup_content).replace("<html><body>","")
            soup_content = str(soup_content).replace("</body></html>","")

            # remove emoji
            soup_content=emoji_pattern.sub(r'', soup_content)
        
            # contact detail
            contact_detail=''.join(contact_detail)
            try:
                tree=html.fromstring(contact_detail)
                contact_detail=''.join(tree.xpath('//text()'))
            except Exception as e:
                print(f'{e}')

            if self.url_pattern != None:
                if self.deny_url_pattern == '1':
                    deny_url = self.url_pattern.split("|")
                    for du in deny_url:
                        if len(re.findall(r''+du, response.url)) != 0:
                            logging.log(logging.WARNING,"URL pattern invalid: " + response.url)
                            return
                else:
                    deny_url = self.url_pattern.split("|")
                    for du in deny_url:
                        if len(re.findall(r''+du, response.url)) == 0:
                            logging.log(logging.WARNING,"URL pattern invalid: " + response.url)
                            return
                        
            if response.url not in self.exist_urls:
                return {'city_id':self.city_id,
                'area_id':self.area_id,
                'abstract':str(''.join(abstract).strip()) if (abstract) else '',
                'application_end_date':"",
                'application_period': ''.join(application_period),
                'application_start_date':"",
                'area':self.area,
                'category':''.join(category).strip(),
                'contact_detail':''.join(contact_detail),
                'contents': soup_content,
                'crawled_at':currentDate,
                'institution':self.area,
                'support_details':''.join(support_details),
                'target':''.join(target),
                'title':''.join(self.title.getall()).replace('>','').strip(),
                'url':response.url,
                'update_date':''.join(updated_at).strip(),
                'status':1,
                'active_url':'yes',
                'created_at':currentDate,
                'crawl_update':'yes'}
        

    def check_get_or_not(self, response):
        try:
            for get_title in self.path_to_get_title:
                if "|" in get_title:
                    self.title = response.xpath(self.check_and_replace(get_title.split('|')[0]))[int(get_title.split('|')[1])]
                else:
                    self.title = response.xpath(self.check_and_replace(get_title))
                if self.title:
                    break

            if self.title is not None:
                self.contents = response.xpath(self.check_and_replace(self.path_to_get_content))
                if len(self.title.re(r''+self.keyword_title)):
                    return True
                else:
                    count_index = 0
                    for content in self.contents:
                        if content.xpath('name()').get() in self.title_tags:
                            header = content.xpath('.//text()')
                            if header is not None:
                                if len(header.re(r''+self.keyword_in_content)) > 0:
                                    if(count_index == 3):
                                        return True
                                    count_index = count_index+1
            return False

        except Exception as e:
            logging.log(logging.ERROR,"<b>Error on XPATH Title at url " + response.url+"</b>")
            logging.log(logging.ERROR,str(f"<b>{e=}, {type(e)=}</b>"))
            return False       

    def check_url(self, url):
        # if self.area_id == 1389
        #     url = url.replace('contents/aboutsite/','')
        #     url = url.replace('contents/lifestage/','')
        #     url = url.replace('contents/shisetu/','')
        # return True
        if(url.split('?')[0].endswith(tuple(self.IGNORED_EXTENSIONS)) or "mailto" in url or "javascript" in url):
            return False
        else:
            return True
        
    def remov_duplicates(self, url):
        # if self.area_id == 1389
        #     url = url.replace('contents/aboutsite/','')
        #     url = url.replace('contents/lifestage/','')
        #     url = url.replace('contents/shisetu/','')

        # input = url.split("/")
        # UniqW = Counter(input)
        # result = "/".join(UniqW.keys())
        # if url[-1] == '/':
        #     return result+"/"
        # else:
        #     return result
        return url

    def check_and_replace(self, xpath):
        xpath=xpath.replace("'''", "")
        if("contains" in xpath):
            return xpath.replace('=',',')
        else:
            return xpath

    def setUplogs(self, logfile_path):
        log_file = self.log_file_path + logfile_path
        f = open(log_file, 'a+')
        f.truncate(0)
        f.close()
        configure_logging(install_root_handler=False)
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        formatter = logging.Formatter('<strong>[%(asctime)s-%(name)s-%(levelname)s]</strong> %(message)s<br>')#2022-08-04 04:36:32 [root] ERROR:
        rotating_file_log = RotatingFileHandler(log_file, maxBytes=100485760, backupCount=1)
        rotating_file_log.setLevel(logging.INFO)
        rotating_file_log.setFormatter(formatter)
        root_logger.addHandler(rotating_file_log)