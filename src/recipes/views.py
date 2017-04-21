from django.http import HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import send_mail
from .models import Recipe, Food
from .serializers import RecipeSerializer

from django.views.generic import ListView, CreateView, DetailView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class RecipeList(APIView):
    def get(self, request, format=None):
        restaurants = Recipe.objects.all()
        serializer = RecipeSerializer(restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def root(request):
    return HttpResponseRedirect("/cookbook")

class RecipeListView(ListView):
    model = Recipe
    paginate_by = 100

    def get_queryset(self):
        qs = Recipe.objects.all()
        return qs

class RecipeDetailView(DetailView):
    model = Recipe

    def get_object(self, queryset=None):
        recipe = super(RecipeDetailView, self).get_object(queryset=queryset)
        if 'scale' in self.request.GET:
            recipe.scale = float(self.request.GET['scale'])
            print("set scale to", recipe.scale)
        else:
            recipe.scale = 1.0
        return recipe

class FoodConversionListView(ListView):
    model = Food

    def get_queryset(self):
        qs = Food.objects.with_conversions()
        return qs

