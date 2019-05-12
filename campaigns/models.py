from django.db import models
from django.utils import timezone
from datetime import date
from django.conf import settings
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class County(models.Model):
    county_name = models.CharField(max_length=100)
    county_code = models.CharField(max_length=100)

    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.county_name


class OpenCampaign(models.Model):

    CAMPAIGN_STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed')
    )

    campaign_title = models.CharField(max_length=250)
    region = models.ForeignKey(County, on_delete=models.CASCADE)
    target_population = models.CharField(max_length=250)
    running_from = models.DateField()
    running_to = models.DateField()
    thumbnail = models.ImageField(upload_to='open_campaigns')

    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    registration_status = models.CharField(max_length=250, choices=CAMPAIGN_STATUS_CHOICES, default='Open')
    voting_status = models.CharField(max_length=250, choices=CAMPAIGN_STATUS_CHOICES, default='Open')

    # Restring end date(should not be less than start date)
    def clean(self):
        start_date = self.running_from
        end_date = self.running_to
        if end_date < start_date:
            raise ValidationError({'running_to': ["Invalid end date, cannot be before start date"]})

    # Restring start date(should not be less than today's date)
        if start_date < date.today():
            raise ValidationError({'running_from': ["Invalid start date, cannot be a date before today's date"]})

    def __str__(self):
        return self.campaign_title


class SubmittedCampaign(models.Model):

    CAMPAIGN_STATUS = (
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('waiting', 'Waiting')
    )

    APPLICANT_TYPE_CHOICES = (
        ('group', 'Group'),
        ('organization', 'Organization')
    )

    open_campaign = models.ForeignKey(OpenCampaign, on_delete=models.CASCADE)
    applicant_type = models.CharField(max_length=100, choices=APPLICANT_TYPE_CHOICES)
    organization_or_group_name = models.CharField(max_length=100)
    email_address = models.EmailField(max_length=255)
    mobile_number = models.CharField(max_length=10)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)

    group_or_org_description = models.TextField(max_length=1000, help_text='Briefly describe your group/organization')
    supporting_image = models.ImageField(upload_to='campaign_images')
    group_or_org_profile = models.FileField(upload_to='campaign_profiles', help_text='Upload a pdf of your profile')
    status = models.CharField(max_length=255, choices=CAMPAIGN_STATUS, default='waiting')

    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    total_votes = models.IntegerField(default=0, blank=True, null=True)

    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.organization_or_group_name

    class Meta:
        verbose_name_plural = 'Submitted Campaigns'


class Vote(models.Model):
    open_campaign = models.CharField(max_length=250)
    organization_or_group_name = models.CharField(max_length=255)
    voter_name = models.CharField(max_length=250)
    voter_id = models.IntegerField()
    vote_time = models.CharField(max_length=250, default='')

    def __str__(self):
        return self.voter_name

    class Meta:
        verbose_name_plural = "Votes"





