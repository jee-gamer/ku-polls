import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question, Choice


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        :return:
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for question whose
        pub_date is older than 1 day.
        :return:
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertFalse(old_question.was_published_recently())

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59,
                                                   seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no question exist, an appropriate message is displayed.
        :return:
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the index page.
        :return:
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future should not display on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )


class DetailViewTest(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future Question.",
                                          days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5
                                        )
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class IsPublishedTest(TestCase):
    def test_future_pub_date(self):
        """
        If the publish date is in the future there should be no question found
        in UI.
        """
        future_question = create_question(question_text="Future", days=5)
        status = future_question.is_published()
        self.assertFalse(status)

    def test_default_pub_date(self):
        """
        If the publish date is default (now) we should be able to see question.
        """
        default_question = create_question(question_text="default_question",
                                           days=0)
        status = default_question.is_published()
        self.assertTrue(status)

    def test_past_pub_date(self):
        """
        If the publish date is in the past we should be able to see question.
        """
        past_question = create_question(question_text="past_question",
                                           days=-5)
        status = past_question.is_published()
        self.assertTrue(status)


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
        Choice.objects.create(question=question, choice_text=choice_text,
                              votes=0)
    return question


class CanVoteTest(TestCase):
    def test_cannot_vote_after_end_date(self):
        """
        Cannot vote if the end date is in the past
        """
        sample_question = create_question_with_choices_and_time(
            question_text="sample_question",
            choice_texts=["c1", "c2"],
            pub_day=-2,
            end_day=-1
        )
        url = reverse("polls:detail", args=(sample_question.id,))
        response = self.client.get(url)

        choice = sample_question.choice_set.first()
        vote_url = reverse("polls:vote", args=(sample_question.id,))
        response = self.client.post(vote_url, {'choice': choice.id})
        # You should not be able to vote.. what response? idk yet

    def test_cannot_vote_before_pub_date(self):
        """
        Cannot vote if the pub date is in the future
        """
        sample_question = create_question_with_choices_and_time(
            question_text="sample_question",
            choice_texts=["c1", "c2"],
            pub_day=1,
            end_day=2
        )
        url = reverse("polls:detail", args=(sample_question.id,))
        response = self.client.get(url)

        choice = sample_question.choice_set.first()
        vote_url = reverse("polls:vote", args=(sample_question.id,))
        response = self.client.post(vote_url, {'choice': choice.id})
        # You should not be able to vote.. what response? idk yet

    def test_can_vote_after_publish(self):
        """
        Can vote if the time now is between pub date and end date
        """
        sample_question = create_question_with_choices_and_time(
            question_text="sample_question",
            choice_texts=["c1", "c2"],
            pub_day=0,
            end_day=1
        )
        url = reverse("polls:detail", args=(sample_question.id,))
        response = self.client.get(url)

        choice = sample_question.choice_set.first()
        vote_url = reverse("polls:vote", args=(sample_question.id,))
        response = self.client.post(vote_url, {'choice': choice.id})

        self.assertEqual(Choice.objects.get(id=choice.id).votes, 1)
        self.assertRedirects(response, reverse("polls:results",
                                               args=(sample_question.id,)))