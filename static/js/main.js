/**
 * main.js - JavaScript Principal de webMuebles
 * Optimizado para rendimiento, accesibilidad y cumplimiento de CSP.
 */

// --- Variables de Estado ---
let voiceEnabled = false;
const synthesis = window.speechSynthesis;

// --- Funciones de Utilidad y Throttling ---
let ticking = false;

function handleScrollResize() {
    if (!ticking) {
        window.requestAnimationFrame(() => {
            adjustFloatingWidgets();
            ticking = false;
        });
        ticking = true;
    }
}

// --- WhatsApp Widget Menu ---
function toggleWhatsAppMenu() {
    const menu = document.getElementById('whatsapp-options');
    const btn = document.getElementById('whatsapp-btn');
    if (!menu) return;
    const isHidden = menu.style.display === 'none' || menu.style.display === '';

    if (isHidden) {
        menu.style.display = 'block';
        if (btn) btn.style.opacity = '0.5';
    } else {
        menu.style.display = 'none';
        if (btn) btn.style.opacity = '1';
    }
}

// --- Ajuste de Posición de Widgets Flotantes (Optimizado con rAF) ---
function adjustFloatingWidgets() {
    const footer = document.querySelector('.site-footer');
    const whatsappWidget = document.getElementById('whatsapp-widget');
    const accessibilityWidget = document.getElementById('accessibility-wrapper');

    if (!footer) return;

    const footerRect = footer.getBoundingClientRect();
    const windowHeight = window.innerHeight;
    const baseBottom = 20;

    if (footerRect.top < windowHeight) {
        const offset = windowHeight - footerRect.top + 20;
        if (whatsappWidget) {
            whatsappWidget.style.bottom = offset + 'px';
        }
        if (accessibilityWidget) {
            accessibilityWidget.style.bottom = offset + 'px';
        }
    } else {
        if (whatsappWidget) {
            whatsappWidget.style.bottom = baseBottom + 'px';
        }
        if (accessibilityWidget) {
            accessibilityWidget.style.bottom = baseBottom + 'px';
        }
    }
}

// --- Funciones de Accesibilidad ---
function toggleAccessibilityMenu() {
    const menu = document.getElementById('accessibility-menu');
    if (!menu) return;
    if (menu.style.display === 'none' || menu.style.display === '') {
        menu.style.display = 'block';
    } else {
        menu.style.display = 'none';
    }
}

function adjustFontSize(change) {
    const html = document.documentElement;
    let currentSize = parseFloat(window.getComputedStyle(html).fontSize);
    if (isNaN(currentSize)) currentSize = 16;
    let newSize = currentSize + change;
    if (newSize < 12) newSize = 12;
    if (newSize > 28) newSize = 28;
    html.style.fontSize = newSize + 'px';
    localStorage.setItem('userFontSize', newSize);
}

function toggleHighContrast() {
    document.body.classList.toggle('high-contrast');
    const isHighContrast = document.body.classList.contains('high-contrast');
    localStorage.setItem('highContrast', isHighContrast);

    const btn = document.getElementById('contrast-toggle');
    if (btn) {
        if (isHighContrast) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    }
}

function toggleVoice(forceEnable = false) {
    if (!forceEnable) {
        voiceEnabled = !voiceEnabled;
    } else {
        voiceEnabled = true;
    }

    const btn = document.getElementById('voice-toggle');
    const currentLang = (typeof getCurrentLanguage === 'function') ? getCurrentLanguage() : 'es';

    // check if translations exists
    const translationsMap = (window.translations && window.translations[currentLang]) ? window.translations[currentLang] : {};

    if (voiceEnabled) {
        if (btn) {
            btn.classList.add('active');
            btn.innerHTML = '<span>Narrador</span><i class="bi bi-mic-fill"></i>';
        }
        const activatedMsg = translationsMap['voice.activated'] || 'Narrador activado.';
        speak(activatedMsg, currentLang);
        localStorage.setItem('voiceEnabled', 'true');
    } else {
        if (btn) {
            btn.classList.remove('active');
            btn.innerHTML = '<span>Narrador</span><i class="bi bi-volume-up-fill"></i>';
        }
        if (synthesis) synthesis.cancel();
        const deactivatedMsg = translationsMap['voice.deactivated'] || 'Narrador desactivado.';
        speak(deactivatedMsg, currentLang);
        localStorage.setItem('voiceEnabled', 'false');
    }
}

