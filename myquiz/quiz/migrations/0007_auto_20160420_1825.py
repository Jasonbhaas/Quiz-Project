# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_auto_20160412_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question_attempt',
            name='end',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='question_attempt',
            name='start',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='quiz_attempt',
            name='end',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='quiz_attempt',
            name='score',
            field=models.IntegerField(null=True),
        ),
    ]
