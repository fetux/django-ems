# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_auto_20170929_0027'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectuserstory',
            old_name='project_epic',
            new_name='epic',
        ),
        migrations.RemoveField(
            model_name='projectepic',
            name='assessment',
        ),
        migrations.AddField(
            model_name='projectepic',
            name='project',
            field=models.ForeignKey(related_name='epics', null=True, to='crm.Project'),
        ),
        migrations.AlterField(
            model_name='projectuserstory',
            name='assignee',
            field=models.ForeignKey(blank=True, related_name='user_stories', null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='projectuserstory',
            name='eta_hours',
            field=models.DecimalField(decimal_places=2, blank=True, default=0, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='projectuserstory',
            name='ref',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
