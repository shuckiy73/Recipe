# from django.apps import AppConfig
# from django.utils.translation import gettext_lazy as _

# class RecipesConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'recipes'
#     verbose_name = _('Кулинарные рецепты')

#     def ready(self):
#         # Регистрируем сигналы после полной загрузки приложения
#         from django.db.models.signals import post_migrate
        
#         def register_signals(**kwargs):
#             # Импортируем сигналы только после миграций
#             try:
#                 from . import signals  # noqa: F401
#             except ImportError:
#                 # Файл signals.py не обязателен
#                 pass
        
#         # Подключаем обработчик после завершения миграций
#         post_migrate.connect(register_signals, sender=self)


from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RecipesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes'
    verbose_name = _('Кулинарные рецепты')

    def ready(self):
        # Регистрируем сигналы после полной загрузки приложения
        from django.db.models.signals import post_migrate
        
        def register_signals(sender, **kwargs):
            # Импортируем сигналы только после миграций
            try:
                from . import signals  # noqa: F401
            except ImportError:
                # Файл signals.py не обязателен
                pass
        
        # Подключаем обработчик после завершения миграций
        post_migrate.connect(register_signals, sender=self)