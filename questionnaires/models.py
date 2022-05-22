import datetime

from django.db import models
from django.utils import timezone
# from django_utils import choices


# Create your models here.


class Questionnaire(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.title

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Question(models.Model):
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text


class QuestionChoice(models.Model):
    questionnaire = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE, null=True, blank=True
    )
    question_type = models.CharField(default="Choice Answer", max_length=50)
    question_text = models.CharField(max_length=200, blank=True)
    position = models.IntegerField("position", default=0)


    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(QuestionChoice, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class ShortAnswer(models.Model):
    questionnaire = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE, null=True, blank=True
    )
    question_type = models.CharField(default="Short Answer", max_length=50)
    question_text = models.CharField(max_length=200, blank=True)
    short_answer = models.TextField(max_length=300, blank=True)
    position = models.IntegerField("position", default=0)




class LongAnswer(models.Model):
    questionnaire = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE, null=True, blank=True
    )
    question_type = models.CharField(default="Long Answer", max_length=50)
    question_text = models.CharField(max_length=200, blank=True)
    long_answer = models.TextField(max_length=1000, blank=True)
    position = models.IntegerField("position", default=0)


class FileAnswer(models.Model):
    questionnaire = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE, null=True, blank=True
    )
    question_type = models.CharField(default="File Answer", max_length=50)
    question_text = models.CharField(max_length=200, blank=True)
    file_answer = models.FileField(upload_to='documents/', blank=True)
    position = models.IntegerField("position", default=0)


"""
class Questionnaire(models.Model):
    TYPES = (
        ('short_answer', 'Short Answer'),
        ('long_answer', 'Long Answer'),
        ('choice_answer', 'Choice Answer'),
        ('file_answer', 'File Answer'),
    )
    name = models.CharField(max_length=200)
    question_type = models.CharField(choices=TYPES, max_length=100, default='Short Answer')
    questions = models.ForeignKey(
        Questions, on_delete=models.CASCADE, null=True, blank=True
    )
    position = models.IntegerField("position")

    def add_question(self, question_type):
        if question_type == 'Short Answer':
            short_answer = models.ForeignKey(
                ShortAnswer, on_delete=models.CASCADE, null=True, blank=True
            )


class Question:
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey('ChoiceQuestion')
    choice_text = models.CharField(max_length=200)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class ChoiceQuestion(models.Model):
    question = models.CharField(max_length=200)
    choices = models.ManyToManyField(
        Choice,
        related_name='question_choices', blank=True)

    def check_answer(self, choice):
        return self.choice_set.filter(id=choice.id, is_answer=True).exists()

    def get_answers(self):
        return self.choice_set.filter(is_answer=True)
"""
