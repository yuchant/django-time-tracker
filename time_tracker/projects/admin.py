from django import http
from django.contrib import admin

from django.conf.urls.defaults import patterns
from django.shortcuts import render

from .models import Project, ProjectHours


class ProjectHoursInline(admin.TabularInline):
    model = ProjectHours
    extra = 1

# where do project documents go?

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', )
    inlines = [ProjectHoursInline]

    def get_urls(self):
        urls = super(ProjectAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^(?P<pk>\d+)/render_invoice/$', self.render_invoice)
        )
        return my_urls + urls


    def render_invoice(self, request, pk):
        ctx = {}
        return render(request, "projects/invoices/template1.html", ctx)


admin.site.register(Project, ProjectAdmin)