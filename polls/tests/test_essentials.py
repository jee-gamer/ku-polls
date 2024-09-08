import datetime

from django.test import TestCase
from django.utils import timezone

from django.contrib.auth.models import User

from polls.models import Question, Choice


def create_question_with_choices_and_time(question_text, choice_texts, pub_day, end_day):
    """
    Create a question with the given `question_text`, published the
    given number of `days` offset to now, and a list of `choice_texts`.
    """
    pub_time = timezone.now() + datetime.timedelta(days=pub_day)
    end_time = timezone.now() + datetime.timedelta(days=end_day)
    question = Question.objects.create(question_text=question_text,
                                       pub_date=pub_time,
                                       end_date=end_time)
    for choice_text in choice_texts:
        Choice.objects.create(question=question, choice_text=choice_text)

    return question


class AuthenticationTest(TestCase):

    username = 'ordinaryGuy'
    password = 'extras'

    @classmethod
    def setUp(cls):
        User.objects.create_user(username=cls.username,
                                 password=cls.password)

    def test_auth_user(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertTrue(login)


def login(self):
    AuthenticationTest.setUp()
    self.client.login(username=AuthenticationTest.username,
                      password=AuthenticationTest.password)