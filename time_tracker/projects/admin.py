from django.contrib import admin

from .models import Project, ProjectHours


class ProjectHoursInline(admin.TabularInline):
	model = ProjectHours
	extra = 1


class ProjectAdmin(admin.ModelAdmin):
	list_display = ('name', )

	inlines = [ProjectHoursInline]


admin.site.register(Project, ProjectAdmin)