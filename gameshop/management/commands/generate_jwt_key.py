from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
'''TODO DALEJ NIE DZIALA XD'''
class Command(BaseCommand):
    help = "Generates pair of JWT keys for user manually"

    def add_arguments(self, parser):
        parser.add_argument("user", nargs="+", type=str)

    def handle(self, *args, **options):
        user = User.objects.filter(username=options["user"]).values_list("username", flat=True)
        refresh = RefreshToken.for_user(user)
        print(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }