from django import forms
from .models import StatementTemplates

class uploadTemplates(forms.ModelForm):
    class Meta:
        file_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        files=forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))

        model=StatementTemplates
        fields='__all__'