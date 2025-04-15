from django.db import models
from django.contrib.auth.models import User
import uuid # Required for unique book instances
import random
# Create your models here.
class vocabulary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')

    question = models.CharField(max_length=100, default = 'test_voc')
    answer = models.CharField(max_length=100, default = 'test_sol')

    def __str__(self):
        return self.question + ',' + self.answer
    def reverse(self):
        self.question, self.answer = self.answer, self.question

class QuizSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    name = models.CharField(max_length=100, default='default_session')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    voc_idx = models.JSONField(default = list)

class Quiz:
    num_choice = 4

    def __init__(self, num_voc):
        vocs = vocabulary.objects.order_by('?').values()[:num_voc]
        vocs = list(vocs)
        voc_id = [str(voc['id']) for voc in vocs]
        self.vocs = vocs
        self.quiz_session = QuizSession(voc_idx = voc_id)
        # request.session['quiz_session'] = quiz
        # self.quiz_session.save()
        self.problem = None
        self.choices = None
        self.load_new_problem()
        # return self.quiz_session, vocs
    # return render(request, 'test/quiz/MCQ.html', locals())

    def load_record(self, vocabulary_ids, record):
        self.vocs = vocabulary.objects.order_by('?').filter(id__in=vocabulary_ids)
        self.record = record


    def load_new_problem(self):
        self.choices = random.sample(self.vocs, self.num_choice)
        self.problem = random.sample(self.choices, 1)[0]


    def get_problem_view(self):
        self.load_new_problem()
        question = self.problem['question']
        options = [i['answer'] for i in self.choices]
        return question, options

    def answering(self, answer):
        if answer != self.problem['answer']:
            return False
        else:
            self.vocs.remove(self.problem)
            return True


class User_Answering(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    question = models.ForeignKey( vocabulary, on_delete=models.CASCADE )
    Q2A = 'Q2A'
    A2Q = 'A2Q'
    genre_choice = [
        (Q2A, 'Question_to_Answer'),
        (A2Q, 'Answer_to_Question')
    ]

    genre_choice = models.CharField(
        max_length= 20,
        choices=genre_choice,
        default=Q2A
    )
