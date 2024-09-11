"""
Models for Django
Contains class for database and functions on the base level.
"""

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib import admin
# Create your models here.


class Question(models.Model):
    """
    The Question model contains all variables and function related
    to a question.
    """

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", default=timezone.now)
    end_date = models.DateTimeField("end date", default=None,
                                    null=True,
                                    blank=True)

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="published recently?",
    )
    def was_published_recently(self):
        """Check if the poll was published within a day or not."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """
        Returns True if the pub_date of the question is in the past or now.
        :return: boolean
        """
        now = timezone.now()
        return self.pub_date <= now

    def default_date(self):
        """
        Set default date to now.
        unused for now.
        """
        self.pub_date = timezone.now()

    def can_vote(self):
        """
        Return True if question is within voting time.
        :return: boolean
        """
        now = timezone.now()
        if self.pub_date < now:
            if self.end_date is None:
                return True
            elif self.end_date > now:
                return True
        return False

    def __str__(self):
        """Return question text."""
        return self.question_text


class Choice(models.Model):
    """
    The Choice model contains all variable related to a choice.
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    @property
    def votes(self):
        """Return the votes for this choice."""
        return self.vote_set.count()

    def user_voted(self):
        """Return all the users that have voted on this choice."""
        return (vote.user for vote in self.vote_set.all())

    def __str__(self):
        """Return choice text."""
        return self.choice_text


class Vote(models.Model):
    """A vote by a user for a choice in a poll."""

    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return choice and user string."""
        return f"{self.choice} by {self.user}"
