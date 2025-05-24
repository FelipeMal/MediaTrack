from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Media

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
    class Meta:
        model = Media
        fields = ['nombre', 'tipo', 'enlace_plataforma', 'imagen_url', 'total_capitulos', 'duracion_minutos']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control', 'onchange': 'toggleFields()'}),
            'enlace_plataforma': forms.URLInput(attrs={'class': 'form-control'}),
            'imagen_url': forms.URLInput(attrs={'class': 'form-control'}),
            'total_capitulos': forms.NumberInput(attrs={'class': 'form-control'}),
            'duracion_minutos': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar las etiquetas
        self.fields['total_capitulos'].label = 'Total de Capítulos'
        self.fields['duracion_minutos'].label = 'Duración (minutos)'
        
        # Si es una edición, mostrar los campos según el tipo
        if self.instance.pk:
            if self.instance.tipo in ['serie', 'anime']:
                self.fields['total_capitulos'].widget.attrs['style'] = 'display: block;'
            elif self.instance.tipo == 'pelicula':
                self.fields['duracion_minutos'].widget.attrs['style'] = 'display: block;'

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        total_capitulos = cleaned_data.get('total_capitulos')
        duracion_minutos = cleaned_data.get('duracion_minutos')

        if tipo in ['serie', 'anime']:
            if not total_capitulos:
                # Solo validar si total_capitulos es requerido y no fue proporcionado
                if self.fields['total_capitulos'].required and total_capitulos is None:
                     raise forms.ValidationError('Para series y animes, debes especificar el total de capítulos.')
            # Limpiar duración si no es película
            cleaned_data['duracion_minutos'] = None
        
        elif tipo == 'pelicula':
            if not duracion_minutos:
                 # Solo validar si duracion_minutos es requerido y no fue proporcionado
                 if self.fields['duracion_minutos'].required and duracion_minutos is None:
                      raise forms.ValidationError('Para películas, debes especificar la duración en minutos.')
            # Limpiar capítulos si no es serie/anime
            cleaned_data['total_capitulos'] = None
        
        # Si el tipo es 'otro', limpiar ambos campos
        elif tipo == 'otro':
             cleaned_data['total_capitulos'] = None
             cleaned_data['duracion_minutos'] = None

        return cleaned_data 