from django.contrib import admin
from .models import Case


class CasesAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Sender information', {
            'fields': ['first_name', 'last_name', 'email_address', 'mobile_number'],
            'classes': []
        }),

        ('Affected Location Details', {
            'fields': ['affected_county', 'affected_persons', 'case_description', 'supportive_image'],
            'classes': []
        }),

        ('Date Information', {
            'fields': ['published'],
            'classes': []
        }),


    ]
    list_display = (
        'affected_county',
        'affected_persons',
        'first_name',
        'last_name',
        'email_address',
        'mobile_number',
        'published',
    )

    list_filter = (
        'affected_county',
        'affected_persons',
        'first_name',
        'last_name',
        'email_address',
        'mobile_number',
        'published',
    )

    readonly_fields = (
        'affected_county',
        'affected_persons',
        'first_name',
        'last_name',
        'email_address',
        'mobile_number',
        'case_description',
        'supportive_image',
        'published',
    )
    search_fields = (
        'affected_county',
        'affected_persons',
        'first_name',
        'last_name',
        'email_address',
        'mobile_number',
        'published',
    )


admin.site.register(Case, CasesAdmin)
