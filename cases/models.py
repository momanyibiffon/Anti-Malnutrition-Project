from django.db import models
from django.utils import timezone
from django.conf import settings


class Case(models.Model):
    AFFECTED_PERSONS_CHOICES = (
        ('children_under_5', 'Children Under 5 years'),
        ('children_under_18', 'Children Under 18 years'),
        ('adults_under_40', 'Adults Under 40 years'),
        ('adults_over_40', 'Children Over 40 years'),
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.EmailField(max_length=255, unique_for_date="published")
    mobile_number = models.CharField(max_length=10)
    affected_county = models.CharField(max_length=10)
    affected_persons = models.CharField(max_length=255, choices=AFFECTED_PERSONS_CHOICES)
    case_description = models.TextField(max_length=500, unique=True)
    supportive_image = models.ImageField(upload_to='cases_images')

    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.affected_county
