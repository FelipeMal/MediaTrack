from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Usuario, Media
import re

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Usuario
        fields = ('email', 'username', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class MediaForm(forms.ModelForm):
    # Campo de texto para la duración en formato HH:MM
    duracion_hh_mm = forms.CharField(
        label='Duración (HH:MM)',
        required=False, # No requerido por defecto, la validación se hace en clean
        help_text='Formato: HH:MM (ej. 1:30 para 1 hora y 30 minutos, o 90 para 90 minutos)',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Media
        fields = ['nombre', 'tipo', 'enlace_plataforma', 'imagen_url', 'total_capitulos', 'duracion_minutos']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control', 'onchange': 'toggleFields()'}),
            'enlace_plataforma': forms.URLInput(attrs={'class': 'form-control'}),
            'imagen_url': forms.URLInput(attrs={'class': 'form-control'}),
            'total_capitulos': forms.NumberInput(attrs={'class': 'form-control'}),
            'duracion_minutos': forms.HiddenInput(), # Mantenemos este oculto ya que usamos el campo HH:MM
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar las etiquetas
        self.fields['total_capitulos'].label = 'Total de Capítulos'
        
        # Si es una edición y tiene duración en minutos, convertirla a HH:MM para mostrar en el campo de texto
        if self.instance.pk and self.instance.duracion_minutos is not None:
            minutos_totales = self.instance.duracion_minutos
            horas = minutos_totales // 60
            minutos = minutos_totales % 60
            self.fields['duracion_hh_mm'].initial = f'{horas}:{minutos:02d}'

        # Eliminamos la lógica de mostrar/ocultar en el init; el JavaScript lo manejará

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        total_capitulos = cleaned_data.get('total_capitulos')
        duracion_hh_mm = cleaned_data.get('duracion_hh_mm')

        if tipo in ['serie', 'anime']:
            # Validar total_capitulos para series/animes
            if total_capitulos is None:
                 raise forms.ValidationError({'total_capitulos': 'Para series y animes, debes especificar el total de capítulos.'})
            # Limpiar duración si no es película
            cleaned_data['duracion_minutos'] = None
            cleaned_data['duracion_hh_mm'] = None # Limpiar campo HH:MM
        
        elif tipo == 'pelicula':
            # Validar duracion_hh_mm para películas
            if not duracion_hh_mm:
                 raise forms.ValidationError({'duracion_hh_mm': 'Para películas, debes especificar la duración en formato HH:MM.'})
            
            # Intentar parsear HH:MM
            match = re.match(r'^(\d+):(\d{2})$', duracion_hh_mm)
            if not match:
                 # Si no coincide HH:MM, intentar solo minutos
                 if duracion_hh_mm.isdigit():
                     minutos_totales = int(duracion_hh_mm)
                 else:
                     raise forms.ValidationError({'duracion_hh_mm': 'Formato de duración inválido. Usa HH:MM o solo minutos.'})
            else:
                horas = int(match.group(1))
                minutos = int(match.group(2))
                if minutos >= 60:
                     raise forms.ValidationError({'duracion_hh_mm': 'Los minutos deben ser menores de 60.'})
                minutos_totales = horas * 60 + minutos
            
            # Asignar la duración total en minutos al campo del modelo
            cleaned_data['duracion_minutos'] = minutos_totales
            cleaned_data['total_capitulos'] = None # Limpiar capítulos

        # Si el tipo es 'otro', limpiar ambos campos
        elif tipo == 'otro':
             cleaned_data['total_capitulos'] = None
             cleaned_data['duracion_minutos'] = None
             cleaned_data['duracion_hh_mm'] = None # Limpiar campo HH:MM

        return cleaned_data 