function resetAccessibility() {
    // Reset Font Size
    document.documentElement.style.fontSize = '16px';
    localStorage.removeItem('userFontSize');

    // Reset High Contrast
    document.body.classList.remove('high-contrast');
    localStorage.removeItem('highContrast');
    const contrastBtn = document.getElementById('contrast-toggle');
    if (contrastBtn) contrastBtn.classList.remove('active');

    // Reset Voice
    if (voiceEnabled) {
        toggleVoice(); // Desactivar narrador
    }
    localStorage.removeItem('voiceEnabled');

    // Close menu
    const menu = document.getElementById('accessibility-menu');
    if (menu) menu.style.display = 'none';
}

function speak(text, lang) {
    if (!text || !synthesis) return;
    synthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);

    const langMap = {
        'es': 'es-ES',
        'en': 'en-US',
        'de': 'de-DE'
    };

    const currentLang = lang || ((typeof getCurrentLanguage === 'function') ? getCurrentLanguage() : 'es');
    utterance.lang = langMap[currentLang] || 'es-ES';
    synthesis.speak(utterance);
}

function handleInteraction(event) {
    if (!voiceEnabled) return;
    const target = event.target;

    const readableTags = ['P', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'A', 'BUTTON', 'LABEL', 'SPAN', 'LI', 'TD', 'TH', 'DIV', 'IMG'];

    if (readableTags.includes(target.tagName)) {
        let text = target.innerText || target.textContent;
        if (target.tagName === 'IMG' && target.alt) text = "Imagen: " + target.alt;

        if (target.tagName === 'DIV') {
            const isCalendarElement = target.classList.contains('calendar-day') ||
                target.classList.contains('calendar-header') ||
                target.classList.contains('calendar-month-title');
            const isFAQAnswer = target.classList.contains('accordion-body');

            if (!isCalendarElement && !isFAQAnswer && text.length > 200) {
                return;
            }
        }

        if (text && text.trim().length > 0 && text.trim().length < 1000) {
            const currentLang = (typeof getCurrentLanguage === 'function') ? getCurrentLanguage() : 'es';
            document.querySelectorAll('.speaking-highlight').forEach(el => el.classList.remove('speaking-highlight'));
            target.classList.add('speaking-highlight');
            speak(text, currentLang);
            target.addEventListener('mouseleave', () => {
                target.classList.remove('speaking-highlight');
                if (synthesis) synthesis.cancel();
            }, { once: true });
        }
    }
}

// --- Cookie Consent ---
function checkCookieConsent() {
    const consent = localStorage.getItem('cookieConsent');
    const consentDate = localStorage.getItem('cookieConsentDate');

    if (!consent || !consentDate) {
        setTimeout(() => {
            const banner = document.getElementById('cookie-banner');
            if (banner) banner.style.display = 'block';
        }, 1000);
    } else {
        const daysSinceConsent = (Date.now() - parseInt(consentDate)) / (1000 * 60 * 60 * 24);
        if (daysSinceConsent > 365) {
            localStorage.removeItem('cookieConsent');
            localStorage.removeItem('cookieConsentDate');
            const banner = document.getElementById('cookie-banner');
            if (banner) banner.style.display = 'block';
        }
    }
}

function acceptCookies() {
    localStorage.setItem('cookieConsent', 'accepted');
    localStorage.setItem('cookieConsentDate', Date.now().toString());
    const banner = document.getElementById('cookie-banner');
    if (banner) banner.style.display = 'none';
    console.log('Cookies aceptadas');
}

function rejectCookies() {
    localStorage.setItem('cookieConsent', 'rejected');
    localStorage.setItem('cookieConsentDate', Date.now().toString());
    const banner = document.getElementById('cookie-banner');
    if (banner) banner.style.display = 'none';
    console.log('Cookies rechazadas - solo cookies esenciales');
}

// --- Inicialización y Event Listeners ---
(function () {
    const savedSize = localStorage.getItem('userFontSize');
    if (savedSize) document.documentElement.style.fontSize = savedSize + 'px';
})();

document.addEventListener('DOMContentLoaded', function () {
    // 1. Restaurar configuraciones previas
    if (localStorage.getItem('highContrast') === 'true') {
        document.body.classList.add('high-contrast');
        const btn = document.getElementById('contrast-toggle');
        if (btn) btn.classList.add('active');
    }

    if (localStorage.getItem('voiceEnabled') === 'true') {
        toggleVoice(true);
    }

    checkCookieConsent();
    adjustFloatingWidgets();

    // 2. Vincular Eventos de WhatsApp
    const whatsappBtn = document.getElementById('whatsapp-btn');
    if (whatsappBtn) {
        whatsappBtn.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            toggleWhatsAppMenu();
        });
    }

    // 3. Vincular Eventos de Selección de Idioma
    document.querySelectorAll('.lang-option').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const lang = this.getAttribute('data-lang');
            if (typeof setLanguage === 'function') {
                setLanguage(lang);
            }
        });
    });

    // 4. Vincular Eventos de Accesibilidad
    const accessibilityToggle = document.getElementById('accessibility-toggle');
    if (accessibilityToggle) {
        accessibilityToggle.addEventListener('click', toggleAccessibilityMenu);
    }

    const accessibilityClose = document.getElementById('accessibility-close');
    if (accessibilityClose) {
        accessibilityClose.addEventListener('click', toggleAccessibilityMenu);
    }

    const decFontBtn = document.getElementById('accessibility-dec-font');
    if (decFontBtn) {
        decFontBtn.addEventListener('click', () => adjustFontSize(-1));
    }

    const incFontBtn = document.getElementById('accessibility-inc-font');
    if (incFontBtn) {
        incFontBtn.addEventListener('click', () => adjustFontSize(1));
    }

    const contrastToggle = document.getElementById('contrast-toggle');
    if (contrastToggle) {
        contrastToggle.addEventListener('click', toggleHighContrast);
    }

    const voiceToggle = document.getElementById('voice-toggle');
    if (voiceToggle) {
        voiceToggle.addEventListener('click', () => toggleVoice());
    }

    const accessibilityReset = document.getElementById('accessibility-reset');
    if (accessibilityReset) {
        accessibilityReset.addEventListener('click', resetAccessibility);
    }

    // 5. Vincular Eventos de Cookies
    const cookieAccept = document.getElementById('cookie-accept');
    if (cookieAccept) {
        cookieAccept.addEventListener('click', acceptCookies);
    }

    const cookieReject = document.getElementById('cookie-reject');
    if (cookieReject) {
        cookieReject.addEventListener('click', rejectCookies);
    }

    // 6. Eventos de Cierre con Click Externo
    document.addEventListener('click', function (event) {
        const widget = document.getElementById('whatsapp-widget');
        const menu = document.getElementById('whatsapp-options');
        const btn = document.getElementById('whatsapp-btn');
        if (widget && menu && !widget.contains(event.target) && menu.style.display === 'block') {
            menu.style.display = 'none';
            if (btn) btn.style.opacity = '1';
        }

        const accWrapper = document.getElementById('accessibility-wrapper');
        const accMenu = document.getElementById('accessibility-menu');
        if (accWrapper && accMenu && !accWrapper.contains(event.target) && accMenu.style.display === 'block') {
            accMenu.style.display = 'none';
        }
    });

    // 7. Eventos de Narrador por Hover/Enfoque
    document.addEventListener('mouseover', handleInteraction);
    document.addEventListener('focus', handleInteraction, true);

    // 8. Eventos de Scroll y Resize Optimizados
    window.addEventListener('scroll', handleScrollResize, { passive: true });
    window.addEventListener('resize', handleScrollResize, { passive: true });
});
