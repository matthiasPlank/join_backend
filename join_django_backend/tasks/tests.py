from django.test import TestCase

# Create your tests here.
class URLTaskTests(TestCase): 

    def test_getTask(self): 
        response = self.client.get('/tasks/') 
        self.assertEqual(response.status_code, 200)