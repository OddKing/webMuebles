// ============================================
// MULTI-LANGUAGE TRANSLATION SYSTEM
// Pure JavaScript - No Server Dependencies
// ============================================

const translations = {
    es: {
        // Navbar
        'nav.terms': 'Términos & Condiciones',
        'nav.privacy': 'Política de Privacidad',

        // Footer
        'footer.rights': 'Todos los derechos reservados',
        'footer.terms': 'Términos y Condiciones',
        'footer.privacy': 'Política de Privacidad',

        // Homepage
        'home.title': 'Portada',
        'home.schedule': 'Agendar Reunión',
        'home.quote': 'Cotiza Aquí',

        // Catalog Page
        'catalog.title': 'Catálogo de Productos',
        'catalog.hero.title': 'Nuestros Productos',
        'catalog.hero.subtitle': 'Diseños exclusivos para tu hogar y oficina',
        'catalog.empty.title': 'No hay productos disponibles',
        'catalog.empty.message': 'Pronto agregaremos nuevos productos a nuestro catálogo.',
        'catalog.btn.quote': 'Cotizar',
        'catalog.cta.title': '¿Necesitas un diseño personalizado?',
        'catalog.cta.message': 'Contáctanos y creamos el mueble perfecto para ti',
        'catalog.cta.button': 'Agendar Reunión',

        // Meeting Scheduler Page
        'meeting.title': 'Agendar Reunión',
        'meeting.hero.title': 'Agendar tu Reunión',
        'meeting.hero.subtitle': 'Selecciona la fecha y hora que mejor se ajuste a tu agenda',
        'meeting.form.personal': 'Información Personal',
        'meeting.form.name': 'Nombre Completo',
        'meeting.form.email': 'Email',
        'meeting.form.phone': 'Teléfono',
        'meeting.form.address': 'Dirección',
        'meeting.form.type': 'Tipo de Reunión',
        'meeting.form.online': 'Online',
        'meeting.form.inperson': 'Presencial',
        'meeting.form.selectdate': 'Selecciona una Fecha',
        'meeting.form.selecttime': 'Selecciona un Horario',
        'meeting.form.schedule': 'Horario de atención: 10:00 AM - 6:00 PM',
        'meeting.form.workdays': 'Solo días laborables (Lunes a Viernes)',
        'meeting.summary.title': 'Resumen de tu Cita',
        'meeting.summary.date': 'Fecha:',
        'meeting.summary.time': 'Hora:',
        'meeting.consent.read': 'He leído y acepto los',
        'meeting.consent.and': 'y la',
        'meeting.consent.error': 'Debes aceptar los términos y condiciones para continuar.',
        'meeting.btn.confirm': 'Confirmar Reunión',

        // Days of week
        'calendar.mon': 'Lun',
        'calendar.tue': 'Mar',
        'calendar.wed': 'Mié',
        'calendar.thu': 'Jue',
        'calendar.fri': 'Vie',
        'calendar.sat': 'Sáb',
        'calendar.sun': 'Dom',

        // Months
        'month.january': 'Enero',
        'month.february': 'Febrero',
        'month.march': 'Marzo',
        'month.april': 'Abril',
        'month.may': 'Mayo',
        'month.june': 'Junio',
        'month.july': 'Julio',
        'month.august': 'Agosto',
        'month.september': 'Septiembre',
        'month.october': 'Octubre',
        'month.november': 'Noviembre',
        'month.december': 'Diciembre',

        // Legal Pages - Terms
        'legal.terms.title': 'Términos y Condiciones',
        'legal.terms.updated': 'Última actualización:',
        'legal.terms.version': 'Versión',
        'legal.toc.title': 'Contenido',
        'legal.btn.print': 'Imprimir',
        'legal.btn.home': 'Volver al Inicio',

        // Legal Pages - Privacy
        'legal.privacy.title': 'Política de Privacidad',

        // WhatsApp Widget
        'whatsapp.menu.title': 'Contáctanos por WhatsApp',
        'whatsapp.taylor.name': 'Taylor Barrera',
        'whatsapp.taylor.desc': 'Cotizaciones y dudas',
        'whatsapp.michael.name': 'Michael Barrera',
        'whatsapp.michael.desc': 'Medidas y diseños',

        // Voice Assistant
        'voice.activated': 'Narrador activado. Pase el mouse sobre el texto para escuchar.',
        'voice.deactivated': 'Narrador desactivado.',

        // Calendar availability
        'calendar.available': 'Disponible',
        'calendar.notavailable': 'No disponible',
        'calendar.past': 'Fecha pasada, no disponible',
        'calendar.weekend': 'Fin de semana, no disponible',
        'calendar.holiday': 'Festivo, no disponible',
        'calendar.outofrange': 'Fuera del rango disponible',

        // Meta
        'meta.backToHome': 'Volver al inicio'
    },
    en: {
        // Navbar
        'nav.terms': 'Terms & Conditions',
        'nav.privacy': 'Privacy Policy',

        // Footer
        'footer.rights': 'All rights reserved',
        'footer.terms': 'Terms and Conditions',
        'footer.privacy': 'Privacy Policy',

        // Homepage
        'home.title': 'Home',
        'home.schedule': 'Book Meeting',
        'home.quote': 'Get Quote',

        // Catalog Page
        'catalog.title': 'Product Catalog',
        'catalog.hero.title': 'Our Products',
        'catalog.hero.subtitle': 'Exclusive designs for your home and office',
        'catalog.empty.title': 'No products available',
        'catalog.empty.message': 'We will soon add new products to our catalog.',
        'catalog.btn.quote': 'Get Quote',
        'catalog.cta.title': 'Need a custom design?',
        'catalog.cta.message': 'Contact us and we will create the perfect furniture for you',
        'catalog.cta.button': 'Book Meeting',

        // Meeting Scheduler Page
        'meeting.title': 'Book Meeting',
        'meeting.hero.title': 'Book Your Meeting',
        'meeting.hero.subtitle': 'Select the date and time that best fits your schedule',
        'meeting.form.personal': 'Personal Information',
        'meeting.form.name': 'Full Name',
        'meeting.form.email': 'Email',
        'meeting.form.phone': 'Phone',
        'meeting.form.address': 'Address',
        'meeting.form.type': 'Meeting Type',
        'meeting.form.online': 'Online',
        'meeting.form.inperson': 'In-Person',
        'meeting.form.selectdate': 'Select a Date',
        'meeting.form.selecttime': 'Select a Time',
        'meeting.form.schedule': 'Business hours: 10:00 AM - 6:00 PM',
        'meeting.form.workdays': 'Weekdays only (Monday - Friday)',
        'meeting.summary.title': 'Appointment Summary',
        'meeting.summary.date': 'Date:',
        'meeting.summary.time': 'Time:',
        'meeting.consent.read': 'I have read and accept the',
        'meeting.consent.and': 'and the',
        'meeting.consent.error': 'You must accept the terms and conditions to continue.',
        'meeting.btn.confirm': 'Confirm Meeting',

        // Days of week
        'calendar.mon': 'Mon',
        'calendar.tue': 'Tue',
        'calendar.wed': 'Wed',
        'calendar.thu': 'Thu',
        'calendar.fri': 'Fri',
        'calendar.sat': 'Sat',
        'calendar.sun': 'Sun',

        // Months
        'month.january': 'January',
        'month.february': 'February',
        'month.march': 'March',
        'month.april': 'April',
        'month.may': 'May',
        'month.june': 'June',
        'month.july': 'July',
        'month.august': 'August',
        'month.september': 'September',
        'month.october': 'October',
        'month.november': 'November',
        'month.december': 'December',

        // Legal Pages - Terms
        'legal.terms.title': 'Terms and Conditions',
        'legal.terms.updated': 'Last updated:',
        'legal.terms.version': 'Version',
        'legal.toc.title': 'Contents',
        'legal.btn.print': 'Print',
        'legal.btn.home': 'Back to Home',

        // Legal Pages - Privacy
        'legal.privacy.title': 'Privacy Policy',

        // WhatsApp Widget
        'whatsapp.menu.title': 'Contact us via WhatsApp',
        'whatsapp.taylor.name': 'Taylor Barrera',
        'whatsapp.taylor.desc': 'Quotes and general questions',
        'whatsapp.michael.name': 'Michael Barrera',
        'whatsapp.michael.desc': 'Measurements and designs',

        // Voice Assistant
        'voice.activated': 'Narrator activated. Hover over text to listen.',
        'voice.deactivated': 'Narrator deactivated.',

        // Calendar availability
        'calendar.available': 'Available',
        'calendar.notavailable': 'Not available',
        'calendar.past': 'Past date, not available',
        'calendar.weekend': 'Weekend, not available',
        'calendar.holiday': 'Holiday, not available',
        'calendar.outofrange': 'Out of available range',

        // Meta
        'meta.backToHome': 'Back to home'
    },
    de: {
        // Navbar
        'nav.terms': 'Allgemeine Geschäftsbedingungen',
        'nav.privacy': 'Datenschutzerklärung',

        // Footer
        'footer.rights': 'Alle Rechte vorbehalten',
        'footer.terms': 'Allgemeine Geschäftsbedingungen',
        'footer.privacy': 'Datenschutzerklärung',

        // Homepage
        'home.title': 'Startseite',
        'home.schedule': 'Termin vereinbaren',
        'home.quote': 'Angebot anfordern',

        // Catalog Page
        'catalog.title': 'Produktkatalog',
        'catalog.hero.title': 'Unsere Produkte',
        'catalog.hero.subtitle': 'Exklusive Designs für Ihr Zuhause und Büro',
        'catalog.empty.title': 'Keine Produkte verfügbar',
        'catalog.empty.message': 'Wir werden bald neue Produkte zu unserem Katalog hinzufügen.',
        'catalog.btn.quote': 'Angebot anfordern',
        'catalog.cta.title': 'Benötigen Sie ein individuelles Design?',
        'catalog.cta.message': 'Kontaktieren Sie uns und wir erstellen das perfekte Möbelstück für Sie',
        'catalog.cta.button': 'Termin vereinbaren',

        // Meeting Scheduler Page
        'meeting.title': 'Termin buchen',
        'meeting.hero.title': 'Termin buchen',
        'meeting.hero.subtitle': 'Wählen Sie das Datum und die Uhrzeit, die am besten zu Ihrem Zeitplan passt',
        'meeting.form.personal': 'Persönliche Informationen',
        'meeting.form.name': 'Vollständiger Name',
        'meeting.form.email': 'E-Mail',
        'meeting.form.phone': 'Telefon',
        'meeting.form.address': 'Adresse',
        'meeting.form.type': 'Besprechungsart',
        'meeting.form.online': 'Online',
        'meeting.form.inperson': 'Persönlich',
        'meeting.form.selectdate': 'Datum auswählen',
        'meeting.form.selecttime': 'Uhrzeit auswählen',
        'meeting.form.schedule': 'Geschäftszeiten: 10:00 - 18:00 Uhr',
        'meeting.form.workdays': 'Nur Werktage (Montag - Freitag)',
        'meeting.summary.title': 'Terminübersicht',
        'meeting.summary.date': 'Datum:',
        'meeting.summary.time': 'Uhrzeit:',
        'meeting.consent.read': 'Ich habe gelesen und akzeptiere die',
        'meeting.consent.and': 'und die',
        'meeting.consent.error': 'Sie müssen die Allgemeinen Geschäftsbedingungen akzeptieren, um fortzufahren.',
        'meeting.btn.confirm': 'Termin bestätigen',

        // Days of week
        'calendar.mon': 'Mo',
        'calendar.tue': 'Di',
        'calendar.wed': 'Mi',
        'calendar.thu': 'Do',
        'calendar.fri': 'Fr',
        'calendar.sat': 'Sa',
        'calendar.sun': 'So',

        // Months
        'month.january': 'Januar',
        'month.february': 'Februar',
        'month.march': 'März',
        'month.april': 'April',
        'month.may': 'Mai',
        'month.june': 'Juni',
        'month.july': 'Juli',
        'month.august': 'August',
        'month.september': 'September',
        'month.october': 'Oktober',
        'month.november': 'November',
        'month.december': 'Dezember',

        // Legal Pages - Terms
        'legal.terms.title': 'Allgemeine Geschäftsbedingungen',
        'legal.terms.updated': 'Letzte Aktualisierung:',
        'legal.terms.version': 'Ausführung',
        'legal.toc.title': 'Inhalt',
        'legal.btn.print': 'Drucken',
        'legal.btn.home': 'Zurück zur Startseite',

        // Legal Pages - Privacy
        'legal.privacy.title': 'Datenschutzerklärung',

        // WhatsApp Widget
        'whatsapp.menu.title': 'Kontaktieren Sie uns über WhatsApp',
        'whatsapp.taylor.name': 'Taylor Barrera',
        'whatsapp.taylor.desc': 'Angebote und allgemeine Fragen',
        'whatsapp.michael.name': 'Michael Barrera',
        'whatsapp.michael.desc': 'Maße und Entwürfe',

        // Voice Assistant
        'voice.activated': 'Erzähler aktiviert. Bewegen Sie die Maus über den Text, um ihn anzuhören.',
        'voice.deactivated': 'Erzähler deaktiviert.',

        // Calendar availability
        'calendar.available': 'Verfügbar',
        'calendar.notavailable': 'Nicht verfügbar',
        'calendar.past': 'Vergangenes Datum, nicht verfügbar',
        'calendar.weekend': 'Wochenende, nicht verfügbar',
        'calendar.holiday': 'Feiertag, nicht verfügbar',
        'calendar.outofrange': 'Außerhalb des verfügbaren Bereichs',

        // Meta
        'meta.backToHome': 'Zurück zur Startseite'
    }
};

