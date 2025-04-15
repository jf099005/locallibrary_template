from django.shortcuts import render
from .models import vocabulary, QuizSession, User_Answering, Quiz
from django.http import JsonResponse
import random
import json
# Create your views here.
def index(request):
    question = 'haha'
    print('views is triggered')
    print(dict(request.session))
    # print(request)
    num_voc = vocabulary.objects.all().count()
    # num_press += 1
    ii = range(5)
    context = {'num_voc': num_voc}
    return render(request, 'test/index.html', locals())

def button_view(request):
    print('received')

            # 获取请求的body
    body = request.body
            # 假设是JSON格式的数据
    data = json.loads(body)
    print('data:', data)
    print('session:', request.session.values())
            # 返回收到的JSON数据作为响应
    return JsonResponse({'received': data})    # num_voc = vocabulary.objects.all().count()
    # # num_press += 1
    # ii = range(5)
    # context = {'num_voc': num_voc}
    # print("按鈕被點擊，執行操作！")
    # test_content = 'Haha'
    # if request.method == "GET":
    #     print("按鈕被點擊，執行操作2！")
    # return JsonResponse({'content': '成功呼叫後端函數！'})


def MCQ_view(request):
    num_voc = 4
    # num_choice = 4
    # vocs = vocabulary.objects.order_by('?').values()[:num_voc]
    # vocs = list(vocs)
    # voc_id = [voc['id'] for voc in vocs]
    # print(voc_id)
    # # quiz = QuizSession(voc_idx = vocs)
    # choices = random.sample(vocs, num_choice)
    # problem = random.sample(choices, 1)[0]
    # question = problem['question']
    # options = [i['answer'] for i in choices]
    # print('question:', question)
    # print('options:', options)
    # request.session['quiz_session'] = quiz
    # quiz.save()
    quiz = Quiz(4)
    question, options = quiz.get_problem_view()
#     request.session['quiz'] = quiz
    return render(request, 'test/quiz/MCQ.html', locals())


def MCQ_answering(request):
     body = request.body
     data = json.loads(body)
     reply = data['answer']
     request.session['quiz']
     
     return JsonResponse({'received': data})    # num_voc = vocabulary.objects.all().count()
