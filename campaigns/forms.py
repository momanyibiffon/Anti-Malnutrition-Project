from django import forms
from .models import Vote, SubmittedCampaign
from django.contrib.auth.models import User


class VoterForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ('open_campaign', 'organization_or_group_name', 'voter_name', 'voter_id', 'vote_time')


class CampaignForm(forms.ModelForm):
    class Meta:
        model = SubmittedCampaign
        fields = ('open_campaign', 'applicant_type',
                  'organization_or_group_name', 'email_address', 'mobile_number', 'county', 'city',
                  'group_or_org_description', 'supporting_image', 'group_or_org_profile')

    def clean_mobile_number(self):

        data = self.cleaned_data['mobile_number']
        if '@' in data or '-' in data or '|' in data or ' ' in data or '_' in data:
            raise forms.ValidationError("Mobile number cannot have special characters.")
        if 'a' in data or 'b' in data or 'c' in data or 'd' in data or 'e' in data or 'f' in data or 'g' in data:
            raise forms.ValidationError("Mobile number must only contain integers")
        if 'h' in data or 'i' in data or 'j' in data or 'k' in data or 'l' in data or 'm' in data or 'n' in data:
            raise forms.ValidationError("Mobile number must only contain integers")
        if 'o' in data or 'p' in data or 'q' in data or 'r' in data or 's' in data or 't' in data or 'u' in data:
            raise forms.ValidationError("Mobile number must only contain integers")
        if 'v' in data or 'w' in data or 'x' in data or 'y' in data or 'z' in data:
            raise forms.ValidationError("Mobile number must only contain integers")

        return data

    def clean_email_address(self):
        data = self.cleaned_data['email_address']
        if data != User.email:
            raise forms.ValidationError("Email address doesn't match your account email.")
