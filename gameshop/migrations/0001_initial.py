# Generated by Django 4.1.7 on 2023-06-24 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(db_index=True, max_length=256, unique=True, verbose_name='Kategoria')),
                ('slug', models.SlugField(max_length=256, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Kategorie',
            },
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('developer', models.CharField(db_index=True, max_length=256, unique=True, verbose_name='Nazwa developera')),
                ('slug', models.SlugField(max_length=256, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Developerzy',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Tytuł')),
                ('description', models.TextField(blank=True, verbose_name='Opis')),
                ('instock', models.BooleanField(default=False, verbose_name='Dostępność')),
                ('price', models.DecimalField(decimal_places=2, max_digits=30, verbose_name='Cena')),
                ('release_date', models.DateField(verbose_name='Data wydania')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Data dodania')),
                ('image', models.ImageField(upload_to='')),
                ('slug', models.SlugField(max_length=256, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cat', to='gameshop.category', verbose_name='Kategoria')),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dev', to='gameshop.developer', verbose_name='Developer')),
            ],
            options={
                'verbose_name_plural': 'Gry',
            },
        ),
    ]
