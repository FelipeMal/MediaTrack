from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, LoginForm, MediaForm
from .models import Media

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
    medios = Media.objects.filter(usuario=request.user)
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
