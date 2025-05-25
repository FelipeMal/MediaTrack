from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import RegistroForm, LoginForm, MediaForm, CalificacionComentarioEpisodioForm, CalificacionComentarioPeliculaForm
from .models import Media, SeguimientoEpisodio

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
    
    # Calcular episodios vistos y porcentaje para series y animes, y promedio de calificación
    for medio in medios:
        if medio.tipo in ['serie', 'anime']:
            episodios_vistos = medio.episodios_vistos.all()
            medio.vistos_count = sum(1 for episodio in episodios_vistos if episodio.visto)
            if medio.total_capitulos and medio.total_capitulos > 0:
                medio.progreso_porcentaje = int((medio.vistos_count / medio.total_capitulos) * 100)
            else:
                medio.progreso_porcentaje = 0
            
            # Calcular promedio de calificación para series/animes (solo de episodios vistos y calificados)
            calificaciones_episodios = [ep.calificacion for ep in episodios_vistos if ep.visto and ep.calificacion is not None]
            if calificaciones_episodios:
                medio.promedio_calificacion = sum(calificaciones_episodios) / len(calificaciones_episodios)
            else:
                medio.promedio_calificacion = None

        elif medio.tipo == 'pelicula':
            medio.vistos_count = 1 if medio.visto else 0
            medio.total_capitulos = 1 # Para consistencia en la visualización del progreso
            medio.progreso_porcentaje = 100 if medio.visto else 0
            medio.promedio_calificacion = medio.calificacion_pelicula

        else:
            medio.vistos_count = 0 # No aplica para otros
            medio.total_capitulos = 0
            medio.progreso_porcentaje = 0 # No aplica para otros
            medio.promedio_calificacion = None

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
def detalle_serie_anime(request, medio_pk):
    medio = get_object_or_404(Media, pk=medio_pk, usuario=request.user, tipo__in=['serie', 'anime'])
    
    # Crear entradas de seguimiento si no existen
    if medio.total_capitulos:
        episodios_existentes = set(SeguimientoEpisodio.objects.filter(media=medio, usuario=request.user).values_list('numero_episodio', flat=True))
        for i in range(1, medio.total_capitulos + 1):
            if i not in episodios_existentes:
                SeguimientoEpisodio.objects.create(
                    media=medio,
                    usuario=request.user,
                    numero_episodio=i,
                    visto=False
                )
    
    episodios_seguimiento = SeguimientoEpisodio.objects.filter(media=medio, usuario=request.user).order_by('numero_episodio')

    # Los formularios de calificación se manejarán por separado si el usuario edita un episodio
    # Aquí solo los preparamos para mostrar los valores existentes
    forms_calificacion = {}
    for seguimiento in episodios_seguimiento:
        forms_calificacion[seguimiento.pk] = CalificacionComentarioEpisodioForm(instance=seguimiento, prefix=f'calificacion_{seguimiento.pk}')

    return render(request, 'mediatrack_app/detalle_serie_anime.html', {
        'medio': medio,
        'episodios_seguimiento': episodios_seguimiento,
        'forms_calificacion': forms_calificacion,
    })

@login_required
def detalle_pelicula(request, medio_pk):
    # Para películas: mostrar detalles completos, opción de marcar como visto, calificación y comentario
    medio = get_object_or_404(Media, pk=medio_pk, usuario=request.user, tipo='pelicula')
    
    form_calificacion = CalificacionComentarioPeliculaForm(instance=medio)

    if request.method == 'POST':
        if 'toggle_visto' in request.POST:
             # Manejar toggle visto
             medio.visto = not medio.visto
             medio.save()
             messages.success(request, 'Estado de visto de película actualizado.')
             return redirect('detalle_pelicula', medio_pk=medio.pk)
             
        # Si no es toggle_visto, intentar manejar formulario de calificación/comentario
        form_calificacion = CalificacionComentarioPeliculaForm(request.POST, instance=medio)
        if form_calificacion.is_valid():
            form_calificacion.save()
            messages.success(request, 'Calificación y comentario de película guardados.')
            return redirect('detalle_pelicula', medio_pk=medio.pk)
        else:
            messages.error(request, 'Error al guardar calificación y comentario.')

    return render(request, 'mediatrack_app/detalle_pelicula.html', {
        'medio': medio,
        'form_calificacion': form_calificacion,
    })

@login_required
def editar_episodio_calificacion(request, seguimiento_pk):
    # Vista para editar la calificación y comentario de un episodio específico
    seguimiento_episodio = get_object_or_404(SeguimientoEpisodio, pk=seguimiento_pk, usuario=request.user)

    if request.method == 'POST':
        form = CalificacionComentarioEpisodioForm(request.POST, instance=seguimiento_episodio)
        if form.is_valid():
            form.save()
            messages.success(request, f'Calificación y comentario para Episodio {seguimiento_episodio.numero_episodio} guardados.')
            # Redirigir de vuelta a la página de detalles de la serie
            return redirect('detalle_serie_anime', medio_pk=seguimiento_episodio.media.pk)
    else:
        form = CalificacionComentarioEpisodioForm(instance=seguimiento_episodio)

    return render(request, 'mediatrack_app/editar_episodio_calificacion.html', {
        'seguimiento_episodio': seguimiento_episodio,
        'form': form,
    })

# Vista para manejar el toggle visto de episodios
@login_required
def toggle_episodio_visto(request, seguimiento_pk):
    seguimiento_episodio = get_object_or_404(SeguimientoEpisodio, pk=seguimiento_pk, usuario=request.user)
    if request.method == 'POST':
        seguimiento_episodio.visto = not seguimiento_episodio.visto
        if seguimiento_episodio.visto:
            seguimiento_episodio.fecha_visto = timezone.now()
        else:
            seguimiento_episodio.fecha_visto = None
        seguimiento_episodio.save()
        messages.success(request, f'Episodio {seguimiento_episodio.numero_episodio} actualizado.')
        # Redirigir de vuelta a la página de detalles de la serie/anime
        return redirect('detalle_serie_anime', medio_pk=seguimiento_episodio.media.pk)
    # Si no es POST, redirigir al detalle (comportamiento por defecto si alguien accede directamente a la URL POST)
    return redirect('detalle_serie_anime', medio_pk=seguimiento_episodio.media.pk)

# Vista para manejar el toggle visto de películas (simplificada ya que la lógica principal está en detalle_pelicula)
@login_required
def toggle_visto(request, medio_pk):
     # Esta vista ahora solo redirige a la página de detalle después de la acción en el template
    medio = get_object_or_404(Media, pk=medio_pk, usuario=request.user, tipo='pelicula')
    # La lógica de toggle ahora está en detalle_pelicula, esta vista es solo para el endpoint POST
    return redirect('detalle_pelicula', medio_pk=medio.pk)
