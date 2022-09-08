import logging

from django.db.models import F
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Question, Choice

logger = logging.getLogger(__name__)


def index(request):
    questions = Question.objects.order_by('pub_date')
    context = {
        'questions': questions
    }
    return render(request, 'index.html', context)


def details(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        context = {
            'question': question
        }
    except Question.DoesNotExist:
        logger.info(Question.DoesNotExist)
        raise Http404("Question does not exist")
    return render(request, 'detail.html', context)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'result.html', {'question': question})


def vote(request, question_id):
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


