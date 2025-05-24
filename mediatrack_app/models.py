from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email

class Media(models.Model):
    TIPO_CHOICES = [
        ('serie', 'Serie'),
        ('pelicula', 'Película'),
        ('anime', 'Anime'),
        ('otro', 'Otro'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='medios')
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    enlace_plataforma = models.URLField(blank=True)
    
    # Campos específicos según el tipo
    total_capitulos = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text='Número total de capítulos (solo para series y animes)'
    )
    duracion_minutos = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text='Duración en minutos (solo para películas)'
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Medio'
        verbose_name_plural = 'Medios'
        ordering = ['-fecha_actualizacion']

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"
