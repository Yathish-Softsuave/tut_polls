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
