# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='description',
            field=models.TextField(default='this is a quiz'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='instructions',
            field=models.TextField(default='take the test'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='name',
            field=models.CharField(default='Final', max_length=30),
            preserve_default=False,
        ),
    ]
