from django.urls import path

from . import views
from .views import (
    GameshopApiCheck,
    GameshopApiGamesView,
    GameshopApiCategoriesView,
    GameshopApiDevelopersView,
    GameshopApiAddDeveloper,
    GameshopApiManageDeveloper,
    GameshopApiAddCategory,
    GameshopApiManageCategory
)

app_name = 'gameshop'

urlpatterns = [
    path('', views.index, name='index'),# Strona główna
    path('products/', views.products, name='products'),# Lista produktów
    path('regulamin/', views.regulamin, name='regulamin'),# Regulamin
    path('pomoc/', views.pomoc, name='pomoc'),# Strona pomocy
    path('login/', views.userlogin, name='login'),# Logowanie użytkownika
    path('register/', views.register, name='register'),# Rejestracja użytkownika
    path('otpaRegister/', views.otpaRegister, name='otpaRegister'),# Rejestracja z weryfikacją OTP
    path('game/<slug:slug>/',views.game, name='game'),# Strona gry
    path('game/<slug:slug>/buy',views.buy, name='buy'),# Zakup gry
    path('logout/', views.userlogout, name='logout'),# Wylogowanie użytkownika
    path('otpaLogin/', views.otpaLogin, name='otpaLogin'),# Logowanie z weryfikacją OTP
    path('api/', GameshopApiCheck.as_view()), # Sprawdzenie działania API
    path('api/games/', GameshopApiGamesView.as_view()), # Lista gier w API
    path('api/developers/', GameshopApiDevelopersView.as_view()),# Lista deweloperów w API
    path('api/categories/', GameshopApiCategoriesView.as_view()),# Lista kategorii gier w API
    path('api/admin/developers/', GameshopApiAddDeveloper.as_view()),# Dodawanie dewelopera w API (dla administratora)
    path('api/admin/developers/<int:pk>', GameshopApiManageDeveloper.as_view()),# Zarządzanie deweloperem w API (dla administratora)
    path('api/admin/category/', GameshopApiAddCategory.as_view()),# Dodawanie kategorii gry w API (dla administratora)
    path('api/admin/category/<int:pk>', GameshopApiManageCategory.as_view())# Zarządzanie kategorią gry w API (dla administratora)
]