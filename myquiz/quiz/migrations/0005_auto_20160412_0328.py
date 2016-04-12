# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_remove_question_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='point_value',
            field=models.IntegerField(default=3, choices=[(1, b'Wrong'), (2, b'Partially Correct'), (3, b'Correct')]),
        ),
    ]
