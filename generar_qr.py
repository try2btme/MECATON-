#!/usr/bin/env python3
"""
Script para generar QR de la URL de Streamlit Cloud
Una vez que la app esté desplegada, ejecuta este script para generar el QR
"""

import sys

def generar_qr(url):
    """Genera un QR a partir de una URL"""
    try:
        import qrcode
    except ImportError:
        print("❌ No instalado: qrcode")
        print("Instala con: pip install qrcode[pil]")
        sys.exit(1)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("QR_CALCULADORA_MECATON.png")
    print(f"✅ QR generado: QR_CALCULADORA_MECATON.png")
    print(f"📱 URL codificada: {url}")

if __name__ == "__main__":
    print("🔢 GENERADOR DE QR - MECATON Calculator")
    print("=" * 50)
    print()

    url = input("Pega la URL de tu app en Streamlit Cloud:\n> ").strip()

    if not url:
        print("❌ URL vacía")
        sys.exit(1)

    if not url.startswith("http"):
        url = "https://" + url

    generar_qr(url)
    print()
    print("📲 Ahora puedes compartir el QR con tus compañeras!")
