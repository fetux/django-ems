# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20170926_0315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectuserstory',
            name='assignee',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='user_stories'),
        ),
        migrations.AlterField(
            model_name='projectuserstory',
            name='eta_hours',
            field=models.DecimalField(default=0, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='projectuserstory',
            name='ref',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='projectuserstory',
            name='status',
            field=models.CharField(blank=True, null=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='projectuserstory',
            name='title',
            field=models.CharField(blank=True, null=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='projectuserstory',
            name='type',
            field=models.CharField(blank=True, null=True, max_length=255),
        ),
    ]