// Get current language from localStorage or default to Spanish
function getCurrentLanguage() {
    return localStorage.getItem('siteLanguage') || 'es';
}

// Set language and save to localStorage
function setLanguage(lang) {
    if (!translations[lang]) {
        console.warn(`Language ${lang} not supported, falling back to Spanish`);
        lang = 'es';
    }

    localStorage.setItem('siteLanguage', lang);
    translatePage(lang);
    updateLanguageSelector(lang);

    // Dispatch custom event for other components to react to language change
    window.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
}

// Translate all elements with data-i18n attribute
function translatePage(lang) {
    const elements = document.querySelectorAll('[data-i18n]');

    elements.forEach(element => {
        const key = element.getAttribute('data-i18n');
        const translation = translations[lang][key];

        if (translation) {
            // Handle different element types
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                element.placeholder = translation;
            } else if (element.hasAttribute('title')) {
                element.title = translation;
            } else {
                element.textContent = translation;
            }
        } else {
            console.warn(`Translation key "${key}" not found for language "${lang}"`);
        }
    });

    // Update document title if present
    const titleElement = document.querySelector('[data-i18n-title]');
    if (titleElement) {
        const titleKey = titleElement.getAttribute('data-i18n-title');
        const titleTranslation = translations[lang][titleKey];
        if (titleTranslation) {
            document.title = titleTranslation + ' - Muebles Barguay';
        }
    }
}

// Update language selector visual state
function updateLanguageSelector(lang) {
    const selector = document.getElementById('languageSelector');
    if (!selector) return;

    // Update dropdown button
    const flagMap = {
        'es': '🇪🇸',
        'en': '🇬🇧',
        'de': '🇩🇪'
    };

    const nameMap = {
        'es': 'Español',
        'en': 'English',
        'de': 'Deutsch'
    };

    selector.innerHTML = `${flagMap[lang]} ${nameMap[lang]}`;

    // Update active state in dropdown
    document.querySelectorAll('.lang-option').forEach(option => {
        const optionLang = option.getAttribute('data-lang');
        if (optionLang === lang) {
            option.classList.add('active');
        } else {
            option.classList.remove('active');
        }
    });
}

// Initialize translation on page load
document.addEventListener('DOMContentLoaded', () => {
    const currentLang = getCurrentLanguage();
    translatePage(currentLang);
    updateLanguageSelector(currentLang);
});
