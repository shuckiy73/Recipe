from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Recipe
from .serializers import RecipeSerializer
from django_filters import FilterSet, NumberFilter, CharFilter, ChoiceFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.db.models import Q

class RecipeFilter(FilterSet):
    # Фильтры для числовых полей
    min_price = NumberFilter(field_name="price", lookup_expr='gte', 
                           help_text="Минимальная цена (>=)")
    max_price = NumberFilter(field_name="price", lookup_expr='lte',
                           help_text="Максимальная цена (<=)")
    title_contains = CharFilter(field_name="title", lookup_expr='icontains',
                              help_text="Поиск по части названия")
    cooking_time_min = NumberFilter(field_name="cooking_time", lookup_expr='gte',
                                 help_text="Минимальное время приготовления (мин)")
    cooking_time_max = NumberFilter(field_name="cooking_time", lookup_expr='lte',
                                 help_text="Максимальное время приготовления (мин)")
    
    # Фильтры для полей с choices (используем явное определение choices)
    category = ChoiceFilter(
        field_name="category",
        choices=[
            ("Десерты", "Десерты"),
            ("Первые блюда", "Первые блюда"),
            ("Вторые блюда", "Вторые блюда"),
            ("Напитки", "Напитки"),
            ("Закуски", "Закуски"),
        ],
        label="Категория"
    )
    
    difficulty = ChoiceFilter(
        field_name="difficulty",
        choices=[
            ("Легко", "Легко"),
            ("Средне", "Средне"),
            ("Сложно", "Сложно"),
        ],
        label="Сложность"
    )
    
    class Meta:
        model = Recipe
        fields = {
            'author': ['exact'],
            'is_published': ['exact'],
        }

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related('author').order_by('-created_at')
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    
    filterset_class = RecipeFilter
    search_fields = ['title', 'ingredients', 'cooking_steps', 'author__username']
    ordering_fields = ['id', 'title', 'price', 'created_at', 'cooking_time']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Базовые фильтры
        if not user.is_staff:
            queryset = queryset.filter(is_published=True)
        
        # Дополнительные фильтры из параметров запроса
        query_params = self.request.query_params
        
        # Фильтр "мои рецепты"
        if query_params.get('my_recipes', '').lower() in ['true', '1']:
            if user.is_authenticated:
                queryset = queryset.filter(author=user)
        
        # Фильтр по нескольким категориям (category=Десерты,Напитки)
        if 'category' in query_params:
            categories = query_params['category'].split(',')
            queryset = queryset.filter(category__in=categories)
        
        return queryset

    def perform_create(self, serializer):
        """Автоматическое назначение автора"""
        serializer.save(author=self.request.user)

    def get_permissions(self):
        """Дополнительные проверки прав для опасных методов"""
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()

    def check_object_permissions(self, request, obj):
        """Проверка прав для конкретного объекта"""
        super().check_object_permissions(request, obj)
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if obj.author != request.user and not request.user.is_staff:
                self.permission_denied(
                    request,
                    message="У вас нет прав для этого действия",
                    code=status.HTTP_403_FORBIDDEN
                )