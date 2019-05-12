from django import forms
from .models import Case


class AlertForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ('first_name', 'last_name', 'email_address', 'mobile_number', 'affected_county', 'affected_persons',
                  'case_description', 'supportive_image')

    def clean_mobile_number(self):

        data = self.cleaned_data['mobile_number']
        if '@' in data or '-' in data or '|' in data or ' ' in data:
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
