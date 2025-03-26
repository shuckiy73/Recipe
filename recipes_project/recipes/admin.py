from django.contrib import admin
from django.utils.html import format_html
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'cooking_time_display', 
                   'difficulty', 'author', 'is_published', 'created_at')
    list_filter = ('category', 'difficulty', 'is_published', 'created_at')
    search_fields = ('title', 'ingredients', 'author__username')
    list_editable = ('price', 'is_published')
    readonly_fields = ('slug', 'created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'author', 'category', 'is_published')
        }),
        ('Детали рецепта', {
            'fields': ('ingredients', 'cooking_steps', 'difficulty')
        }),
        ('Метаданные', {
            'fields': ('price', 'cooking_time', 'image', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    filter_horizontal = ()
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 25
    actions = ['make_published', 'make_unpublished']

    def cooking_time_display(self, obj):
        return obj.get_cooking_time_display()
    cooking_time_display.short_description = 'Время приготовления'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = 'Превью'

    @admin.action(description="Опубликовать выбранные рецепты")
    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Снять с публикации выбранные рецепты")
    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            fieldsets[0][1]['fields'] = tuple(
                f for f in fieldsets[0][1]['fields'] if f != 'is_published'
            )
        return fieldsets