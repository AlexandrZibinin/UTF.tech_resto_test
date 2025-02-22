from django.db import DatabaseError
from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from food.models import FoodCategory, Food
from food.pagination import FoodPagination
from food.serializers import FoodListSerializer


class FoodListView(APIView):
    # пагинация отключена
    # pagination_class = FoodPagination

    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        try:
            categories = FoodCategory.objects.filter(food__is_publish=True).distinct()
            categories = categories.prefetch_related(
                Prefetch("food", queryset=Food.objects.filter(is_publish=True))
            )

            serializer = FoodListSerializer(categories, many=True)

            return Response(serializer.data)


        except DatabaseError as e:
            return Response(
                {"error": "Ошибка подключения к БД", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
