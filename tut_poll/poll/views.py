import logging

from django.db.models import F
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Question, Choice

logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    """
        view to show the list of all the questions present for the poll.
    """

    template_name = 'index.html'
    context_object_name = 'questions'

    def get_queryset(self):
        """
            queryset for IndexView
        :return:
            questions which are published in the past
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class DetailView(generic.DetailView):
    """
        view to show the details and options for the questions to vote
    """
    model = Question
    template_name = 'detail.html'


class ResultsView(generic.DetailView):
    """
        view to show the results for the questions.
    """
    model = Question
    template_name = 'result.html'


def vote(request, question_id):
    """
    view to vote on the question
    :param request: request body
    :param question_id: pk of the question
    :return: redirects to results
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist) :
        return render(
            request,
            'detail.html',
            {
                'question': question,
                'error_message': 'you have not selected any choice',
            }
        )
    else:
        selected_choice.vote = F('vote')+1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



