# Generated by Django 3.1.3 on 2020-12-01 21:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0002_auto_20201128_1346'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'permissions': [('author_admin', 'Administrar Autores')]},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'permissions': [('book_admin', 'Administrar Livros')]},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL),
        ),
    ]
