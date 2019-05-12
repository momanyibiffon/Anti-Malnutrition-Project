import csv
from django.contrib import admin
from django.shortcuts import HttpResponse
from . models import County, SubmittedCampaign, Vote, OpenCampaign
from import_export.admin import ImportExportModelAdmin


def export_campaigns(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="campaigns.csv"'
    writer = csv.writer(response)
    writer.writerow(['open_campaign', 'applicant_type', 'organization_or_group_name', 'email_address', 'mobile_number',
        'county', 'city', 'supporting_image', 'group_or_org_profile', 'total_votes', 'status'])
    campaigns = queryset.values_list('title', 'publication_date', 'author', 'price', 'pages', 'book_type')
    for campaign in campaigns:
        writer.writerow(campaign)
    return response


export_campaigns.short_description = 'Export to csv'


class CampaignAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Owner information', {
            'fields': ['open_campaign', 'applicant_type', 'organization_or_group_name', 'group_or_org_description',
                       'supporting_image'],
            'classes': []
        }),
        ('Contact & Location information', {
            'fields': ['email_address', 'mobile_number', 'county', 'city'],
            # 'classes': ['collapse']
        }),
        ('Date information', {
            'fields': ['published'],
            # 'classes': ['collapse']
        }),
        ('Total Votes and Status', {
            'fields': ['total_votes', 'status'],
            # 'classes': ['collapse']
        }),
    ]
    list_display = (
        'open_campaign',
        'applicant_type',
        'organization_or_group_name',
        'email_address',
        'mobile_number',
        'county',
        'city',
        'supporting_image',
        'group_or_org_profile',
        'total_votes',
        'status'
    )
    #readonly_fields = ('open_campaign', 'applicant_type', 'organization_or_group_name', 'group_or_org_description',
     #                  'email_address', 'mobile_number', 'county', 'city',
      #                 'total_votes', 'published')

    readonly_fields = ('total_votes', 'published')
    actions = [export_campaigns]


class VoterAdmin(admin.ModelAdmin):
    list_display = ('open_campaign', 'organization_or_group_name', 'voter_name', 'voter_id', 'vote_time')
    list_filter = ('open_campaign', 'organization_or_group_name', 'voter_name', 'vote_time')
    search_fields = ('open_campaign', 'voter_name')
    readonly_fields = ('open_campaign', 'voter_name', 'voter_id', 'vote_time')


class OpenCampaignAdmin(admin.ModelAdmin):
    list_display = ('campaign_title', 'region', 'target_population', 'running_from',
                    'running_to', 'published', 'registration_status', 'voting_status')
    list_filter = ('campaign_title', 'region', 'target_population',  'running_from',
                   'running_to', 'published', 'registration_status', 'voting_status')
    search_fields = ('campaign_title', 'region')


admin.site.site_header = 'Nutritious Kenya Dashboard'
admin.site.register(County)
admin.site.register(SubmittedCampaign, CampaignAdmin)
admin.site.register(Vote, VoterAdmin)
admin.site.register(OpenCampaign, OpenCampaignAdmin)


#@admin.register(SubmittedCampaign)
#class CampaignAdmin(ImportExportModelAdmin):
 #   pass
