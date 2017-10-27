# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_auto_20170929_0040'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectepic',
            name='assessment',
            field=models.ForeignKey(null=True, to='crm.ProjectAssessment', related_name='epics'),
        ),
    ]
