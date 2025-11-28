from datetime import datetime, timedelta

def generate_ics_content(cita):
    """
    Genera el contenido de un archivo .ics para una cita.
    """
    # Combinar fecha y hora
    start_dt = datetime.combine(cita.fecha, cita.hora)
    end_dt = start_dt + timedelta(hours=1) # Asumimos 1 hora de duración por defecto
    
    # Formato de fecha para iCalendar: YYYYMMDDTHHMMSS
    dt_start_str = start_dt.strftime('%Y%m%dT%H%M%S')
    dt_end_str = end_dt.strftime('%Y%m%dT%H%M%S')
    now_str = datetime.now().strftime('%Y%m%dT%H%M%SZ')
    
    # Definir ubicación
    if cita.tipo_reunion == 'online':
        location = "Google Meet / Online"
        if cita.meeting_link:
            location += f" ({cita.meeting_link})"
    else:
        # Usar la dirección exacta del taller
        location = "Av Lo Espejo 964, El Bosque, Santiago"
        
    # Descripción del evento
    description = f"Reunión con Muebles Barguay.\\nTipo: {cita.get_tipo_reunion_display()}"
    if cita.meeting_link:
        description += f"\\nLink de reunión: {cita.meeting_link}"
    
    # Construir contenido ICS
    ics_content = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Muebles Barguay//Agenda//ES",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "BEGIN:VEVENT",
        f"UID:cita-{cita.id}@mueblesbarguay.cl",
        f"DTSTAMP:{now_str}",
        f"DTSTART:{dt_start_str}",
        f"DTEND:{dt_end_str}",
        f"SUMMARY:Reunión Muebles Barguay",
        f"DESCRIPTION:{description}",
        f"LOCATION:{location}",
        "STATUS:CONFIRMED",
        "END:VEVENT",
        "END:VCALENDAR"
    ]
    
    return "\r\n".join(ics_content)
