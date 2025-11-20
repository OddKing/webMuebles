from django import forms
from .models import Cotizacion
import re


class CotizacionForm(forms.ModelForm):
    """
    Formulario para solicitar cotización de productos personalizados
    """
    # Campos adicionales para el consentimiento legal
    acepto_terminos = forms.BooleanField(
        required=True,
        label="Acepto los Términos y Condiciones",
        error_messages={'required': 'Debe aceptar los términos y condiciones para continuar'}
    )
    
    acepto_privacidad = forms.BooleanField(
        required=True,
        label="Acepto la Política de Privacidad",
        error_messages={'required': 'Debe aceptar la política de privacidad para continuar'}
    )
    
    class Meta:
        model = Cotizacion
        fields = [
            'nombre_completo', 
            'rut',
            'direccion',
            'email', 
            'telefono',
            'medidas_ancho',
            'medidas_alto', 
            'medidas_profundidad',
            'material_preferido',
            'foto_lugar',
            'descripcion_proyecto'
        ]
        
        widgets = {
            'nombre_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Juan Pérez González'
            }),
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12.345.678-9',
                'maxlength': '12'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Av. Principal 123, Depto 4B, Santiago'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56912345678 (opcional)'
            }),
            'medidas_ancho': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 120',
                'step': '0.01',
                'min': '0'
            }),
            'medidas_alto': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 80',
                'step': '0.01',
                'min': '0'
            }),
            'medidas_profundidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 60',
                'step': '0.01',
                'min': '0'
            }),
            'material_preferido': forms.Select(attrs={
                'class': 'form-select'
            }),
            'foto_lugar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'descripcion_proyecto': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Cuéntanos sobre tu proyecto, detalles específicos, ideas, etc. (opcional)'
            }),
        }
        
        labels = {
            'nombre_completo': 'Nombre Completo *',
            'rut': 'RUT *',
            'direccion': 'Dirección *',
            'email': 'Email *',
            'telefono': 'Teléfono',
            'medidas_ancho': 'Ancho del Espacio (cm) *',
            'medidas_alto': 'Alto del Espacio (cm) *',
            'medidas_profundidad': 'Fondo/Profundidad del Espacio (cm) *',
            'material_preferido': 'Material Preferido *',
            'foto_lugar': 'Foto del Lugar (opcional)',
            'descripcion_proyecto': 'Detalles Adicionales',
        }
        
        help_texts = {
            'medidas_ancho': 'Ancho del lugar donde irá el mueble',
            'medidas_alto': 'Altura disponible en el espacio',
            'medidas_profundidad': 'Profundidad o fondo del espacio',
            'rut': 'Formato: 12.345.678-9',
            'foto_lugar': 'Sube una foto del espacio para una mejor evaluación'
        }
    
    def clean_rut(self):
        """
        Valida el formato del RUT chileno
        """
        rut = self.cleaned_data.get('rut', '').strip()
        
        # Validar formato básico (XX.XXX.XXX-X o XXXXXXXX-X)
        pattern = r'^\d{1,2}\.\d{3}\.\d{3}[-][0-9kK]{1}$|^\d{7,8}[-][0-9kK]{1}$'
        if not re.match(pattern, rut):
            raise forms.ValidationError(
                'RUT inválido. Use el formato: 12.345.678-9'
            )
        
        return rut
    
    def clean_foto_lugar(self):
        """
        Valida el archivo de imagen
        """
        foto = self.cleaned_data.get('foto_lugar')
        
        if foto:
            # Validar tamaño (máximo 5MB)
            if foto.size > 5 * 1024 * 1024:
                raise forms.ValidationError('La imagen no debe superar los 5MB')
            
            # Validar tipo de archivo
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
            if foto.content_type not in allowed_types:
                raise forms.ValidationError(
                    'Solo se permiten imágenes en formato JPG, PNG o WEBP'
                )
        
        return foto
    
    def clean(self):
        """
        Validación general del formulario
        """
        cleaned_data = super().clean()
        
        # Validar que las dimensiones sean positivas
        dimensiones = ['medidas_ancho', 'medidas_alto', 'medidas_profundidad']
        for dim in dimensiones:
            valor = cleaned_data.get(dim)
            if valor and valor <= 0:
                self.add_error(dim, 'Las medidas deben ser mayores a 0')
        
        return cleaned_data
