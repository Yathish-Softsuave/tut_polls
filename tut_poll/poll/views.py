import logging
from django.http import HttpResponse, Http404
from django.shortcuts import render

from .models import Question

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
    return HttpResponse(f'result for question {question_id}')


def vote(request, question_id):
    return HttpResponse(f'you voted on question {question_id}')
