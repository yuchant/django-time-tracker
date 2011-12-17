from django import http
from django.contrib import admin

from django.conf.urls.defaults import patterns
from django.shortcuts import render

from .models import Address, Project, ProjectHours, Invoice


class ProjectHoursInline(admin.TabularInline):
    model = ProjectHours
    extra = 1

# where do project documents go?

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', )
    inlines = [ProjectHoursInline]

    actions = [
        'action_generate_invoice',
    ]

    def action_generate_invoice(self, request, queryset):
        if not queryset.count() == 1:
            self.message_user(request, "Must only select 1 project to invoice")
            return
        project = queryset[0]
        hours = project.projecthours_set.filter(paid=False)
        
        if not hours:
            self.message_user(request, "No hours to charge")


        invoice = project.invoice_set.create()
        invoice.hours = hours
        invoice.save() # saves m2m


class InvoiceAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(InvoiceAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^(?P<pk>\d+)/render/$', self.render_invoice)
        )
        return my_urls + urls


    def render_invoice(self, request, pk):
        ctx = {}
        invoice = Invoice.objects.select_related('project', 'hours').get(pk=pk)
        ctx['invoice'] = invoice
        ctx['project'] = invoice.project
        return render(request, "projects/invoices/template1.html", ctx)


admin.site.register(Address)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Invoice, InvoiceAdmin)
