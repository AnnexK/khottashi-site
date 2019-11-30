from django.db import models
from django.utils import timezone

import datetime
# Create your models here.


class Question(models.Model):
    question_text = models.CharField('Question', max_length=256)
    pub_date = models.DateTimeField('Date published')

    def __str__(self):
        return self.question_text

    def multiple_answers(self):
        return self.choice_set.count() > 1

    def was_published_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=1)

    @property
    def short_text(self):
        chars = 16
        ellipsis_len = 3

        if len(self.question_text) > chars-ellipsis_len:
            return self.question_text[:chars-ellipsis_len] + '...'
        else:
            return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField('Choice', max_length=256)
    votes = models.IntegerField('Votes amount', default=0)

    def __str__(self):
        return self.choice_text
