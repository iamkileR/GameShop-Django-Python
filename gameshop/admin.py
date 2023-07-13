from django.contrib import admin

from .models import Category, Developer, Game

#Poprzez rejestrację modeli w panelu administratora, można zarządzać nimi
# poprzez interfejs administratora, co umożliwia dodawanie, edytowanie
# i usuwanie obiektów tych modeli.
admin.site.register(Category)
admin.site.register(Developer)
admin.site.register(Game)

