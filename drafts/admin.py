from django.contrib import admin
from drafts.models import Document, Draft


class DraftInline(admin.TabularInline):
    model = Draft
    extra = 1


class DocumentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['hashid', 'user']}),
        ('Document Info', {'fields': ['date_created', 'latest_draft']}),
    ]
    inlines = [DraftInline]
    list_display = ('hashid', 'latest_draft', 'user', 'date_created')
    readonly_fields = ['latest_draft', 'date_created']

admin.site.register(Document, DocumentAdmin)
