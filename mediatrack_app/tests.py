from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Media,SeguimientoEpisodio
from django.urls import reverse
from django.utils import timezone
from .forms import RegistroForm, LoginForm, MediaForm

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
    
    def test_media_creation(self):
        """Tests that a Media object can be created."""
        print("\n--- Test: Creación de Objeto Media ---")
        user = User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='testpassword123'
        )
        print(f"Usuario de prueba para Media: {user.username}")
        media = Media.objects.create(
            usuario=user,
            nombre='Test Movie',
            tipo='pelicula',
            duracion_minutos=120,
            imagen_url='http://example.com/image.jpg'
        )
        print(f"Objeto Media creado: {media.nombre} ({media.tipo})")
        self.assertEqual(media.nombre, 'Test Movie')
        self.assertEqual(media.tipo, 'pelicula')
        self.assertEqual(media.duracion_minutos, 120)
        print(f"Duración (minutos): {media.duracion_minutos}")
        self.assertEqual(media.usuario, user)
        print(f"Asignado a usuario: {media.usuario.username}")
        print("--- Test de Media Finalizado ---")
    
    def test_seguimiento_episodio_creation(self):
        """Tests that a SeguimientoEpisodio object can be created."""        
        print("\n--- Test: Creación de Objeto SeguimientoEpisodio ---")
        user = User.objects.create_user(
            username='testuser3',
            email='testuser3@example.com',
            password='testpassword123'
        )
        print(f"Usuario de prueba para SeguimientoEpisodio: {user.username}")
        media = Media.objects.create(
            usuario=user,
            nombre='Test Series',
            tipo='serie',
            total_capitulos=10
        )
        print(f"Objeto Media asociado: {media.nombre}")
        seguimiento = SeguimientoEpisodio.objects.create(
            media=media,
            usuario=user,
            numero_episodio=1,
            visto=False
        )
        print(f"Objeto SeguimientoEpisodio creado para Episodio {seguimiento.numero_episodio}")
        self.assertEqual(seguimiento.media, media)
        self.assertEqual(seguimiento.usuario, user)
        self.assertEqual(seguimiento.numero_episodio, 1)
        self.assertFalse(seguimiento.visto)
        print(f"Estado 'visto': {seguimiento.visto}")
        print("--- Test de SeguimientoEpisodio Finalizado ---")
        
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
        
    def test_media_form_pelicula_valid_data(self):
        """Test MediaForm with valid data for a movie."""
        print("\n--- Test: MediaForm - Película (Datos Válidos) ---")
        form_data = {
            'nombre': 'Valid Movie',
            'tipo': 'pelicula',
            'duracion_hh_mm': '02:30',
            'imagen_url': 'http://example.com/movie.jpg'
        }
        form = MediaForm(data=form_data)
        is_valid = form.is_valid()
        print(f"Formulario de Media (Película Válida): is_valid() = {is_valid}")
        if not is_valid:
            print(f"Errores: {form.errors}")
        self.assertTrue(is_valid)
        # Verificar que duracion_hh_mm se convierte correctamente a duracion_minutos
        self.assertEqual(form.cleaned_data['duracion_minutos'], 150)
        print(f"Duración convertida a minutos: {form.cleaned_data['duracion_minutos']}")
        print("--- Test de MediaForm (Película Válida) Finalizado ---")

    def test_media_form_serie_valid_data(self):
        """Test MediaForm with valid data for a series."""
        print("\n--- Test: MediaForm - Serie (Datos Válidos) ---")
        form_data = {
            'nombre': 'Valid Series',
            'tipo': 'serie',
            'total_capitulos': 24,
            'imagen_url': 'http://example.com/series.jpg'
        }
        form = MediaForm(data=form_data)
        is_valid = form.is_valid()
        print(f"Formulario de Media (Serie Válida): is_valid() = {is_valid}")
        if not is_valid:
            print(f"Errores: {form.errors}")
        self.assertTrue(is_valid)
        # Verificar que duracion_minutos se limpia para series
        self.assertIsNone(form.cleaned_data.get('duracion_minutos'))
        print("duracion_minutos limpiado para serie.")
        print("--- Test de MediaForm (Serie Válida) Finalizado ---")

    def test_media_form_pelicula_invalid_duration(self):
        """Test MediaForm with invalid duration format for a movie."""
        print("\n--- Test: MediaForm - Película (Duración Inválida) ---")
        form_data = {
            'nombre': 'Invalid Movie',
            'tipo': 'pelicula',
            'duracion_hh_mm': 'abc',
            'imagen_url': 'http://example.com/movie.jpg'
        }
        form = MediaForm(data=form_data)
        is_valid = form.is_valid()
        print(f"Formulario de Media (Película Duración Inválida): is_valid() = {is_valid}")
        self.assertFalse(is_valid)
        self.assertIn('duracion_hh_mm', form.errors.keys())
        print(f"Errores en duracion_hh_mm: {form.errors.get('duracion_hh_mm')}")
        print("--- Test de MediaForm (Película Duración Inválida) Finalizado ---")

    def test_media_form_serie_with_duration(self):
        """Test MediaForm for a series submitted with duration data (should be ignored)."""
        print("\n--- Test: MediaForm - Serie con Duración (Ignorada) ---")
        form_data = {
            'nombre': 'Series with Duration',
            'tipo': 'serie',
            'total_capitulos': 10,
            'duracion_hh_mm': '01:00', # Debería ser ignorado
            'duracion_minutos': 60, # Debería ser ignorado
            'imagen_url': 'http://example.com/series.jpg'
        }
        form = MediaForm(data=form_data)
        is_valid = form.is_valid()
        print(f"Formulario de Media (Serie con Duración): is_valid() = {is_valid}")
        self.assertTrue(is_valid)
        # Verificar que duracion_minutos se limpia para series
        self.assertIsNone(form.cleaned_data.get('duracion_minutos'))
        self.assertIsNone(form.cleaned_data.get('duracion_hh_mm'))
        print("Campos de duración limpiados para serie.")
        print("--- Test de MediaForm (Serie con Duración) Finalizado ---")
    
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

    def test_agregar_medio_view_get(self):
        """Test the add media page GET request."""
        print("\n--- Test: Vista de Agregar Medio (GET) ---")
        self.client.login(username=self.user.email, password='viewpassword')
        print("Usuario de prueba loggeado para test de agregar medio.")

        response = self.client.get(reverse('agregar_medio'))
        print(f"GET /medio/agregar/ - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 200)
        print("Status Code: 200 (OK)")
        self.assertTemplateUsed(response, 'mediatrack_app/medio_form.html')
        print("Plantilla usada: mediatrack_app/medio_form.html")
        print("--- Test de Vista de Agregar Medio (GET) Finalizado ---")

    def test_agregar_medio_view_post_pelicula(self):
        """Test adding a movie with valid data."""
        print("\n--- Test: Vista de Agregar Medio - Película (POST) ---")
        self.client.login(username=self.user.email, password='viewpassword')
        print("Usuario de prueba loggeado para test de agregar película.")

        form_data = {
            'nombre': 'Test Movie',
            'tipo': 'pelicula',
            'duracion_hh_mm': '02:30',
            'imagen_url': 'http://example.com/movie.jpg'
        }
        response = self.client.post(reverse('agregar_medio'), form_data)
        print(f"POST /medio/agregar/ (Película) - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 302)  # Redirección después de éxito
        print("Status Code: 302 (Redirección)")
        self.assertRedirects(response, reverse('dashboard'))
        print("Redirigido a: /dashboard/")

        # Verificar que el medio se creó correctamente
        medio = Media.objects.get(nombre='Test Movie', usuario=self.user)
        self.assertEqual(medio.tipo, 'pelicula')
        self.assertEqual(medio.duracion_minutos, 150)  # 2:30 = 150 minutos
        print(f"Película creada: {medio.nombre} ({medio.tipo})")
        print(f"Duración: {medio.duracion_minutos} minutos")
        print("--- Test de Vista de Agregar Medio (Película) Finalizado ---")

    def test_agregar_medio_view_post_serie(self):
        """Test adding a series with valid data."""
        print("\n--- Test: Vista de Agregar Medio - Serie (POST) ---")
        self.client.login(username=self.user.email, password='viewpassword')
        print("Usuario de prueba loggeado para test de agregar serie.")

        form_data = {
            'nombre': 'Test Series',
            'tipo': 'serie',
            'total_capitulos': 10,
            'imagen_url': 'http://example.com/series.jpg'
        }
        response = self.client.post(reverse('agregar_medio'), form_data)
        print(f"POST /medio/agregar/ (Serie) - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 302)  # Redirección después de éxito
        print("Status Code: 302 (Redirección)")
        self.assertRedirects(response, reverse('dashboard'))
        print("Redirigido a: /dashboard/")

        # Verificar que el medio se creó correctamente
        medio = Media.objects.get(nombre='Test Series', usuario=self.user)
        self.assertEqual(medio.tipo, 'serie')
        self.assertEqual(medio.total_capitulos, 10)
        print(f"Serie creada: {medio.nombre} ({medio.tipo})")
        print(f"Total capítulos: {medio.total_capitulos}")
        print("--- Test de Vista de Agregar Medio (Serie) Finalizado ---")

    def test_agregar_medio_view_post_invalid(self):
        """Test adding media with invalid data."""
        print("\n--- Test: Vista de Agregar Medio (POST Inválido) ---")
        self.client.login(username=self.user.email, password='viewpassword')
        print("Usuario de prueba loggeado para test de agregar medio inválido.")

        form_data = {
            'nombre': '',  # Nombre vacío
            'tipo': 'pelicula',
            'duracion_hh_mm': 'invalid',  # Duración inválida
            'imagen_url': 'not-a-url'  # URL inválida
        }
        response = self.client.post(reverse('agregar_medio'), form_data)
        print(f"POST /medio/agregar/ (Inválido) - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 200)  # Vuelve al formulario
        print("Status Code: 200 (OK)")
        self.assertTemplateUsed(response, 'mediatrack_app/medio_form.html')
        print("Plantilla usada: mediatrack_app/medio_form.html")
        self.assertIsNotNone(response.context['form'].errors)
        print("Errores del formulario presentes en el contexto.")
        print("--- Test de Vista de Agregar Medio (POST Inválido) Finalizado ---")

    def test_agregar_medio_view_unauthenticated(self):
        """Test adding media when not authenticated."""
        print("\n--- Test: Vista de Agregar Medio (No Autenticado) ---")
        self.client.logout()
        print("Asegurando que el cliente no esté loggeado.")

        response = self.client.get(reverse('agregar_medio'))
        print(f"GET /medio/agregar/ (No Autenticado) - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 302)
        print("Status Code: 302 (Redirección)")
        self.assertRedirects(response, f'/accounts/login/?next={reverse('agregar_medio')}', fetch_redirect_response=False)
        print(f"Redirigido a: /accounts/login/?next={reverse('agregar_medio')}")
        print("--- Test de Vista de Agregar Medio (No Autenticado) Finalizado ---")

    def test_editar_medio_view_get(self):
        """Test the edit media page GET request."""
        print("\n--- Test: Vista de Editar Medio (GET) ---")
        self.client.login(username=self.user.email, password='viewpassword')
        print("Usuario de prueba loggeado para test de editar medio.")

        # Crear un medio de prueba
        medio = Media.objects.create(
            usuario=self.user,
            nombre='Test Media',
            tipo='pelicula',
            duracion_minutos=120,
            imagen_url='http://example.com/image.jpg'
        )
        print(f"Medio de prueba creado: {medio.nombre}")

        response = self.client.get(reverse('editar_medio', kwargs={'pk': medio.pk}))
        print(f"GET /medio/{medio.pk}/editar/ - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 200)
        print("Status Code: 200 (OK)")
        self.assertTemplateUsed(response, 'mediatrack_app/medio_form.html')
        print("Plantilla usada: mediatrack_app/medio_form.html")
        print("--- Test de Vista de Editar Medio (GET) Finalizado ---")

    def test_editar_medio_view_post(self):
        """Test editing media with valid data."""
        print("\n--- Test: Vista de Editar Medio (POST) ---")
        self.client.login(username=self.user.email, password='viewpassword')
        print("Usuario de prueba loggeado para test de editar medio.")

        # Crear un medio de prueba
        medio = Media.objects.create(
            usuario=self.user,
            nombre='Original Name',
            tipo='pelicula',
            duracion_minutos=120,
            imagen_url='http://example.com/image.jpg'
        )
        print(f"Medio de prueba creado: {medio.nombre}")

        form_data = {
            'nombre': 'Updated Name',
            'tipo': 'pelicula',
            'duracion_hh_mm': '01:45',
            'imagen_url': 'http://example.com/new-image.jpg'
        }
        response = self.client.post(reverse('editar_medio', kwargs={'pk': medio.pk}), form_data)
        print(f"POST /medio/{medio.pk}/editar/ - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 302)  # Redirección después de éxito
        print("Status Code: 302 (Redirección)")
        self.assertRedirects(response, reverse('dashboard'))
        print("Redirigido a: /dashboard/")

        # Verificar que el medio se actualizó correctamente
        medio.refresh_from_db()
        self.assertEqual(medio.nombre, 'Updated Name')
        self.assertEqual(medio.duracion_minutos, 105)  # 1:45 = 105 minutos
        self.assertEqual(medio.imagen_url, 'http://example.com/new-image.jpg')
        print(f"Medio actualizado: {medio.nombre}")
        print(f"Nueva duración: {medio.duracion_minutos} minutos")
        print("--- Test de Vista de Editar Medio (POST) Finalizado ---")

    def test_editar_medio_view_post_invalid(self):
        """Test editing media with invalid data."""
        print("\n--- Test: Vista de Editar Medio (POST Inválido) ---")
        self.client.login(username=self.user.email, password='viewpassword')
        print("Usuario de prueba loggeado para test de editar medio inválido.")

        # Crear un medio de prueba
        medio = Media.objects.create(
            usuario=self.user,
            nombre='Test Media',
            tipo='pelicula',
            duracion_minutos=120,
            imagen_url='http://example.com/image.jpg'
        )
        print(f"Medio de prueba creado: {medio.nombre}")

        form_data = {
            'nombre': '',  # Nombre vacío
            'tipo': 'pelicula',
            'duracion_hh_mm': 'invalid',  # Duración inválida
            'imagen_url': 'not-a-url'  # URL inválida
        }
        response = self.client.post(reverse('editar_medio', kwargs={'pk': medio.pk}), form_data)
        print(f"POST /medio/{medio.pk}/editar/ (Inválido) - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 200)  # Vuelve al formulario
        print("Status Code: 200 (OK)")
        self.assertTemplateUsed(response, 'mediatrack_app/medio_form.html')
        print("Plantilla usada: mediatrack_app/medio_form.html")
        self.assertIsNotNone(response.context['form'].errors)
        print("Errores del formulario presentes en el contexto.")
        print("--- Test de Vista de Editar Medio (POST Inválido) Finalizado ---")

    def test_editar_medio_view_unauthenticated(self):
        """Test editing media when not authenticated."""
        print("\n--- Test: Vista de Editar Medio (No Autenticado) ---")
        self.client.logout()
        print("Asegurando que el cliente no esté loggeado.")

        # Crear un medio de prueba
        medio = Media.objects.create(
            usuario=self.user,
            nombre='Test Media',
            tipo='pelicula',
            duracion_minutos=120,
            imagen_url='http://example.com/image.jpg'
        )
        print(f"Medio de prueba creado: {medio.nombre}")

        response = self.client.get(reverse('editar_medio', kwargs={'pk': medio.pk}))
        print(f"GET /medio/{medio.pk}/editar/ (No Autenticado) - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 302)
        print("Status Code: 302 (Redirección)")
        self.assertRedirects(response, f'/accounts/login/?next={reverse('editar_medio', kwargs={'pk': medio.pk})}', fetch_redirect_response=False)
        print(f"Redirigido a: /accounts/login/?next={reverse('editar_medio', kwargs={'pk': medio.pk})}")
        print("--- Test de Vista de Editar Medio (No Autenticado) Finalizado ---")

    def test_editar_medio_view_wrong_user(self):
        """Test editing media that belongs to another user."""
        print("\n--- Test: Vista de Editar Medio (Usuario Incorrecto) ---")
        self.client.login(username=self.user.email, password='viewpassword')
        print("Usuario de prueba loggeado para test de editar medio de otro usuario.")

        # Crear otro usuario
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpassword'
        )
        print(f"Otro usuario creado: {other_user.username}")

        # Crear un medio perteneciente al otro usuario
        medio = Media.objects.create(
            usuario=other_user,
            nombre='Other User Media',
            tipo='pelicula',
            duracion_minutos=120,
            imagen_url='http://example.com/image.jpg'
        )
        print(f"Medio de otro usuario creado: {medio.nombre}")

        response = self.client.get(reverse('editar_medio', kwargs={'pk': medio.pk}))
        print(f"GET /medio/{medio.pk}/editar/ (Usuario Incorrecto) - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 404)  # No encontrado
        print("Status Code: 404 (No Encontrado)")
        print("--- Test de Vista de Editar Medio (Usuario Incorrecto) Finalizado ---")

    def test_eliminar_medio_view(self):
        """Test deleting media."""
        print("\n--- Test: Vista de Eliminar Medio ---")
        self.client.login(username=self.user.email, password='viewpassword')
        print("Usuario de prueba loggeado para test de eliminar medio.")

        # Crear un medio de prueba
        medio = Media.objects.create(
            usuario=self.user,
            nombre='Test Media',
            tipo='pelicula',
            duracion_minutos=120,
            imagen_url='http://example.com/image.jpg'
        )
        print(f"Medio de prueba creado: {medio.nombre}")

        response = self.client.post(reverse('eliminar_medio', kwargs={'pk': medio.pk}))
        print(f"POST /medio/{medio.pk}/eliminar/ - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 302)  # Redirección después de éxito
        print("Status Code: 302 (Redirección)")
        self.assertRedirects(response, reverse('dashboard'))
        print("Redirigido a: /dashboard/")

        # Verificar que el medio fue eliminado
        with self.assertRaises(Media.DoesNotExist):
            Media.objects.get(pk=medio.pk)
        print("Medio eliminado correctamente.")
        print("--- Test de Vista de Eliminar Medio Finalizado ---")

    def test_eliminar_medio_view_unauthenticated(self):
        """Test deleting media when not authenticated."""
        print("\n--- Test: Vista de Eliminar Medio (No Autenticado) ---")
        self.client.logout()
        print("Asegurando que el cliente no esté loggeado.")

        # Crear un medio de prueba
        medio = Media.objects.create(
            usuario=self.user,
            nombre='Test Media',
            tipo='pelicula',
            duracion_minutos=120,
            imagen_url='http://example.com/image.jpg'
        )
        print(f"Medio de prueba creado: {medio.nombre}")

        response = self.client.post(reverse('eliminar_medio', kwargs={'pk': medio.pk}))
        print(f"POST /medio/{medio.pk}/eliminar/ (No Autenticado) - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 302)
        print("Status Code: 302 (Redirección)")
        self.assertRedirects(response, f'/accounts/login/?next={reverse('eliminar_medio', kwargs={'pk': medio.pk})}', fetch_redirect_response=False)
        print(f"Redirigido a: /accounts/login/?next={reverse('eliminar_medio', kwargs={'pk': medio.pk})}")
        print("--- Test de Vista de Eliminar Medio (No Autenticado) Finalizado ---")

    def test_eliminar_medio_view_wrong_user(self):
        """Test deleting media that belongs to another user."""
        print("\n--- Test: Vista de Eliminar Medio (Usuario Incorrecto) ---")
        self.client.login(username=self.user.email, password='viewpassword')
        print("Usuario de prueba loggeado para test de eliminar medio de otro usuario.")

        # Crear otro usuario
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpassword'
        )
        print(f"Otro usuario creado: {other_user.username}")

        # Crear un medio perteneciente al otro usuario
        medio = Media.objects.create(
            usuario=other_user,
            nombre='Other User Media',
            tipo='pelicula',
            duracion_minutos=120,
            imagen_url='http://example.com/image.jpg'
        )
        print(f"Medio de otro usuario creado: {medio.nombre}")

        response = self.client.post(reverse('eliminar_medio', kwargs={'pk': medio.pk}))
        print(f"POST /medio/{medio.pk}/eliminar/ (Usuario Incorrecto) - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 404)  # No encontrado
        print("Status Code: 404 (No Encontrado)")
        print("--- Test de Vista de Eliminar Medio (Usuario Incorrecto) Finalizado ---")
    
    def test_toggle_visto_view(self):
        """Test toggling media watched status."""
        print("\n--- Test: Vista de Toggle Visto ---")
        self.client.login(username=self.user.email, password='viewpassword')
        print("Usuario de prueba loggeado para test de toggle visto.")

        # Crear un medio de prueba
        medio = Media.objects.create(
            usuario=self.user,
            nombre='Test Media',
            tipo='pelicula',
            duracion_minutos=120,
            imagen_url='http://example.com/image.jpg',
            visto=False
        )
        print(f"Medio de prueba creado: {medio.nombre} (visto=False)")

        # Primera llamada: marcar como visto
        response = self.client.post(reverse('toggle_visto', kwargs={'medio_pk': medio.pk}))
        print(f"POST /medio/{medio.pk}/toggle_visto/ (Marcar como visto) - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 302)  # Redirección después de éxito
        print("Status Code: 302 (Redirección)")
        self.assertRedirects(response, reverse('dashboard'))
        print("Redirigido a: /dashboard/")

        # Verificar que el medio se marcó como visto
        medio.refresh_from_db()
        self.assertTrue(medio.visto)
        print(f"Medio marcado como visto: {medio.visto}")

        # Segunda llamada: marcar como no visto
        response = self.client.post(reverse('toggle_visto', kwargs={'medio_pk': medio.pk}))
        print(f"POST /medio/{medio.pk}/toggle_visto/ (Marcar como no visto) - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 302)
        print("Status Code: 302 (Redirección)")
        self.assertRedirects(response, reverse('dashboard'))
        print("Redirigido a: /dashboard/")

        # Verificar que el medio se marcó como no visto
        medio.refresh_from_db()
        self.assertFalse(medio.visto)
        print(f"Medio marcado como no visto: {medio.visto}")
        print("--- Test de Vista de Toggle Visto Finalizado ---")

    def test_toggle_visto_view_unauthenticated(self):
        """Test toggling media watched status when not authenticated."""
        print("\n--- Test: Vista de Toggle Visto (No Autenticado) ---")
        self.client.logout()
        print("Asegurando que el cliente no esté loggeado.")

        # Crear un medio de prueba
        medio = Media.objects.create(
            usuario=self.user,
            nombre='Test Media',
            tipo='pelicula',
            duracion_minutos=120,
            imagen_url='http://example.com/image.jpg',
            visto=False
        )
        print(f"Medio de prueba creado: {medio.nombre}")

        response = self.client.post(reverse('toggle_visto', kwargs={'medio_pk': medio.pk}))
        print(f"POST /medio/{medio.pk}/toggle_visto/ (No Autenticado) - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 302)
        print("Status Code: 302 (Redirección)")
        self.assertRedirects(response, f'/accounts/login/?next={reverse('toggle_visto', kwargs={'medio_pk': medio.pk})}', fetch_redirect_response=False)
        print(f"Redirigido a: /accounts/login/?next={reverse('toggle_visto', kwargs={'medio_pk': medio.pk})}")
        print("--- Test de Vista de Toggle Visto (No Autenticado) Finalizado ---")

    def test_toggle_visto_view_wrong_user(self):
        """Test toggling media watched status that belongs to another user."""
        print("\n--- Test: Vista de Toggle Visto (Usuario Incorrecto) ---")
        self.client.login(username=self.user.email, password='viewpassword')
        print("Usuario de prueba loggeado para test de toggle visto de otro usuario.")

        # Crear otro usuario
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpassword'
        )
        print(f"Otro usuario creado: {other_user.username}")

        # Crear un medio perteneciente al otro usuario
        medio = Media.objects.create(
            usuario=other_user,
            nombre='Other User Media',
            tipo='pelicula',
            duracion_minutos=120,
            imagen_url='http://example.com/image.jpg',
            visto=False
        )
        print(f"Medio de otro usuario creado: {medio.nombre}")

        response = self.client.post(reverse('toggle_visto', kwargs={'medio_pk': medio.pk}))
        print(f"POST /medio/{medio.pk}/toggle_visto/ (Usuario Incorrecto) - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 404)  # No encontrado
        print("Status Code: 404 (No Encontrado)")
        print("--- Test de Vista de Toggle Visto (Usuario Incorrecto) Finalizado ---")

    def test_detalle_serie_anime_view_authenticated(self):
        """Test the series/anime detail view for an authenticated user."""
        print("\n--- Test: Vista de Detalle Serie/Anime (Autenticado) ---")
        self.client.login(username=self.user.email, password='viewpassword')
        print("Usuario de prueba loggeado para test de detalle serie/anime.")

        # Crear un medio de prueba tipo serie/anime
        medio = Media.objects.create(
            usuario=self.user,
            nombre='Test Series',
            tipo='serie',
            total_capitulos=5
        )
        print(f"Medio de prueba (Serie) creado: {medio.nombre} con {medio.total_capitulos} capítulos")

        # Crear algunos seguimientos de episodios
        for i in range(1, medio.total_capitulos + 1):
            SeguimientoEpisodio.objects.create(
                media=medio,
                usuario=self.user,
                numero_episodio=i,
                visto=(i % 2 == 0) # Marcar algunos como vistos
            )
        print(f"Seguimientos de episodios creados para {medio.nombre}")

        response = self.client.get(reverse('detalle_serie_anime', kwargs={'medio_pk': medio.pk}))
        print(f"GET /serie_anime/{medio.pk}/detalle/ - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 200)
        print("Status Code: 200 (OK)")
        self.assertTemplateUsed(response, 'mediatrack_app/detalle_serie_anime.html')
        print("Plantilla usada: mediatrack_app/detalle_serie_anime.html")

        # Verificar que el medio y los episodios están en el contexto
        self.assertEqual(response.context['medio'], medio)
        print(f"Medio {medio.nombre} encontrado en contexto.")
        self.assertEqual(len(response.context['episodios_seguimiento']), medio.total_capitulos)
        print(f"{len(response.context['episodios_seguimiento'])} episodios de seguimiento encontrados en contexto.")

        print("--- Test de Vista de Detalle Serie/Anime (Autenticado) Finalizado ---")

    def test_detalle_serie_anime_view_unauthenticated(self):
        """Test the series/anime detail view for an unauthenticated user."""
        print("\n--- Test: Vista de Detalle Serie/Anime (No Autenticado) ---")
        self.client.logout()
        print("Asegurando que el cliente no esté loggeado.")

        # Crear un medio de prueba (no importa el usuario ya que no estará autenticado)
        medio = Media.objects.create(
            usuario=self.user,
            nombre='Test Anime',
            tipo='anime',
            total_capitulos=12
        )
        print(f"Medio de prueba (Anime) creado: {medio.nombre}")

        response = self.client.get(reverse('detalle_serie_anime', kwargs={'medio_pk': medio.pk}))
        print(f"GET /serie_anime/{medio.pk}/detalle/ (No Autenticado) - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 302)
        print("Status Code: 302 (Redirección)")
        self.assertRedirects(response, f'/accounts/login/?next={reverse('detalle_serie_anime', kwargs={'medio_pk': medio.pk})}', fetch_redirect_response=False)
        print(f"Redirigido a: /accounts/login/?next={reverse('detalle_serie_anime', kwargs={'medio_pk': medio.pk})}")
        print("--- Test de Vista de Detalle Serie/Anime (No Autenticado) Finalizado ---")

    def test_detalle_serie_anime_view_wrong_user(self):
        """Test accessing series/anime detail that belongs to another user."""
        print("\n--- Test: Vista de Detalle Serie/Anime (Usuario Incorrecto) ---")
        self.client.login(username=self.user.email, password='viewpassword')
        print("Usuario de prueba loggeado para test de detalle de otro usuario.")

        # Crear otro usuario
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpassword'
        )
        print(f"Otro usuario creado: {other_user.username}")

        # Crear un medio perteneciente al otro usuario
        medio = Media.objects.create(
            usuario=other_user,
            nombre='Other User Series',
            tipo='serie',
            total_capitulos=8
        )
        print(f"Medio de otro usuario creado: {medio.nombre}")

        response = self.client.get(reverse('detalle_serie_anime', kwargs={'medio_pk': medio.pk}))
        print(f"GET /serie_anime/{medio.pk}/detalle/ (Usuario Incorrecto) - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 404)  # No encontrado
        print("Status Code: 404 (No Encontrado)")
        print("--- Test de Vista de Detalle Serie/Anime (Usuario Incorrecto) Finalizado ---")
    
    def test_toggle_episodio_visto_view_authenticated(self):
        """Test toggling episode watched status for authenticated user."""
        print("\n--- Test: Vista de Toggle Episodio Visto (Autenticado) ---")
        self.client.login(username=self.user.email, password='viewpassword')
        print("Usuario de prueba loggeado para test de toggle episodio visto.")

        # Crear un medio tipo serie y un seguimiento de episodio
        serie = Media.objects.create(
            usuario=self.user,
            nombre='Test Serie Episodio',
            tipo='serie',
            total_capitulos=1
        )
        seguimiento = SeguimientoEpisodio.objects.create(
            media=serie,
            usuario=self.user,
            numero_episodio=1,
            visto=False
        )
        print(f"Medio de prueba (Serie): {serie.nombre}, Episodio: {seguimiento.numero_episodio} (visto={seguimiento.visto})")

        # Primera llamada: marcar como visto
        response = self.client.post(reverse('toggle_episodio_visto', kwargs={'seguimiento_pk': seguimiento.pk}))
        print(f"POST /seguimiento_episodio/{seguimiento.pk}/toggle_visto/ (Marcar como visto) - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 302) # Redirección
        print("Status Code: 302 (Redirección)")
        self.assertRedirects(response, reverse('detalle_serie_anime', kwargs={'medio_pk': serie.pk}))
        print(f"Redirigido a: /serie_anime/{serie.pk}/detalle/")

        # Verificar que el episodio se marcó como visto
        seguimiento.refresh_from_db()
        self.assertTrue(seguimiento.visto)
        print(f"Episodio marcado como visto: {seguimiento.visto}")

        # Segunda llamada: marcar como no visto
        response = self.client.post(reverse('toggle_episodio_visto', kwargs={'seguimiento_pk': seguimiento.pk}))
        print(f"POST /seguimiento_episodio/{seguimiento.pk}/toggle_visto/ (Marcar como no visto) - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 302) # Redirección
        print("Status Code: 302 (Redirección)")
        self.assertRedirects(response, reverse('detalle_serie_anime', kwargs={'medio_pk': serie.pk}))
        print(f"Redirigido a: /serie_anime/{serie.pk}/detalle/")

        # Verificar que el episodio se marcó como no visto
        seguimiento.refresh_from_db()
        self.assertFalse(seguimiento.visto)
        print(f"Episodio marcado como no visto: {seguimiento.visto}")

        print("--- Test de Vista de Toggle Episodio Visto (Autenticado) Finalizado ---")

    def test_toggle_episodio_visto_view_unauthenticated(self):
        """Test toggling episode watched status when not authenticated."""
        print("\n--- Test: Vista de Toggle Episodio Visto (No Autenticado) ---")
        self.client.logout()
        print("Asegurando que el cliente no esté loggeado.")

        # Crear un medio tipo serie y un seguimiento de episodio (no importa el usuario)
        serie = Media.objects.create(
            usuario=self.user,
            nombre='Test Serie NoAuth',
            tipo='serie',
            total_capitulos=1
        )
        seguimiento = SeguimientoEpisodio.objects.create(
            media=serie,
            usuario=self.user,
            numero_episodio=1,
            visto=False
        )
        print(f"Medio de prueba (Serie): {serie.nombre}, Episodio: {seguimiento.numero_episodio}")

        response = self.client.post(reverse('toggle_episodio_visto', kwargs={'seguimiento_pk': seguimiento.pk}))
        print(f"POST /seguimiento_episodio/{seguimiento.pk}/toggle_visto/ (No Autenticado) - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 302)
        print("Status Code: 302 (Redirección)")
        self.assertRedirects(response, f'/accounts/login/?next={reverse('toggle_episodio_visto', kwargs={'seguimiento_pk': seguimiento.pk})}', fetch_redirect_response=False)
        print(f"Redirigido a: /accounts/login/?next={reverse('toggle_episodio_visto', kwargs={'seguimiento_pk': seguimiento.pk})}")
        print("--- Test de Vista de Toggle Episodio Visto (No Autenticado) Finalizado ---")

    def test_toggle_episodio_visto_view_wrong_user(self):
        """Test toggling episode watched status that belongs to another user."""
        print("\n--- Test: Vista de Toggle Episodio Visto (Usuario Incorrecto) ---")
        self.client.login(username=self.user.email, password='viewpassword')
        print("Usuario de prueba loggeado para test de toggle episodio de otro usuario.")

        # Crear otro usuario y un medio/seguimiento para él
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpassword'
        )
        print(f"Otro usuario creado: {other_user.username}")
        other_serie = Media.objects.create(
            usuario=other_user,
            nombre='Other User Serie Episodio',
            tipo='serie',
            total_capitulos=1
        )
        other_seguimiento = SeguimientoEpisodio.objects.create(
            media=other_serie,
            usuario=other_user,
            numero_episodio=1,
            visto=False
        )
        print(f"Seguimiento de episodio de otro usuario: {other_serie.nombre}, Episodio: {other_seguimiento.numero_episodio}")

        response = self.client.post(reverse('toggle_episodio_visto', kwargs={'seguimiento_pk': other_seguimiento.pk}))
        print(f"POST /seguimiento_episodio/{other_seguimiento.pk}/toggle_visto/ (Usuario Incorrecto) - Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 404)  # No encontrado
        print("Status Code: 404 (No Encontrado)")
        print("--- Test de Vista de Toggle Episodio Visto (Usuario Incorrecto) Finalizado ---")
