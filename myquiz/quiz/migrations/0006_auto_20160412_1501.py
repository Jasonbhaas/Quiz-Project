# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20160412_0328'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz_attempt',
            name='submitted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='answer',
            name='point_value',
            field=models.IntegerField(default=1, choices=[(1, b'Wrong'), (2, b'Partially Correct'), (3, b'Correct')]),
        ),
        migrations.AlterField(
            model_name='quiz_attempt',
            name='start',
            field=models.DateField(auto_now=True),
        ),
    ]
