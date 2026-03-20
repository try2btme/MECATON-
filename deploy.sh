#!/bin/bash
# Script para subir a GitHub rápidamente

echo "🚀 Preparando deploy a GitHub..."

# Verificar que Git esté instalado
if ! command -v git &> /dev/null; then
    echo "❌ Git no está instalado. Instálalo primero."
    exit 1
fi

# Pedir la URL del repo
echo ""
echo "📌 Primero, crea un repo en GitHub (vacío, sin README)"
echo "Luego copia la URL y pégala aquí:"
read -p "URL del repo (ej: https://github.com/usuario/MECATON-2026.git): " REPO_URL

# Inicializar Git
git init
git add .
git commit -m "Deploy MECATON Numerical Methods Calculator"
git branch -M main
git remote add origin "$REPO_URL"
git push -u origin main

echo ""
echo "✅ ¡Código subido a GitHub!"
echo ""
echo "🌐 Ahora va a Streamlit Cloud:"
echo "1. Ve a https://share.streamlit.io"
echo "2. Inicia sesión con GitHub"
echo "3. Selecciona este repo"
echo "4. Elige app.py como archivo principal"
echo "5. ¡Genera tu URL pública!"
echo ""
echo "🔗 Luego copia la URL y genera un QR"
