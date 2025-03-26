from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Recipe
from django.template.defaultfilters import slugify

@receiver(pre_save, sender=Recipe)
def update_recipe_slug(sender, instance, **kwargs):
    """Автоматически обновляет slug при изменении названия"""
    if not instance.slug or instance.title != sender.objects.get(pk=instance.pk).title:
        instance.slug = slugify(instance.title)

@receiver(post_save, sender=Recipe)
def notify_admins_new_recipe(sender, instance, created, **kwargs):
    """Отправляет уведомление при создании нового рецепта"""
    if created:
        print(f"Создан новый рецепт: {instance.title}")  # Замените на реальную логику отправки