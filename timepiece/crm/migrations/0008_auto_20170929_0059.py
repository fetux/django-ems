# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_projectepic_assessment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectepic',
            name='assessment',
            field=models.ForeignKey(to='crm.ProjectAssessment', related_name='epics', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='projectepic',
            name='project',
            field=models.ForeignKey(to='crm.Project', related_name='epics', blank=True, null=True),
        ),
    ]
