"""PD_Projekt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

# Tworzenie schemy widoku Swagger
schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Projekt API",
        default_version='1.0.0',
        description="Api documentation of App",
    ),
    public=True,
)
# Definicja tras URL
urlpatterns = [
    path('admin/', admin.site.urls), # Trasa dla panelu administracyjnego Django
    path('', include('gameshop.urls',namespace='gameshop')), # Trasa dla aplikacji "gameshop"
    path('api-auth/', include('rest_framework.urls')), # Trasa dla uwierzytelniania w REST Framework
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Trasa dla uzyskiwania tokenu JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Trasa dla odświeżania tokenu JWT
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'), # Trasa dla weryfikacji tokenu JWT
    path('swagger/schema/',schema_view.with_ui('swagger',cache_timeout=0),name="swagger-schema"), # Trasa dla widoku Swagger
]
# Dodawanie tras dla plików statycznych w trybie DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)