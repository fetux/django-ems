# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0003_auto_20151119_0906'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectAssessment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255)),
                ('risk_factor', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
            ],
            options={
                'db_table': 'timepiece_projectassessment',
            },
        ),
        migrations.CreateModel(
            name='ProjectEpic',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('assessment', models.ForeignKey(null=True, related_name='epics', to='crm.ProjectAssessment')),
            ],
            options={
                'db_table': 'timepiece_projectepic',
            },
        ),
        migrations.CreateModel(
            name='ProjectTeam',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('rump_up_factor', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('co_factor', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
            ],
            options={
                'db_table': 'timepiece_projectteam',
            },
        ),
        migrations.CreateModel(
            name='ProjectUserStory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('ref', models.IntegerField()),
                ('type', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('eta_hours', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('status', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'timepiece_projectuserstory',
            },
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
            ],
            options={
                'db_table': 'timepiece_projectteammember',
            },
        ),
        migrations.RenameModel(
            old_name='RelationshipType',
            new_name='TeamMemberRole',
        ),
        migrations.AlterUniqueTogether(
            name='projectrelationship',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='projectrelationship',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projectrelationship',
            name='types',
        ),
        migrations.RemoveField(
            model_name='projectrelationship',
            name='user',
        ),
        migrations.RemoveField(
            model_name='project',
            name='users',
        ),
        migrations.AlterModelTable(
            name='teammemberrole',
            table='timepiece_teammember',
        ),
        migrations.CreateModel(
            name='ProjectTask',
            fields=[
                ('projectuserstory_ptr', models.OneToOneField(parent_link=True, serialize=False, to='crm.ProjectUserStory', auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'timepiece_projecttask',
            },
            bases=('crm.projectuserstory',),
        ),
        migrations.DeleteModel(
            name='ProjectRelationship',
        ),
        migrations.AddField(
            model_name='teammember',
            name='role',
            field=models.ForeignKey(to='crm.TeamMemberRole', related_name='team_members'),
        ),
        migrations.AddField(
            model_name='teammember',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='teams'),
        ),
        migrations.AddField(
            model_name='projectuserstory',
            name='assignee',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user_stories'),
        ),
        migrations.AddField(
            model_name='projectuserstory',
            name='project_epic',
            field=models.ForeignKey(null=True, related_name='user_stories', to='crm.ProjectEpic'),
        ),
        migrations.AddField(
            model_name='projectteam',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='teams', to='crm.TeamMember'),
        ),
        migrations.AddField(
            model_name='projectteam',
            name='project',
            field=models.ManyToManyField(blank=True, related_name='teams', to='crm.Project'),
        ),
        migrations.AddField(
            model_name='projectassessment',
            name='project',
            field=models.ForeignKey(to='crm.Project', related_name='assessments'),
        ),
    ]
