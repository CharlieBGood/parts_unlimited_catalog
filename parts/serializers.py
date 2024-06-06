from parts.models import Part
from rest_framework import serializers

class PartsSerializer(serializers.ModelSerializer):
    """
    Parts serializer
    """
    class Meta:
        model = Part
        fields = "__all__"
