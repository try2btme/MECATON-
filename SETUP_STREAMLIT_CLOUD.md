# 🌐 Guía: Desplegar en Streamlit Cloud (5 minutos)

## Paso 1️⃣: Crear repo en GitHub

1. Ve a [github.com/new](https://github.com/new)
2. Crea un repo llamado `MECATON-2026` (puede ser público o privado)
3. **NO** inicialices con README, .gitignore, ni licencia
4. Haz clic en "Create repository"
5. Copia la URL (algo como `https://github.com/tuusuario/MECATON-2026.git`)

---

## Paso 2️⃣: Subir el código a GitHub

En tu terminal/PowerShell en la carpeta del proyecto:

```powershell
git init
git add .
git commit -m "Deploy MECATON Calculator - UNITEC 2026"
git branch -M main
git remote add origin https://github.com/TUUSUARIO/MECATON-2026.git
git push -u origin main
```

**Si no tienes Git instalado:**
- Windows: Descarga desde [git-scm.com](https://git-scm.com)

---

## Paso 3️⃣: Conectar Streamlit Cloud

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Haz clic en "New app"
3. Selecciona GitHub como fuente
4. Autoriza Streamlit (te redirige a GitHub)
5. **Selecciona:**
   - Repository: `tuusuario/MECATON-2026`
   - Branch: `main`
   - Main file path: `app.py`
6. Haz clic en "Deploy"

**Streamlit automáticamente:**
- Instala dependencias de `requirements.txt`
- Ejecuta `streamlit run app.py`
- Genera una URL pública (algo como `https://mecaton-2026.streamlit.app`)

---

## Paso 4️⃣: Generar QR

1. Ve a [qr-code-generator.com](https://www.qr-code-generator.com)
2. Pega tu URL de Streamlit Cloud
3. Descarga el QR como imagen PNG
4. Comparte con tus compañeras 📱

---

## ✅ Checklist

- [ ] Repo creado en GitHub
- [ ] Código subido (`git push`)
- [ ] App desplegada en Streamlit Cloud
- [ ] URL pública generada
- [ ] QR creado y compartido

---

## 🆘 Problemas?

**La app no abre o da error:**
- Revisa los logs en Streamlit Cloud (pestaña "Logs")
- Verifica que `requirements.txt` esté correcto
- Intenta abrir directamente: `https://share.streamlit.io/`

**No puedo acceder desde otro dispositivo:**
- El QR debe apuntar a la URL COMPLETA de Streamlit Cloud
- Tu dispositivo debe tener internet
- Si usas red privada, puede no funcionar (necesita IP pública)

**¿Cómo ven otros usuarios la app?**
- Escanean el QR → Se abre la URL en navegador
- Pueden usar desde:
  - 📱 Teléfono (iOS/Android)
  - 💻 Laptop/Desktop
  - 📟 Tablet
  - Cualquier navegador web

---

## 💡 Notas

- Streamlit Cloud es **gratis**
- Tu app está disponible **24/7**
- Cualquiera con la URL puede acceder
- Cambios en GitHub se actualizan automáticamente en Streamlit Cloud
- Si dejas de usarla, puedes deletearla desde el dashboard

---

¡Listo! Tu calculadora está en internet 🚀
