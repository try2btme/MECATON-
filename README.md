# 🔢 Calculadora de Métodos Numéricos | MECATON 2026

Aplicación interactiva para resolver problemas usando métodos numéricos avanzados.

## 📋 Módulos

- **Ecuaciones No Lineales**: Bisección, Newton-Raphson, Punto Fijo
- **Sistemas Lineales**: Jacobi, Gauss-Seidel, LU Doolittle
- **Interpolación**: Lagrange, Newton, Splines Cúbicos
- **Integración**: Trapecio, Simpson 1/3, Simpson 3/8
- **EDOs**: Euler, RK2, RK4, Verlet, Análisis de Orden

## 🚀 Ejecución Local

```bash
pip install -r requirements.txt
streamlit run app.py
```

Abre `http://localhost:8501` en tu navegador.

## 🌐 Desplegar en Internet (Streamlit Cloud)

### 1. Subir a GitHub
```bash
git init
git add .
git commit -m "Deploy MECATON Calculator"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/MECATON-2026.git
git push -u origin main
```

### 2. Deploy en Streamlit Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Conecta tu cuenta de GitHub
3. Selecciona el repo `MECATON-2026`
4. Elige `app.py` como archivo principal
5. ¡Listo! Streamlit genera una URL pública

### 3. Generar QR
Usa una de estas herramientas:
- [qr-code-generator.com](https://www.qr-code-generator.com)
- [qrcode.tec-it.com](https://qrcode.tec-it.com)

Pega tu URL de Streamlit Cloud y genera el QR.

## 📁 Estructura

```
MECATON-2026/
├── app.py              (4277 líneas, TODO el código)
├── requirements.txt    (dependencias)
├── README.md
├── .gitignore
└── assets/
    ├── unitec_blanco.png
    └── unitec_color.png
```

## 📝 Requisitos

- Python 3.8+
- Dependencias en `requirements.txt`

## 🎓 UNITEC 2026
