from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid

User = get_user_model()

class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ("Десерты", "Десерты"),
        ("Первые блюда", "Первые блюда"),
        ("Вторые блюда", "Вторые блюда"),  # Исправлена опечатка "Вторые"
        ("Напитки", "Напитки"),
        ("Закуски", "Закуски"),
        ("Салаты", "Салаты"),
    ]

    DIFFICULTY_CHOICES = [
        ("Легко", "Легко"),
        ("Средне", "Средне"),
        ("Сложно", "Сложно"),
    ]

    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Название рецепта"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        verbose_name="URL-адрес"
    )
    ingredients = models.TextField(verbose_name="Ингредиенты")
    cooking_steps = models.TextField(verbose_name="Шаги приготовления")
    cooking_time = models.PositiveIntegerField(
        verbose_name="Время приготовления (мин)",
        validators=[MinValueValidator(1)],
        default=30
    )
    difficulty = models.CharField(
        max_length=50,
        choices=DIFFICULTY_CHOICES,
        default="Средне",
        verbose_name="Сложность"
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Примерная стоимость",
        validators=[MinValueValidator(0)]
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        blank=True,
        verbose_name="Категория"
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=True,
        null=True,
        verbose_name="Изображение"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name="Автор",
        null=True,
        blank=True
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано"
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['category']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug
            
            # Добавляем уникальный суффикс если slug уже существует
            while Recipe.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{uuid.uuid4().hex[:4]}"  # Используем 4 символа для краткости
        
        # Автоматическое определение категории
        if not self.category:
            title_lower = self.title.lower()
            if any(word in title_lower for word in ["торт", "пирог", "печенье", "десерт"]):
                self.category = "Десерты"
            elif any(word in title_lower for word in ["суп", "борщ", "уха", "бульон"]):
                self.category = "Первые блюда"
            elif any(word in title_lower for word in ["котлета", "паста", "мясо", "рыба"]):
                self.category = "Вторые блюда"
            elif any(word in title_lower for word in ["коктейль", "чай", "кофе", "сок"]):
                self.category = "Напитки"
            else:
                self.category = "Закуски"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_cooking_time_display(self):
        """Возвращает время приготовления в формате '1 ч 30 мин'"""
        hours = self.cooking_time // 60
        minutes = self.cooking_time % 60
        return f"{hours} ч {minutes} мин" if hours else f"{minutes} мин"

    def get_absolute_url(self):
        return reverse('recipe-detail', kwargs={'slug': self.slug})