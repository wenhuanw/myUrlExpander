from django import forms
from .models import ExpandedUrl

class ExpandedUrlForm(forms.ModelForm):

    class Meta:
        model = ExpandedUrl
        fields = ('origin',)
