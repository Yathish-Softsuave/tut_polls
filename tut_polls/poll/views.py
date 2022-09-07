from django.http import HttpResponse
from django.template import loader

from .models import Question


def index(request):
    questions = Question.objects.order_by('pub_date')
    template = loader.get_template('index.html')
    context = {
        'questions':questions
    }
    output = ','.join([question.question_text for question in questions])
    return HttpResponse(template.render(context, request))
