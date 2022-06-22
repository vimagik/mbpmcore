from rest_framework import serializers

from conman.models import CmProcessContext


class StartFormSerializer(serializers.ModelSerializer):
    responsible = serializers.CharField(max_length=50)

    class Meta:
        model = CmProcessContext
        fields = ['short_name', 'what_to_do', 'perform_before', 'responsible']
