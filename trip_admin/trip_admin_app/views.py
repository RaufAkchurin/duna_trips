
from .models import Chanel, Post
from .serializers import ChanelSerializer, PostSerializer, PostLastViewSerializer
from rest_framework import viewsets


class ChanelListView(viewsets.ModelViewSet):
    serializer_class = ChanelSerializer
    queryset = Chanel.objects.all()


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostLastViewChanger(viewsets.ModelViewSet):
    serializer_class = PostLastViewSerializer
    queryset = Post.objects.all()

    def update(self, request, *args, **kwargs):
        post_id = kwargs['pk']
        post = Post.objects.filter(id=post_id).last()
        post.last_viewed_destination_index = request.data["last_viewed_destination_index"]
        return super().update(request, *args, **kwargs)









