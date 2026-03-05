# SSL Certificate Monitor & Email Reporter

## Descripción

**SSL Certificate Monitor** es una herramienta escrita en Python que permite verificar automáticamente la fecha de expiración de certificados SSL/TLS de múltiples dominios y generar un reporte profesional enviado por correo electrónico.

Esta herramienta está diseñada para equipos de **infraestructura, ciberseguridad, SOC, NOC y administración de sistemas**, permitiendo monitorear certificados antes de que expiren y evitar interrupciones de servicio.

El sistema realiza las siguientes tareas:

* Lee una lista de dominios desde un archivo `.txt`
* Obtiene el certificado SSL de cada dominio
* Calcula los días restantes antes de la expiración
* Clasifica el estado del certificado
* Genera un reporte profesional en formato HTML
* Envía el reporte automáticamente por correo electrónico

---

# Características

* Monitoreo de certificados SSL/TLS
* Soporte para múltiples dominios
* Reporte en formato HTML profesional
* Envío automático por correo
* Compatible con Linux y Windows
* Fácil integración con cron o Task Scheduler
* Código simple y extensible

---

# Requisitos

### Software requerido

* Python 3.9 o superior
* Acceso a Internet
* Cuenta SMTP (ej. Gmail)

Verificar instalación de Python:

```bash
python --version
```

o

```bash
python3 --version
```

---

# Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/ssl-certificate-monitor.git
```

Entrar al directorio:

```bash
cd ssl-certificate-monitor
```

---

## 2. Crear archivo de dominios

Crear un archivo llamado:

```
urls.txt
```

Ejemplo:

```
https://ejemplo.com

```

Cada dominio debe ir en una línea.

---

## 3. Configurar credenciales de correo

Editar el archivo del script:

```
ssl_reporte_mail.py
```

Buscar la sección:

```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_REMITENTE = "tu_correo@gmail.com"
EMAIL_PASSWORD = "APP_PASSWORD"

EMAIL_DESTINOS = [
    "destinatario1@empresa.com",
    "destinatario2@empresa.com"
]
```

### Importante

Para Gmail se recomienda usar **App Password**.

Crear App Password:

https://myaccount.google.com/apppasswords

---

# Uso

Ejecutar el script indicando el archivo de dominios.

## Linux

```bash
python3 ssl_reporte_mail.py urls.txt
```

## Windows

```powershell
python ssl_reporte_mail.py urls.txt
```

---

# Ejemplo de salida en consola

```
Analizando certificados...

ejemplo.com

Generando reporte...

Reporte enviado correctamente.
```

---

# Ejemplo de correo recibido

Asunto:

```
Reporte de Certificados SSL
```

Contenido:

| Dominio                                                     | Fecha Expiración | Días Restantes | Estado  |
| ----------------------------------------------------------- | ---------------- | -------------- | ------- |
| dominioejemplo                                              | 2027-02-04       | 336            | Vigente |
| ejemplo.com                                                 | 2026-08-20       | 168            | Vigente |
| gmail                                                       | 2026-07-07       | 124            | Vigente |

Estados posibles:

| Estado            | Significado                    |
| ----------------- | ------------------------------ |
| Vigente           | Certificado válido             |
| Próximo a expirar | Expira en menos de 30 días     |
| Expirado          | Certificado vencido            |
| Error             | No se pudo obtener certificado |

---

# Automatización

## Linux (Cron)

Editar cron:

```bash
crontab -e
```

Ejemplo ejecutar diariamente:

```bash
0 9 * * * /usr/bin/python3 /ruta/ssl_reporte_mail.py /ruta/urls.txt
```

Esto ejecutará el script todos los días a las **09:00 AM**.

---

## Windows (Task Scheduler)

1. Abrir **Task Scheduler**
2. Crear nueva tarea
3. Acción → Start a program
4. Programa:

```
python
```

Argumentos:

```
C:\ruta\ssl_reporte_mail.py C:\ruta\urls.txt
```

---

# Estructura del proyecto

```
ssl-certificate-monitor/
│
├── ssl_reporte_mail.py
├── urls.txt
├── README.md
└── LICENSE
```

---

# Seguridad

Recomendaciones importantes:

* No subir credenciales SMTP a GitHub
* Usar variables de entorno
* Usar App Password en lugar de contraseña real
* Restringir acceso al script

Ejemplo usando variables de entorno:

Linux:

```bash
export EMAIL_PASSWORD="tu_password"
```

Windows:

```powershell
setx EMAIL_PASSWORD "tu_password"
```

---

# Solución de problemas

## Error SMTPRecipientsRefused

Significa que los correos no están separados correctamente.

Incorrecto:

```
correo1@empresa.comcorreo2@empresa.com
```

Correcto:

```python
EMAIL_DESTINOS = [
    "correo1@empresa.com",
    "correo2@empresa.com"
]
```

---

## Error de conexión SSL

Verificar:

* Conectividad a Internet
* Firewall
* Dominio válido

---

## Warning datetime.utcnow()

Python 3.13 deprecó `utcnow()`.

Se recomienda usar:

```python
from datetime import datetime, UTC
datetime.now(UTC)
```

---

# Mejoras futuras

Posibles mejoras:

* Exportar reporte a CSV
* Exportar reporte a PDF
* Dashboard web
* Multithreading
* Integración con SIEM
* Notificaciones Slack o Teams
* Historial de certificados
* API REST

---

# Contribuciones

Pull requests y mejoras son bienvenidas.

Flujo recomendado:

```
fork → branch → commit → pull request
```

---

# Licencia

MIT License

---

# Autor

Proyecto desarrollado para monitoreo de certificados SSL en entornos de infraestructura y seguridad.

---

# Contacto

Para mejoras o dudas:

```
ale609jandro609@gmail.com
```
