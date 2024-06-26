from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Chanel, Post, Log
from .serializers import ChanelSerializer, PostSerializer, PostLastViewSerializer, LogCreateViewSerializer
from rest_framework import viewsets


class ChanelListView(viewsets.ModelViewSet):
    serializer_class = ChanelSerializer
    queryset = Chanel.objects.all()


class PostsListViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostDetailView(APIView):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)


class PostLastViewChanger(viewsets.ModelViewSet):
    serializer_class = PostLastViewSerializer
    queryset = Post.objects.all()

    def update(self, request, *args, **kwargs):
        post_id = kwargs['pk']
        post = Post.objects.filter(id=post_id).last()
        post.last_viewed_destination_index = request.data["last_viewed_destination_index"]
        return super().update(request, *args, **kwargs)


class LogCreate(viewsets.ModelViewSet):
    serializer_class = LogCreateViewSerializer
    queryset = Log.objects.all()
