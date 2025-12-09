from django import template
from django.utils.translation import get_language

register = template.Library()

# Dictionary of translations
TRANSLATIONS = {
    'es': {
        'Términos & Condiciones': 'Términos & Condiciones',
        'Política de Privacidad': 'Política de Privacidad',
        'Todos los derechos reservados': 'Todos los derechos reservados',
        'Términos y Condiciones': 'Términos y Condiciones',
        'Portada': 'Portada',
        'Agendar Reunión': 'Agendar Reunión',
        'Proyectos': 'Proyectos',
        'Volver al inicio': 'Volver al inicio',
    },
    'en': {
        'Términos & Condiciones': 'Terms & Conditions',
        'Política de Privacidad': 'Privacy Policy',
        'Todos los derechos reservados': 'All rights reserved',
        'Términos y Condiciones': 'Terms and Conditions',
        'Portada': 'Home',
        'Agendar Reunión': 'Book Meeting',
        'Proyectos': 'Projects',
        'Volver al inicio': 'Back to home',
    },
    'de': {
        'Términos & Condiciones': 'Allgemeine Geschäftsbedingungen',
        'Política de Privacidad': 'Datenschutzerklärung',
        'Todos los derechos reservados': 'Alle Rechte vorbehalten',
        'Términos y Condiciones': 'Allgemeine Geschäftsbedingungen',
        'Portada': 'Startseite',
        'Agendar Reunión': 'Termin vereinbaren',
        'Proyectos': 'Projekte',
        'Volver al inicio': 'Zurück zur Startseite',
    }
}

@register.simple_tag(takes_context=True)
def simple_trans(context, text):
    """
    Custom template tag to translate text based on the current language
    without relying on gettext binaries.
    Usage: {% simple_trans "Text to translate" %}
    """
    # Get current language from request or django utils
    lang = get_language()
    if not lang:
        lang = 'es'
    
    # Normalize language code (e.g. 'es-cl' -> 'es')
    lang = lang.split('-')[0]
    
    # Fallback to Spanish if language not found
    if lang not in TRANSLATIONS:
        lang = 'es'
        
    # Return translated text or original if not found
    return TRANSLATIONS.get(lang, {}).get(text, text)
