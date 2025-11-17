from rest_framework import serializers
from .models import RSVP,WeddingMedia

class RSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RSVP
        fields = '__all__'


class WeddingMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeddingMedia
        fields = '__all__'