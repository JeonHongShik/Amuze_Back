from django.test import TestCase
from .models import Post,wish_types
import django

# Create your tests here.
def get_post(self):
    return self.request.Post.get(self.field_name)