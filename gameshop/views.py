from django.shortcuts import render, get_object_or_404, redirect
from .models import Game, Developer, Category
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import CreateUserForm, UserLoginForm, OTPVerificationForm
from django.contrib import messages
from django.http import Http404
from django_otp.decorators import otp_required
from django_otp.forms import OTPAuthenticationForm
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import CategorySerializer, DeveloperSerializer, GameSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.views.decorators.http import require_http_methods, require_GET, require_POST

User = get_user_model()

def generate_otp_code():
    return get_random_string(length=6)

# Widok strony głównej
@require_GET
def index(request):
    return render(request, "gameshop/index.html")
# Widok listy produktów
@require_GET
def products(request):
    products = Game.objects.all()
    return render(request, 'gameshop/products.html', {'products': products})
# Widok regulaminu
@require_GET
def regulamin(request):
    return render(request, 'gameshop/regulamin.html')
# Widok pomocy
@require_GET
def pomoc(request):
    return render(request, 'gameshop/pomoc.html')
# Widok rejestracji użytkownika
@require_http_methods(["GET", "POST"])
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()  # Zapisz użytkownika, aby otrzymać ID

            # Dodaj kod OTP i zapisz go w sesji
            otp_code = generate_otp_code()
            subject = 'Kod weryfikacyjny OTP'
            message = f'Twój kod weryfikacyjny OTP to: {otp_code}'
            from_email = 'noreply@semycolon.com'
            recipient_list = [form.cleaned_data['email']]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            request.session['otp_code'] = otp_code
            request.session['new_user_id'] = user.id  # Zapisz ID nowo utworzonego użytkownika

            return redirect("gameshop:otpaRegister")
    context = {'form': form}
    return render(request, 'gameshop/authenticate/register.html', context)
# Widok weryfikacji kodu OTP podczas rejestracji
@require_http_methods(["GET", "POST"])
def otpaRegister(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            stored_otp_code = request.session.get('otp_code')
            if otp_code == stored_otp_code:
                # Kod OTP jest poprawny
                del request.session['otp_code']  # Usuń kod OTP z sesji po weryfikacji

                user_id = request.session.get('new_user_id')
                if user_id:
                    user = User.objects.get(id=user_id)
                    user.email_verified = True
                    user.save()

                    messages.success(request, 'Konto zostało założone pomyślnie. Możesz się teraz zalogować.')
                    return redirect('gameshop:login')
                else:
                    messages.error(request, 'Wystąpił błąd podczas rejestracji. Spróbuj ponownie.')
            else:
                # Kod OTP jest niepoprawny
                messages.error(request, 'Podany kod OTP jest niepoprawny.')
    else:
        form = OTPVerificationForm()

    return render(request, 'gameshop/authenticate/otpaRegister.html', {'form': form})

# Widok gry
@require_GET
def game(request, slug):
    game = get_object_or_404(Game, slug=slug)
    return render(request, 'gameshop/game.html', {'game': game})
# Widok zakupu
@require_GET
def buy(request, slug):
    game = get_object_or_404(Game, slug=slug)
    code = get_random_string(length=16)
    return render(request, 'gameshop/buy.html', {'game': game, 'code': code})
# Widok logowania użytkownika
@require_http_methods(["GET", "POST"])
def userlogin(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                otp_code = generate_otp_code()
                print(otp_code)
                subject = 'Kod weryfikacyjny OTP'
                message = f'Twój kod weryfikacyjny OTP to: {otp_code}'
                from_email = 'noreply@semycolon.com'
                recipient_list = [user.email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                request.session['otp_code'] = otp_code

                return redirect('gameshop:otpaLogin')
            else:
                messages.info(request, 'Login lub hasło błędne')
    else:
        form = UserLoginForm()
    return render(request, 'gameshop/authenticate/login.html', {'form': form})

@require_GET
def userlogout(request):
    logout(request)
    return redirect('gameshop:index')
# Widok wylogowania użytkownika
@require_http_methods(["GET", "POST"])
def otpaLogin(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            stored_otp_code = request.session.get('otp_code')
            print(otp_code)
            print(stored_otp_code)
            if otp_code == stored_otp_code:
                # Kod OTP jest poprawny
                del request.session['otp_code']  # Usuń kod OTP z sesji po weryfikacji
                # Zaimplementuj dalsze działania po pomyślnej weryfikacji
                messages.success(request, 'Weryfikacja kodu OTP przebiegła pomyślnie.')
                return redirect('gameshop:index')
            else:
                # Kod OTP jest niepoprawny
                messages.error(request, 'Podany kod OTP jest niepoprawny.')
    else:
        form = OTPVerificationForm()

    return render(request, 'gameshop/authenticate/otpaLogin.html', {'form': form})

class GameshopApiCheck(APIView):
    # permisje - tu kazdy moze sprawdzic
    permission_classes = [permissions.AllowAny]

    # 0. taki endpoint, ze zwraca 200 kiedy serwer po prostu dziala
    def get(self, request, *args, **kwargs):
        return Response("API functional!", status=status.HTTP_200_OK)

class GameshopApiGamesView(APIView):
    # permisje - tu kazdy moze sprawdzic
    permission_classes = [permissions.AllowAny]

    # 1. wypisz wszystkie gry
    def get(self, request, *args, **kwargs):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GameshopApiCategoriesView(APIView):
    # permisje - tu kazdy moze sprawdzic
    permission_classes = [permissions.AllowAny]

    # 2. wypisz wszystkie kategorie
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GameshopApiDevelopersView(APIView):
    # permisje - tu kazdy moze sprawdzic
    permission_classes = [permissions.AllowAny]

    # 3. wypisz developerow
    def get(self, request, *args, **kwargs):
        developers = Developer.objects.all()
        serializer = DeveloperSerializer(developers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GameshopApiAddDeveloper(APIView):
    # standardowo permisje
    permission_classes = [permissions.IsAdminUser]

    # 4. dodawanie nowego developera
    def post(self, request, *args, **kwargs):
        serializer = DeveloperSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameshopApiManageDeveloper(APIView):
    # permisje - tylko admin
    permission_classes = [permissions.IsAdminUser]

    # funkcja pomocnicza, która zwraca obiekt z bazy po PK
    def get_object(self, pk):
        try:
            return Developer.objects.get(pk=pk)
        except Developer.DoesNotExist:
            raise Http404
    
    # 5. otrzymaj element o podanym id
    def get(self, request, pk, *args, **kwargs):
        developer = self.get_object(pk)
        serializer = DeveloperSerializer(developer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 6. aktualizacja elementu
    def put(self, request, pk, *args, **kwargs):
        developer = self.get_object(pk)
        serializer = DeveloperSerializer(developer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 7. Usuwanie elementu
    def delete(self, request, pk, *args, **kwargs):
        developer = self.get_object(pk)
        developer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class GameshopApiAddCategory(APIView):
    # standardowo permisje
    permission_classes = [permissions.IsAdminUser]

    # 8. dodawanie nowej kategorii
    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class GameshopApiManageCategory(APIView):
    # permisje - tylko admin
    permission_classes = [permissions.IsAdminUser]

    # funkcja pomocnicza, która zwraca obiekt z bazy po PK
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404
    
    # 9. otrzymaj element o podanym id
    def get(self, request, pk, *args, **kwargs):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 10. aktualizacja elementu
    def put(self, request, pk, *args, **kwargs):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 11. Usuwanie elementu
    def delete(self, request, pk, *args, **kwargs):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


