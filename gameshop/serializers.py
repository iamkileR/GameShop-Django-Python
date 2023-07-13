from .models import Developer, Category, Game
from rest_framework import serializers

# Serializery powoduja, ze obiekt z bazy danych zamieniany jest na obiekt JSON
class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ["developer", "slug"] # Pola serializera dla modelu Developer: developer, slug

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category", "slug"] # Pola serializera dla modelu Category: category, slug

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        # Pola serializera dla modelu Game: category, developer, title, description, instock, price, release_date, creation_date, slug
        fields = ["category", "developer", "title", "description", "instock", "price", "release_date", "creation_date", "slug"]