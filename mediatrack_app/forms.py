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
        fields = ['nombre', 'tipo', 'enlace_plataforma', 'total_episodios', 'duracion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'enlace_plataforma': forms.URLInput(attrs={'class': 'form-control'}),
            'total_episodios': forms.NumberInput(attrs={'class': 'form-control'}),
            'duracion': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        total_episodios = cleaned_data.get('total_episodios')
        duracion = cleaned_data.get('duracion')

        if tipo in ['serie', 'anime'] and not total_episodios:
            raise forms.ValidationError('Para series y animes, debes especificar el total de episodios.')
        
        if tipo == 'pelicula' and not duracion:
            raise forms.ValidationError('Para películas, debes especificar la duración.')

        return cleaned_data 