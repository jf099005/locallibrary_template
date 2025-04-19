from .QuizViews import *
from .models import vocabulary_table, vocabulary
from django.contrib.auth.models import User  # 若你要指定 user
from django.forms.models import model_to_dict

add_new = True
def main(request, username = None):
    print(dict(request.session))
    # if True:
    #     voc_ids = [str(i) for i in (vocabulary.objects.values_list('id', flat=True))]

    #     # 2. 創建 vocabulary_table，假設你要給一個 user（也可以不指定 user）
    #     user = User.objects.first()  # 或其他你想指定的 user

    #     vocab_table = vocabulary_table(
    #         add_user=user,
    #         voc_list=voc_ids,
    #         name = 'test'
    #     )
    #     add_new = False
    #     vocab_table.save()
    #     print('save table')
    voc_tables = [table.name for table in vocabulary_table.objects.all()]

    return render(request, 'main.html', locals())

def table_detail_page(request, table_name):
    print('call table_detail_page with table name ',table_name)
    voc_table = vocabulary_table.objects.get(name=table_name)
    voc_idx = list(voc_table.voc_list)

    voc_list = [vocabulary.objects.get(id = idx) for idx in voc_idx]
    voc_list = [model_to_dict(voc) for voc in voc_list]
    print('voc list:', voc_list)
    question_type = 'endlish'
    answer_type = 'chinese'
    return render(request, 'vocabulary_table.html', {
        'name': table_name,
        'vocabulary_list': voc_list,
        'question_type': question_type,
        'answer_type': answer_type
          })