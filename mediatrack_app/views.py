from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, LoginForm, MediaForm
from .models import Media, SeguimientoEpisodio
from django.utils import timezone

# Create your views here.

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('dashboard')
    else:
        form = RegistroForm()
    return render(request, 'mediatrack_app/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, '¡Inicio de sesión exitoso!')
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'mediatrack_app/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')

@login_required
def dashboard(request):
    medios = Media.objects.filter(usuario=request.user).prefetch_related('episodios_vistos')
    
    # Calcular episodios vistos y porcentaje para series y animes
    for medio in medios:
        if medio.tipo in ['serie', 'anime']:
            medio.vistos_count = sum(1 for episodio in medio.episodios_vistos.all() if episodio.visto)
            if medio.total_capitulos and medio.total_capitulos > 0:
                medio.progreso_porcentaje = int((medio.vistos_count / medio.total_capitulos) * 100)
            else:
                medio.progreso_porcentaje = 0
        else:
            medio.vistos_count = 0 # No aplica para películas u otros
            medio.progreso_porcentaje = 0 # No aplica para películas u otros

    return render(request, 'mediatrack_app/dashboard.html', {'medios': medios})

@login_required
def agregar_medio(request):
    if request.method == 'POST':
        form = MediaForm(request.POST)
        if form.is_valid():
            medio = form.save(commit=False)
            medio.usuario = request.user
            medio.save()
            messages.success(request, 'Medio agregado exitosamente.')
            return redirect('dashboard')
    else:
        form = MediaForm()
    return render(request, 'mediatrack_app/medio_form.html', {'form': form, 'accion': 'Agregar'})

@login_required
def editar_medio(request, pk):
    medio = get_object_or_404(Media, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = MediaForm(request.POST, instance=medio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medio actualizado exitosamente.')
            return redirect('dashboard')
    else:
        form = MediaForm(instance=medio)
    return render(request, 'mediatrack_app/medio_form.html', {'form': form, 'accion': 'Editar'})

@login_required
def eliminar_medio(request, pk):
    medio = get_object_or_404(Media, pk=pk, usuario=request.user)
    if request.method == 'POST':
        medio.delete()
        messages.success(request, 'Medio eliminado exitosamente.')
        return redirect('dashboard')
    return render(request, 'mediatrack_app/confirmar_eliminar.html', {'medio': medio})

@login_required
def toggle_visto(request, medio_pk):
    # Para películas: marcar como visto/no visto
    medio = get_object_or_404(Media, pk=medio_pk, usuario=request.user, tipo='pelicula')
    if request.method == 'POST':
        medio.visto = not medio.visto
        medio.save()
    return redirect('dashboard')

@login_required
def detalle_serie_anime(request, medio_pk):
    # Para series y animes: mostrar episodios y seguimiento
    medio = get_object_or_404(Media, pk=medio_pk, usuario=request.user, tipo__in=['serie', 'anime'])
    episodios_seguimiento = SeguimientoEpisodio.objects.filter(media=medio, usuario=request.user).order_by('numero_episodio')

    # Crear entradas de seguimiento si no existen
    if medio.total_capitulos:
        episodios_existentes = set(episodios_seguimiento.values_list('numero_episodio', flat=True))
        for i in range(1, medio.total_capitulos + 1):
            if i not in episodios_existentes:
                SeguimientoEpisodio.objects.create(
                    media=medio,
                    usuario=request.user,
                    numero_episodio=i,
                    visto=False
                )
        # Volver a obtener el seguimiento después de crear nuevos
        episodios_seguimiento = SeguimientoEpisodio.objects.filter(media=medio, usuario=request.user).order_by('numero_episodio')

    return render(request, 'mediatrack_app/detalle_serie_anime.html', {
        'medio': medio,
        'episodios_seguimiento': episodios_seguimiento
    })

@login_required
def toggle_episodio_visto(request, seguimiento_pk):
    # Marcar un episodio específico como visto/no visto
    seguimiento_episodio = get_object_or_404(SeguimientoEpisodio, pk=seguimiento_pk, usuario=request.user)
    if request.method == 'POST':
        seguimiento_episodio.visto = not seguimiento_episodio.visto
        if seguimiento_episodio.visto:
            seguimiento_episodio.fecha_visto = timezone.now()
        else:
            seguimiento_episodio.fecha_visto = None
        seguimiento_episodio.save()
        # Redirigir de vuelta a la página de detalles de la serie/anime
        return redirect('detalle_serie_anime', medio_pk=seguimiento_episodio.media.pk)
    # Si no es POST, redirigir al detalle
    return redirect('detalle_serie_anime', medio_pk=seguimiento_episodio.media.pk)
