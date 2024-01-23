import json
from django.test import Client, TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# Create your tests here.
class URLTaskTests(TestCase): 

    """
    Checks if tasks can be fetched
    """
    def test_getTask(self): 
        response = self.client.get('/api/tasks/' , headers=getAuthForTest(self)) 
        self.assertEqual(response.status_code, 200)

    """
    Checks if a new task can be created
    """
    def test_createTask(self): 
        data = {
                "title": "Test",
                "description": "Test",
                "category": "media",
                "dueDate": "2024-01-19",
                "assigned": [],
                "kanban": "to-do",
                "priority": "medium",
                "subtasks": [
                    "Test",
                    "Test"
                ],
                "subtaskStatus": [
                    False,
                    False
                ]
            }
        response = self.client.post('/api/tasks/' , json.dumps(data) , content_type='application/json', headers=getAuthForTest(self)) 
        self.assertEqual(response.status_code, 201)

    """
    Checks if a task can be updated
    """
    def test_updateExistingTask(self): 
        addTaskToDB(self)
        data = {
                "id" : "1", 
                "title": "Test",
                "description": "Test Änderung",
                "category": "media",
                "dueDate": "2024-01-19",
                "assigned": [],
                "kanban": "to-do",
                "priority": "medium",
                "subtasks": [
                    "Test",
                    "Test" 
                ],
                "subtaskStatus": [
                    False,
                    False
                ]
            }
        path = '/api/tasks/' + data['id'] + '/'
        response = self.client.put(path, json.dumps(data), content_type='application/json', headers=getAuthForTest(self))
        self.assertEqual(response.status_code, 200)


    """
    Checks if contatcs can be fetched
    """
    def test_getContacts(self): 
        response = self.client.get('/api/contacts/' , headers=getAuthForTest(self)) 
        self.assertEqual(response.status_code, 200)
    
    """
    Checks if a new contact can be created
    """
    def test_createContact(self): 
        data = {
            "firstName": "Matthias",
            "lastName": "Plank",
            "email": "123@123.at",
            "tel": "066412345678",
            "bgIconColor": "#45e3a8"
        }
        response = self.client.post('/api/contacts/', json.dumps(data), content_type='application/json', headers=getAuthForTest(self)) 
        self.assertEqual(response.status_code, 201)

    """
    Checks if a existing contact can be updated
    """
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
        path = '/api/contacts/' + data['id'] + '/'
        response = self.client.put(path , json.dumps(data), content_type='application/json', headers=getAuthForTest(self)) 
        self.assertEqual(response.status_code, 200)


    """
    Checks if a none existing contact can be updated
    """
    def test_updateNotExistingContact(self): 
        data = {
            "id": "11", 
            "firstName": "Mario",
            "lastName": "Plank",
            "email": "123@123.at",
            "tel": "066412345678",
            "bgIconColor": "#45e3a8"
        }
        path = '/api/contacts/' + data['id'] + '/'
        response = self.client.patch(path , json.dumps(data), content_type='application/json', headers=getAuthForTest(self)) 
        self.assertEqual(response.status_code, 404)



"""
Returns the auth header parameters
"""
def getAuthForTest(self): 
    return {}

    # DEACTIVATE FOR TEST WITHOUT CSFR
    """
    self.client = Client()        
    self.user, created = User.objects.get_or_create(username='test_user', password='test_user')        
    self.client.login(username='test_user', password='test_user')
    token, created  = Token.objects.get_or_create(user = self.user)
    header = {"Authorization": "Token " + token.key }

    return header
    """

"""
Adds a new Task to DB
"""
def addTaskToDB(self):
    data = {
                "title": "Test",
                "description": "Test",
                "category": "media",
                "dueDate": "2024-01-19",
                "assigned": [],
                "kanban": "to-do",
                "priority": "medium",
                "subtasks": [
                    "Test",
                    "Test"
                ],
                "subtaskStatus": [
                    False,
                    False
                ]
    }
    response = self.client.post('/api/tasks/' , json.dumps(data) , content_type='application/json', headers=getAuthForTest(self)) 

"""
Adds a new Contact to DB
"""
def addContactToDB(self):
    data = {
            "firstName": "Matthias",
            "lastName": "Plank",
            "email": "123@123.at",
            "tel": "066412345678",
            "bgIconColor": "#45e3a8"
    }
    response = self.client.post('/api/contacts/', json.dumps(data), content_type='application/json', headers=getAuthForTest(self)) 