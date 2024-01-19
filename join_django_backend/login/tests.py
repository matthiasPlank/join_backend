import json
from django.test import Client, TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
# Create your tests here.
class LoginTests(TestCase): 

 """
    Checks login credentials and returns token
 """
 def test_getToken(self): 
        createTestUser(self); 
        data = {
            "email": "test@test.at",
            "password": "test_user"
        }
        response = self.client.post('/api-token-auth/' , data=json.dumps(data) , content_type='application/json') 
        self.assertEqual(response.status_code, 200)


 """
 Check registers new User
 """
 def test_registerNewUser(self): 
        data = {
            "email": "test@test.at",
            "password": "test_user", 
            "username": "test_user"
        }
        response = self.client.post('/register/' , data=json.dumps(data) , content_type='application/json') 
        self.assertEqual(response.status_code, 200)        

 """
 Checks if userToken is valid
 """
 def test_checkToken(self): 
        user = User.objects.create_user(username='test_user', password='test_user' , email="test@test.at")  
        userToken , created = Token.objects.get_or_create(user=user)
        data = {
            "email" : "test@test.at",
            "token" : userToken.key
        }
        response = self.client.post('/checkToken/' , data=json.dumps(data) , content_type='application/json') 
        return response            

"""
Create a testuser
"""
def createTestUser(self): 
    self.client = Client()        
    self.user = User.objects.create_user(username='test_user', password='test_user' , email="test@test.at")        
