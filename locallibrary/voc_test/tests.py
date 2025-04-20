from django.test import TestCase
from .models import vocabulary_table
# Create your tests here.
import csv
with open('F:/OOAD/project/locallibrary/locallibrary/voc_test/test_voc.csv','r' , encoding='utf-8') as f:
    data = csv.reader(f)
    # for (i,j) in data:
    #     print(i,'|',j)
    data = list(data)

voc_table = vocabulary_table.from_list(data, 'test')

print("HAHA")