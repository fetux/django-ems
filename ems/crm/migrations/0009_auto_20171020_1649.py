# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_auto_20170929_0059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectteam',
            name='project',
        ),
        migrations.AddField(
            model_name='projectteam',
            name='project',
            field=models.ForeignKey(to='crm.Project', blank=True, related_name='team', default=None),
            preserve_default=False,
        ),
    ]
