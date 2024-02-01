from rest_framework import serializers

from .models import Chanel, Post, Destination, Log


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
    origin_name = serializers.CharField(source="origin.name")
    destination_code = serializers.CharField(source="destination.code")
    destination_name = serializers.CharField(source="destination.name")

    class Meta:
        model = Destination
        fields = (
            "id",
            "origin_code",
            "origin_name",
            "destination_code",
            "destination_name",
        )


class PostSerializer(serializers.ModelSerializer):
    chanel = ChanelSerializer(read_only=True)
    destinations = serializers.SerializerMethodField(source="id")

    class Meta:
        model = Post
        fields = (
            "id",
            "name",
            "chanel",
            "text_before",
            "text_after",
            "picture",
            "destinations",
            "last_viewed_destination_index",
            "count_of_tickets_in_direction",
            "return_tickets",
            "max_price_of_tickets",
        )

    def get_destinations(self, Post):
        destinations = Destination.objects.filter(post__id=Post.id)
        destination_serializer = DestinationSerializer(destinations, many=True)
        return destination_serializer.data


class PostLastViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "last_viewed_destination_index",
        )


class LogCreateViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = (
            "title",
            "body",
        )
