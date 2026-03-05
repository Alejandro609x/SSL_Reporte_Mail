#!/usr/bin/env python3

import ssl
import socket
import smtplib
import platform
from urllib.parse import urlparse
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys


# CONFIGURACION SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_REMITENTE = "usuario@gmail.com"
EMAIL_PASSWORD = "codigode16"

EMAIL_DESTINOS = [
    "usuario@dominio",
    "usuario@dominio"
]


def obtener_hostname(url):

    if not url.startswith("http"):
        url = "https://" + url

    parsed = urlparse(url)

    return parsed.hostname


def obtener_certificado(hostname):

    try:

        contexto = ssl.create_default_context()

        with socket.create_connection((hostname, 443), timeout=10) as sock:
            with contexto.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        fecha_exp = cert['notAfter']

        fecha_exp = datetime.strptime(
            fecha_exp,
            "%b %d %H:%M:%S %Y %Z"
        )

        hoy = datetime.utcnow()

        dias = (fecha_exp - hoy).days

        if dias < 0:
            estado = "EXPIRADO"
        elif dias <= 30:
            estado = "ALERTA"
        else:
            estado = "OK"

        return fecha_exp.strftime("%Y-%m-%d"), dias, estado

    except Exception:

        return "ERROR", "N/A", "ERROR"


def leer_urls(archivo):

    urls = []

    with open(archivo, "r") as f:

        for linea in f:

            linea = linea.strip()

            if linea:
                urls.append(linea)

    return urls


def generar_reporte_html(resultados):

    fecha = datetime.now()

    html = f"""
    <html>
    <body style="font-family: Arial;">

    <h2 style="color:#2F5597;">
    Reporte de Certificados SSL
    </h2>

    <p>
    <b>Fecha de análisis:</b> {fecha}<br>
    <b>Sistema:</b> {platform.system()}
    </p>

    <table border="1" cellpadding="8" cellspacing="0"
    style="border-collapse: collapse;">

        <tr style="background-color:#2F5597;color:white;">
            <th>Dominio</th>
            <th>Fecha de Expiración</th>
            <th>Días Restantes</th>
            <th>Estado</th>
        </tr>
    """

    for host, fecha_exp, dias, estado in resultados:

        if estado == "OK":
            color = "#C6EFCE"
            texto_estado = "Vigente"

        elif estado == "ALERTA":
            color = "#FFEB9C"
            texto_estado = "Próximo a expirar"

        elif estado == "EXPIRADO":
            color = "#FFC7CE"
            texto_estado = "Expirado"

        else:
            color = "#D9D9D9"
            texto_estado = "Error"

        html += f"""
        <tr>
            <td>{host}</td>
            <td align="center">{fecha_exp}</td>
            <td align="center">{dias}</td>
            <td bgcolor="{color}" align="center">
            <b>{texto_estado}</b>
            </td>
        </tr>
        """

    html += """
    </table>

    <br>

    <p style="font-size:12px;color:gray;">
    Este reporte fue generado automáticamente por el sistema de monitoreo
    de certificados SSL.
    </p>

    </body>
    </html>
    """

    return html


def enviar_correo(reporte_html):

    mensaje = MIMEMultipart()

    mensaje["From"] = EMAIL_REMITENTE
    mensaje["To"] = ", ".join(EMAIL_DESTINOS)

    mensaje["Subject"] = "Reporte de Certificados SSL"

    mensaje.attach(MIMEText(reporte_html, "html"))

    servidor = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

    servidor.starttls()

    servidor.login(EMAIL_REMITENTE, EMAIL_PASSWORD)

    servidor.sendmail(
        EMAIL_REMITENTE,
        EMAIL_DESTINOS,
        mensaje.as_string()
    )

    servidor.quit()


def main():

    if len(sys.argv) != 2:

        print("Uso:")
        print("python reporte_ssl_correo.py urls.txt")

        sys.exit(1)

    archivo = sys.argv[1]

    urls = leer_urls(archivo)

    resultados = []

    for url in urls:

        host = obtener_hostname(url)

        fecha, dias, estado = obtener_certificado(host)

        resultados.append(
            (host, fecha, dias, estado)
        )

    reporte_html = generar_reporte_html(resultados)

    enviar_correo(reporte_html)

    print("\nReporte enviado correctamente.")


if __name__ == "__main__":
    main()
