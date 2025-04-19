from django.shortcuts import render
from .models import vocabulary, QuizSession, User_Answering, Quiz
from django.http import JsonResponse
import random
import json
# Create your views here.

num_voc = 8
def MCQ_view(request, table_name = None):
    if table_name is None:
        quiz = Quiz(num_voc)
        request.session['quiz'] = quiz.state_dict()
    else:
        quiz = Quiz()
        quiz.load_state_dict(request.session['quiz'])

    question, options = quiz.get_problem_view()
    
    instruction = 'select a correct answer from following options'
    page_information = {
        'question' : question,
        'options' : options,
        'instruction' : instruction,
        'num_problems' : quiz.remain_vocs
    }
    return render(request, 'test/quiz/MCQ.html', page_information)


def MCQ_answering(request):
    print('answering')
    body = request.body
    data = json.loads(body)
    reply = data['answer']
    print('answering:', reply)

    quiz_model = Quiz()
    quiz_model.load_state_dict(request.session['quiz'])

    print(quiz_model.answering(reply))
    print(quiz_model.vocs[ quiz_model.problem_idx ])
    
    solution = ''
    if quiz_model.answering(reply):
        quiz_model.answer_state = True
        solution = 'correct!'
    else:
        quiz_model.answer_state = False
        solution = 'wrong...'
        
    instruction = 'press any key to continue'
    
    response = {'solution': solution,
                'instruction': instruction}
    print('new problem:', quiz_model.get_problem_view())
    request.session['quiz'] = quiz_model.state_dict()
    return JsonResponse(response)    # num_voc = vocabulary.objects.all().count()

def MCQ_update_vocabulary(request):
    print('calling update_voc')
    
    quiz_model = Quiz()
    quiz_model.load_state_dict( request.session['quiz'] )
    quiz_model.update_problem()

    question, options = quiz_model.get_problem_view()
    print('update problem:', question, options, quiz_model.get_problem_view())

    instruction = 'select a correct answer from following options'
    solution = ''
    data = {
        'question': question,
        'options': options,
        'num_problems': quiz_model.remain_vocs,
        'instruction': instruction,
        'solution': solution
    }

    request.session['quiz'] = quiz_model.state_dict()
    return JsonResponse(data)    # num_voc = vocabulary.objects.all().count()
