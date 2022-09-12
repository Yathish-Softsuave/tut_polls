import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from poll.models import Question


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(
        days=days
    )
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_questions(self):
        """
            was_published_recently() returns False for questions whose pub_date
            is in the future.
        """
        future_question = create_question('future question', 10)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_questions(self):
        """
            was_published_recently() returns False for questions whose pub_date
            is older than 1 day.
        """
        old_question = create_question('past question', 2)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
           was_published_recently() returns True for questions whose pub_date
           is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTest(TestCase):

    def test_no_questions(self):
        """
            If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['questions'], [])

    def test_past_questions(self):
        """
            Questions with a pub_date in the past are displayed on the
            index page.
        """
        question = create_question('past question', days=-30)
        response = self.client.get(reverse('polls:index'))
        print(response.context['questions'])
        self.assertQuerysetEqual(response.context['questions'], [question])

    def test_future_questions(self):
        """
           Questions with a pub_date in the future aren't displayed on
           the index page.
        """
        create_question('future question', 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['questions'], [])

    def test_past_and_future_questions(self):
        """
           Even if both past and future questions exist, only past questions
           are displayed.
        """
        past_question = create_question('past', -1)
        create_question('future', 1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['questions'], [past_question])

    def test_two_past_questions(self):
        """
            The questions index page may display multiple questions.
        """
        question_one = create_question('first', -2)
        question_two = create_question('second', -2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['questions'],
            [question_two, question_one]
        )
