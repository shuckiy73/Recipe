from rest_framework import serializers
from .models import Recipe
from django.utils.text import slugify
from rest_framework.validators import UniqueValidator

class RecipeSerializer(serializers.ModelSerializer):
    # Дополнительные поля (read-only)
    slug = serializers.CharField(read_only=True)
    cooking_time_display = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    
    # Валидация уникальности названия
    title = serializers.CharField(
        max_length=255,
        validators=[
            UniqueValidator(
                queryset=Recipe.objects.all(),
                message="Рецепт с таким названием уже существует"
            )
        ]
    )
    
    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'ingredients',
            'cooking_steps',
            'cooking_time',
            'cooking_time_display',
            'difficulty',
            'category',
            'image',
            'created_at',
            'updated_at',
            'author',
            'is_favorite',
            'nutrition_facts'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']
        extra_kwargs = {
            'cooking_steps': {'write_only': True},  # Скрываем в списке рецептов
            'nutrition_facts': {'required': False}
        }

    def get_cooking_time_display(self, obj):
        """Отображаем время приготовления в формате '1 ч 30 мин'"""
        hours = obj.cooking_time // 60
        minutes = obj.cooking_time % 60
        return f"{hours} ч {minutes} мин" if hours else f"{minutes} мин"

    def get_is_favorite(self, obj):
        """Проверяем, есть ли рецепт в избранном у текущего пользователя"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False

    def validate_title(self, value):
        """Автоматически создаем slug из названия"""
        self.slug = slugify(value)
        return value

    def validate_cooking_time(self, value):
        """Проверяем, что время приготовления положительное"""
        if value <= 0:
            raise serializers.ValidationError("Время приготовления должно быть положительным числом")
        return value

    def create(self, validated_data):
        """Автоматически устанавливаем автора рецепта"""
        validated_data['author'] = self.context['request'].user
        validated_data['slug'] = self.slug
        return super().create(validated_data)