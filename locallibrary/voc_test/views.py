from .QuizViews import *
from .models import vocabulary_table, vocabulary
from django.contrib.auth.models import User  # 若你要指定 user
from django.forms.models import model_to_dict

add_new = True
def main(request, username = None):
    print(dict(request.session))
    print('calling main')
    current_userID = request.session.get('_auth_user_id')
    voc_tables = []
    if current_userID is not None:
        current_user = User.objects.get(id = request.session['_auth_user_id'])
        voc_tables = [table.name for table in vocabulary_table.objects.filter(add_user = current_user)]

    return render(request, 'main.html', locals())

def table_detail_page(request, table_name):
    print('call table_detail_page with table name ',table_name)
    voc_table = vocabulary_table.objects.get(name=table_name)
    voc_idx = list(voc_table.voc_id_list)

    # voc_list = [vocabulary.objects.get(id = idx) for idx in voc_idx]
    voc_list = vocabulary.objects.filter(id__in = voc_idx)
    voc_list = [model_to_dict(voc) for voc in voc_list]
    print('voc list:', voc_list)
    question_type = 'endlish'
    answer_type = 'chinese'
    # quiz = Quiz.load_from_index_list(voc_list)

    request.session['quiz'] = Quiz.load_from_index_list(voc_idx).state_dict()

    return render(request, 'vocabulary_table.html', {
        'name': table_name,
        'vocabulary_list': voc_list,
        'question_type': question_type,
        'answer_type': answer_type
          })

# ------------
import csv
from .forms import CSVUploadForm

def upload_csv(request):
    print('call upload_csv')
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            file = form.cleaned_data['file']
            decoded_file = file.read().decode('utf-8').splitlines()

            reader = list(csv.reader(decoded_file))
            submit_user = User.objects.get( id = request.session['_auth_user_id'] )

            voc_table = vocabulary_table.from_list(reader, name, submit_user)
            voc_table.save()
            print('user:', submit_user.username)
            print('name:', name)
            for (a,b) in reader:
                # Process each row
                print(a,'|',b)  # or save to DB
            return render(request, 'upload_success.html')
    else:
        form = CSVUploadForm()
    return render(request, 'upload.html', {'form': form})
