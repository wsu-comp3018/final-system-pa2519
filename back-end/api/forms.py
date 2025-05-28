from django import forms
from .models import StatementTemplates

class uploadTemplates(forms.ModelForm):
    class Meta:
        model=StatementTemplates
        fields=('template_path',)