from rest_framework import serializers
from .models import StatementTemplates
class StatementTemplateSerializer(serializers.ModelSerializer):
    model=StatementTemplates
    fields={"template_path"}
