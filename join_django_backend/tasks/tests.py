import json
from django.test import Client, TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# Create your tests here.
class URLTaskTests(TestCase): 

    def test_getTask(self): 
        response = self.client.get('/tasks/' , headers=getAuthForTest(self)) 
        self.assertEqual(response.status_code, 200)

    """
    def test_createTask(self): 
        data = 
        response = self.client.post('/tasks/' , body=data , headers=getAuthForTest(self)) 
        self.assertEqual(response.status_code, 200)
    """

    def test_getContacts(self): 
        response = self.client.get('/contacts/' , headers=getAuthForTest(self)) 
        self.assertEqual(response.status_code, 200)
    

    def test_createContact(self): 
        data = {
            "firstName": "Matthias",
            "lastName": "Plank",
            "email": "123@123.at",
            "tel": "066412345678",
            "bgIconColor": "#45e3a8"
        }
        response = self.client.post('/contacts/', json.dumps(data), content_type='application/json', headers=getAuthForTest(self)) 
        self.assertEqual(response.status_code, 200)


    def test_updateExistingContact(self): 
        addContactToDB(self)
        data = {
            "id": "1", 
            "firstName": "Mario",
            "lastName": "Plank",
            "email": "123@123.at",
            "tel": "066412345678",
            "bgIconColor": "#45e3a8"
        }
        path = '/contacts/' + data['id'] + '/'
        print(path)
        response = self.client.patch(path , json.dumps(data), content_type='application/json', headers=getAuthForTest(self)) 
        self.assertEqual(response.status_code, 200)


    def test_updateNotExistingContact(self): 
        data = {
            "id": "11", 
            "firstName": "Mario",
            "lastName": "Plank",
            "email": "123@123.at",
            "tel": "066412345678",
            "bgIconColor": "#45e3a8"
        }
        path = '/contacts/' + data['id'] + '/'
        print(path)
        response = self.client.patch(path , json.dumps(data), content_type='application/json', headers=getAuthForTest(self)) 
        self.assertEqual(response.status_code, 404)







def getAuthForTest(self): 
    self.client = Client()        
    self.user, created = User.objects.get_or_create(username='test_user', password='test_user')        
    self.client.login(username='test_user', password='test_user')
    token, created  = Token.objects.get_or_create(user = self.user)
    header = {"Authorization": "Token " + token.key }

    return header

def addContactToDB(self):
    data = {
            "firstName": "Matthias",
            "lastName": "Plank",
            "email": "123@123.at",
            "tel": "066412345678",
            "bgIconColor": "#45e3a8"
    }
    response = self.client.post('/contacts/', json.dumps(data), content_type='application/json', headers=getAuthForTest(self)) 
    print(response)
