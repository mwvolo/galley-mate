from django.conf.urls import url
from .views import RecipeList, RecipeDetail


urlpatterns = [

    url(r'^$', RecipeList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', RecipeDetail.as_view()),
]
