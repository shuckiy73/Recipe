from django.db import migrations, models
import django.utils.text
from django.db.models import F

def generate_slugs(apps, schema_editor):
    Recipe = apps.get_model('recipes', 'Recipe')
    for recipe in Recipe.objects.all():
        recipe.slug = django.utils.text.slugify(recipe.title)
        recipe.save()

class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, blank=True),
            preserve_default=False,
        ),
        migrations.RunPython(generate_slugs),
    ]