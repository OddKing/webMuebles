from django import forms
from .models import Cliente
import re


class ClienteForm(forms.ModelForm):
    """Formulario para crear y editar clientes habituales"""
    
    class Meta:
        model = Cliente
        fields = [
            'nombre_completo',
            'rut',
            'email',
            'telefono',
            'direccion',
            'empresa',
            'descuento_habitual',
            'notas',
            'activo'
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
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56912345678'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Av. Principal 123, Santiago'
            }),
            'empresa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la empresa (opcional)'
            }),
            'descuento_habitual': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Notas internas sobre el cliente...'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        
        labels = {
            'nombre_completo': 'Nombre Completo *',
            'rut': 'RUT *',
            'email': 'Email *',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'empresa': 'Empresa',
            'descuento_habitual': 'Descuento Habitual (%)',
            'notas': 'Notas Internas',
            'activo': 'Cliente Activo',
        }
        
        help_texts = {
            'rut': 'Formato: 12.345.678-9 (debe ser único)',
            'descuento_habitual': 'Porcentaje de descuento por ser cliente recurrente (0-100)',
            'notas': 'Información adicional, preferencias, observaciones internas',
            'activo': 'Desmarcar para desactivar el cliente sin eliminarlo',
        }
    
    def clean_rut(self):
        """Valida el formato del RUT chileno"""
        rut = self.cleaned_data.get('rut', '').strip()
        
        # Validar formato básico
        pattern = r'^\d{1,2}\.\d{3}\.\d{3}[-][0-9kK]{1}$|^\d{7,8}[-][0-9kK]{1}$'
        if not re.match(pattern, rut):
            raise forms.ValidationError(
                'RUT inválido. Use el formato: 12.345.678-9'
            )
        
        return rut
    
    def clean_descuento_habitual(self):
        """Valida que el descuento esté en rango válido"""
        descuento = self.cleaned_data.get('descuento_habitual', 0)
        
        if descuento < 0 or descuento > 100:
            raise forms.ValidationError(
                'El descuento debe estar entre 0 y 100'
            )
        
        return descuento
