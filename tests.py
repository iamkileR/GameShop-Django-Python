from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


class Hosttest(LiveServerTestCase):

    def testindex(self):
        """
        Testuje główną stronę (index) sklepu.
        Otwiera przeglądarkę Chrome, przechodzi do adresu strony głównej,
        oczekuje na załadowanie się strony, a następnie sprawdza, czy tytuł zawiera słowo "Sklep".
        """
        driver = webdriver.Chrome()

        driver.get('http://127.0.0.1:8000/')
        time.sleep(5)
        assert "Sklep" in driver.title


class LoginFormTest(LiveServerTestCase):

    def testform(self):
        """
        Testuje formularz logowania.
        Otwiera przeglądarkę Chrome, przechodzi do strony logowania,
        oczekuje na załadowanie się strony, wprowadza nazwę użytkownika i hasło,
        a następnie wysyła formularz.
        """
        driver = webdriver.Chrome()

        driver.get('http://127.0.0.1:8000/login/')
        time.sleep(3)
        user_name = driver.find_element(By.NAME, 'username')
        user_password = driver.find_element(By.NAME, 'password')
        submit = driver.find_element(By.ID, 'submit')

        user_name.send_keys('admin1')
        user_password.send_keys('admin')
        time.sleep(3)
        submit.send_keys(Keys.RETURN)

        #assert 'admin' in driver.page_source

class RegisterFormTest(LiveServerTestCase):

    def testregisterform(self):
        """
        Testuje formularz rejestracji.
        Otwiera przeglądarkę Chrome, przechodzi do strony rejestracji,
        oczekuje na załadowanie się strony, wprowadza dane rejestracyjne,
        a następnie wysyła formularz.
        """
        driver = webdriver.Chrome()

        driver.get('http://127.0.0.1:8000/register/')
        time.sleep(3)
        user_name = driver.find_element(By.NAME, 'username')
        user_password = driver.find_element(By.NAME, 'password1')
        user_password1 = driver.find_element(By.NAME, 'password2')
        user_email = driver.find_element(By.NAME, 'email')
        submit = driver.find_element(By.ID, 'submit')

        user_name.send_keys('testselenium')
        user_password.send_keys('qwerty12345')
        user_password1.send_keys('qwerty12345')
        user_email.send_keys('testselenium@onet.pl')
        time.sleep(3)
        submit.send_keys(Keys.RETURN)

class Regulamintest(LiveServerTestCase):

    def testregulamin(self):
        """
        Testuje stronę regulaminu sklepu.
        Otwiera przeglądarkę Chrome, przechodzi do strony regulaminu,
        oczekuje na załadowanie się strony, a następnie sprawdza, czy tytuł zawiera słowo "Regulamin sklepu".
        """
        driver = webdriver.Chrome()

        driver.get('http://127.0.0.1:8000/regulamin/')
        time.sleep(3)
        assert "Regulamin sklepu" in driver.title

class Productstest(LiveServerTestCase):

    def testproducts(self):
        """
        Testuje stronę z produktami.
        Otwiera przeglądarkę Chrome, przechodzi do strony z produktami,
        oczekuje na załadowanie się strony, a następnie sprawdza, czy tytuł zawiera słowo "Produkty".
        """
        driver = webdriver.Chrome()

        driver.get('http://127.0.0.1:8000/products/')
        time.sleep(3)
        assert "Produkty" in driver.title

class Pomoctest(LiveServerTestCase):

    def testpomoc(self):

        driver = webdriver.Chrome()
        """
        Testuje stronę pomocy.
        Otwiera przeglądarkę Chrome, przechodzi do strony pomocy,
        oczekuje na załadowanie się strony, a następnie sprawdza, czy tytuł zawiera słowo "Pomoc".
        """

        driver.get('http://127.0.0.1:8000/pomoc/')
        time.sleep(3)
        assert "Pomoc" in driver.title

class Gametest(LiveServerTestCase):

    def testgame(self):
        """
        Testuje stronę gry.
        Otwiera przeglądarkę Chrome, przechodzi do strony konkretnej gry,
        oczekuje na załadowanie się strony, a następnie sprawdza, czy tytuł zawiera słowo "Gry".
        """
        driver = webdriver.Chrome()

        driver.get('http://127.0.0.1:8000/game/the-witcher-3-wild-hunt/')
        time.sleep(3)
        assert "Gry" in driver.title

class AdminPagetest(LiveServerTestCase):
    def test_if_admin_panel_is_displayed(self):
        """
        Testuje wyświetlanie panelu administratora.
        Otwiera przeglądarkę Chrome, przechodzi do panelu administratora,
        oczekuje na załadowanie się strony, a następnie sprawdza, czy tytuł zawiera frazę "Log in | Django site admin".
        """
        driver = webdriver.Chrome()

        driver.get('http://127.0.0.1:8000/admin/')
        time.sleep(3)
        # header = driver.find_element(By.ID,'site-name').text
        # driver.assertEqual('Django administration', header)
        assert "Log in | Django site admin" in driver.title

    def test_login_admin_page(self):
        """
        Testuje logowanie do panelu administratora.
        Otwiera przeglądarkę Chrome, przechodzi do panelu administratora,
        oczekuje na załadowanie się strony, wprowadza nazwę użytkownika i hasło,
        a następnie wysyła formularz.
        """
        driver = webdriver.Chrome()

        driver.get('http://127.0.0.1:8000/admin/')
        time.sleep(3)
        user_name = driver.find_element(By.ID, 'id_username')
        user_password = driver.find_element(By.ID, 'id_password')
        submit = driver.find_element(By.XPATH, '//input[@type="submit"]')

        user_name.send_keys('admin1')
        user_password.send_keys('admin')
        # time.sleep(3)
        submit.send_keys(Keys.RETURN)
