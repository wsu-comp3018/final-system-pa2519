from django.shortcuts import render
from uploadTemplates.forms import templateForm

def upload_form(request):
    context={'form': templateForm()}
    return render()