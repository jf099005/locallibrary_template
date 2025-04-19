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
    def set_content(self, q, a):
        self.question = q
        self.answer = a

class QuizSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    name = models.CharField(max_length=100, default='default_session')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    voc_idx = models.JSONField(default = list)

class vocabulary_table(models.Model):
    add_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True )
    voc_list = models.JSONField(default = list)
    name = models.CharField(max_length=100, default='default_session')


class Quiz:
    num_choice = 4

    def __init__(self, num_voc = None, voc_idx_list = None):
        if num_voc is None:
            return
        
        vocs = vocabulary.objects.order_by('?').values()[:num_voc]
        vocs = list(vocs)
        self.vocs = { str(voc['id']):
                        {
                            'question': str(voc['question']),
                            'answer': str(voc['answer']),
                        } 
            for voc in vocs
        }
        # self.quiz_session = QuizSession(voc_idx = self.vocs.keys())
        # request.session['quiz_session'] = quiz
        # self.quiz_session.save()
        self.problem_idx = None
        self.choices_idx = None
        self.answer_state = None
        self.load_new_problem()
        # return self.quiz_session, vocs
    # return render(request, 'test/quiz/MCQ.html', locals())

    def load_state_dict(self, state_dict):
        self.answer_state = state_dict['answer_state']
        self.vocs = state_dict['vocs']
        self.problem_idx = state_dict['problem_idx']
        self.choices_idx = state_dict['choices_idx']

    def load_new_problem(self):
        print('calling load_new_problem')
        self.choices_idx = random.sample(list(self.vocs.keys()), self.num_choice)
        self.problem_idx = random.sample(self.choices_idx, 1)[0]

    def get_problem_view(self):
        # self.load_new_problem()
        question = self.vocs[ self.problem_idx ]['question']
        options = [  self.vocs[i]['answer'] for i in self.choices_idx]
        return question, options

    def answering(self, answer):
        if(not self.problem_idx in self.vocs.keys()):
            print("ERR")
            print(self.problem_idx)
            print(self.vocs.keys())
            return
        
        if answer != self.vocs[self.problem_idx]['answer']:
            return False
        else:
            # self.vocs.remove(self.problem)
            print('set to true')
            self.answer_state = True
            return True
    
    @property
    def remain_vocs(self):
        return len(self.vocs)

    # when user answering correct, this function remove problem from problemset and load a new problem
    def update_problem(self):
        print(self.answer_state)
        if self.answer_state is True:
            print('delete problem')
            self.vocs.pop(self.problem_idx, None)

        self.answer_state = None
        if len(self.vocs) <= 1:
            return False
        else:
            self.load_new_problem()
            return True

    def state_dict(self):
        # question_dict = {  str(k):str(self.vocs['question'][k]) for k in self.vocs['question'].keys()}
        # answer_dict = {  str(k):str(self.vocs['answer'][k]) for k in self.vocs['answer'].keys()}
        return {
            'answer_state': self.answer_state,
            'vocs':self.vocs,
            'problem_idx': self.problem_idx,
            'choices_idx': self.choices_idx
            }

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
