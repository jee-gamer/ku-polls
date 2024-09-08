from . import *

from django.urls import reverse


class CanVoteTest(TestCase):

    def test_cannot_vote_after_end_date(self):
        """
        Cannot vote if the end date is in the past
        """
        login(self)
        sample_question = create_question_with_choices_and_time(
            question_text="sample_question",
            choice_texts=["c1", "c2"],
            pub_day=-2,
            end_day=-1
        )
        url = reverse("polls:detail", args=(sample_question.id,))
        response = self.client.get(url)

        choice = sample_question.choice_set.first()
        old_vote = Choice.objects.get(id=choice.id).votes

        vote_url = reverse("polls:vote", args=(sample_question.id,))
        response = self.client.post(vote_url, {'choice': choice.id})

        # Vote number should be the same after voting
        self.assertEqual(Choice.objects.get(id=choice.id).votes, old_vote)

    def test_cannot_vote_before_pub_date(self):
        """
        Cannot vote if the pub date is in the future
        """
        login(self)
        sample_question = create_question_with_choices_and_time(
            question_text="sample_question",
            choice_texts=["c1", "c2"],
            pub_day=1,
            end_day=2
        )
        url = reverse("polls:detail", args=(sample_question.id,))
        response = self.client.get(url)

        choice = sample_question.choice_set.first()
        old_vote = Choice.objects.get(id=choice.id).votes

        vote_url = reverse("polls:vote", args=(sample_question.id,))
        response = self.client.post(vote_url, {'choice': choice.id})

        # Vote number should be the same after voting
        self.assertEqual(Choice.objects.get(id=choice.id).votes, old_vote)

    def test_can_vote_after_publish(self):
        """
        Can vote if the time now is between pub date and end date
        """
        login(self)
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

    def test_can_vote_after_voted(self):
        """
        can't vote the same choice again after already voted
        (It will not change anything)
        """
        login(self)
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

        # Vote again
        vote_url = reverse("polls:vote", args=(sample_question.id,))
        response = self.client.post(vote_url, {'choice': choice.id})

        # Votes should still be 1
        self.assertEqual(Choice.objects.get(id=choice.id).votes, 1)

    def test_can_change_vote(self):
        """
        can change vote after voted on a poll
        """
        login(self)
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

        # Change the choice
        new_choice = sample_question.choice_set.all()[1]
        vote_url = reverse("polls:vote", args=(sample_question.id,))
        response = self.client.post(vote_url, {'choice': new_choice.id})

        # Old choice vote should be 0 and new one should be 1
        self.assertEqual(Choice.objects.get(id=choice.id).votes, 0)
        self.assertEqual(Choice.objects.get(id=new_choice.id).votes, 1)