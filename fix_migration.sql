-- Agregar columnas faltantes a la base de datos MySQL
-- Add field admin_notas to cita
ALTER TABLE `cotizaciones_cita` ADD COLUMN `admin_notas` longtext NOT NULL DEFAULT '';

-- Add field fecha_aprobacion to cita
ALTER TABLE `cotizaciones_cita` ADD COLUMN `fecha_aprobacion` datetime(6) NULL;

-- Add field fecha_aprobacion to cotizacion
ALTER TABLE `cotizaciones_cotizacion` ADD COLUMN `fecha_aprobacion` datetime(6) NULL;

-- Alter field estado on cita
ALTER TABLE `cotizaciones_cita` MODIFY `estado` varchar(25) NOT NULL;

-- Alter field estado on cotizacion
ALTER TABLE `cotizaciones_cotizacion` MODIFY `estado` varchar(25) NOT NULL;
