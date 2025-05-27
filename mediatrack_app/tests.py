from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from .forms import RegistroForm, LoginForm

User = get_user_model()

# Create your tests here.

class ModelTests(TestCase):

    def test_usuario_creation(self):
        """Tests that a custom user can be created with an email."""
        print("\n--- Test: Creación de Usuario Personalizado ---")
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        self.assertEqual(user.email, 'testuser@example.com')
        print(f"Usuario creado: {user.email}")
        self.assertEqual(user.username, 'testuser')
        print(f"Username: {user.username}")
        self.assertTrue(user.is_active)
        print("is_active: True")
        self.assertFalse(user.is_staff)
        print("is_staff: False")
        self.assertFalse(user.is_superuser)
        print("is_superuser: False")
        print("--- Test de Usuario Finalizado ---")
        
class FormTests(TestCase):

    def test_registro_form_valid_data(self):
        """Test RegistroForm with valid data."""
        print("\n--- Test: RegistroForm - Datos Válidos ---")
        form_data = {'username': 'newuser', 'email': 'newuser@example.com', 'password1': 'securepassword', 'password2': 'securepassword'}
        form = RegistroForm(data=form_data)
        self.assertTrue(form.is_valid())
        print("Formulario de Registro (datos válidos): is_valid() = True")
        print("--- Test de RegistroForm (Válido) Finalizado ---")

    def test_registro_form_invalid_data(self):
        """Test RegistroForm with invalid data (missing email or passwords)."""
        print("\n--- Test: RegistroForm - Datos Inválidos ---")
        form_data = {'username': 'anotheruser'}
        form = RegistroForm(data=form_data)
        self.assertFalse(form.is_valid())
        print("Formulario de Registro (datos inválidos): is_valid() = False")
        self.assertIn('email', form.errors.keys())
        self.assertIn('password1', form.errors.keys())
        self.assertIn('password2', form.errors.keys())
        print(f"Errores en formulario: {form.errors.keys()}")
        print("--- Test de RegistroForm (Inválido) Finalizado ---")

    def test_registro_form_passwords_mismatch(self):
        """Test RegistroForm with passwords that do not match."""
        print("\n--- Test: RegistroForm - Contraseñas No Coinciden ---")
        form_data = {'username': 'mismatchuser', 'email': 'mismatch@example.com', 'password1': 'pass1', 'password2': 'pass2'}
        form = RegistroForm(data=form_data)
        self.assertFalse(form.is_valid())
        print("Formulario de Registro (contraseñas no coinciden): is_valid() = False")
        self.assertIn('password2', form.errors.keys())
        print(f"Errores en formulario: {form.errors.keys()}")
        print("--- Test de RegistroForm (Contraseñas) Finalizado ---")

    def test_login_form_valid_data(self):
        """Test LoginForm with valid data."""
        print("\n--- Test: LoginForm - Datos Válidos ---")
        user = User.objects.create_user(username='loginuser', email='login@example.com', password='loginpassword')
        print(f"Usuario de prueba para Login creado: {user.username} ({user.email})")
        form_data = {'username': 'login@example.com', 'password': 'loginpassword'}
        form = LoginForm(data=form_data)
        
        is_valid = form.is_valid()
        print(f"Formulario de Login (datos válidos): is_valid() = {is_valid}")
        
        if not is_valid:
            print(f"Errores del formulario válido: {form.errors}")
            
        self.assertTrue(is_valid)
        user_authenticated = form.get_user()
        self.assertEqual(user_authenticated, user)
        print("Usuario autenticado correctamente.")
        print("--- Test de LoginForm (Válido) Finalizado ---")

    def test_login_form_invalid_data(self):
        """Test LoginForm with invalid data (wrong password)."""
        print("\n--- Test: LoginForm - Datos Inválidos ---")
        user = User.objects.create_user(username='invaliduser', email='invalid@example.com', password='correctpassword')
        print(f"Usuario de prueba para Login (inválido) creado: {user.username}")
        form_data = {'username': 'invalid@example.com', 'password': 'wrongpassword'}
        form = LoginForm(data=form_data)
        
        is_valid = form.is_valid()
        print(f"Formulario de Login (datos inválidos): is_valid() = {is_valid}")
        
        self.assertFalse(is_valid)
        self.assertTrue('__all__' in form.errors.keys() or 'username' in form.errors.keys())
        print(f"Errores en formulario: {form.errors.keys()}")

        user_authenticated = form.get_user()
        self.assertIsNone(user_authenticated)
        print("Usuario NO autenticado correctamente.")
        print("--- Test de LoginForm (Inválido) Finalizado ---")
    
