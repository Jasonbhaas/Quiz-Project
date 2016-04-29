# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_auto_20160422_0244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question_attempt',
            name='end',
        ),
        migrations.AlterField(
            model_name='quiz_attempt',
            name='end',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='quiz_attempt',
            name='start',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
