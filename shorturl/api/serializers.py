from shorturl.models import Url
from rest_framework import serializers

class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = '__all__'
        read_only_fields = ['short', 'owner', 'date', 'id']
            


