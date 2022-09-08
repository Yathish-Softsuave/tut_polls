from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import Question


def index(request):
    questions = Question.objects.order_by('pub_date')
    context = {
        'questions': questions
    }
    return render(request, 'index.html', context)


def details(request, question_id):
    return HttpResponse(f'you are in question {question_id}')


def results(request, question_id):
    return HttpResponse(f'result for question {question_id}')


def vote(request, question_id):
    return HttpResponse(f'you voted on question {question_id}')
