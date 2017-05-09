from .models import Recipe
from .serializers import RecipeSerializer

from rest_framework import generics, permissions


class RecipeList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer