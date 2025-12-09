// ============================================
// MULTI-LANGUAGE TRANSLATION SYSTEM
// Pure JavaScript - No Server Dependencies
// ============================================

const translations = {
    es: {
        // Navbar
        'nav.faq': 'Preguntas',
        'nav.terms': 'Términos & Condiciones',
        'nav.privacy': 'Política de Privacidad',

        // Footer
        'footer.rights': 'Todos los derechos reservados',
        'footer.terms': 'Términos y Condiciones',
        'footer.privacy': 'Política de Privacidad',

        // Homepage
        'home.title': 'Portada',
        'home.schedule': 'Agendar Reunión',
        'home.quote': 'Proyectos',

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

        // FAQ Page
        'faq.hero.title': 'Preguntas Frecuentes',
        'faq.hero.subtitle': 'Encuentra respuestas a las preguntas más comunes sobre nuestros muebles y servicios',
        'faq.category.general': 'General',
        'faq.category.quotes': 'Cotizaciones',
        'faq.category.delivery': 'Entrega e Instalación',
        'faq.category.warranty': 'Garantía y Mantenimiento',
        'faq.general.q1': '¿Qué tipo de muebles fabrican?',
        'faq.general.a1': 'Fabricamos todo tipo de muebles a medida: cocinas integrales, closets, muebles de baño, escritorios, bibliotecas, muebles de TV, y más. Nos especializamos en muebles modulares que se adaptan perfectamente a tu espacio.',
        'faq.general.q2': '¿Hacen muebles a medida?',
        'faq.general.a2': 'Sí, todos nuestros muebles son diseñados y fabricados a medida según tus necesidades específicas. Nos adaptamos al espacio disponible y a tus preferencias de diseño y funcionalidad.',
        'faq.general.q3': '¿Cuánto tiempo toma fabricar un mueble?',
        'faq.general.a3': 'El tiempo de fabricación varía según la complejidad del mueble. Generalmente, un proyecto promedio toma entre 15 a 30 días hábiles desde la aprobación del diseño hasta la instalación. Proyectos más grandes pueden tomar más tiempo.',
        'faq.general.q4': '¿En qué zonas trabajan?',
        'faq.general.a4': 'Atendemos principalmente en la Región Metropolitana de Santiago y alrededores. Para proyectos en otras regiones, contáctanos para evaluar la viabilidad.',
        'faq.quotes.q1': '¿Cómo solicito una cotización?',
        'faq.quotes.a1': 'Puedes solicitar una cotización de tres formas: (1) a través de nuestro catálogo en línea haciendo clic en "Cotizar", (2) agendando una reunión con nuestros diseñadores, o (3) contactándonos directamente por WhatsApp.',
        'faq.quotes.q2': '¿La cotización tiene costo?',
        'faq.quotes.a2': 'No, nuestras cotizaciones son completamente gratuitas y sin compromiso. Queremos que puedas tomar la mejor decisión para tu proyecto.',
        'faq.quotes.q3': '¿Cuánto demoran en responder una cotización?',
        'faq.quotes.a3': 'Generalmente respondemos cotizaciones en un plazo de 24 a 48 horas hábiles. Para proyectos más complejos que requieren diseño personalizado, podría tomar un poco más de tiempo.',
        'faq.quotes.q4': '¿Puedo modificar mi cotización?',
        'faq.quotes.a4': 'Sí, puedes solicitar modificaciones a tu cotización antes de aprobarla. Una vez aprobada y en producción, los cambios pueden generar costos adicionales.',
        'faq.delivery.q1': '¿Incluyen entrega e instalación?',
        'faq.delivery.a1': 'Sí, todos nuestros muebles incluyen entrega e instalación profesional sin costo adicional dentro de la Región Metropolitana. Para otras regiones, consulta costo de envío.',
        'faq.delivery.q2': '¿Cuánto demora la instalación?',
        'faq.delivery.a2': 'La instalación típicamente toma entre 4 a 8 horas dependiendo de la complejidad del mueble. Para proyectos grandes como cocinas completas, puede tomar 1-2 días.',
        'faq.delivery.q3': '¿Puedo elegir la fecha de instalación?',
        'faq.delivery.a3': 'Sí, una vez que tu mueble esté listo, coordinamos contigo la fecha más conveniente para la instalación dentro de nuestra agenda disponible.',
        'faq.warranty.q1': '¿Los muebles tienen garantía?',
        'faq.warranty.a1': 'Sí, todos nuestros muebles cuentan con 12 meses de garantía contra defectos de fabricación. La garantía cubre mano de obra y materiales.',
        'faq.warranty.q2': '¿Qué cubre la garantía?',
        'faq.warranty.a2': 'La garantía cubre defectos de fabricación, fallas en herrajes y bisagras, desprendimiento de enchapados, y problemas estructurales. No cubre daños por mal uso, desgaste natural o accidentes.',
        'faq.warranty.q3': '¿Ofrecen servicio de mantenimiento?',
        'faq.warranty.a3': 'Sí, ofrecemos servicio de mantenimiento y reparación post-garantía. Contáctanos para agendar una revisión o reparación de tu mueble.',
        'faq.warranty.q4': '¿Qué materiales utilizan?',
        'faq.warranty.a4': 'Trabajamos con materiales de primera calidad: melamina, MDF, madera maciza, vidrios templados, herrajes de marca reconocida, y acabados de alta durabilidad. Te asesoramos en la mejor opción según tu presupuesto y necesidades.',
        'faq.cta.title': '¿No encontraste tu respuesta?',
        'faq.cta.message': 'Estamos aquí para ayudarte. Contáctanos directamente',
        'faq.cta.schedule': 'Agendar Reunión',

        // Meta
        'meta.backToHome': 'Volver al inicio'
    },
    en: {
        // Navbar
        'nav.faq': 'Questions',
        'nav.terms': 'Terms & Conditions',
        'nav.privacy': 'Privacy Policy',

        // Footer
        'footer.rights': 'All rights reserved',
        'footer.terms': 'Terms and Conditions',
        'footer.privacy': 'Privacy Policy',

        // Homepage
        'home.title': 'Home',
        'home.schedule': 'Book Meeting',
        'home.quote': 'Projects',

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

        // FAQ Page
        'faq.hero.title': 'Frequently Asked Questions',
        'faq.hero.subtitle': 'Find answers to the most common questions about our furniture and services',
        'faq.category.general': 'General',
        'faq.category.quotes': 'Quotes',
        'faq.category.delivery': 'Delivery & Installation',
        'faq.category.warranty': 'Warranty & Maintenance',
        'faq.general.q1': 'What type of furniture do you make?',
        'faq.general.a1': 'We manufacture all types of custom furniture: fitted kitchens, closets, bathroom furniture, desks, bookcases, TV units, and more. We specialize in modular furniture that adapts perfectly to your space.',
        'faq.general.q2': 'Do you make custom furniture?',
        'faq.general.a2': 'Yes, all our furniture is designed and manufactured to measure according to your specific needs. We adapt to the available space and your design and functionality preferences.',
        'faq.general.q3': 'How long does it take to manufacture a piece of furniture?',
        'faq.general.a3': 'Manufacturing time varies depending on the complexity of the furniture. Generally, an average project takes between 15 to 30 business days from design approval to installation. Larger projects may take longer.',
        'faq.general.q4': 'What areas do you work in?',
        'faq.general.a4': 'We mainly serve the Metropolitan Region of Santiago and surroundings. For projects in other regions, contact us to assess feasibility.',
        'faq.quotes.q1': 'How do I request a quote?',
        'faq.quotes.a1': 'You can request a quote in three ways: (1) through our online catalog by clicking "Get Quote", (2) scheduling a meeting with our designers, or (3) contacting us directly via WhatsApp.',
        'faq.quotes.q2': 'Does the quote have a cost?',
        'faq.quotes.a2': 'No, our quotes are completely free and without obligation. We want you to be able to make the best decision for your project.',
        'faq.quotes.q3': 'How long does it take to respond to a quote?',
        'faq.quotes.a3': 'We generally respond to quotes within 24 to 48 business hours. For more complex projects that require custom design, it may take a bit longer.',
        'faq.quotes.q4': 'Can I modify my quote?',
        'faq.quotes.a4': 'Yes, you can request modifications to your quote before approving it. Once approved and in production, changes may generate additional costs.',
        'faq.delivery.q1': 'Do you include delivery and installation?',
        'faq.delivery.a1': 'Yes, all our furniture includes professional delivery and installation at no additional cost within the Metropolitan Region. For other regions, consult shipping cost.',
        'faq.delivery.q2': 'How long does installation take?',
        'faq.delivery.a2': 'Installation typically takes between 4 to 8 hours depending on the complexity of the furniture. For large projects like complete kitchens, it may take 1-2 days.',
        'faq.delivery.q3': 'Can I choose the installation date?',
        'faq.delivery.a3': 'Yes, once your furniture is ready, we coordinate with you the most convenient date for installation within our available schedule.',
        'faq.warranty.q1': 'Does the furniture have a warranty?',
        'faq.warranty.a1': 'Yes, all our furniture has a 12-month warranty against manufacturing defects. The warranty covers labor and materials.',
        'faq.warranty.q2': 'What does the warranty cover?',
        'faq.warranty.a2': 'The warranty covers manufacturing defects, failures in hardware and hinges, veneer detachment, and structural problems. It does not cover damage from misuse, natural wear or accidents.',
        'faq.warranty.q3': 'Do you offer maintenance service?',
        'faq.warranty.a3': 'Yes, we offer post-warranty maintenance and repair service. Contact us to schedule a review or repair of your furniture.',
        'faq.warranty.q4': 'What materials do you use?',
        'faq.warranty.a4': 'We work with top quality materials: melamine, MDF, solid wood, tempered glass, branded hardware, and high durability finishes. We advise you on the best option according to your budget and needs.',
        'faq.cta.title': 'Didn\'t find your answer?',
        'faq.cta.message': 'We are here to help you. Contact us directly',
        'faq.cta.schedule': 'Book Meeting',

        // Meta
        'meta.backToHome': 'Back to home'
    },
    de: {
        // Navbar
        'nav.faq': 'Fragen',
        'nav.terms': 'Allgemeine Geschäftsbedingungen',
        'nav.privacy': 'Datenschutzerklärung',

        // Footer
        'footer.rights': 'Alle Rechte vorbehalten',
        'footer.terms': 'Allgemeine Geschäftsbedingungen',
        'footer.privacy': 'Datenschutzerklärung',

        // Homepage
        'home.title': 'Startseite',
        'home.schedule': 'Termin vereinbaren',
        'home.quote': 'Projekte',

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

        // FAQ Page
        'faq.hero.title': 'Häufig gestellte Fragen',
        'faq.hero.subtitle': 'Finden Sie Antworten auf die häufigsten Fragen zu unseren Möbeln und Dienstleistungen',
        'faq.category.general': 'Allgemein',
        'faq.category.quotes': 'Angebote',
        'faq.category.delivery': 'Lieferung & Installation',
        'faq.category.warranty': 'Garantie & Wartung',
        'faq.general.q1': 'Welche Art von Möbeln stellen Sie her?',
        'faq.general.a1': 'Wir fertigen alle Arten von maßgefertigten Möbeln: Einbauküchen, Schränke, Badezimmermöbel, Schreibtische, Bücherregale, TV-Möbel und mehr. Wir sind spezialisiert auf modulare Möbel, die sich perfekt an Ihren Raum anpassen.',
        'faq.general.q2': 'Fertigen Sie Möbel nach Maß?',
        'faq.general.a2': 'Ja, alle unsere Möbel werden nach Maß nach Ihren spezifischen Bedürfnissen entworfen und gefertigt. Wir passen uns an den verfügbaren Raum und Ihre Design- und Funktionalitätspräferenzen an.',
        'faq.general.q3': 'Wie lange dauert es, ein Möbelstück herzustellen?',
        'faq.general.a3': 'Die Herstellungszeit variiert je nach Komplexität der Möbel. Im Allgemeinen dauert ein durchschnittliches Projekt zwischen 15 und 30 Werktagen von der Designgenehmigung bis zur Installation. Größere Projekte können länger dauern.',
        'faq.general.q4': 'In welchen Bereichen arbeiten Sie?',
        'faq.general.a4': 'Wir bedienen hauptsächlich die Metropolregion Santiago und Umgebung. Für Projekte in anderen Regionen kontaktieren Sie uns bitte, um die Machbarkeit zu prüfen.',
        'faq.quotes.q1': 'Wie fordere ich ein Angebot an?',
        'faq.quotes.a1': 'Sie können ein Angebot auf drei Wegen anfordern: (1) über unseren Online-Katalog durch Klicken auf "Angebot anfordern", (2) durch Vereinbarung eines Termins mit unseren Designern oder (3) durch direkten Kontakt über WhatsApp.',
        'faq.quotes.q2': 'Kostet das Angebot etwas?',
        'faq.quotes.a2': 'Nein, unsere Angebote sind völlig kostenlos und unverbindlich. Wir möchten, dass Sie die beste Entscheidung für Ihr Projekt treffen können.',
        'faq.quotes.q3': 'Wie lange dauert es, auf ein Angebot zu antworten?',
        'faq.quotes.a3': 'Wir antworten in der Regel innerhalb von 24 bis 48 Werktunden auf Angebote. Für komplexere Projekte, die ein individuelles Design erfordern, kann es etwas länger dauern.',
        'faq.quotes.q4': 'Kann ich mein Angebot ändern?',
        'faq.quotes.a4': 'Ja, Sie können vor der Genehmigung Änderungen an Ihrem Angebot anfordern. Nach Genehmigung und in Produktion können Änderungen zusätzliche Kosten verursachen.',
        'faq.delivery.q1': 'Sind Lieferung und Installation inbegriffen?',
        'faq.delivery.a1': 'Ja, alle unsere Möbel beinhalten professionelle Lieferung und Installation ohne zusätzliche Kosten innerhalb der Metropolregion. Für andere Regionen fragen Sie bitte nach den Versandkosten.',
        'faq.delivery.q2': 'Wie lange dauert die Installation?',
        'faq.delivery.a2': 'Die Installation dauert in der Regel zwischen 4 und 8 Stunden, abhängig von der Komplexität der Möbel. Für große Projekte wie komplette Küchen kann es 1-2 Tage dauern.',
        'faq.delivery.q3': 'Kann ich das Installationsdatum wählen?',
        'faq.delivery.a3': 'Ja, sobald Ihre Möbel fertig sind, koordinieren wir mit Ihnen das günstigste Datum für die Installation innerhalb unseres verfügbaren Zeitplans.',
        'faq.warranty.q1': 'Haben die Möbel eine Garantie?',
        'faq.warranty.a1': 'Ja, alle unsere Möbel haben eine 12-monatige Garantie gegen Herstellungsfehler. Die Garantie deckt Arbeit und Materialien ab.',
        'faq.warranty.q2': 'Was deckt die Garantie ab?',
        'faq.warranty.a2': 'Die Garantie deckt Herstellungsfehler, Ausfälle von Beschlägen und Scharnieren, Ablösung von Furnieren und strukturelle Probleme ab. Sie deckt keine Schäden durch Missbrauch, natürliche Abnutzung oder Unfälle ab.',
        'faq.warranty.q3': 'Bieten Sie Wartungsservice an?',
        'faq.warranty.a3': 'Ja, wir bieten Wartungs- und Reparaturservice nach Garantieablauf an. Kontaktieren Sie uns, um eine Überprüfung oder Reparatur Ihrer Möbel zu vereinbaren.',
        'faq.warranty.q4': 'Welche Materialien verwenden Sie?',
        'faq.warranty.a4': 'Wir arbeiten mit hochwertigen Materialien: Melamin, MDF, Massivholz, Sicherheitsglas, Markenbeschläge und hochwertige Oberflächen. Wir beraten Sie über die beste Option entsprechend Ihrem Budget und Ihren Bedürfnissen.',
        'faq.cta.title': 'Haben Sie Ihre Antwort nicht gefunden?',
        'faq.cta.message': 'Wir sind hier, um Ihnen zu helfen. Kontaktieren Sie uns direkt',
        'faq.cta.schedule': 'Termin vereinbaren',

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
        'es': 'ES',
        'en': 'EN',
        'de': 'DE'
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