class ViewTests(TestCase):

    def setUp(self):
        """Set up a client for view tests."""
        self.client = Client()
        # Create a user for authenticated tests
        self.user = User.objects.create_user(
            username='testuser_view',
            email='viewtest@example.com',
            password='viewpassword'
        )
        print("\n--- Setup: Cliente y Usuario de Prueba Creados para ViewTests ---")

    def test_registro_view_get(self):
        """Test the registration page GET request."""
        print("\n--- Test: Vista de Registro (GET) ---")
        response = self.client.get(reverse('registro'))
        print(f"GET /registro/ - Status Code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mediatrack_app/registro.html')
        print("Plantilla usada: mediatrack_app/registro.html")
        print("--- Test de Vista de Registro (GET) Finalizado ---")

    def test_registro_view_post_valid(self):
        """Test registration view with valid POST data."""
        print("\n--- Test: Vista de Registro (POST Válido) ---")
        user_count_before = User.objects.count()
        print(f"Usuarios antes del registro: {user_count_before}")
        form_data = {
            'username': 'newuser_view',
            'email': 'newviewuser@example.com',
            'password1': 'secureviewpassword',
            'password2': 'secureviewpassword',
        }
        response = self.client.post(reverse('registro'), form_data)
        print(f"POST /registro/ (Válido) - Status Code: {response.status_code}")
        user_count_after = User.objects.count()
        print(f"Usuarios después del registro: {user_count_after}")

        self.assertEqual(user_count_after, user_count_before + 1)
        print("Nuevo usuario creado exitosamente.")
        # Verificar redirección al dashboard después del registro exitoso
        self.assertRedirects(response, reverse('dashboard'))
        print("Redirigido a: /dashboard/")
        # Verificar que el usuario recién registrado está autenticado (opcional, pero útil)
        # Nota: Client.post no autentica automáticamente en la sesión de prueba
        # Si quieres verificar autenticación, necesitarías simular el login después del registro
        # o usar TestCase.client.login() si la vista lo maneja
        print("--- Test de Vista de Registro (POST Válido) Finalizado ---")

    def test_registro_view_post_invalid(self):
        """Test registration view with invalid POST data."""
        print("\n--- Test: Vista de Registro (POST Inválido) ---")
        user_count_before = User.objects.count()
        print(f"Usuarios antes del registro: {user_count_before}")
        form_data = {
            'username': 'invaliduser_view',
            'email': 'invalid-email', # Email inválido
            'password1': 'pass',
            'password2': 'word', # Contraseñas no coinciden
        }
        response = self.client.post(reverse('registro'), form_data)
        print(f"POST /registro/ (Inválido) - Status Code: {response.status_code}")
        user_count_after = User.objects.count()
        print(f"Usuarios después del registro: {user_count_after}")

        self.assertEqual(user_count_after, user_count_before) # No se debe crear nuevo usuario
        print("No se creó ningún nuevo usuario.")
        self.assertEqual(response.status_code, 200) # Debe volver a mostrar el formulario
        print("Se volvió a mostrar el formulario de registro.")
        self.assertTemplateUsed(response, 'mediatrack_app/registro.html')
        print("Plantilla usada: mediatrack_app/registro.html")
        # Verificar que los errores del formulario están en el contexto
        self.assertIsNotNone(response.context['form'].errors)
        print("Errores del formulario presentes en el contexto.")
        print("--- Test de Vista de Registro (POST Inválido) Finalizado ---")

    def test_login_view_get(self):
        """Test the login page GET request."""
        print("\n--- Test: Vista de Login (GET) ---")
        response = self.client.get(reverse('login'))
        print(f"GET /login/ - Status Code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mediatrack_app/login.html')
        print("Plantilla usada: mediatrack_app/login.html")
        print("--- Test de Vista de Login (GET) Finalizado ---")

    def test_login_view_post_valid(self):
        """Test login view with valid POST data."""
        print("\n--- Test: Vista de Login (POST Válido) ---")
        # El usuario de prueba ya fue creado en setUp
        form_data = {'username': self.user.email, 'password': 'viewpassword'}
        response = self.client.post(reverse('login'), form_data)
        print(f"POST /login/ (Válido) - Status Code: {response.status_code}")

        # Verificar redirección al dashboard después del login exitoso
        self.assertRedirects(response, reverse('dashboard'))
        print("Redirigido a: /dashboard/")
        # Verificar que el usuario está autenticado en la sesión del cliente de prueba
        self.assertTrue('_auth_user_id' in self.client.session)
        print("Usuario autenticado en la sesión.")
        print("--- Test de Vista de Login (POST Válido) Finalizado ---")

    def test_login_view_post_invalid(self):
        """Test login view with invalid POST data."""
        print("\n--- Test: Vista de Login (POST Inválido) ---")
        # No necesitamos crear un usuario, solo intentar loggear con credenciales incorrectas
        form_data = {'username': 'nonexistent@example.com', 'password': 'wrongpassword'}
        response = self.client.post(reverse('login'), form_data)
        print(f"POST /login/ (Inválido) - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 200) # Debe volver a mostrar el formulario
        print("Se volvió a mostrar el formulario de login.")
        self.assertTemplateUsed(response, 'mediatrack_app/login.html')
        print("Plantilla usada: mediatrack_app/login.html")
        # Verificar que los errores del formulario están en el contexto
        self.assertIsNotNone(response.context['form'].errors)
        print("Errores del formulario presentes en el contexto.")
        # Verificar que el usuario NO está autenticado
        self.assertFalse('_auth_user_id' in self.client.session)
        print("Usuario NO autenticado en la sesión.")
        print("--- Test de Vista de Login (POST Inválido) Finalizado ---")

    def test_logout_view(self):
        """Test the logout view."""
        print("\n--- Test: Vista de Logout ---")
        # Primero, loggeamos al usuario de prueba para que haya una sesión activa
        self.client.login(username=self.user.email, password='viewpassword')
        print("Usuario de prueba loggeado para test de logout.")
        self.assertTrue('_auth_user_id' in self.client.session) # Verificar que está loggeado inicialmente

        response = self.client.get(reverse('logout'))
        print(f"GET /logout/ - Status Code: {response.status_code}")

        # Verificar redirección a la página de login después del logout
        self.assertRedirects(response, reverse('login'))
        print("Redirigido a: /login/")
        # Verificar que el usuario ya NO está autenticado en la sesión
        self.assertFalse('_auth_user_id' in self.client.session)
        print("Usuario desloggeado de la sesión.")
        print("--- Test de Vista de Logout Finalizado ---")

    def test_dashboard_view_authenticated(self):
        """Test the dashboard view for an authenticated user."""
        print("\n--- Test: Vista de Dashboard (Autenticado) ---")
        # Log in the test user created in setUp
        self.client.login(username=self.user.email, password='viewpassword')
        print("Usuario de prueba loggeado para test de dashboard.")

        response = self.client.get(reverse('dashboard'))
        print(f"GET /dashboard/ (Autenticado) - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 200)
        print("Status Code: 200 (OK)")
        self.assertTemplateUsed(response, 'mediatrack_app/dashboard.html')
        print("Plantilla usada: mediatrack_app/dashboard.html")
        # Optionally, check for some content that should be on the dashboard
        # self.assertContains(response, self.user.username)
        print("--- Test de Vista de Dashboard (Autenticado) Finalizado ---")

    def test_dashboard_view_unauthenticated(self):
        """Test the dashboard view for an unauthenticated user."""
        print("\n--- Test: Vista de Dashboard (No Autenticado) ---")
        # Ensure the client is not logged in (it is by default, but good practice)
        self.client.logout()
        print("Asegurando que el cliente no esté loggeado.")

        response = self.client.get(reverse('dashboard'))
        print(f"GET /dashboard/ (No Autenticado) - Status Code: {response.status_code}")

        # Views protected with @login_required redirect to the login URL
        # A 302 status code indicates a redirection.
        self.assertEqual(response.status_code, 302)
        print("Status Code: 302 (Redirección)")
        # Check that the redirection is to the login page
        # The 'next' query parameter is added automatically by @login_required
        self.assertRedirects(response, f'/accounts/login/?next={reverse('dashboard')}', fetch_redirect_response=False)
        print(f"Redirigido a: /accounts/login/?next={reverse('dashboard')}")
        print("--- Test de Vista de Dashboard (No Autenticado) Finalizado ---")