from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        # Formularz rejestracji użytkownika, dziedziczy po klasie UserCreationForm
        # Zdefiniowane pola to 'username', 'email', 'password1' (hasło) i 'password2' (potwierdzenie hasła)


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    # Formularz logowania użytkownika
    # Zawiera pola 'username' (nazwa użytkownika) i 'password' (hasło)
class OTPVerificationForm(forms.Form):
    otp_code = forms.CharField(label='Kod weryfikacyjny', max_length=6)
    # Formularz weryfikacji kodu OTP
    # Zawiera pole 'otp_code' (kod weryfikacyjny) o maksymalnej długości 6 znaków