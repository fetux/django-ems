# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_auto_20170929_0059'),
        ('entries', '0003_auto_20151217_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='task',
            field=models.ForeignKey(to='crm.ProjectTask', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='user_story',
            field=models.ForeignKey(to='crm.ProjectUserStory', related_name='project_hours', blank=True, null=True),
        ),
    ]
