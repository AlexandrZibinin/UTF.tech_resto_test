from django.urls import path

from food.apps import FoodConfig
from food.views import FoodListView

app_name = FoodConfig.name

urlpatterns = [
    path("api/v1/foods/", FoodListView.as_view(), name="foods-list"),
]
