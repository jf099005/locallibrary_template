from django.contrib import admin
from .models import vocabulary, QuizSession, vocabulary_table, User_Answering
# Register your models here.
admin.site.register(vocabulary)
admin.site.register(QuizSession)
admin.site.register(vocabulary_table)
admin.site.register(User_Answering)