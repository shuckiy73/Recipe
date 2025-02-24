from django.db import models


class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ("Десерты", "Десерты"),
        ("Первые блюда", "Первые блюда"),
        ("Вторые блюда", "Вторые блюда"),
        ("Напитки", "Напитки"),
    ]

    title = models.CharField(max_length=255, unique=True)
    ingredients = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    owner_name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True)

    def save(self, *args, **kwargs):
        # Автоматически назначаем категорию по названию рецепта
        if any(word in self.title.lower() for word in ["торт", "пирог", "печенье"]):
            self.category = "Десерты"
        elif any(word in self.title.lower() for word in ["суп", "борщ", "уха"]):
            self.category = "Первые блюда"
        elif any(word in self.title.lower() for word in ["котлета", "паста", "мясо"]):
            self.category = "Вторые блюда"
        else:
            self.category = "Напитки"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

