import logging
import re, json, sys, os
sys.path.append(os.getcwd())
from src.scrapy_crawl.utils.check_and_replace import check_and_replace

def is_sub_list_aid(response,tag_sub_list,url,title,abstract,application_period,support_details,target,contact_detail,public_at,contents, path_to_get_content):
        # Crawl Table status = 6 detail page as sub menu
        # Approve Table Status = 4 detail page as sub menu
        
        if url.endswith('index.html'):
            if abstract or application_period or support_details or target or contact_detail:
                if abstract and contact_detail=="" and public_at=="":
                    for i, get_sub_link in enumerate(tag_sub_list):
                        sub_list_date = response.xpath(check_and_replace(get_sub_link))
                        if len(sub_list_date)>0:
                            logging.log(logging.INFO,"Menu Page z1.2: "+url)
                            return True
                        else:
                            logging.log(logging.INFO,"Detail Page z1.3: "+url)
                            return False
                    return
                else:
                    for i, get_sub_link in enumerate(tag_sub_list):
                        sub_list = response.xpath(check_and_replace(get_sub_link))
                        if len(sub_list)>0:
                            contents = response.xpath(check_and_replace(path_to_get_content))
                            demo = re.findall(r'"([^"]*)"', get_sub_link)
                            demo = json.dumps(demo)
                            demo = demo.replace('[', '')
                            demo = demo.replace(']', '')
                            demo = demo.replace('"', '')

                            if str(demo) in contents or ("ul" in contents and "a href" in contents):
                                logging.log(logging.INFO,str(demo))
                                logging.log(logging.INFO,"Menu Page z1.4: "+url)
                                return True
                            else:
                                logging.log(logging.INFO,"Detail Page z1: "+url)
                                return False

              
            else:
                for i, get_sub_link in enumerate(tag_sub_list):
                    sub_list_date = response.xpath(check_and_replace(get_sub_link))
                    if len(sub_list_date)>0:
                        logging.log(logging.INFO,"Menu Page z1.1: "+url)
                        return True

        if len(title)<4:
            if len(title)<=2 and contact_detail=='' and public_at=='':
            
                logging.log(logging.INFO,"Menu Page s1.1: "+url)
                return True

            if abstract or application_period or support_details or target:
                logging.log(logging.INFO,"Detail Page s1: "+url)
                return False

            else:
                for i, get_sub in enumerate(tag_sub_list):
                    sub_list_date = response.xpath(check_and_replace(get_sub))
                    contents = response.xpath(check_and_replace(path_to_get_content))
                    sub_list = re.findall(r'"([^"]*)"', get_sub)
                    sub_list = json.dumps(sub_list)
                    sub_list = sub_list.replace('[', '')
                    sub_list = sub_list.replace(']', '')
                    sub_list = sub_list.replace('"', '')
                    if len(sub_list_date)>0 or str(sub_list):
                        logging.log(logging.INFO,"Menu Page s1: "+url)
                        return True
                    else:
                        if i == 0:
                            logging.log(logging.INFO,"Detail Page s1.1: "+url)
                            return False
            return

        for i, get_sub_link in enumerate(tag_sub_list):
            sub_list = response.xpath(check_and_replace(get_sub_link))
            if len(sub_list)>0:
                contents = response.xpath(check_and_replace(path_to_get_content))
                demo = re.findall(r'"([^"]*)"', get_sub_link)
                demo = json.dumps(demo)
                demo = demo.replace('[', '')
                demo = demo.replace(']', '')
                demo = demo.replace('"', '')
                if abstract or application_period or support_details or target :
                    if  abstract or contact_detail or len(title) >= 7:
                        if contact_detail=='' and public_at=='' and abstract=='':
                            logging.log(logging.INFO,"Menu Page s2.1: "+url)
                            return True
                        else:
                            logging.log(logging.INFO,"Detail Page s2: "+url)
                            return False
                    else:
                        
                        logging.log(logging.INFO,"Menu Page s2: "+url)
                        return False

                else:
                    if abstract and contact_detail=="" and public_at=="":
                        logging.log(logging.INFO,"Menu Page z1.2: "+url)
                        return True

                    if len(title) > 15:
                        if contact_detail and public_at:
                            logging.log(logging.INFO,"Detail Page s3: "+url+" , Len Title:"+str(len(title)))
                            return False
                        else:
                            # if len(title) < 15:
                            if str(demo) in contents or ("ul" in contents and "a href" in contents):
                                
                                logging.log(logging.INFO,"Menu Page s3: "+url)
                                return True
                            else:
                                logging.log(logging.INFO,str(demo))
                                logging.log(logging.INFO,"Detail Page s3.1: "+url+" , Len Title:"+str(len(title)))
                                return False
                            
                    else:
                        if contact_detail and len(title) >= 10 and len(sub_list) < 5 and public_at:
                            logging.log(logging.INFO,"Detail Page a2: "+url+" Len Title:"+str(len(title)))
                            return False
                        else:
                            if str(demo) in contents or ("ul" in contents and "a href" in contents):
                            
                                logging.log(logging.INFO,"Menu Page a2: "+url)
                                return True
                            else:
                                logging.log(logging.INFO,str(demo))
                                logging.log(logging.INFO,"Detail Page a2.1: "+url+" Len Title:"+str(len(title)))
                                return False
            else:
                if i == 0:
                    if abstract or application_period or support_details or target:
                        logging.log(logging.INFO,"Detail Page s4: "+url)
                        return False
            logging.log(logging.INFO,"Detail Page: "+url)
            return False
