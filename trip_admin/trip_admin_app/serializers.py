from rest_framework import serializers

from .models import Chanel


class ChanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chanel
        fields = (
            "id",
            "name",
            "chanel_chat_id"
        )
