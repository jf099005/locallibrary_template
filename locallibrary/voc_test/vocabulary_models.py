from django.db import models
from django.contrib.auth.models import User
import uuid # Required for unique book instances
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

class vocabulary_table(models.Model):
    add_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True )
    voc_id_list = models.JSONField(default = list)
    name = models.CharField(max_length=100, default='default_session')

    def __str__(self):
        return f'{self.add_user} , {self.name}'

    @classmethod
    def from_list(cls, voc_list, table_name, user):
        if (user is not  None) and not isinstance(user, User):
            raise TypeError("invalid user")
        
        voc_idx_list = []
        for (q,a) in voc_list:
            voc = vocabulary(question = q, answer = a)
            voc.save()
            voc_idx_list.append(str(voc.id))

        return cls(voc_id_list = voc_idx_list, name = table_name , add_user = user)
    

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