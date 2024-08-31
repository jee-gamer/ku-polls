from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from .models import Choice, Question

not_published_msg = "That poll is not published yet."
cannot_vote_msg = "That poll had ended."


class IndexView(generic.ListView):
    """
    This view displays a list of 5 poll last created.
    """
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions"""
        return Question.objects.filter(pub_date__lte=timezone.now()) \
            .order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    """
    This view displays question and choices.
    """
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):  # Set of response
        """Exclude any question that aren't published yet."""
        return Question.objects.all()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.object.is_published():
            messages.add_message(request, messages.INFO,
                                 not_published_msg)
            return HttpResponseRedirect(reverse("polls:index"))

        elif not self.object.can_vote():
            messages.add_message(request, messages.INFO,
                                 cannot_vote_msg)
            return HttpResponseRedirect(reverse("polls:index"))

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ResultView(generic.DetailView):
    """
    This view displays the results of the poll in table format.
    """
    model = Question
    template_name = "polls/results.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.object.is_published():
            messages.add_message(request, messages.INFO,
                                 not_published_msg)
            return HttpResponseRedirect(reverse("polls:index"))

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


def vote(request, question_id):
    """
    This function is called when a visitor vote on a poll.
    :return: HttpResponse
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:

        if not question.can_vote():
            messages.add_message(request, messages.INFO,
                                 cannot_vote_msg)
            return HttpResponseRedirect(reverse("polls:index"))

        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
            reverse("polls:results", args=(question.id,)))
