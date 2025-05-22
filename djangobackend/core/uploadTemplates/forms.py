from django import forms
from uploadTemplates.models import template

class templateForm(forms.ModelForm):
    class Meta:
        model=template
        field=('name','file')