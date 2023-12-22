from rest_framework import serializers

from .models import Chanel, Post, Destination


class ChanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chanel
        fields = (
            "id",
            "name",
            "chanel_chat_id"
        )


class DestinationSerializer(serializers.ModelSerializer):
    origin_code = serializers.CharField(source="origin.code")
    destination_code = serializers.CharField(source="destination.code")

    class Meta:
        model = Destination
        fields = (
            "id",
            "origin_code",
            "destination_code"
        )


class PostSerializer(serializers.ModelSerializer):
    destinations = serializers.SerializerMethodField(source="id")

    class Meta:
        model = Post
        fields = (
            "name",
            "chanel",
            "text",
            "destinations"
        )

    def get_destinations(self, Post):
        destinations = Destination.objects.filter(post__id=Post.id)
        destination_serializer = DestinationSerializer(destinations, many=True)
        return destination_serializer.data