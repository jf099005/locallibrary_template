# Generated by Django 5.2 on 2025-04-18 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voc_test', '0006_vocabulary_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='vocabulary_table',
            name='name',
            field=models.CharField(default='default_session', max_length=100),
        ),
    ]
