# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_auto_20160404_2113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='order',
        ),
    ]
