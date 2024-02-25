from dotenv import load_dotenv
import os
import requests
import json

class Conn:
    def __init__(self):
        load_dotenv()
        self.API = os.getenv("API_URL")
        self.url = self.API

    def get_data(self):
        self.response = requests.get(self.url)
        self.responseJson = self.response.json()
        self.result = self.responseJson['results'][0]
        return self.result
    
    def format_data(self, response):
        self.data = {}
        self.res = response
        self.location = self.res['location']

        # Register data
        self.data['username'] = self.res['login']['username']
        self.data['email'] = self.res['email']
        self.data['picture'] = self.res['picture']['medium']
        self.data['dob'] = self.res['dob']['date']
        self.data['registered_date'] = self.res['registered']['date']
        
        # Person data
        self.data['first_name'] = self.res['name']['first']
        self.data['last_name'] = self.res['name']['last']
        self.data['gender'] = self.res['gender']
        self.data['phone'] = self.res['phone']
        
        # postal data
        self.data['address'] = f"{str(self.location['street']['number'])} {self.location['street']['name']}" \
                          f"{self.location['city']}, {self.location['state']}, {self.location['country']}"
        self.data['postcode'] = self.location['postcode']

        return self.data

    def stream_data(self):
        self.response = self.get_data()
        self.response = self.format_data(self.response)
        print(json.dumps(self.response, indent=2))

conn = Conn()
conn.stream_data()