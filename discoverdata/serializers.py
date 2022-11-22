from rest_framework import serializers

class FileTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=2000)
