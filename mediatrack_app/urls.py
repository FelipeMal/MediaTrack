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
    path('medio/<int:medio_pk>/toggle_visto/', views.toggle_visto, name='toggle_visto'),
    path('serie_anime/<int:medio_pk>/detalle/', views.detalle_serie_anime, name='detalle_serie_anime'),
    path('pelicula/<int:medio_pk>/detalle/', views.detalle_pelicula, name='detalle_pelicula'),
    path('seguimiento_episodio/<int:seguimiento_pk>/toggle_visto/', views.toggle_episodio_visto, name='toggle_episodio_visto'),
    path('episodio/<int:seguimiento_pk>/editar_calificacion/', views.editar_episodio_calificacion, name='editar_episodio_calificacion'),
    path('buscar/', views.buscar_medio, name='buscar_medio'),
] 