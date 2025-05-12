import unittest
import json
from app import app

class TestStudentAPI(unittest.TestCase):
    def setUp(self):
        # Set up a test client to simulate requests to the app
        self.app = app.test_client()
        self.app.testing = True

    def test_1_get_tasks_details(self):
        # Assuming the endpoint for retrieving all tasks is '/todos'
        response = self.app.get('/todos')
        
        # Assert the status code is 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Check if the response contains an array under the "todos" key
        data = json.loads(response.data)
        self.assertIn("todos", data)
        self.assertIsInstance(data["todos"], list)

    def test_2_post_tasks_details(self):
        # Define a sample task to post
        new_task = {
            "title": "Sample Task",
            "description": "This is a test task for the API",
            "completed": False
        }

        # Post the task to the '/todos' endpoint
        response = self.app.post('/todos', 
                                 data=json.dumps(new_task), 
                                 content_type='application/json')
        
        # Assert the status code is 201 Created
        self.assertEqual(response.status_code, 201)
        
        # Verify the content of the response (the task should be returned)
        data = json.loads(response.data)
        self.assertEqual(data["title"], new_task["title"])
        self.assertEqual(data["description"], new_task["description"])
        self.assertEqual(data["completed"], new_task["completed"])

if __name__ == '__main__':
    unittest.main()
