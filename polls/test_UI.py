import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Question, Choice

from test_essentials import *

class UITest(TestCase):
    pass


# Too complicated, I don't know how to do this yet.