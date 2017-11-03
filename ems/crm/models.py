from collections import OrderedDict

from django.apps import apps
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from ems.utils import get_active_entry


# Add a utility method to the User class that will tell whether or not a
# particular user has any unclosed entries
_clocked_in = lambda user: bool(get_active_entry(user))
User.add_to_class('clocked_in', property(_clocked_in))


# Utility method to get user's name, falling back to username.
_get_name_or_username = lambda user: user.get_full_name() or user.username
User.add_to_class('get_name_or_username', _get_name_or_username)


_get_absolute_url = lambda user: reverse('view_user', args=(user.pk,))
User.add_to_class('get_absolute_url', _get_absolute_url)


@python_2_unicode_compatible
class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, related_name='profile')
    hours_per_week = models.DecimalField(
        max_digits=8, decimal_places=2, default=40)

    class Meta:
        db_table = 'ems_userprofile'  # Using legacy table name.

    def __str__(self):
        return self.user


class TypeAttributeManager(models.Manager):
    """Object manager for type attributes."""

    def get_queryset(self):
        qs = super(TypeAttributeManager, self).get_queryset()
        return qs.filter(type=Attribute.PROJECT_TYPE)


class StatusAttributeManager(models.Manager):
    """Object manager for status attributes."""

    def get_queryset(self):
        qs = super(StatusAttributeManager, self).get_queryset()
        return qs.filter(type=Attribute.PROJECT_STATUS)


@python_2_unicode_compatible
class Attribute(models.Model):
    PROJECT_TYPE = 'project-type'
    PROJECT_STATUS = 'project-status'
    ATTRIBUTE_TYPES = OrderedDict((
        (PROJECT_TYPE, 'Project Type'),
        (PROJECT_STATUS, 'Project Status'),
    ))
    SORT_ORDER_CHOICES = [(x, x) for x in range(-20, 21)]

    type = models.CharField(max_length=32, choices=ATTRIBUTE_TYPES.items())
    label = models.CharField(max_length=255)
    sort_order = models.SmallIntegerField(
        null=True, blank=True, choices=SORT_ORDER_CHOICES)
    enable_timetracking = models.BooleanField(
        default=False,
        help_text=('Enable time tracking functionality for projects '
                   'with this type or status.'))
    billable = models.BooleanField(default=False)

    objects = models.Manager()
    types = TypeAttributeManager()
    statuses = StatusAttributeManager()

    class Meta:
        db_table = 'ems_attribute'  # Using legacy table name.
        unique_together = ('type', 'label')
        ordering = ('sort_order',)

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class Business(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    external_id = models.CharField(max_length=32, blank=True)

    class Meta:
        db_table = 'ems_business'  # Using legacy table name.
        ordering = ('name',)
        verbose_name_plural = 'Businesses'
        permissions = (
            ('view_business', 'Can view businesses'),
        )

    def __str__(self):
        return self.get_display_name()

    def get_absolute_url(self):
        return reverse('view_business', args=(self.pk,))

    def get_display_name(self):
        return self.short_name or self.name


class TrackableProjectManager(models.Manager):

    def get_queryset(self):
        return super(TrackableProjectManager, self).get_queryset().filter(
            status__enable_timetracking=True,
            type__enable_timetracking=True,
        )


@python_2_unicode_compatible
class Project(models.Model):
    name = models.CharField(max_length=255)
    tracker_url = models.CharField(
        max_length=255, blank=True, null=False, default="")
    business = models.ForeignKey(
        Business, related_name='new_business_projects')
    point_person = models.ForeignKey(User, limit_choices_to={'is_staff': True})
    activity_group = models.ForeignKey(
        'entries.ActivityGroup', related_name='activity_group', null=True,
        blank=True, verbose_name='restrict activities to')
    type = models.ForeignKey(
        Attribute, limit_choices_to={'type': 'project-type'},
        related_name='projects_with_type')
    status = models.ForeignKey(
        Attribute, limit_choices_to={'type': 'project-status'},
        related_name='projects_with_status')
    description = models.TextField()

    objects = models.Manager()
    trackable = TrackableProjectManager()

    class Meta:
        db_table = 'ems_project'  # Using legacy table name.
        ordering = ('name', 'status', 'type',)
        permissions = (
            ('view_project', 'Can view project'),
            ('email_project_report', 'Can email project report'),
            ('view_project_time_sheet', 'Can view project time sheet'),
            ('export_project_time_sheet', 'Can export project time sheet'),
            ('generate_project_invoice', 'Can generate project invoice'),
        )

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.business.get_display_name())

    @property
    def billable(self):
        return self.type.billable

    def get_absolute_url(self):
        return reverse('view_project', args=(self.pk,))

    def get_active_contracts(self):
        """Returns all associated contracts which are not marked complete."""
        ProjectContract = apps.get_model('contracts', 'ProjectContract')
        return self.contracts.exclude(status=ProjectContract.STATUS_COMPLETE)


@python_2_unicode_compatible
class TeamMemberRole(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)

    class Meta:
        db_table = 'ems_teammember'  # Using legacy table name.

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class TeamMember(models.Model):
    role = models.ForeignKey(TeamMemberRole, related_name='team_members')
    user = models.ForeignKey(User, related_name='teams')

    class Meta:
        db_table = 'ems_projectteammember'  # Using legacy table name.

    def __str__(self):
        return "{user} as {role}".format(
            user=self.user.get_name_or_username(),
            role=self.role.name,
        )


@python_2_unicode_compatible
class ProjectTeam(models.Model):
    project = models.ForeignKey(Project, blank=True, related_name='team')
    active = models.BooleanField(default=False)
    members = models.ManyToManyField(
        TeamMember, blank=True, related_name='members')
    rump_up_factor = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    co_factor = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        db_table = 'ems_projectteam'  # Using legacy table name.

    def __str__(self):
        return "{project}'".format(
            project=self.project.name,
        )


@python_2_unicode_compatible
class ProjectAssessment(models.Model):
    slug = models.SlugField(max_length=255)
    project = models.ForeignKey(Project, related_name='assessments')
    risk_factor = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        db_table = 'ems_projectassessment'  # Using legacy table name.

    def __str__(self):
        return "{slug}' from {project}".format(
            slug=self.slug,
            project=self.project.name,
        )


@python_2_unicode_compatible
class ProjectEpic(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, related_name='epics', blank=True, null=True)
    assessment = models.ForeignKey(ProjectAssessment, related_name='epics', blank=True, null=True)

    class Meta:
        db_table = 'ems_projectepic'  # Using legacy table name.

    def __str__(self):
        return "{project} - {epic}".format(
            project=self.project.name,
            epic=self.name,
        )


@python_2_unicode_compatible
class ProjectUserStory(models.Model):
    epic = models.ForeignKey(ProjectEpic, related_name='user_stories', null=True)
    ref = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    assignee = models.ForeignKey(User, related_name='user_stories', null=True, blank=True)
    eta_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'ems_projectuserstory'  # Using legacy table name.

    def __str__(self):
        return "{project} - {user_story}".format(
            project=self.epic.project.name,
            user_story=self.title
        )


@python_2_unicode_compatible
class ProjectTask(ProjectUserStory):

    class Meta:
        db_table = 'ems_projecttask'  # Using legacy table name.

    def __str__(self):
        return "{project} - {user_story} - {task}".format(
            project=self.user_story.epic.project.name,
            user_story=self.user_story.title,
            task=self.title
        )
