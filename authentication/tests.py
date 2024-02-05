from django.test import TestCase
from authentication.models import *

# Create your tests here.
class MockTest(TestCase):
    def testTodo(self):
        label = "mock"
        description = "mock"
        obj = Todo(label=label,description=description)
        self.assertEqual(obj.label,label)
