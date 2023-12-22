
from .models import Chanel, Post
from .serializers import ChanelSerializer, PostSerializer
from rest_framework import viewsets


class ChanelListView(viewsets.ModelViewSet):
    serializer_class = ChanelSerializer
    queryset = Chanel.objects.all()


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()











