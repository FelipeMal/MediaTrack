from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('medio/agregar/', views.agregar_medio, name='agregar_medio'),
    path('medio/<int:pk>/editar/', views.editar_medio, name='editar_medio'),
    path('medio/<int:pk>/eliminar/', views.eliminar_medio, name='eliminar_medio'),
] 