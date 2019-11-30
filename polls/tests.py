from django.test import TestCase
from django.utils import timezone
from django.urls import reverse


import datetime


from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently returns False for questions whose
        pub_date is in future.
        """
        time = timezone.now() + datetime.timedelta(days=1)
        future_q = Question(pub_date=time)
        self.assertIs(future_q.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_q = Question(pub_date=time)
        self.assertIs(old_q.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23,
                                                   minutes=59,
                                                   seconds=59)
        rec_q = Question(pub_date=time)
        self.assertIs(rec_q.was_published_recently(), True)


def create_question(text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_questions'], [])

    def test_past_question(self):
        create_question('Past question', days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_questions'],
                                 ['<Question: Past question>'])

    def test_future_question(self):
        create_question('Future question', days=5)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_questions'], [])

    def test_past_and_future(self):
        create_question('Future question', days=5)
        create_question('Past question', days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_questions'],
                                 ['<Question: Past question>'])

    def test_several_past(self):
        create_question('Another past question', days=-1)
        create_question('Past question', days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_questions'],
                                 ['<Question: Another past question>',
                                  '<Question: Past question>',])
