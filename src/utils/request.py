
import requests
import json

class Request:
    def __init__(self, url, user, param=None):
        self.url=url
        self.param=param
        self.user=user

    def get(self):
        headers = {"Authorization": f"Bearer {self.user['token']}"}
        result=requests.get(self.url, json=self.param, headers=headers)
        dict_result= json.loads(str(result.text))
        if dict_result['status']:
            return dict_result
        else:
            return None
        
    def post_file(self, file_path):
        headers = {"Authorization": f"Bearer {self.user['token']}"}
        files = {'file': open(file_path,'rb')}
        result=requests.post(self.url,files=files, headers=headers)
        dict_result= json.loads(str(result.text))
        if dict_result['status']:
            return dict_result
        else:
            return None
