# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_auto_20160429_0531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz_attempt',
            name='score',
            field=models.FloatField(null=True),
        ),
    ]
