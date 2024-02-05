from authentication.models import *
from django.test import TestCase

class MockTest(TestCase):
    def testTodo(self):
        label = "mock"
        description = "mock"
        obj = Todo(label=label,description=description)
        self.assertEqual(obj.label,label)

