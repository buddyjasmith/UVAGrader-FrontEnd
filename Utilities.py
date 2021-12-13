from requests.auth import HTTPBasicAuth
import requests
import datetime
import json
import bson
from models import Assignment,  ClassModel
class utilities:
    def __init__(self, ):
        self.api_addy = "http://147.182.202.105:8004"
        self.credentials = HTTPBasicAuth('TerryGriffin', "P4$$W0Rd123")

    def decode_bytes(self, byte_str):
        result = json.loads(byte_str.decode('utf-8'))
        return result
    def create_new_class(self, data):
        url = f'{self.api_addy}/new_class'
        print(type(data))
        print(data)

        print(f'NEW DATA = {data}')
        print(type(data))
        #
        res = requests.post(url,
                            data=json.dumps(data),
                            auth=self.credentials
        )
        print(res.content)
        res = self.decode_bytes(res.content)
        return res

    def update_class_submissions(self, class_name):
        url = f'{self.api_addy}/update_class/{class_name}'
        print(f'URL = {url}')
        result = requests.put(url, auth=self.credentials)
        result = self.decode_bytes(result.content)
        return result
    def get_class_list(self):
        print('IS THIS BEING CCALLED')
        url = f'{self.api_addy}/class_list'
        print(url)
        classes = requests.get(url, auth=self.credentials)
        print(classes.content)
        classes = self.decode_bytes(classes.content)
        return classes
    def get_class_assn(self, class_name):
        url = f'{self.api_addy}/class_assignments/{class_name}'
        print(url)
        response = requests.get(url, auth=self.credentials)

        response = self.decode_bytes(response.content)

        return response
    def add_class_assignment(self,assignment):
        print(assignment)
        print(f'ASSIGNMENT TYPE ={assignment}')
        url = f'{self.api_addy}/new_assignment/'
        response = requests.post(url,
                                 data=json.dumps(assignment),
                                 auth=self.credentials)
        response = self.decode_bytes(response.content)
        return response
    def get_class_data(self, semester):
        url = f'{self.api_addy}/class_submissions/{semester}'
        result = requests.get(url, auth=self.credentials)
        result = self.decode_bytes(result.content)
        return result
    def get_all_student_data(self, class_name):
        url = f'{self.api_addy}/get_class_data/{class_name}'
        students=requests.get(url, auth=self.credentials)
        students = self.decode_bytes(students.content)
        return students
