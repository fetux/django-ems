from django.contrib import admin

from ems.crm.models import (
    Attribute, Business, Project, TeamMemberRole, TeamMember,
    ProjectTeam, ProjectAssessment, ProjectUserStory, ProjectEpic,
    ProjectTask, UserProfile)


class AttributeAdmin(admin.ModelAdmin):
    search_fields = ('label', 'type')
    list_display = ('label', 'type', 'enable_timetracking', 'billable')
    list_filter = ('type', 'enable_timetracking', 'billable')
    ordering = ('type', 'sort_order')  # Django honors only first field.


class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name']
    search_fields = ['name', 'short_name']


class ProjectTaskInline(admin.StackedInline):
    model = ProjectTask


class ProjectUserStoryAdmin(admin.ModelAdmin):
    model = ProjectUserStory
    inlines = (ProjectTaskInline,)


class ProjectUserStoryInline(admin.StackedInline):
    model = ProjectUserStory


class ProjectEpicAdmin(admin.ModelAdmin):
    model = ProjectEpic
    inlines = (ProjectUserStoryInline, )


class ProjectEpicInline(admin.StackedInline):
    model = ProjectEpic

class ProjectAssessmentAdmin(admin.ModelAdmin):
    model = ProjectAssessment

class ProjectAssessmentInline(admin.StackedInline):
    model = ProjectAssessment


class ProjectAdmin(admin.ModelAdmin):
    raw_id_fields = ('business',)
    list_display = ('name', 'business', 'point_person', 'status', 'type')
    list_filter = ('type', 'status')
    search_fields = ('name', 'business__name', 'point_person__username',
                     'point_person__first_name', 'point_person__last_name',
                     'description')
    inlines = (ProjectAssessmentInline, ProjectEpicInline)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'hours_per_week')


admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Business, BusinessAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(TeamMemberRole)
admin.site.register(TeamMember)
admin.site.register(ProjectTeam)
admin.site.register(ProjectAssessment, ProjectAssessmentAdmin)
admin.site.register(ProjectUserStory, ProjectUserStoryAdmin)
admin.site.register(ProjectEpic, ProjectEpicAdmin)
