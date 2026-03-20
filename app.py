"""
================================================================
app.py - CALCULADORA DE METODOS NUMERICOS | MECATON 2026
================================================================
Archivo unico consolidado que contiene TODA la logica de la
Calculadora de Metodos Numericos para el proyecto MECATON 2026.

Incluye:
  - Parseo de expresiones matematicas
  - Validacion de entradas
  - Generacion de reportes PDF
  - Generacion de pasos en LaTeX
  - Graficas interactivas con Plotly
  - Metodos de ecuaciones no lineales
  - Metodos de sistemas lineales
  - Metodos de interpolacion
  - Metodos de integracion numerica
  - Metodos de EDOs
  - Vistas de la interfaz (Streamlit)
  - Punto de entrada principal

Ejecucion: streamlit run app.py
================================================================
"""

# ================================================================
# TABLA DE CONTENIDOS
# ================================================================
#  1. IMPORTS GLOBALES
#  2. CSS GLOBAL (GLASSMORPHISM)
#  3. PARSEO DE EXPRESIONES (utils/parser.py)
#  4. VALIDACION DE ENTRADAS (utils/validation.py)
#  5. GENERADOR DE REPORTES PDF (utils/pdf_report.py)
#  6. PASOS EN LaTeX (visualization/latex_steps.py)
#  7. GRAFICAS CON PLOTLY (visualization/plots.py)
#  8. ECUACIONES NO LINEALES (methods/no_lineales.py)
#  9. SISTEMAS LINEALES (methods/sistemas_lineales.py)
# 10. INTERPOLACION (methods/interpolacion.py)
# 11. INTEGRACION NUMERICA (methods/integracion.py)
# 12. EDOs (methods/edo.py)
# 13. VISTA: INICIO (views/home.py)
# 14. VISTA: ECUACIONES NO LINEALES (views/no_lineales.py)
# 15. VISTA: SISTEMAS LINEALES (views/sistemas_lineales.py)
# 16. VISTA: INTERPOLACION (views/interpolacion.py)
# 17. VISTA: INTEGRACION NUMERICA (views/integracion.py)
# 18. VISTA: EDOs (views/edo.py)
# 19. PUNTO DE ENTRADA PRINCIPAL
# ================================================================


# ══════════════════════════════════════════════════════════════════
# SECCION 1: IMPORTS GLOBALES
# ══════════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import numpy as np
import sympy as sp
import plotly.graph_objects as go
import re
import os
import io
import tempfile
from fpdf import FPDF
from datetime import datetime

# Configurar tema oscuro forzado
st.set_page_config(
    page_title="Calculadora de Métodos Numéricos | MECATON 2026",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"Get help": None, "Report a bug": None, "About": None}
)

# Forzar tema oscuro
st.markdown("""
<script>
if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
    window.location.href = window.location.href;
}
</script>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# SECCION 2: CSS GLOBAL (GLASSMORPHISM)
# ══════════════════════════════════════════════════════════════════

CSS_GLOBAL = """
/* ============================================================
   TEMA OSCURO GLASSMORPHISM - Calculadora de Metodos Numericos
   ============================================================
   Este archivo define el estilo visual completo de la aplicacion.
   Usa un tema oscuro con efectos de glassmorphism (fondo difuminado
   con bordes semitransparentes) y acentos en cyan neon.

   Secciones:
     1. Imports y Variables
     2. Fondo principal
     3. Sidebar
     4. Tarjetas Glassmorphism
     5. Metricas
     6. Botones
     7. Inputs
     8. Tablas
     9. Tabs
    10. Tipografia
    11. Mensajes
    12. Animaciones
    13. Scrollbar
    14. Elementos especiales
   ============================================================ */

/* --- 1. IMPORTS: Fuente moderna Google Fonts --- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* --- VARIABLES GLOBALES DE COLOR --- */
:root {
    --bg-primary: #0a0a0f;
    --bg-secondary: #12121a;
    --bg-card: rgba(255, 255, 255, 0.03);
    --border-glass: rgba(255, 255, 255, 0.08);
    --accent-cyan: #00e5ff;
    --accent-purple: #b388ff;
    --accent-pink: #ff007f;
    --accent-green: #00ffcc;
    --accent-yellow: #ffea00;
    --text-primary: #e8e8ed;
    --text-secondary: #8b8b9e;
    --shadow-glow: 0 0 20px rgba(0, 229, 255, 0.1);
}

/* --- 2. FONDO PRINCIPAL DE LA APP --- */
.stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0a0a0f 100%) !important;
    font-family: 'Inter', sans-serif !important;
}

/* --- 3. SIDEBAR: Panel lateral de navegacion --- */
section[data-testid="stSidebar"] {
    background: rgba(10, 10, 15, 0.97) !important;
    border-right: 1px solid rgba(0, 229, 255, 0.1) !important;
}

/* --- Radio buttons del sidebar: Estilo tipo menu de navegacion --- */
section[data-testid="stSidebar"] .stRadio > div {
    gap: 2px !important;
}

section[data-testid="stSidebar"] .stRadio label {
    color: var(--text-primary) !important;
    font-weight: 500 !important;
    padding: 10px 16px !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
    font-size: 0.9rem !important;
    border: 1px solid transparent !important;
}

section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(0, 229, 255, 0.08) !important;
    color: var(--accent-cyan) !important;
    border-color: rgba(0, 229, 255, 0.15) !important;
}

section[data-testid="stSidebar"] .stRadio label[data-checked="true"],
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
    background: rgba(0, 229, 255, 0.12) !important;
    border-color: rgba(0, 229, 255, 0.3) !important;
    color: var(--accent-cyan) !important;
    box-shadow: 0 0 15px rgba(0, 229, 255, 0.1) !important;
}

/* --- 4. TARJETAS GLASSMORPHISM: Contenedores principales --- */
div[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: 16px !important;
    box-shadow: var(--shadow-glow) !important;
    transition: all 0.3s ease !important;
}

div[data-testid="stExpander"]:hover {
    border-color: rgba(0, 229, 255, 0.2) !important;
    box-shadow: 0 0 30px rgba(0, 229, 255, 0.15) !important;
}

/* --- 5. METRICAS: Indicadores de resultado final --- */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.03) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(0, 229, 255, 0.12) !important;
    border-radius: 14px !important;
    padding: 18px !important;
    box-shadow: 0 0 20px rgba(0, 229, 255, 0.06) !important;
    transition: all 0.3s ease !important;
}

div[data-testid="stMetric"]:hover {
    border-color: rgba(0, 229, 255, 0.25) !important;
    box-shadow: 0 0 25px rgba(0, 229, 255, 0.12) !important;
    transform: translateY(-2px) !important;
}

div[data-testid="stMetric"] label {
    color: var(--text-secondary) !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    font-weight: 600 !important;
}

div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    color: var(--accent-cyan) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 600 !important;
    font-size: 1.4rem !important;
}

/* --- 6. BOTONES: Boton de calcular y exportar --- */
.stButton > button {
    background: linear-gradient(135deg, rgba(0, 229, 255, 0.15), rgba(179, 136, 255, 0.15)) !important;
    border: 1px solid rgba(0, 229, 255, 0.3) !important;
    border-radius: 12px !important;
    color: var(--accent-cyan) !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    font-size: 0.85rem !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0, 229, 255, 0.25), rgba(179, 136, 255, 0.25)) !important;
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 25px rgba(0, 229, 255, 0.3) !important;
    transform: translateY(-2px) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
    box-shadow: 0 0 15px rgba(0, 229, 255, 0.2) !important;
}

/* --- 7. INPUTS: Campos de texto y numeros --- */
.stTextInput input, .stNumberInput input {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    transition: all 0.3s ease !important;
}

.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 15px rgba(0, 229, 255, 0.15) !important;
}

/* --- SELECT BOX: Selector de metodos y ejemplos --- */
.stSelectbox > div > div {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

/* --- 8. TABLAS DE ITERACIONES: Dataframes --- */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
}

div[data-testid="stDataFrame"] > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: 12px !important;
}

/* --- 9. TABS: Pestanas de navegacion interna --- */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px !important;
    background: transparent !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
    padding-bottom: 0 !important;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid var(--border-glass) !important;
    border-bottom: none !important;
    border-radius: 10px 10px 0 0 !important;
    color: var(--text-secondary) !important;
    padding: 10px 20px !important;
    transition: all 0.3s ease !important;
    font-weight: 500 !important;
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(0, 229, 255, 0.06) !important;
    color: var(--text-primary) !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(0, 229, 255, 0.1) !important;
    border-color: var(--accent-cyan) !important;
    color: var(--accent-cyan) !important;
    box-shadow: 0 -2px 10px rgba(0, 229, 255, 0.1) !important;
}

/* --- 10. TIPOGRAFIA --- */
h1 {
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple)) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px !important;
}

h2, h3 {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

p, li {
    color: var(--text-secondary) !important;
}

/* --- DIVIDER: Linea separadora --- */
hr {
    border-color: rgba(255, 255, 255, 0.06) !important;
}

/* --- 11. MENSAJES SUCCESS/ERROR/WARNING/INFO --- */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: 1px solid !important;
}

.stSuccess, div[data-baseweb="notification"][kind="positive"] {
    background: rgba(0, 255, 204, 0.06) !important;
    border-color: rgba(0, 255, 204, 0.2) !important;
}

.stError, div[data-baseweb="notification"][kind="negative"] {
    background: rgba(255, 0, 127, 0.06) !important;
    border-color: rgba(255, 0, 127, 0.2) !important;
}

.stWarning, div[data-baseweb="notification"][kind="warning"] {
    background: rgba(255, 234, 0, 0.06) !important;
    border-color: rgba(255, 234, 0, 0.15) !important;
}

.stInfo, div[data-baseweb="notification"][kind="info"] {
    background: rgba(0, 229, 255, 0.06) !important;
    border-color: rgba(0, 229, 255, 0.15) !important;
}

/* --- SLIDER: Control deslizante --- */
.stSlider > div > div > div {
    background: var(--accent-cyan) !important;
}

/* --- 12. ANIMACIONES --- */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(15px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes glowPulse {
    0%, 100% { box-shadow: 0 0 15px rgba(0, 229, 255, 0.08); }
    50% { box-shadow: 0 0 25px rgba(0, 229, 255, 0.15); }
}

.element-container {
    animation: fadeInUp 0.35s ease-out !important;
}

/* --- 13. SCROLLBAR PERSONALIZADA --- */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: var(--bg-primary);
}

::-webkit-scrollbar-thumb {
    background: rgba(0, 229, 255, 0.25);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 229, 255, 0.45);
}

/* --- 14. ELEMENTOS ESPECIALES --- */

/* LaTeX: Estilos para formulas matematicas */
.katex {
    color: var(--text-primary) !important;
    font-size: 1.1rem !important;
}

/* Download Button: Boton de descargar PDF */
.stDownloadButton > button {
    background: linear-gradient(135deg, rgba(0, 255, 204, 0.15), rgba(0, 229, 255, 0.15)) !important;
    border: 1px solid rgba(0, 255, 204, 0.3) !important;
    color: var(--accent-green) !important;
}

.stDownloadButton > button:hover {
    box-shadow: 0 0 25px rgba(0, 255, 204, 0.3) !important;
    transform: translateY(-2px) !important;
}

/* Sidebar logo image */
section[data-testid="stSidebar"] img {
    border-radius: 8px;
    padding: 10px 20px;
}

/* Ocultar el punto del radio button para look mas limpio */
section[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] {
    font-size: 0.92rem !important;
}

/* --- BOTON PARA REABRIR SIDEBAR (cuando esta colapsado) ---
   Sin esto, el boton queda invisible en tema oscuro y
   el usuario no puede volver a abrir el sidebar. */
[data-testid="stSidebarCollapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: rgba(10, 10, 15, 0.97) !important;
    border: 1px solid rgba(0, 229, 255, 0.25) !important;
    border-left: none !important;
    border-radius: 0 10px 10px 0 !important;
    padding: 12px 6px !important;
    transition: all 0.3s ease !important;
    box-shadow: 3px 0 15px rgba(0, 229, 255, 0.08) !important;
}

[data-testid="stSidebarCollapsedControl"]:hover {
    background: rgba(0, 229, 255, 0.12) !important;
    border-color: rgba(0, 229, 255, 0.5) !important;
    box-shadow: 3px 0 20px rgba(0, 229, 255, 0.2) !important;
}

/* Icono de flecha dentro del boton */
[data-testid="stSidebarCollapsedControl"] svg {
    fill: #00e5ff !important;
    color: #00e5ff !important;
}

/* Boton de colapsar/expandir sidebar DENTRO del sidebar */
[data-testid="stSidebar"] [data-testid="stBaseButton-header"] {
    color: rgba(0, 229, 255, 0.6) !important;
    transition: color 0.3s ease !important;
}

[data-testid="stSidebar"] [data-testid="stBaseButton-header"]:hover {
    color: #00e5ff !important;
}
"""


# ══════════════════════════════════════════════════════════════════
# SECCION 3: PARSEO DE EXPRESIONES (utils/parser.py)
# ══════════════════════════════════════════════════════════════════

def parsear_funcion(texto):
    """
    Convierte una expresion matematica escrita por el usuario
    en una expresion valida para SymPy.

    Parametros:
        texto (str): Expresion del usuario, ej: "2x^2 + sen(x)"

    Retorna:
        sp.Expr: Expresion de SymPy lista para evaluar

    Lanza:
        ValueError: Si la expresion no es valida matematicamente
    """
    if not texto or not texto.strip():
        raise ValueError("La expresion esta vacia. Ingrese una funcion valida.")

    expr_str = texto.strip()

    # --- Paso 1: Reemplazar ^ por ** (potencia) ---
    expr_str = expr_str.replace("^", "**")

    # --- Paso 2: Reemplazar funciones en espanol por SymPy ---
    # Esto permite que el usuario escriba "sen(x)" en vez de "sin(x)"
    reemplazos = {
        "sen(": "sin(",
        "cos(": "cos(",
        "tan(": "tan(",
        "ln(": "log(",
        "raiz(": "sqrt(",
        "arcsen(": "asin(",
        "arccos(": "acos(",
        "arctan(": "atan(",
        "abs(": "Abs(",
        "pi": "pi",
        "euler": "E",
    }
    for viejo, nuevo in reemplazos.items():
        expr_str = expr_str.replace(viejo, nuevo)

    # --- Paso 3: Insertar multiplicacion implicita ---
    # Transforma "2x" en "2*x", "3sin" en "3*sin", "x(" en "x*(", ")(" en ")*("
    # Numero seguido de letra o parentesis abierto
    expr_str = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expr_str)
    # Letra seguida de parentesis abierto (excepto funciones conocidas)
    funciones_conocidas = ['sin', 'cos', 'tan', 'log', 'sqrt', 'exp', 'asin',
                           'acos', 'atan', 'Abs', 'pi']
    # Parentesis cerrado seguido de parentesis abierto o letra
    expr_str = re.sub(r'\)(\()', r')*(', expr_str)
    expr_str = re.sub(r'\)([a-zA-Z0-9])', r')*\1', expr_str)

    # --- Paso 4: Convertir a expresion SymPy ---
    try:
        x, y, t = sp.symbols('x y t')
        expresion = sp.sympify(expr_str, locals={
            'x': x, 'y': y, 't': t,
            'e': sp.E, 'pi': sp.pi,
            'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
            'log': sp.log, 'sqrt': sp.sqrt, 'exp': sp.exp,
            'asin': sp.asin, 'acos': sp.acos, 'atan': sp.atan,
            'Abs': sp.Abs,
        })
        return expresion
    except Exception as e:
        raise ValueError(
            f"No se pudo interpretar la funcion: '{texto}'. "
            f"Verifique la sintaxis. Detalle: {str(e)}"
        )


def crear_funcion_numerica(expresion, variable=None):
    """
    Convierte una expresion SymPy en funcion numerica evaluable.

    Parametros:
        expresion: Expresion de SymPy
        variable: Simbolo de SymPy (default: x)

    Retorna:
        callable: Funcion que acepta floats/arrays de NumPy
    """
    if variable is None:
        variable = sp.Symbol('x')

    return sp.lambdify(variable, expresion, modules=['numpy'])


def crear_funcion_numerica_2vars(expresion):
    """
    Convierte una expresion SymPy f(t, y) en funcion numerica de 2 variables.

    Retorna:
        callable: Funcion que acepta (t, y) como floats
    """
    t, y = sp.symbols('t y')
    return sp.lambdify((t, y), expresion, modules=['numpy'])


# ══════════════════════════════════════════════════════════════════
# SECCION 4: VALIDACION DE ENTRADAS (utils/validation.py)
# ══════════════════════════════════════════════════════════════════

def validar_intervalo_biseccion(a, b, f):
    """
    Valida el intervalo para el metodo de biseccion.

    Parametros:
        a (float): Extremo izquierdo
        b (float): Extremo derecho
        f (callable): Funcion evaluable

    Retorna:
        tuple: (es_valido: bool, mensaje_error: str)
    """
    if a >= b:
        return False, "El valor de 'a' debe ser menor que 'b'."

    try:
        fa = f(a)
        fb = f(b)
    except Exception:
        return False, "No se pudo evaluar la funcion en los extremos del intervalo."

    if fa * fb >= 0:
        return False, (
            f"No hay cambio de signo en [{a}, {b}]. "
            f"f({a}) = {fa:.6f}, f({b}) = {fb:.6f}. "
            f"El metodo de biseccion requiere que f(a) y f(b) tengan signos opuestos."
        )

    return True, ""


def validar_tolerancia(tol):
    """
    Valida que la tolerancia sea positiva y razonable.

    Parametros:
        tol (float): Tolerancia ingresada

    Retorna:
        tuple: (es_valido: bool, mensaje_error: str)
    """
    if tol <= 0:
        return False, "La tolerancia debe ser un numero positivo mayor que cero."
    if tol > 1:
        return False, "La tolerancia es muy grande. Use un valor como 0.001 o 0.0001."
    return True, ""


def validar_max_iteraciones(max_iter):
    """
    Valida el numero maximo de iteraciones.

    Parametros:
        max_iter (int): Maximo de iteraciones

    Retorna:
        tuple: (es_valido: bool, mensaje_error: str)
    """
    if max_iter < 1:
        return False, "El numero de iteraciones debe ser al menos 1."
    if max_iter > 100000:
        return False, "Demasiadas iteraciones. Use un maximo de 100,000."
    return True, ""


def validar_matriz(A, b):
    """
    Valida que la matriz A sea cuadrada y compatible con el vector b.

    Parametros:
        A (list[list]): Matriz de coeficientes
        b (list): Vector de terminos independientes

    Retorna:
        tuple: (es_valido: bool, mensaje_error: str)
    """
    n = len(A)
    if n == 0:
        return False, "La matriz esta vacia."

    for i, fila in enumerate(A):
        if len(fila) != n:
            return False, f"La fila {i+1} tiene {len(fila)} columnas, pero se esperan {n}."

    if len(b) != n:
        return False, f"El vector b tiene {len(b)} elementos, pero la matriz es {n}x{n}."

    return True, ""


def validar_diagonal_dominante(A):
    """
    Verifica si la matriz es diagonalmente dominante.
    Retorna una advertencia (no un error) si no lo es.

    Parametros:
        A (list[list]): Matriz de coeficientes

    Retorna:
        tuple: (es_dominante: bool, mensaje: str)
    """
    n = len(A)
    for i in range(n):
        diagonal = abs(A[i][i])
        suma_fila = sum(abs(A[i][j]) for j in range(n) if j != i)
        if diagonal <= suma_fila:
            return False, (
                "La matriz NO es diagonalmente dominante. "
                "Los metodos de Jacobi y Gauss-Seidel podrian no converger."
            )
    return True, "La matriz es diagonalmente dominante. Convergencia garantizada."


def validar_puntos_interpolacion(xi, yi):
    """
    Valida los puntos para interpolacion.

    Parametros:
        xi (list): Valores de x
        yi (list): Valores de y

    Retorna:
        tuple: (es_valido: bool, mensaje_error: str)
    """
    if len(xi) < 2:
        return False, "Se necesitan al menos 2 puntos para interpolar."

    if len(xi) != len(yi):
        return False, f"La cantidad de valores x ({len(xi)}) no coincide con y ({len(yi)})."

    if len(set(xi)) != len(xi):
        return False, "Los valores de x no pueden repetirse."

    return True, ""


def validar_integracion(a, b, n, metodo):
    """
    Valida parametros para integracion numerica.

    Parametros:
        a (float): Limite inferior
        b (float): Limite superior
        n (int): Numero de subintervalos
        metodo (str): Nombre del metodo

    Retorna:
        tuple: (es_valido: bool, mensaje_error: str)
    """
    if a >= b:
        return False, "El limite inferior 'a' debe ser menor que el limite superior 'b'."

    if n < 1:
        return False, "El numero de subintervalos debe ser al menos 1."

    if metodo == "Simpson 1/3" and n % 2 != 0:
        return False, "Simpson 1/3 requiere un numero PAR de subintervalos."

    if metodo == "Simpson 3/8" and n % 3 != 0:
        return False, "Simpson 3/8 requiere que n sea multiplo de 3."

    return True, ""


def validar_edo(t0, tf, N):
    """
    Valida parametros para EDOs.

    Parametros:
        t0 (float): Tiempo inicial
        tf (float): Tiempo final
        N (int): Numero de pasos

    Retorna:
        tuple: (es_valido: bool, mensaje_error: str)
    """
    if t0 >= tf:
        return False, "El tiempo inicial t0 debe ser menor que el tiempo final tf."

    if N < 1:
        return False, "El numero de pasos N debe ser al menos 1."

    if N > 1000000:
        return False, "Demasiados pasos. Use un maximo de 1,000,000."

    return True, ""


# ══════════════════════════════════════════════════════════════════
# SECCION 5: GENERADOR DE REPORTES PDF (utils/pdf_report.py)
# ══════════════════════════════════════════════════════════════════

class ReportePDF(FPDF):
    """
    Clase personalizada que extiende FPDF para generar
    informes tecnicos con formato profesional.
    """

    def header(self):
        """
        Encabezado del PDF: se ejecuta automaticamente en
        cada pagina nueva. Muestra el titulo y una linea.
        """
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(0, 100, 180)
        self.cell(0, 10, 'Reporte de Analisis Numerico', 0, 1, 'C')
        self.set_font('Helvetica', '', 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, f'Generado: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 1, 'C')
        self.cell(0, 5, 'Calculadora de Metodos Numericos — MECATON 2026', 0, 1, 'C')
        self.ln(5)
        # Linea separadora
        self.set_draw_color(0, 100, 180)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        """
        Pie de pagina: numero de pagina.
        """
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Pagina {self.page_no()}/{{nb}}', 0, 0, 'C')

    def seccion_titulo(self, titulo):
        """
        Agrega un titulo de seccion con formato destacado.
        """
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(0, 80, 150)
        self.cell(0, 8, titulo, 0, 1, 'L')
        self.ln(2)

    def seccion_parametro(self, nombre, valor):
        """
        Agrega una linea de parametro: "Nombre: valor"
        """
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(50, 50, 50)
        self.cell(50, 6, f'{nombre}:', 0, 0)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(0, 0, 0)
        self.cell(0, 6, str(valor), 0, 1)

    def seccion_tabla(self, encabezados, datos, anchos=None):
        """
        Agrega una tabla formateada al PDF.

        Parametros:
            encabezados (list[str]): Nombres de las columnas
            datos (list[list]): Filas de datos
            anchos (list[float]): Anchos de columna (opcional)
        """
        n_cols = len(encabezados)
        if anchos is None:
            ancho_disponible = 190
            anchos = [ancho_disponible / n_cols] * n_cols

        # --- Encabezado de la tabla ---
        self.set_font('Helvetica', 'B', 8)
        self.set_fill_color(0, 100, 180)
        self.set_text_color(255, 255, 255)
        for i, enc in enumerate(encabezados):
            self.cell(anchos[i], 7, str(enc), 1, 0, 'C', True)
        self.ln()

        # --- Filas de datos ---
        self.set_font('Helvetica', '', 7)
        self.set_text_color(0, 0, 0)
        fill = False
        for fila in datos:
            if self.get_y() > 260:  # Salto de pagina si no hay espacio
                self.add_page()
            if fill:
                self.set_fill_color(230, 240, 250)
            else:
                self.set_fill_color(255, 255, 255)
            for i, val in enumerate(fila):
                texto = f"{val:.8f}" if isinstance(val, float) else str(val)
                self.cell(anchos[i], 6, texto, 1, 0, 'C', True)
            self.ln()
            fill = not fill


def generar_reporte_pdf(metodo_nombre, parametros, resultado, historial_keys=None,
                        grafica_bytes=None):
    """
    Genera un reporte PDF con los resultados de un metodo numerico.

    Parametros:
        metodo_nombre (str): Nombre del metodo (ej: "Biseccion")
        parametros (dict): Parametros de entrada {nombre: valor}
        resultado (dict): Resultado del metodo
        historial_keys (list[str]): Claves del historial a incluir en la tabla
        grafica_bytes (bytes): Imagen PNG de la grafica (opcional)

    Retorna:
        bytes: Contenido del PDF listo para descargar
    """
    pdf = ReportePDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # --- Seccion: Metodo utilizado ---
    pdf.seccion_titulo(f'Metodo: {metodo_nombre}')

    # --- Seccion: Parametros de entrada ---
    pdf.seccion_titulo('Parametros de Entrada')
    for nombre, valor in parametros.items():
        pdf.seccion_parametro(nombre, valor)
    pdf.ln(5)

    # --- Seccion: Resultado ---
    pdf.seccion_titulo('Resultado')
    if "raiz" in resultado:
        pdf.seccion_parametro("Raiz encontrada", f"{resultado['raiz']:.10f}")
    if "solucion" in resultado:
        pdf.seccion_parametro("Solucion", str(resultado['solucion']))
    if "area" in resultado:
        pdf.seccion_parametro("Integral aproximada", f"{resultado['area']:.10f}")
    if "iteraciones" in resultado:
        pdf.seccion_parametro("Iteraciones", resultado["iteraciones"])
    if "error_final" in resultado:
        pdf.seccion_parametro("Error final", f"{resultado['error_final']:.2e}")
    if "mensaje" in resultado:
        pdf.seccion_parametro("Estado", resultado["mensaje"])
    pdf.ln(5)

    # --- Seccion: Grafica (si se proporciona imagen) ---
    if grafica_bytes:
        pdf.seccion_titulo('Grafica')
        try:
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                tmp.write(grafica_bytes)
                tmp_path = tmp.name
            pdf.image(tmp_path, x=15, w=180)
            os.unlink(tmp_path)
        except Exception:
            pdf.cell(0, 10, '(No se pudo insertar la grafica)', 0, 1)
        pdf.ln(5)

    # --- Seccion: Tabla de iteraciones ---
    if "historial" in resultado and resultado["historial"]:
        pdf.seccion_titulo('Tabla de Iteraciones')

        historial = resultado["historial"]
        # Determinar columnas automaticamente
        if historial_keys:
            keys = historial_keys
        else:
            keys = list(historial[0].keys())

        encabezados = keys
        datos = []
        for h in historial:
            fila = [h.get(k, "") for k in keys]
            datos.append(fila)

        pdf.seccion_tabla(encabezados, datos)

    # --- Retornar bytes del PDF ---
    return pdf.output()


# ══════════════════════════════════════════════════════════════════
# SECCION 6: PASOS EN LaTeX (visualization/latex_steps.py)
# ══════════════════════════════════════════════════════════════════

def latex_metodo_descripcion(metodo):
    """
    Retorna la formula general del metodo en LaTeX.

    Parametros:
        metodo (str): Nombre del metodo

    Retorna:
        str: String LaTeX con la formula del metodo
    """
    descripciones = {
        "Biseccion": r"c = \frac{a + b}{2}, \quad \text{si } f(a) \cdot f(c) < 0 \Rightarrow b = c, \quad \text{sino } a = c",
        "Newton-Raphson": r"x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}",
        "Punto Fijo": r"x_{n+1} = g(x_n), \quad \text{converge si } |g'(x)| < 1",
        "Jacobi": r"x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j \neq i} a_{ij} x_j^{(k)} \right)",
        "Gauss-Seidel": r"x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j<i} a_{ij} x_j^{(k+1)} - \sum_{j>i} a_{ij} x_j^{(k)} \right)",
        "LU Doolittle": r"A = LU, \quad Ly = b, \quad Ux = y",
        "Lagrange": r"P(x) = \sum_{i=0}^{n} y_i \prod_{\substack{j=0 \\ j \neq i}}^{n} \frac{x - x_j}{x_i - x_j}",
        "Newton Interpolacion": r"P(x) = f[x_0] + f[x_0,x_1](x-x_0) + f[x_0,x_1,x_2](x-x_0)(x-x_1) + \cdots",
        "Trazador Cubico": r"S_j(x) = a_j + b_j(x - x_j) + c_j(x - x_j)^2 + d_j(x - x_j)^3",
        "Trapecio": r"\int_a^b f(x)\,dx \approx \frac{h}{2}\left[f(x_0) + 2\sum_{i=1}^{n-1}f(x_i) + f(x_n)\right]",
        "Simpson 1/3": r"\int_a^b f(x)\,dx \approx \frac{h}{3}\left[f(x_0) + 4\sum_{\text{impar}} f(x_i) + 2\sum_{\text{par}} f(x_i) + f(x_n)\right]",
        "Simpson 3/8": r"\int_a^b f(x)\,dx \approx \frac{3h}{8}\left[f(x_0) + 3f(x_1) + 3f(x_2) + 2f(x_3) + \cdots + f(x_n)\right]",
        "Euler": r"y_{n+1} = y_n + h \cdot f(t_n, y_n)",
        "RK2": r"y_{n+1} = y_n + \frac{1}{2}(k_1 + k_2), \quad k_1 = hf(t_n,y_n), \quad k_2 = hf(t_{n+1}, y_n+k_1)",
        "RK4": r"y_{n+1} = y_n + \frac{1}{6}(k_1 + 2k_2 + 2k_3 + k_4)",
        "Verlet": r"x_{n+1} = 2x_n - x_{n-1} + a(t_n, x_n) \cdot h^2",
    }
    return descripciones.get(metodo, "")


def latex_biseccion_paso(iteracion, a, b, c, fc, error):
    """
    Genera LaTeX para un paso de biseccion.

    Retorna:
        str: String LaTeX
    """
    return (
        f"\\text{{Iteracion {iteracion}:}} \\quad "
        f"c = \\frac{{{a:.6f} + {b:.6f}}}{{2}} = {c:.6f}, \\quad "
        f"f(c) = {fc:.6e}, \\quad "
        f"|b - a| = {error:.6e}"
    )


def latex_newton_paso(iteracion, xn, fxn, dfxn, xn1, error):
    """
    Genera LaTeX para un paso de Newton-Raphson.

    Retorna:
        str: String LaTeX
    """
    return (
        f"\\text{{Iteracion {iteracion}:}} \\quad "
        f"x_{{{iteracion}}} = {xn:.8f} - \\frac{{{fxn:.6e}}}{{{dfxn:.6e}}} = {xn1:.8f}, \\quad "
        f"\\varepsilon = {error:.6e}"
    )


def latex_punto_fijo_paso(iteracion, xn, gxn, error):
    """
    Genera LaTeX para un paso de punto fijo.

    Retorna:
        str: String LaTeX
    """
    return (
        f"\\text{{Iteracion {iteracion}:}} \\quad "
        f"x_{{{iteracion}}} = g({xn:.8f}) = {gxn:.8f}, \\quad "
        f"\\varepsilon = {error:.6e}"
    )


def latex_euler_paso(paso, tn, yn, ftn, yn1, h):
    """
    Genera LaTeX para un paso de Euler.

    Retorna:
        str: String LaTeX
    """
    return (
        f"\\text{{Paso {paso}:}} \\quad "
        f"y_{{{paso}}} = {yn:.6f} + {h:.6f} \\cdot {ftn:.6f} = {yn1:.6f}"
    )


def latex_rk4_paso(paso, tn, yn, k1, k2, k3, k4, yn1):
    """
    Genera LaTeX para un paso de RK4.

    Retorna:
        str: String LaTeX
    """
    return (
        f"\\text{{Paso {paso}:}} \\quad "
        f"k_1={k1:.6f},\\ k_2={k2:.6f},\\ k_3={k3:.6f},\\ k_4={k4:.6f} \\quad "
        f"y_{{{paso}}} = {yn1:.6f}"
    )


# ══════════════════════════════════════════════════════════════════
# SECCION 7: GRAFICAS CON PLOTLY (visualization/plots.py)
# ══════════════════════════════════════════════════════════════════

# --- Tema oscuro global para Plotly ---
LAYOUT_OSCURO = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(10,10,15,0.8)',
    font=dict(color='#e8e8ed', family='Inter'),
    xaxis=dict(
        gridcolor='rgba(255,255,255,0.06)',
        zerolinecolor='rgba(255,255,255,0.15)',
        tickfont=dict(size=11)
    ),
    yaxis=dict(
        gridcolor='rgba(255,255,255,0.06)',
        zerolinecolor='rgba(255,255,255,0.15)',
        tickfont=dict(size=11)
    ),
    margin=dict(l=50, r=30, t=50, b=50),
    hoverlabel=dict(
        bgcolor='rgba(20,20,30,0.95)',
        font_size=12,
        font_family='JetBrains Mono'
    )
)

# Colores neon para las lineas
CYAN = '#00e5ff'
MAGENTA = '#ff007f'
VERDE = '#00ffcc'
MORADO = '#b388ff'
AMARILLO = '#ffea00'
NARANJA = '#ff6d00'


def _evaluar_seguro(f_eval, x_vals, clip=1e10):
    """
    Evalua f(x) sobre un array, reemplazando infinitos/NaN con np.nan
    para que Plotly no rompa la grafica al hacer pan lejos.
    """
    try:
        y = f_eval(x_vals)
        y = np.where(np.isfinite(y) & (np.abs(y) < clip), y, np.nan)
    except Exception:
        y = np.array([f_eval(xi) if np.isfinite(xi) else np.nan for xi in x_vals])
        y = np.array([yi if (np.isfinite(yi) and abs(yi) < clip) else np.nan for yi in y])
    return y


def graficar_funcion_raiz(f_eval, raiz, a, b, titulo="f(x)", historial=None):
    """
    Grafica f(x) con datos pre-calculados en un rango 10x mas amplio
    que el visible inicial. Al hacer pan la curva ya existe — no aparece
    espacio en blanco.

    Parametros:
        f_eval (callable): Funcion evaluable f(x)
        raiz (float): Valor de la raiz encontrada
        a, b (float): Rango inicial visible
        titulo (str): Titulo del grafico
        historial (list): Lista de puntos intermedios (opcional)

    Retorna:
        plotly.graph_objects.Figure
    """
    span = b - a if b != a else 1.0
    margen_vista = span * 0.2          # Vista inicial: [a-20%, b+20%]
    extension    = span * 5.0          # Datos pre-calc: [a-500%, b+500%] => 10x rango

    # 2000 puntos sobre el rango extendido — solo los visibles se renderizan
    x_vals = np.linspace(a - extension, b + extension, 2000)
    y_vals = _evaluar_seguro(f_eval, x_vals)

    fig = go.Figure()

    # --- Curva de f(x) (rango completo pre-calculado) ---
    fig.add_trace(go.Scatter(
        x=x_vals, y=y_vals,
        mode='lines',
        name='f(x)',
        line=dict(color=CYAN, width=3),
        hovertemplate='x = %{x:.6f}<br>f(x) = %{y:.6f}<extra></extra>'
    ))

    # --- Linea y = 0 (eje x) ---
    fig.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.3)")

    # --- Marcador de la raiz ---
    fig.add_trace(go.Scatter(
        x=[raiz], y=[0],
        mode='markers',
        name=f'Raiz = {raiz:.8f}',
        marker=dict(size=14, color=MAGENTA, symbol='circle',
                    line=dict(width=2, color='white')),
        hovertemplate=f'RAIZ<br>x = {raiz:.10f}<extra></extra>'
    ))

    # --- Puntos intermedios del historial (convergencia) ---
    if historial:
        x_hist = []
        y_hist = []
        for h in historial:
            if "c (punto medio)" in h:
                xh = h["c (punto medio)"]
            elif "x_n" in h:
                xh = h["x_n"]
            else:
                continue
            try:
                x_hist.append(xh)
                y_hist.append(f_eval(xh))
            except Exception:
                pass

        if x_hist:
            fig.add_trace(go.Scatter(
                x=x_hist, y=y_hist,
                mode='markers',
                name='Iteraciones',
                marker=dict(size=7, color=VERDE, opacity=0.7),
                hovertemplate='Iteracion<br>x = %{x:.6f}<br>f(x) = %{y:.6f}<extra></extra>'
            ))

    layout_extra = dict(**LAYOUT_OSCURO)
    layout_extra['xaxis'] = dict(
        range=[a - margen_vista, b + margen_vista],  # Vista inicial
        gridcolor='rgba(255,255,255,0.06)',
        zerolinecolor='rgba(255,255,255,0.15)',
        tickfont=dict(size=11)
    )

    fig.update_layout(
        title=dict(text=titulo, font=dict(size=16)),
        xaxis_title="x",
        yaxis_title="f(x)",
        showlegend=True,
        uirevision='funcion_raiz',   # Preserva zoom/pan en re-render de Streamlit
        legend=dict(bgcolor='rgba(0,0,0,0.5)', bordercolor='rgba(255,255,255,0.1)'),
        **layout_extra
    )

    return fig


def graficar_convergencia(historial, key_error="error", titulo="Convergencia del Error"):
    """
    Grafica la evolucion del error por iteracion.

    Parametros:
        historial (list[dict]): Datos de cada iteracion
        key_error (str): Nombre de la clave del error en el dict
        titulo (str): Titulo del grafico

    Retorna:
        plotly.graph_objects.Figure
    """
    iteraciones = [h.get("iteracion", h.get("paso", i + 1)) for i, h in enumerate(historial)]
    errores = []
    for h in historial:
        e = h.get(key_error, h.get("error |b-a|", h.get("error", 0)))
        errores.append(e if e > 0 else 1e-16)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=iteraciones, y=errores,
        mode='lines+markers',
        name='Error',
        line=dict(color=MAGENTA, width=2.5),
        marker=dict(size=6, color=MAGENTA),
        hovertemplate='Iteracion %{x}<br>Error = %{y:.2e}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(text=titulo, font=dict(size=16)),
        xaxis_title="Iteracion",
        yaxis_title="Error",
        yaxis_type="log",
        uirevision='convergencia',
        **LAYOUT_OSCURO
    )

    return fig


def graficar_integracion(f_eval, x_puntos, y_puntos, metodo="Trapecio", a=None, b=None):
    """
    Grafica la funcion y el area aproximada para integracion.

    Parametros:
        f_eval (callable): Funcion evaluable
        x_puntos (list): Puntos x de los subintervalos
        y_puntos (list): Valores f(x) en los puntos
        metodo (str): Nombre del metodo
        a, b (float): Limites de integracion

    Retorna:
        plotly.graph_objects.Figure
    """
    if a is None:
        a = x_puntos[0]
    if b is None:
        b = x_puntos[-1]

    span = b - a if b != a else 1.0
    margen_vista = span * 0.1
    extension    = span * 5.0   # Pre-calcular 10x el rango visible

    fig = go.Figure()

    # --- Curva continua de f(x) (rango extendido para pan infinito) ---
    x_fino = np.linspace(a - extension, b + extension, 2000)
    y_fino = _evaluar_seguro(f_eval, x_fino)

    fig.add_trace(go.Scatter(
        x=x_fino, y=y_fino,
        mode='lines',
        name='f(x)',
        line=dict(color=CYAN, width=3)
    ))

    # --- Area bajo la curva (trapezoides coloreados) ---
    x_pts = np.array(x_puntos)
    y_pts = np.array(y_puntos)

    for i in range(len(x_pts) - 1):
        fig.add_trace(go.Scatter(
            x=[x_pts[i], x_pts[i], x_pts[i + 1], x_pts[i + 1], x_pts[i]],
            y=[0, y_pts[i], y_pts[i + 1], 0, 0],
            fill='toself',
            fillcolor='rgba(0, 229, 255, 0.15)',
            line=dict(color='rgba(0, 229, 255, 0.4)', width=1),
            showlegend=False,
            hoverinfo='skip'
        ))

    # --- Puntos de los subintervalos ---
    fig.add_trace(go.Scatter(
        x=x_pts, y=y_pts,
        mode='markers',
        name='Puntos',
        marker=dict(size=8, color=VERDE, line=dict(width=1, color='white'))
    ))

    layout_integ = dict(**LAYOUT_OSCURO)
    layout_integ['xaxis'] = dict(
        range=[a - margen_vista, b + margen_vista],
        gridcolor='rgba(255,255,255,0.06)',
        zerolinecolor='rgba(255,255,255,0.15)',
        tickfont=dict(size=11)
    )

    fig.update_layout(
        title=dict(text=f"Integracion: {metodo}", font=dict(size=16)),
        xaxis_title="x",
        yaxis_title="f(x)",
        uirevision='integracion',
        **layout_integ
    )

    return fig


def graficar_edo(resultados, titulo="Solucion de la EDO"):
    """
    Grafica soluciones de EDO (uno o varios metodos).

    Parametros:
        resultados (list[dict]): Lista de resultados de metodos EDO
        titulo (str): Titulo del grafico

    Retorna:
        plotly.graph_objects.Figure
    """
    colores = [CYAN, MAGENTA, VERDE, MORADO, AMARILLO, NARANJA]

    fig = go.Figure()

    for idx, res in enumerate(resultados):
        color = colores[idx % len(colores)]
        nombre = res.get("metodo", f"Metodo {idx + 1}")
        t_vals = res.get("t", [])
        y_vals = res.get("y", res.get("x", []))

        fig.add_trace(go.Scatter(
            x=t_vals, y=y_vals,
            mode='lines',
            name=nombre,
            line=dict(color=color, width=2.5),
            hovertemplate=f'{nombre}<br>t = %{{x:.4f}}<br>y = %{{y:.6f}}<extra></extra>'
        ))

    fig.update_layout(
        title=dict(text=titulo, font=dict(size=16)),
        xaxis_title="t",
        yaxis_title="y(t)",
        showlegend=True,
        uirevision='edo',
        legend=dict(bgcolor='rgba(0,0,0,0.5)', bordercolor='rgba(255,255,255,0.1)'),
        **LAYOUT_OSCURO
    )

    return fig


def graficar_analisis_orden(h_values, errores, orden_estimado, titulo="Analisis de Orden"):
    """
    Grafica error vs h en escala log-log para analisis de orden.

    Parametros:
        h_values (list): Tamanios de paso
        errores (list): Errores correspondientes
        orden_estimado (float): Orden estimado del metodo

    Retorna:
        plotly.graph_objects.Figure
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=h_values, y=errores,
        mode='lines+markers',
        name=f'Error (orden ≈ {orden_estimado:.2f})',
        line=dict(color=CYAN, width=2.5),
        marker=dict(size=8, color=CYAN),
        hovertemplate='h = %{x:.6f}<br>Error = %{y:.2e}<extra></extra>'
    ))

    # Linea de referencia para el orden esperado
    if len(h_values) >= 2 and errores[0] > 0:
        h_ref = np.array(h_values)
        e_ref = errores[0] * (h_ref / h_values[0]) ** orden_estimado
        fig.add_trace(go.Scatter(
            x=h_ref, y=e_ref,
            mode='lines',
            name=f'Referencia O(h^{orden_estimado:.1f})',
            line=dict(color=MORADO, width=1.5, dash='dash')
        ))

    fig.update_layout(
        title=dict(text=titulo, font=dict(size=16)),
        xaxis_title="h (tamano de paso)",
        yaxis_title="Error",
        xaxis_type="log",
        yaxis_type="log",
        **LAYOUT_OSCURO
    )

    return fig


def graficar_interpolacion(xi, yi, funciones_eval, nombres, titulo="Interpolacion"):
    """
    Grafica puntos y polinomios interpolantes.

    Parametros:
        xi, yi: Puntos originales
        funciones_eval (list[callable]): Funciones de los polinomios
        nombres (list[str]): Nombres de los metodos

    Retorna:
        plotly.graph_objects.Figure
    """
    colores = [CYAN, MAGENTA, VERDE, MORADO]

    fig = go.Figure()

    # Rango extendido: 10x el rango de los puntos para pan continuo
    x_min, x_max = min(xi), max(xi)
    span = x_max - x_min if x_max != x_min else 1.0
    margen_vista = span * 0.15
    extension    = span * 5.0
    x_fino = np.linspace(x_min - extension, x_max + extension, 2000)

    for idx, (f_eval, nombre) in enumerate(zip(funciones_eval, nombres)):
        color = colores[idx % len(colores)]
        try:
            y_fino = f_eval(x_fino)
            if isinstance(y_fino, (int, float)):
                y_fino = np.full_like(x_fino, float(y_fino))
            y_fino = np.where(np.isfinite(y_fino) & (np.abs(y_fino) < 1e10), y_fino, np.nan)
        except Exception:
            y_fino = np.array([float(f_eval(xv)) if np.isfinite(f_eval(xv)) else np.nan for xv in x_fino])

        fig.add_trace(go.Scatter(
            x=x_fino, y=y_fino,
            mode='lines',
            name=nombre,
            line=dict(color=color, width=2.5)
        ))

    # Puntos originales
    fig.add_trace(go.Scatter(
        x=list(xi), y=list(yi),
        mode='markers',
        name='Datos',
        marker=dict(size=12, color=AMARILLO, symbol='circle',
                    line=dict(width=2, color='white')),
        hovertemplate='(%{x:.4f}, %{y:.4f})<extra></extra>'
    ))

    layout_interp = dict(**LAYOUT_OSCURO)
    layout_interp['xaxis'] = dict(
        range=[x_min - margen_vista, x_max + margen_vista],
        gridcolor='rgba(255,255,255,0.06)',
        zerolinecolor='rgba(255,255,255,0.15)',
        tickfont=dict(size=11)
    )

    fig.update_layout(
        title=dict(text=titulo, font=dict(size=16)),
        xaxis_title="x",
        yaxis_title="y",
        showlegend=True,
        uirevision='interpolacion',
        legend=dict(bgcolor='rgba(0,0,0,0.5)'),
        **layout_interp
    )

    return fig


# ══════════════════════════════════════════════════════════════════
# SECCION 8: ECUACIONES NO LINEALES (methods/no_lineales.py)
# ══════════════════════════════════════════════════════════════════

def biseccion(func_str, a, b, tol, max_iter=100):
    """
    Encuentra una raiz de f(x)=0 en el intervalo [a, b]
    usando el metodo de biseccion.

    Parametros:
        func_str (str): Expresion de la funcion, ej: "x**2 - 2"
        a (float): Extremo izquierdo del intervalo
        b (float): Extremo derecho del intervalo
        tol (float): Tolerancia del error
        max_iter (int): Maximo de iteraciones permitidas

    Retorna:
        dict con keys: status, raiz, historial, mensaje, iteraciones
    """
    # --- Crear la funcion evaluable a partir del string ---
    x = sp.Symbol('x')
    try:
        f_expr = sp.sympify(func_str)
        F = sp.lambdify(x, f_expr, modules=['numpy'])
    except Exception as e:
        return {"status": "Error", "mensaje": f"Funcion invalida: {e}"}

    # --- Verificar cambio de signo en el intervalo ---
    fa = F(a)
    fb = F(b)
    if fa * fb >= 0:
        return {
            "status": "Error",
            "mensaje": f"No hay cambio de signo en [{a}, {b}]. f({a})={fa:.6f}, f({b})={fb:.6f}"
        }

    # --- Iteraciones del metodo de biseccion ---
    historial = []
    error = abs(b - a)
    c = a  # valor inicial

    for i in range(1, max_iter + 1):
        # Paso 1: Calcular punto medio
        c = (a + b) / 2.0
        fc = F(c)
        error = abs(b - a)

        # Paso 2: Guardar datos de esta iteracion en el historial
        historial.append({
            "iteracion": i,
            "a": a,
            "b": b,
            "c (punto medio)": c,
            "f(c)": fc,
            "error |b-a|": error
        })

        # Paso 3: Verificar si encontramos la raiz exacta
        if abs(fc) < 1e-15:
            return {
                "status": "OK",
                "raiz": c,
                "historial": historial,
                "iteraciones": i,
                "error_final": error,
                "mensaje": f"Raiz encontrada exacta en iteracion {i}: x = {c}"
            }

        # Paso 4: Verificar si alcanzamos la tolerancia
        if error < tol:
            return {
                "status": "OK",
                "raiz": c,
                "historial": historial,
                "iteraciones": i,
                "error_final": error,
                "mensaje": f"Convergencia alcanzada en {i} iteraciones. Raiz ≈ {c:.10f}"
            }

        # Paso 5: Decidir en que subintervalo esta la raiz
        if fa * fc < 0:
            b = c  # La raiz esta en [a, c]
        else:
            a = c  # La raiz esta en [c, b]
            fa = fc

    # Si se agotaron las iteraciones sin converger
    return {
        "status": "Advertencia",
        "raiz": c,
        "historial": historial,
        "iteraciones": max_iter,
        "error_final": error,
        "mensaje": f"Se alcanzo el maximo de {max_iter} iteraciones. Raiz ≈ {c:.10f}, error = {error:.2e}"
    }


def newton_raphson(func_str, x0, tol, max_iter=100):
    """
    Encuentra una raiz de f(x)=0 usando el metodo de Newton-Raphson.

    Parametros:
        func_str (str): Expresion de la funcion, ej: "x**3 - x - 2"
        x0 (float): Valor inicial (aproximacion de la raiz)
        tol (float): Tolerancia del error
        max_iter (int): Maximo de iteraciones permitidas

    Retorna:
        dict con keys: status, raiz, historial, mensaje, iteraciones
    """
    # --- Crear funcion y su derivada usando SymPy ---
    x = sp.Symbol('x')
    try:
        f_expr = sp.sympify(func_str)
        df_expr = sp.diff(f_expr, x)  # Derivada simbolica automatica
        F = sp.lambdify(x, f_expr, modules=['numpy'])
        dF = sp.lambdify(x, df_expr, modules=['numpy'])
    except Exception as e:
        return {"status": "Error", "mensaje": f"Funcion invalida: {e}"}

    # --- Iteraciones del metodo de Newton-Raphson ---
    xi = float(x0)
    historial = []

    for i in range(1, max_iter + 1):
        # Paso 1: Evaluar f(x_i) y f'(x_i)
        fxi = F(xi)
        dfxi = dF(xi)

        # Paso 2: Verificar que la derivada no sea cero
        if abs(dfxi) < 1e-15:
            return {
                "status": "Error",
                "raiz": xi,
                "historial": historial,
                "iteraciones": i,
                "mensaje": f"Derivada cero en x = {xi:.10f}. El metodo no puede continuar."
            }

        # Paso 3: Calcular la siguiente aproximacion
        x_new = xi - fxi / dfxi
        error = abs(x_new - xi)

        # Paso 4: Guardar datos de esta iteracion
        historial.append({
            "iteracion": i,
            "x_n": xi,
            "f(x_n)": fxi,
            "f'(x_n)": dfxi,
            "x_{n+1}": x_new,
            "error": error
        })

        # Paso 5: Verificar convergencia
        if error < tol:
            return {
                "status": "OK",
                "raiz": x_new,
                "historial": historial,
                "iteraciones": i,
                "error_final": error,
                "derivada_str": str(df_expr),
                "mensaje": f"Convergencia en {i} iteraciones. Raiz ≈ {x_new:.10f}"
            }

        xi = x_new

    return {
        "status": "Advertencia",
        "raiz": xi,
        "historial": historial,
        "iteraciones": max_iter,
        "error_final": error,
        "derivada_str": str(df_expr),
        "mensaje": f"Se alcanzo el maximo de {max_iter} iteraciones. Raiz ≈ {xi:.10f}"
    }


def punto_fijo(g_str, x0, tol, max_iter=1000):
    """
    Encuentra un punto fijo x = g(x) usando iteracion de punto fijo.

    Parametros:
        g_str (str): Expresion de g(x), ej: "sqrt(x + 2)"
        x0 (float): Valor inicial
        tol (float): Tolerancia del error
        max_iter (int): Maximo de iteraciones

    Retorna:
        dict con keys: status, raiz, historial, mensaje, iteraciones
    """
    # --- Crear la funcion g(x) evaluable ---
    x = sp.Symbol('x')
    try:
        g_expr = sp.sympify(g_str)
        G = sp.lambdify(x, g_expr, modules=['numpy'])
    except Exception as e:
        return {"status": "Error", "mensaje": f"Funcion g(x) invalida: {e}"}

    # --- Iteraciones del metodo de punto fijo ---
    xi = float(x0)
    historial = []

    for i in range(1, max_iter + 1):
        # Paso 1: Evaluar g(x_i)
        try:
            x_new = float(G(xi))
        except Exception:
            return {
                "status": "Error",
                "raiz": xi,
                "historial": historial,
                "iteraciones": i,
                "mensaje": f"Error al evaluar g({xi:.6f}). La funcion puede no estar definida."
            }

        # Paso 2: Verificar que no diverja (valor demasiado grande)
        if abs(x_new) > 1e15 or np.isnan(x_new) or np.isinf(x_new):
            return {
                "status": "Error",
                "raiz": xi,
                "historial": historial,
                "iteraciones": i,
                "mensaje": "El metodo diverge. Verifique que |g'(x)| < 1 cerca de la raiz."
            }

        error = abs(x_new - xi)

        # Paso 3: Guardar datos de esta iteracion
        historial.append({
            "iteracion": i,
            "x_n": xi,
            "g(x_n)": x_new,
            "error": error
        })

        # Paso 4: Verificar convergencia
        if error < tol:
            return {
                "status": "OK",
                "raiz": x_new,
                "historial": historial,
                "iteraciones": i,
                "error_final": error,
                "mensaje": f"Convergencia en {i} iteraciones. Punto fijo ≈ {x_new:.10f}"
            }

        xi = x_new

    return {
        "status": "Advertencia",
        "raiz": xi,
        "historial": historial,
        "iteraciones": max_iter,
        "error_final": error,
        "mensaje": f"Se alcanzo el maximo de {max_iter} iteraciones. x ≈ {xi:.10f}"
    }


# ══════════════════════════════════════════════════════════════════
# SECCION 9: SISTEMAS LINEALES (methods/sistemas_lineales.py)
# ══════════════════════════════════════════════════════════════════

def jacobi(A, b, x0, tol, max_iter=100):
    """
    Resuelve Ax = b usando el metodo iterativo de Jacobi.

    Parametros:
        A (list[list[float]]): Matriz de coeficientes (n x n)
        b (list[float]): Vector de terminos independientes
        x0 (list[float]): Vector inicial (aproximacion)
        tol (float): Tolerancia del error
        max_iter (int): Maximo de iteraciones

    Retorna:
        dict con keys: status, solucion, historial, mensaje, iteraciones
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(A)
    x = np.array(x0, dtype=float)
    historial = []

    # --- Verificar que no haya ceros en la diagonal ---
    for i in range(n):
        if abs(A[i][i]) < 1e-15:
            return {
                "status": "Error",
                "mensaje": f"Cero en la diagonal principal en la posicion ({i+1},{i+1}). "
                           "Reordene las ecuaciones."
            }

    # --- Iteraciones del metodo de Jacobi ---
    for k in range(1, max_iter + 1):
        x_new = np.zeros(n)

        # Para cada ecuacion i, calcular x_i nuevo
        for i in range(n):
            # Suma de a_{ij} * x_j para j != i (usando valores ANTERIORES)
            suma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - suma) / A[i][i]

        # Calcular el error maximo entre componentes
        error = np.max(np.abs(x_new - x))

        # Guardar datos de esta iteracion
        historial.append({
            "iteracion": k,
            "x": x_new.tolist(),
            "error": error
        })

        # Verificar convergencia
        if error < tol:
            return {
                "status": "OK",
                "solucion": x_new.tolist(),
                "historial": historial,
                "iteraciones": k,
                "error_final": error,
                "mensaje": f"Convergencia en {k} iteraciones."
            }

        x = x_new.copy()

    return {
        "status": "Advertencia",
        "solucion": x.tolist(),
        "historial": historial,
        "iteraciones": max_iter,
        "error_final": error,
        "mensaje": f"No convergio en {max_iter} iteraciones. Error = {error:.2e}"
    }


def gauss_seidel(A, b, x0, tol, max_iter=100):
    """
    Resuelve Ax = b usando el metodo iterativo de Gauss-Seidel.

    Parametros:
        A (list[list[float]]): Matriz de coeficientes (n x n)
        b (list[float]): Vector de terminos independientes
        x0 (list[float]): Vector inicial
        tol (float): Tolerancia del error
        max_iter (int): Maximo de iteraciones

    Retorna:
        dict con keys: status, solucion, historial, mensaje, iteraciones
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(A)
    x = np.array(x0, dtype=float)
    historial = []

    # --- Verificar que no haya ceros en la diagonal ---
    for i in range(n):
        if abs(A[i][i]) < 1e-15:
            return {
                "status": "Error",
                "mensaje": f"Cero en la diagonal principal en la posicion ({i+1},{i+1})."
            }

    # --- Iteraciones del metodo de Gauss-Seidel ---
    for k in range(1, max_iter + 1):
        x_prev = x.copy()

        for i in range(n):
            # Suma de a_{ij}*x_j para j < i (valores YA actualizados)
            s1 = sum(A[i][j] * x[j] for j in range(i))
            # Suma de a_{ij}*x_j para j > i (valores de la iteracion anterior)
            s2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
            x[i] = (b[i] - s1 - s2) / A[i][i]

        # Calcular error maximo
        error = np.max(np.abs(x - x_prev))

        historial.append({
            "iteracion": k,
            "x": x.tolist(),
            "error": error
        })

        if error < tol:
            return {
                "status": "OK",
                "solucion": x.tolist(),
                "historial": historial,
                "iteraciones": k,
                "error_final": error,
                "mensaje": f"Convergencia en {k} iteraciones."
            }

    return {
        "status": "Advertencia",
        "solucion": x.tolist(),
        "historial": historial,
        "iteraciones": max_iter,
        "error_final": error,
        "mensaje": f"No convergio en {max_iter} iteraciones. Error = {error:.2e}"
    }


def lu_doolittle(A, b=None):
    """
    Realiza la descomposicion LU de Doolittle y opcionalmente
    resuelve el sistema Ax = b.

    Parametros:
        A (list[list[float]]): Matriz de coeficientes (n x n)
        b (list[float], optional): Vector de terminos independientes

    Retorna:
        dict con keys: status, L, U, solucion (si b fue dado), mensaje
    """
    A = np.array(A, dtype=float)
    n = len(A)
    L = np.eye(n)  # Matriz identidad (1s en diagonal)
    U = np.zeros((n, n))

    # --- Construir L y U fila por fila ---
    for i in range(n):
        # Llenar la fila i de U (triangular superior)
        for j in range(i, n):
            U[i][j] = A[i][j] - sum(L[i][k] * U[k][j] for k in range(i))

        # Verificar pivote no nulo
        if abs(U[i][i]) < 1e-15:
            return {
                "status": "Error",
                "mensaje": f"Pivote cero en la posicion ({i+1},{i+1}). "
                           "La matriz puede ser singular."
            }

        # Llenar la columna i de L (triangular inferior)
        for j in range(i + 1, n):
            L[j][i] = (A[j][i] - sum(L[j][k] * U[k][i] for k in range(i))) / U[i][i]

    resultado = {
        "status": "OK",
        "L": L.tolist(),
        "U": U.tolist(),
        "mensaje": "Descomposicion LU completada exitosamente."
    }

    # --- Si se proporciono b, resolver el sistema ---
    if b is not None:
        b = np.array(b, dtype=float)

        # Sustitucion hacia adelante: Ly = b
        y = np.zeros(n)
        for i in range(n):
            y[i] = b[i] - sum(L[i][k] * y[k] for k in range(i))

        # Sustitucion hacia atras: Ux = y
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - sum(U[i][k] * x[k] for k in range(i + 1, n))) / U[i][i]

        resultado["solucion"] = x.tolist()
        resultado["y_intermedio"] = y.tolist()
        resultado["mensaje"] += f" Solucion: {x.tolist()}"

    return resultado


# ══════════════════════════════════════════════════════════════════
# SECCION 10: INTERPOLACION (methods/interpolacion.py)
# ══════════════════════════════════════════════════════════════════

def lagrange(xi, yi):
    """
    Construye el polinomio interpolante de Lagrange.

    Parametros:
        xi (list[float]): Valores de x de los puntos conocidos
        yi (list[float]): Valores de y de los puntos conocidos

    Retorna:
        dict con keys: status, polinomio, polinomio_expandido,
                        funcion_eval, pasos_latex
    """
    n = len(xi)
    x = sp.Symbol('x')

    # --- Construir cada polinomio base L_i(x) ---
    polinomios_base = []
    pasos = []

    for i in range(n):
        # L_i(x) = prod_{j!=i} (x - x_j) / (x_i - x_j)
        numerador = sp.Integer(1)
        denominador = 1.0
        for j in range(n):
            if i != j:
                numerador *= (x - xi[j])
                denominador *= (xi[i] - xi[j])

        Li = numerador / denominador
        polinomios_base.append(Li)

        # Guardar paso para mostrar en LaTeX
        pasos.append({
            "i": i,
            "Li": str(sp.simplify(Li)),
            "yi": yi[i],
            "termino": str(sp.simplify(yi[i] * Li))
        })

    # --- Sumar todos los terminos: P(x) = sum(yi * Li) ---
    P = sum(yi[i] * polinomios_base[i] for i in range(n))
    P_expandido = sp.expand(P)
    P_simplificado = sp.simplify(P)

    # --- Crear funcion evaluable para graficar ---
    P_func = sp.lambdify(x, P_expandido, modules=['numpy'])

    return {
        "status": "OK",
        "polinomio": str(P_simplificado),
        "polinomio_expandido": str(P_expandido),
        "funcion_eval": P_func,
        "expr_sympy": P_expandido,
        "grado": n - 1,
        "pasos": pasos,
        "mensaje": f"Polinomio de Lagrange de grado {n-1} construido exitosamente."
    }


def newton_interpolacion(xi, yi):
    """
    Construye el polinomio interpolante de Newton
    usando diferencias divididas.

    Parametros:
        xi (list[float]): Valores de x
        yi (list[float]): Valores de y

    Retorna:
        dict con keys: status, polinomio, coeficientes,
                        tabla_diferencias, funcion_eval
    """
    n = len(xi)
    x = sp.Symbol('x')

    # --- Construir tabla de diferencias divididas ---
    # tabla[i][j] = f[x_i, x_{i+1}, ..., x_{i+j}]
    tabla = np.zeros((n, n))
    tabla[:, 0] = yi  # Primera columna = valores y

    for j in range(1, n):
        for i in range(n - j):
            tabla[i][j] = (tabla[i + 1][j - 1] - tabla[i][j - 1]) / (xi[i + j] - xi[i])

    # Los coeficientes son la primera fila de la tabla
    coeficientes = tabla[0, :].tolist()

    # --- Construir el polinomio simbolicamente ---
    P = coeficientes[0]
    producto = sp.Integer(1)

    for i in range(1, n):
        producto *= (x - xi[i - 1])
        P += coeficientes[i] * producto

    P_expandido = sp.expand(P)

    # --- Crear funcion evaluable ---
    P_func = sp.lambdify(x, P_expandido, modules=['numpy'])

    return {
        "status": "OK",
        "polinomio": str(sp.simplify(P)),
        "polinomio_expandido": str(P_expandido),
        "coeficientes": coeficientes,
        "tabla_diferencias": tabla.tolist(),
        "funcion_eval": P_func,
        "expr_sympy": P_expandido,
        "grado": n - 1,
        "mensaje": f"Polinomio de Newton de grado {n-1} construido."
    }


def trazador_cubico_natural(x_arr, y_arr):
    """
    Construye trazadores cubicos naturales (natural cubic splines).

    Parametros:
        x_arr (list[float]): Valores de x (ordenados)
        y_arr (list[float]): Valores de y

    Retorna:
        dict con keys: status, trazos, funcion_eval, mensaje
    """
    x_pts = np.array(x_arr, dtype=float)
    y_pts = np.array(y_arr, dtype=float)
    n = len(x_pts) - 1  # Numero de intervalos

    if n < 1:
        return {"status": "Error", "mensaje": "Se necesitan al menos 2 puntos."}

    # --- Calcular diferencias h_i = x_{i+1} - x_i ---
    h = np.diff(x_pts)

    # --- Construir sistema tridiagonal para los coeficientes c ---
    # Ac = d, donde A es tridiagonal
    A_mat = np.zeros((n + 1, n + 1))
    d = np.zeros(n + 1)

    # Condiciones naturales: c_0 = 0, c_n = 0
    A_mat[0, 0] = 1
    A_mat[n, n] = 1

    # Ecuaciones interiores
    for i in range(1, n):
        A_mat[i, i - 1] = h[i - 1]
        A_mat[i, i] = 2 * (h[i - 1] + h[i])
        A_mat[i, i + 1] = h[i]
        d[i] = 3 * ((y_pts[i + 1] - y_pts[i]) / h[i] -
                     (y_pts[i] - y_pts[i - 1]) / h[i - 1])

    # Resolver el sistema para obtener los coeficientes c
    c = np.linalg.solve(A_mat, d)

    # --- Calcular coeficientes a, b, d para cada tramo ---
    a = y_pts[:-1]
    b_coef = (y_pts[1:] - y_pts[:-1]) / h - h * (2 * c[:-1] + c[1:]) / 3
    d_coef = (c[1:] - c[:-1]) / (3 * h)

    # --- Construir la lista de trazos ---
    trazos = []
    for j in range(n):
        trazos.append({
            "intervalo": [float(x_pts[j]), float(x_pts[j + 1])],
            "a": float(a[j]),
            "b": float(b_coef[j]),
            "c": float(c[j]),
            "d": float(d_coef[j]),
            "ecuacion": (f"S_{j}(x) = {a[j]:.6f} + {b_coef[j]:.6f}(x - {x_pts[j]:.4f}) "
                         f"+ {c[j]:.6f}(x - {x_pts[j]:.4f})^2 "
                         f"+ {d_coef[j]:.6f}(x - {x_pts[j]:.4f})^3")
        })

    # --- Crear funcion evaluable por tramos ---
    def evaluar_spline(x_eval):
        x_eval = np.atleast_1d(np.array(x_eval, dtype=float))
        y_eval = np.zeros_like(x_eval)
        for idx, xv in enumerate(x_eval):
            # Encontrar el intervalo correspondiente
            j = min(max(np.searchsorted(x_pts, xv) - 1, 0), n - 1)
            dx = xv - x_pts[j]
            y_eval[idx] = a[j] + b_coef[j] * dx + c[j] * dx**2 + d_coef[j] * dx**3
        return y_eval if len(y_eval) > 1 else y_eval[0]

    return {
        "status": "OK",
        "trazos": trazos,
        "funcion_eval": evaluar_spline,
        "n_intervalos": n,
        "mensaje": f"Trazador cubico natural con {n} tramos construido exitosamente."
    }


# ══════════════════════════════════════════════════════════════════
# SECCION 11: INTEGRACION NUMERICA (methods/integracion.py)
# ══════════════════════════════════════════════════════════════════

def trapecio(func_str, a, b, n):
    """
    Calcula la integral de f(x) en [a, b] usando la regla del trapecio.

    Parametros:
        func_str (str): Expresion de la funcion, ej: "x**2 + 1"
        a (float): Limite inferior de integracion
        b (float): Limite superior de integracion
        n (int): Numero de subintervalos

    Retorna:
        dict con keys: status, area, h, x_puntos, y_puntos, mensaje
    """
    x_sym = sp.Symbol('x')
    try:
        f_expr = sp.sympify(func_str)
        f = sp.lambdify(x_sym, f_expr, modules=['numpy'])
    except Exception as e:
        return {"status": "Error", "mensaje": f"Funcion invalida: {e}"}

    # --- Calcular el paso h y los puntos ---
    h = (b - a) / n
    x_puntos = np.linspace(a, b, n + 1)
    y_puntos = f(x_puntos)

    # --- Aplicar la formula del trapecio compuesto ---
    # area = (h/2) * [f(x_0) + 2*sum(f(x_i)) + f(x_n)]
    area = (h / 2) * (y_puntos[0] + y_puntos[-1] + 2 * np.sum(y_puntos[1:-1]))

    # --- Calcular integral exacta con SymPy para comparar ---
    try:
        integral_exacta = float(sp.integrate(f_expr, (x_sym, a, b)))
        error_abs = abs(integral_exacta - area)
    except Exception:
        integral_exacta = None
        error_abs = None

    return {
        "status": "OK",
        "area": float(area),
        "h": h,
        "n": n,
        "x_puntos": x_puntos.tolist(),
        "y_puntos": y_puntos.tolist(),
        "integral_exacta": integral_exacta,
        "error_absoluto": error_abs,
        "mensaje": f"Integral ≈ {area:.10f} con {n} subintervalos (h = {h:.6f})"
    }


def simpson_13(func_str, a, b, n):
    """
    Calcula la integral usando la regla de Simpson 1/3.

    Parametros:
        func_str (str): Expresion de la funcion
        a (float): Limite inferior
        b (float): Limite superior
        n (int): Numero de subintervalos (debe ser par)

    Retorna:
        dict con keys: status, area, h, x_puntos, y_puntos, mensaje
    """
    # --- Ajustar n para que sea par ---
    if n % 2 != 0:
        n += 1

    x_sym = sp.Symbol('x')
    try:
        f_expr = sp.sympify(func_str)
        f = sp.lambdify(x_sym, f_expr, modules=['numpy'])
    except Exception as e:
        return {"status": "Error", "mensaje": f"Funcion invalida: {e}"}

    h = (b - a) / n
    x_puntos = np.linspace(a, b, n + 1)
    y_puntos = f(x_puntos)

    # --- Aplicar la formula de Simpson 1/3 ---
    # Coeficientes: 1, 4, 2, 4, 2, ..., 4, 1
    area = y_puntos[0] + y_puntos[-1]
    area += 4 * np.sum(y_puntos[1:-1:2])   # Indices impares: coeficiente 4
    area += 2 * np.sum(y_puntos[2:-2:2])   # Indices pares (internos): coeficiente 2
    area *= h / 3

    # --- Integral exacta para comparacion ---
    try:
        integral_exacta = float(sp.integrate(f_expr, (x_sym, a, b)))
        error_abs = abs(integral_exacta - area)
    except Exception:
        integral_exacta = None
        error_abs = None

    return {
        "status": "OK",
        "area": float(area),
        "h": h,
        "n": n,
        "x_puntos": x_puntos.tolist(),
        "y_puntos": y_puntos.tolist(),
        "integral_exacta": integral_exacta,
        "error_absoluto": error_abs,
        "mensaje": f"Integral ≈ {area:.10f} con {n} subintervalos (h = {h:.6f})"
    }


def simpson_38(func_str, a, b, n):
    """
    Calcula la integral usando la regla de Simpson 3/8.

    Parametros:
        func_str (str): Expresion de la funcion
        a (float): Limite inferior
        b (float): Limite superior
        n (int): Numero de subintervalos (multiplo de 3)

    Retorna:
        dict con keys: status, area, h, x_puntos, y_puntos, mensaje
    """
    # --- Ajustar n para que sea multiplo de 3 ---
    if n % 3 != 0:
        n += (3 - n % 3)

    x_sym = sp.Symbol('x')
    try:
        f_expr = sp.sympify(func_str)
        f = sp.lambdify(x_sym, f_expr, modules=['numpy'])
    except Exception as e:
        return {"status": "Error", "mensaje": f"Funcion invalida: {e}"}

    h = (b - a) / n
    x_puntos = np.linspace(a, b, n + 1)
    y_puntos = f(x_puntos)

    # --- Aplicar la formula de Simpson 3/8 ---
    # Coeficientes: 1, 3, 3, 2, 3, 3, 2, ..., 3, 3, 1
    area = y_puntos[0] + y_puntos[-1]
    for i in range(1, n):
        if i % 3 == 0:
            area += 2 * y_puntos[i]  # Cada 3er punto interno: coeficiente 2
        else:
            area += 3 * y_puntos[i]  # Los demas: coeficiente 3
    area *= 3 * h / 8

    # --- Integral exacta para comparacion ---
    try:
        integral_exacta = float(sp.integrate(f_expr, (x_sym, a, b)))
        error_abs = abs(integral_exacta - area)
    except Exception:
        integral_exacta = None
        error_abs = None

    return {
        "status": "OK",
        "area": float(area),
        "h": h,
        "n": n,
        "x_puntos": x_puntos.tolist(),
        "y_puntos": y_puntos.tolist(),
        "integral_exacta": integral_exacta,
        "error_absoluto": error_abs,
        "mensaje": f"Integral ≈ {area:.10f} con {n} subintervalos (h = {h:.6f})"
    }


# ══════════════════════════════════════════════════════════════════
# SECCION 12: EDOs (methods/edo.py)
# ══════════════════════════════════════════════════════════════════

def euler(func_str, t0, tf, y0, N):
    """
    Resuelve dy/dt = f(t, y) con el metodo de Euler.

    Parametros:
        func_str (str): Expresion de f(t, y), ej: "t + y"
        t0 (float): Tiempo inicial
        tf (float): Tiempo final
        y0 (float): Condicion inicial y(t0) = y0
        N (int): Numero de pasos

    Retorna:
        dict con keys: status, t, y, h, mensaje
    """
    t_sym, y_sym = sp.symbols('t y')
    try:
        f_expr = sp.sympify(func_str)
        f = sp.lambdify((t_sym, y_sym), f_expr, modules=['numpy'])
    except Exception as e:
        return {"status": "Error", "mensaje": f"Funcion invalida: {e}"}

    h = (tf - t0) / N
    t = np.zeros(N + 1)
    y = np.zeros(N + 1)
    t[0] = t0
    y[0] = y0

    # --- Iteraciones del metodo de Euler ---
    historial = []
    for i in range(N):
        pendiente = f(t[i], y[i])
        t[i + 1] = t[i] + h
        y[i + 1] = y[i] + h * pendiente

        historial.append({
            "paso": i + 1,
            "t_n": t[i],
            "y_n": y[i],
            "f(t_n, y_n)": pendiente,
            "y_{n+1}": y[i + 1]
        })

    return {
        "status": "OK",
        "t": t.tolist(),
        "y": y.tolist(),
        "h": h,
        "historial": historial,
        "metodo": "Euler",
        "orden": 1,
        "mensaje": f"Euler completado con {N} pasos (h = {h:.6f}). y({tf}) ≈ {y[-1]:.10f}"
    }


def rk2(func_str, t0, tf, y0, N):
    """
    Resuelve dy/dt = f(t, y) con Runge-Kutta de 2do orden (Heun).

    Parametros:
        func_str (str): Expresion de f(t, y)
        t0 (float): Tiempo inicial
        tf (float): Tiempo final
        y0 (float): Condicion inicial
        N (int): Numero de pasos

    Retorna:
        dict con keys: status, t, y, h, historial, mensaje
    """
    t_sym, y_sym = sp.symbols('t y')
    try:
        f_expr = sp.sympify(func_str)
        f = sp.lambdify((t_sym, y_sym), f_expr, modules=['numpy'])
    except Exception as e:
        return {"status": "Error", "mensaje": f"Funcion invalida: {e}"}

    h = (tf - t0) / N
    t = np.zeros(N + 1)
    y = np.zeros(N + 1)
    t[0] = t0
    y[0] = y0

    historial = []
    for i in range(N):
        # Paso 1: Pendiente al inicio del intervalo
        k1 = h * f(t[i], y[i])
        # Paso 2: Pendiente al final del intervalo (usando prediccion de Euler)
        k2 = h * f(t[i] + h, y[i] + k1)
        # Paso 3: Promedio de ambas pendientes
        t[i + 1] = t[i] + h
        y[i + 1] = y[i] + 0.5 * (k1 + k2)

        historial.append({
            "paso": i + 1,
            "t_n": t[i],
            "y_n": y[i],
            "k1": k1,
            "k2": k2,
            "y_{n+1}": y[i + 1]
        })

    return {
        "status": "OK",
        "t": t.tolist(),
        "y": y.tolist(),
        "h": h,
        "historial": historial,
        "metodo": "RK2 (Heun)",
        "orden": 2,
        "mensaje": f"RK2 completado con {N} pasos (h = {h:.6f}). y({tf}) ≈ {y[-1]:.10f}"
    }


def rk4(func_str, t0, tf, y0, N):
    """
    Resuelve dy/dt = f(t, y) con Runge-Kutta de 4to orden.

    Parametros:
        func_str (str): Expresion de f(t, y)
        t0 (float): Tiempo inicial
        tf (float): Tiempo final
        y0 (float): Condicion inicial
        N (int): Numero de pasos

    Retorna:
        dict con keys: status, t, y, h, historial, mensaje
    """
    t_sym, y_sym = sp.symbols('t y')
    try:
        f_expr = sp.sympify(func_str)
        f = sp.lambdify((t_sym, y_sym), f_expr, modules=['numpy'])
    except Exception as e:
        return {"status": "Error", "mensaje": f"Funcion invalida: {e}"}

    h = (tf - t0) / N
    t = np.zeros(N + 1)
    y = np.zeros(N + 1)
    t[0] = t0
    y[0] = y0

    historial = []
    for i in range(N):
        k1 = h * f(t[i], y[i])
        k2 = h * f(t[i] + h / 2, y[i] + k1 / 2)
        k3 = h * f(t[i] + h / 2, y[i] + k2 / 2)
        k4 = h * f(t[i] + h, y[i] + k3)

        t[i + 1] = t[i] + h
        y[i + 1] = y[i] + (k1 + 2 * k2 + 2 * k3 + k4) / 6

        historial.append({
            "paso": i + 1,
            "t_n": t[i],
            "y_n": y[i],
            "k1": k1,
            "k2": k2,
            "k3": k3,
            "k4": k4,
            "y_{n+1}": y[i + 1]
        })

    return {
        "status": "OK",
        "t": t.tolist(),
        "y": y.tolist(),
        "h": h,
        "historial": historial,
        "metodo": "RK4",
        "orden": 4,
        "mensaje": f"RK4 completado con {N} pasos (h = {h:.6f}). y({tf}) ≈ {y[-1]:.10f}"
    }


def verlet(a_func_str, t0, tf, x0, v0, N):
    """
    Resuelve x'' = a(t, x) con el metodo de Verlet.

    Parametros:
        a_func_str (str): Expresion de la aceleracion a(t, x), ej: "-x"
        t0 (float): Tiempo inicial
        tf (float): Tiempo final
        x0 (float): Posicion inicial x(t0) = x0
        v0 (float): Velocidad inicial x'(t0) = v0
        N (int): Numero de pasos

    Retorna:
        dict con keys: status, t, x, h, historial, mensaje
    """
    t_sym, x_sym = sp.symbols('t x')
    try:
        a_expr = sp.sympify(a_func_str)
        a_func = sp.lambdify((t_sym, x_sym), a_expr, modules=['numpy'])
    except Exception as e:
        return {"status": "Error", "mensaje": f"Funcion de aceleracion invalida: {e}"}

    h = (tf - t0) / N
    t = np.zeros(N + 1)
    x = np.zeros(N + 1)
    t[0] = t0
    x[0] = x0

    # --- Primer paso con expansion de Taylor ---
    t[1] = t0 + h
    x[1] = x0 + v0 * h + 0.5 * a_func(t0, x0) * h**2

    historial = [{
        "paso": 1,
        "t_n": t[0],
        "x_n": x[0],
        "a(t_n, x_n)": a_func(t0, x0),
        "x_{n+1}": x[1]
    }]

    # --- Iteraciones del metodo de Verlet ---
    for i in range(1, N):
        t[i + 1] = t[i] + h
        a_i = a_func(t[i], x[i])
        x[i + 1] = 2 * x[i] - x[i - 1] + a_i * h**2

        historial.append({
            "paso": i + 1,
            "t_n": t[i],
            "x_n": x[i],
            "a(t_n, x_n)": a_i,
            "x_{n+1}": x[i + 1]
        })

    return {
        "status": "OK",
        "t": t.tolist(),
        "x": x.tolist(),
        "h": h,
        "historial": historial,
        "metodo": "Verlet",
        "orden": 2,
        "mensaje": f"Verlet completado con {N} pasos (h = {h:.6f}). x({tf}) ≈ {x[-1]:.10f}"
    }


def analisis_orden(metodo_func, func_str, t0, tf, y0, solucion_exacta_str=None,
                   N_base=10, niveles=6, **kwargs):
    """
    Analiza el orden de convergencia de un metodo numerico.

    Parametros:
        metodo_func (callable): Funcion del metodo (euler, rk2, rk4)
        func_str (str): Expresion de f(t, y)
        t0, tf, y0: Condiciones del problema
        solucion_exacta_str (str): Expresion de la solucion exacta (opcional)
        N_base (int): Numero de pasos base
        niveles (int): Cuantos refinamientos hacer

    Retorna:
        dict con: h_values, errores, ordenes_estimados, mensaje
    """
    # Si se da solucion exacta, usarla; si no, usar la solucion con N muy grande
    if solucion_exacta_str:
        t_sym = sp.Symbol('t')
        y_exacta_func = sp.lambdify(t_sym, sp.sympify(solucion_exacta_str), modules=['numpy'])
        y_ref = y_exacta_func(tf)
    else:
        # Usar solucion con N muy grande como referencia
        res_ref = metodo_func(func_str, t0, tf, y0, N_base * (2**niveles), **kwargs)
        y_ref = res_ref["y"][-1] if "y" in res_ref else res_ref["x"][-1]

    h_values = []
    errores = []

    for k in range(niveles):
        N = N_base * (2**k)
        resultado = metodo_func(func_str, t0, tf, y0, N, **kwargs)

        if resultado["status"] == "Error":
            continue

        h = (tf - t0) / N
        y_final = resultado["y"][-1] if "y" in resultado else resultado["x"][-1]
        error = abs(y_final - y_ref)

        h_values.append(h)
        errores.append(error if error > 0 else 1e-16)

    # --- Estimar el orden de convergencia ---
    ordenes = []
    for i in range(1, len(errores)):
        if errores[i] > 0 and errores[i - 1] > 0 and h_values[i] > 0 and h_values[i - 1] > 0:
            p = np.log(errores[i - 1] / errores[i]) / np.log(h_values[i - 1] / h_values[i])
            ordenes.append(round(p, 2))

    orden_promedio = np.mean(ordenes) if ordenes else 0

    return {
        "status": "OK",
        "h_values": h_values,
        "errores": errores,
        "ordenes_estimados": ordenes,
        "orden_promedio": orden_promedio,
        "mensaje": f"Orden de convergencia estimado: {orden_promedio:.2f}"
    }


# ══════════════════════════════════════════════════════════════════
# SECCION 13: VISTA: INICIO (views/home.py)
# ══════════════════════════════════════════════════════════════════

def vista_inicio():
    """Renderiza la pagina de inicio tipo dashboard."""

    # ============================================================
    # HEADER: Logo y titulo principal
    # ============================================================
    col_spacer1, col_logo, col_spacer2 = st.columns([1, 2, 1])
    with col_logo:
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "unitec_color.png")
        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)

    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="
            font-size: 2.8rem;
            background: linear-gradient(135deg, #00e5ff 0%, #b388ff 50%, #ff007f 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            font-weight: 800;
            letter-spacing: -1px;
        ">Calculadora de Metodos Numericos</h1>
        <p style="
            color: #8b8b9e;
            font-size: 1.1rem;
            margin: 0;
        ">Herramienta interactiva para el analisis numerico | MECATON 2026</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ============================================================
    # METRICAS GLOBALES: Resumen de la calculadora
    # ============================================================
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Modulos", "5")
    m2.metric("Metodos", "15")
    m3.metric("Graficas", "Interactivas")
    m4.metric("Exportacion", "PDF")

    st.markdown("")

    # ============================================================
    # TARJETAS DE MODULOS: Acceso rapido a cada seccion
    # ============================================================
    st.markdown("### Modulos Disponibles")
    st.markdown("Selecciona un modulo en el **panel lateral izquierdo** para comenzar.")
    st.markdown("")

    # --- Fila 1: 3 tarjetas ---
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="
            background: rgba(0, 229, 255, 0.05);
            border: 1px solid rgba(0, 229, 255, 0.15);
            border-radius: 16px;
            padding: 24px;
            min-height: 220px;
            transition: all 0.3s ease;
        ">
            <h3 style="color: #00e5ff; margin-top: 0; font-size: 1.2rem;">
                Ecuaciones No Lineales
            </h3>
            <p style="color: #8b8b9e; font-size: 0.9rem; line-height: 1.6;">
                Encuentra raices de <strong style="color:#e8e8ed;">f(x) = 0</strong>
            </p>
            <ul style="color: #b0b0c0; font-size: 0.85rem; padding-left: 16px;">
                <li>Biseccion</li>
                <li>Newton-Raphson</li>
                <li>Punto Fijo</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
            background: rgba(179, 136, 255, 0.05);
            border: 1px solid rgba(179, 136, 255, 0.15);
            border-radius: 16px;
            padding: 24px;
            min-height: 220px;
            transition: all 0.3s ease;
        ">
            <h3 style="color: #b388ff; margin-top: 0; font-size: 1.2rem;">
                Sistemas de Ecuaciones Lineales
            </h3>
            <p style="color: #8b8b9e; font-size: 0.9rem; line-height: 1.6;">
                Resuelve sistemas <strong style="color:#e8e8ed;">Ax = b</strong>
            </p>
            <ul style="color: #b0b0c0; font-size: 0.85rem; padding-left: 16px;">
                <li>Jacobi</li>
                <li>Gauss-Seidel</li>
                <li>Descomposicion LU</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="
            background: rgba(0, 255, 204, 0.05);
            border: 1px solid rgba(0, 255, 204, 0.15);
            border-radius: 16px;
            padding: 24px;
            min-height: 220px;
            transition: all 0.3s ease;
        ">
            <h3 style="color: #00ffcc; margin-top: 0; font-size: 1.2rem;">
                Interpolacion
            </h3>
            <p style="color: #8b8b9e; font-size: 0.9rem; line-height: 1.6;">
                Construye polinomios por <strong style="color:#e8e8ed;">puntos dados</strong>
            </p>
            <ul style="color: #b0b0c0; font-size: 0.85rem; padding-left: 16px;">
                <li>Lagrange</li>
                <li>Newton (Dif. Divididas)</li>
                <li>Trazadores Cubicos</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # --- Fila 2: 2 tarjetas centradas ---
    col4, col5 = st.columns(2)

    with col4:
        st.markdown("""
        <div style="
            background: rgba(255, 0, 127, 0.05);
            border: 1px solid rgba(255, 0, 127, 0.15);
            border-radius: 16px;
            padding: 24px;
            min-height: 220px;
            transition: all 0.3s ease;
        ">
            <h3 style="color: #ff007f; margin-top: 0; font-size: 1.2rem;">
                Integracion Numerica
            </h3>
            <p style="color: #8b8b9e; font-size: 0.9rem; line-height: 1.6;">
                Aproxima integrales definidas de funciones
            </p>
            <ul style="color: #b0b0c0; font-size: 0.85rem; padding-left: 16px;">
                <li>Regla del Trapecio</li>
                <li>Simpson 1/3</li>
                <li>Simpson 3/8</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div style="
            background: rgba(255, 234, 0, 0.05);
            border: 1px solid rgba(255, 234, 0, 0.15);
            border-radius: 16px;
            padding: 24px;
            min-height: 220px;
            transition: all 0.3s ease;
        ">
            <h3 style="color: #ffea00; margin-top: 0; font-size: 1.2rem;">
                Ecuaciones Diferenciales (EDO)
            </h3>
            <p style="color: #8b8b9e; font-size: 0.9rem; line-height: 1.6;">
                Resuelve EDOs de la forma <strong style="color:#e8e8ed;">dy/dt = f(t, y)</strong>
            </p>
            <ul style="color: #b0b0c0; font-size: 0.85rem; padding-left: 16px;">
                <li>Euler</li>
                <li>RK2 y RK4</li>
                <li>Verlet</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    st.divider()

    # ============================================================
    # STACK TECNOLOGICO
    # ============================================================
    st.markdown("### Stack Tecnologico")
    t1, t2, t3, t4 = st.columns(4)
    t1.markdown("**Python** — Motor principal")
    t2.markdown("**Streamlit** — Interfaz web")
    t3.markdown("**SymPy** — Algebra simbolica")
    t4.markdown("**Plotly** — Graficas interactivas")


# ══════════════════════════════════════════════════════════════════
# SECCION 14: VISTA: ECUACIONES NO LINEALES (views/no_lineales.py)
# ══════════════════════════════════════════════════════════════════

EJEMPLOS_BISECCION = {
    "Seleccionar ejemplo...": {"func": "x^3 - x - 2", "a": 1.0, "b": 2.0, "tol": 0.0001},
    "Polinomio cubico: x^3 - x - 2": {"func": "x^3 - x - 2", "a": 1.0, "b": 2.0, "tol": 0.0001},
    "Trigonometrica: cos(x) - x": {"func": "cos(x) - x", "a": 0.0, "b": 1.5, "tol": 0.00001},
    "Exponencial: e^(-x) - x": {"func": "exp(-x) - x", "a": 0.0, "b": 1.0, "tol": 0.0001},
    "Cuadratica: x^2 - 4": {"func": "x^2 - 4", "a": 0.0, "b": 3.0, "tol": 0.0001},
    "Logaritmica: ln(x) - 1": {"func": "ln(x) - 1", "a": 1.0, "b": 4.0, "tol": 0.0001},
}

EJEMPLOS_NEWTON = {
    "Seleccionar ejemplo...": {"func": "x^3 - x - 2", "x0": 1.5, "tol": 0.0001},
    "Polinomio cubico: x^3 - x - 2": {"func": "x^3 - x - 2", "x0": 1.5, "tol": 0.0001},
    "Raiz cuadrada de 2: x^2 - 2": {"func": "x^2 - 2", "x0": 1.0, "tol": 1e-10},
    "Trigonometrica: sin(x) - x/2": {"func": "sin(x) - x/2", "x0": 2.0, "tol": 0.00001},
    "Exponencial: exp(x) - 3*x": {"func": "exp(x) - 3*x", "x0": 1.0, "tol": 0.0001},
}

EJEMPLOS_PUNTO_FIJO = {
    "Seleccionar ejemplo...": {"func": "(x + 2/x) / 2", "x0": 1.0, "tol": 0.0001},
    "Raiz de 2: g(x) = (x + 2/x)/2": {"func": "(x + 2/x) / 2", "x0": 1.0, "tol": 0.0001},
    "Cubica: g(x) = (x + 2)^(1/3)": {"func": "(x + 2)**(1/3)", "x0": 1.0, "tol": 0.0001},
    "Coseno: g(x) = cos(x)": {"func": "cos(x)", "x0": 0.5, "tol": 0.00001},
}


def vista_no_lineales():
    """Renderiza la vista completa de ecuaciones no lineales."""

    # ============================================================
    # HEADER: Titulo, descripcion y boton reiniciar
    # ============================================================
    col_titulo, col_reset = st.columns([5, 1])
    with col_titulo:
        st.title("Ecuaciones No Lineales")
        st.markdown("Encuentra raices de ecuaciones de la forma **f(x) = 0**")
    with col_reset:
        st.markdown("")
        st.markdown("")
        # --- Boton Reiniciar: Limpia todos los campos del modulo ---
        if st.button("Reiniciar", key="reset_nl", help="Limpia todos los campos y resultados"):
            for key in list(st.session_state.keys()):
                if any(s in key for s in ["bis", "nr", "pf", "func_", "ejemplo_"]):
                    del st.session_state[key]
            st.rerun()

    # ============================================================
    # TABS: Selector de metodo
    # ============================================================
    tab_biseccion, tab_newton, tab_punto_fijo = st.tabs([
        "Biseccion",
        "Newton-Raphson",
        "Punto Fijo"
    ])

    # ============================================================
    # TAB 1: METODO DE BISECCION
    # ============================================================
    with tab_biseccion:
        st.latex(latex_metodo_descripcion("Biseccion"))
        st.divider()

        # --- Selector de ejemplos pre-cargados ---
        ejemplo_bis = st.selectbox(
            "Ejemplos rapidos",
            options=list(EJEMPLOS_BISECCION.keys()),
            key="ejemplo_bis",
            help="Selecciona un problema clasico para cargar automaticamente"
        )
        ej = EJEMPLOS_BISECCION[ejemplo_bis]

        # --- Campos de entrada ---
        col1, col2 = st.columns(2)
        with col1:
            func_bis = st.text_input(
                "Funcion f(x)",
                value=ej["func"],
                key="func_bis",
                help="Escriba la funcion. Puede usar: x^2, sen(x), cos(x), exp(x), ln(x), raiz(x)"
            )
        with col2:
            tol_bis = st.number_input(
                "Tolerancia", value=ej["tol"], format="%.6f",
                min_value=1e-15, max_value=1.0, key="tol_bis"
            )

        col3, col4, col5 = st.columns(3)
        with col3:
            a_bis = st.number_input("a (limite inferior)", value=ej["a"], key="a_bis")
        with col4:
            b_bis = st.number_input("b (limite superior)", value=ej["b"], key="b_bis")
        with col5:
            max_iter_bis = st.number_input("Max iteraciones", value=100, min_value=1, key="max_bis")

        # --- Boton calcular ---
        if st.button("CALCULAR BISECCION", key="btn_bis", type="primary"):
            try:
                expr = parsear_funcion(func_bis)
                func_str = str(expr)

                resultado = biseccion(func_str, a_bis, b_bis, tol_bis, int(max_iter_bis))

                if resultado["status"] == "Error":
                    st.error(f"Error: {resultado['mensaje']}")
                else:
                    # --- Metricas de resultado ---
                    st.success(resultado["mensaje"])
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Raiz", f"{resultado['raiz']:.10f}")
                    m2.metric("Iteraciones", resultado["iteraciones"])
                    m3.metric("Error Final", f"{resultado['error_final']:.2e}")

                    # --- Graficas lado a lado ---
                    f_eval = crear_funcion_numerica(expr)
                    gc1, gc2 = st.columns(2)
                    with gc1:
                        fig = graficar_funcion_raiz(
                            f_eval, resultado["raiz"], a_bis, b_bis,
                            titulo="f(x) — Biseccion",
                            historial=resultado["historial"]
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    with gc2:
                        fig_conv = graficar_convergencia(
                            resultado["historial"], key_error="error |b-a|"
                        )
                        st.plotly_chart(fig_conv, use_container_width=True)

                    # --- Tabla de iteraciones ---
                    with st.expander("Ver tabla de iteraciones", expanded=True):
                        df = pd.DataFrame(resultado["historial"])
                        st.dataframe(df, use_container_width=True, hide_index=True)

                    # --- Pasos en LaTeX ---
                    with st.expander("Ver pasos matematicos (LaTeX)"):
                        for h in resultado["historial"][:10]:
                            st.latex(latex_biseccion_paso(
                                h["iteracion"], h["a"], h["b"],
                                h["c (punto medio)"], h["f(c)"], h["error |b-a|"]
                            ))
                        if len(resultado["historial"]) > 10:
                            st.info(f"... mostrando 10 de {len(resultado['historial'])} iteraciones")

            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Error inesperado: {e}")

    # ============================================================
    # TAB 2: METODO DE NEWTON-RAPHSON
    # ============================================================
    with tab_newton:
        st.latex(latex_metodo_descripcion("Newton-Raphson"))
        st.divider()

        # --- Selector de ejemplos pre-cargados ---
        ejemplo_nr = st.selectbox(
            "Ejemplos rapidos",
            options=list(EJEMPLOS_NEWTON.keys()),
            key="ejemplo_nr",
            help="Selecciona un problema clasico para cargar automaticamente"
        )
        ej_nr = EJEMPLOS_NEWTON[ejemplo_nr]

        col1, col2 = st.columns(2)
        with col1:
            func_nr = st.text_input(
                "Funcion f(x)",
                value=ej_nr["func"],
                key="func_nr",
                help="La derivada se calcula automaticamente con SymPy"
            )
        with col2:
            tol_nr = st.number_input(
                "Tolerancia", value=ej_nr["tol"], format="%.6f",
                min_value=1e-15, key="tol_nr"
            )

        col3, col4 = st.columns(2)
        with col3:
            x0_nr = st.number_input("x0 (valor inicial)", value=ej_nr["x0"], key="x0_nr")
        with col4:
            max_iter_nr = st.number_input("Max iteraciones", value=100, min_value=1, key="max_nr")

        # --- Mostrar derivada calculada automaticamente ---
        try:
            expr_nr = parsear_funcion(func_nr)
            x = sp.Symbol('x')
            derivada = sp.diff(expr_nr, x)
            st.markdown(f"**Derivada calculada:** f'(x) = `{derivada}`")
        except Exception:
            pass

        if st.button("CALCULAR NEWTON-RAPHSON", key="btn_nr", type="primary"):
            try:
                expr_nr = parsear_funcion(func_nr)
                func_str = str(expr_nr)

                resultado = newton_raphson(func_str, x0_nr, tol_nr, int(max_iter_nr))

                if resultado["status"] == "Error":
                    st.error(f"Error: {resultado['mensaje']}")
                else:
                    st.success(resultado["mensaje"])
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Raiz", f"{resultado['raiz']:.10f}")
                    m2.metric("Iteraciones", resultado["iteraciones"])
                    m3.metric("Error Final", f"{resultado['error_final']:.2e}")

                    f_eval = crear_funcion_numerica(expr_nr)
                    gc1, gc2 = st.columns(2)
                    with gc1:
                        fig = graficar_funcion_raiz(
                            f_eval, resultado["raiz"],
                            resultado["raiz"] - 2, resultado["raiz"] + 2,
                            titulo="f(x) — Newton-Raphson",
                            historial=resultado["historial"]
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    with gc2:
                        fig_conv = graficar_convergencia(resultado["historial"])
                        st.plotly_chart(fig_conv, use_container_width=True)

                    with st.expander("Ver tabla de iteraciones", expanded=True):
                        df = pd.DataFrame(resultado["historial"])
                        st.dataframe(df, use_container_width=True, hide_index=True)

                    with st.expander("Ver pasos matematicos (LaTeX)"):
                        for h in resultado["historial"][:10]:
                            st.latex(latex_newton_paso(
                                h["iteracion"], h["x_n"], h["f(x_n)"],
                                h["f'(x_n)"], h["x_{n+1}"], h["error"]
                            ))

            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Error inesperado: {e}")

    # ============================================================
    # TAB 3: METODO DE PUNTO FIJO
    # ============================================================
    with tab_punto_fijo:
        st.latex(latex_metodo_descripcion("Punto Fijo"))
        st.divider()

        st.info(
            "Transforme f(x) = 0 en la forma x = g(x). "
            "Ejemplo: si f(x) = x^2 - 2, puede usar g(x) = (x + 2/x)/2"
        )

        # --- Selector de ejemplos pre-cargados ---
        ejemplo_pf = st.selectbox(
            "Ejemplos rapidos",
            options=list(EJEMPLOS_PUNTO_FIJO.keys()),
            key="ejemplo_pf",
            help="Selecciona un problema clasico para cargar automaticamente"
        )
        ej_pf = EJEMPLOS_PUNTO_FIJO[ejemplo_pf]

        col1, col2 = st.columns(2)
        with col1:
            func_pf = st.text_input(
                "Funcion g(x) (forma x = g(x))",
                value=ej_pf["func"],
                key="func_pf"
            )
        with col2:
            tol_pf = st.number_input(
                "Tolerancia", value=ej_pf["tol"], format="%.6f",
                min_value=1e-15, key="tol_pf"
            )

        col3, col4 = st.columns(2)
        with col3:
            x0_pf = st.number_input("x0 (valor inicial)", value=ej_pf["x0"], key="x0_pf")
        with col4:
            max_iter_pf = st.number_input("Max iteraciones", value=1000, min_value=1, key="max_pf")

        if st.button("CALCULAR PUNTO FIJO", key="btn_pf", type="primary"):
            try:
                expr_pf = parsear_funcion(func_pf)
                func_str = str(expr_pf)

                resultado = punto_fijo(func_str, x0_pf, tol_pf, int(max_iter_pf))

                if resultado["status"] == "Error":
                    st.error(f"Error: {resultado['mensaje']}")
                else:
                    st.success(resultado["mensaje"])
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Punto Fijo", f"{resultado['raiz']:.10f}")
                    m2.metric("Iteraciones", resultado["iteraciones"])
                    m3.metric("Error Final", f"{resultado['error_final']:.2e}")

                    with st.expander("Ver tabla de iteraciones", expanded=True):
                        df = pd.DataFrame(resultado["historial"])
                        st.dataframe(df, use_container_width=True, hide_index=True)

                    fig_conv = graficar_convergencia(resultado["historial"])
                    st.plotly_chart(fig_conv, use_container_width=True)

                    with st.expander("Ver pasos matematicos (LaTeX)"):
                        for h in resultado["historial"][:10]:
                            st.latex(latex_punto_fijo_paso(
                                h["iteracion"], h["x_n"], h["g(x_n)"], h["error"]
                            ))

            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Error inesperado: {e}")


# ══════════════════════════════════════════════════════════════════
# SECCION 15: VISTA: SISTEMAS LINEALES (views/sistemas_lineales.py)
# ══════════════════════════════════════════════════════════════════

def vista_sistemas_lineales():
    """Renderiza la vista completa de sistemas lineales."""

    # ============================================================
    # HEADER: Titulo y boton reiniciar
    # ============================================================
    col_titulo, col_reset = st.columns([5, 1])
    with col_titulo:
        st.title("Sistemas de Ecuaciones Lineales")
        st.markdown("Resuelve sistemas de la forma **Ax = b**")
    with col_reset:
        st.markdown("")
        st.markdown("")
        # --- Boton Reiniciar: Limpia todos los campos del modulo ---
        if st.button("Reiniciar", key="reset_sl", help="Limpia todos los campos y resultados"):
            for key in list(st.session_state.keys()):
                if any(s in key for s in ["jacobi", "gaussseidel", "lu", "a_", "b_", "n_"]):
                    del st.session_state[key]
            st.rerun()

    # ============================================================
    # TABS: Selector de metodo
    # ============================================================
    tab_jacobi, tab_gs, tab_lu = st.tabs([
        "Jacobi",
        "Gauss-Seidel",
        "Descomposicion LU"
    ])

    # ============================================================
    # TAB 1: METODO DE JACOBI
    # ============================================================
    with tab_jacobi:
        st.latex(latex_metodo_descripcion("Jacobi"))
        st.divider()
        _render_metodo_iterativo("Jacobi", jacobi)

    # ============================================================
    # TAB 2: METODO DE GAUSS-SEIDEL
    # ============================================================
    with tab_gs:
        st.latex(latex_metodo_descripcion("Gauss-Seidel"))
        st.divider()
        _render_metodo_iterativo("Gauss-Seidel", gauss_seidel)

    # ============================================================
    # TAB 3: DESCOMPOSICION LU
    # ============================================================
    with tab_lu:
        st.latex(latex_metodo_descripcion("LU Doolittle"))
        st.divider()
        _render_lu()


def _render_metodo_iterativo(nombre, metodo_func):
    """
    Renderiza la interfaz para un metodo iterativo (Jacobi o Gauss-Seidel).
    Esta funcion se reutiliza para ambos metodos ya que la UI es identica.
    """
    key = nombre.lower().replace("-", "")

    # --- Selector de ejemplo pre-cargado ---
    ejemplo = st.selectbox(
        "Ejemplos rapidos",
        options=["Seleccionar ejemplo...", "Sistema 3x3 diagonal dominante", "Sistema 3x3 tridiagonal"],
        key=f"ejemplo_{key}",
        help="Selecciona un sistema clasico"
    )

    # --- Tamano de la matriz ---
    n = st.number_input(
        f"Tamano del sistema (n x n)",
        min_value=2, max_value=10, value=3,
        key=f"n_{key}"
    )

    st.markdown("**Matriz A (coeficientes):**")

    # --- Determinar valores por defecto segun ejemplo seleccionado ---
    def default_a(i, j):
        if i == j:
            return 4.0
        elif abs(i - j) == 1:
            return -1.0
        return 0.0

    def default_b(i):
        return 5.0 if (i == 0 or i == n - 1) else 6.0

    # --- Editor de Matriz A ---
    cols_a = st.columns(n)
    A = []
    for i in range(n):
        fila = []
        for j in range(n):
            with cols_a[j]:
                val = st.number_input(
                    f"A[{i+1},{j+1}]",
                    value=default_a(i, j),
                    key=f"a_{key}_{i}_{j}",
                    label_visibility="collapsed" if i > 0 else "visible"
                )
                fila.append(val)
        A.append(fila)

    # --- Vector b ---
    st.markdown("**Vector b (terminos independientes):**")
    cols_b = st.columns(n)
    b = []
    for i in range(n):
        with cols_b[i]:
            val = st.number_input(
                f"b[{i+1}]",
                value=default_b(i),
                key=f"b_{key}_{i}"
            )
            b.append(val)

    # --- Parametros ---
    col1, col2 = st.columns(2)
    with col1:
        tol = st.number_input("Tolerancia", value=0.0001, format="%.6f", key=f"tol_{key}")
    with col2:
        max_iter = st.number_input("Max iteraciones", value=100, min_value=1, key=f"max_{key}")

    # --- Vector inicial ---
    st.markdown("**Vector inicial x0:** (todos en cero)")
    x0 = [0.0] * n

    # --- Boton calcular ---
    if st.button(f"RESOLVER CON {nombre.upper()}", key=f"btn_{key}", type="primary"):
        # Validar la matriz
        valido, msg = validar_matriz(A, b)
        if not valido:
            st.error(msg)
            return

        # Advertencia de diagonal dominante
        dom, msg_dom = validar_diagonal_dominante(A)
        if not dom:
            st.warning(msg_dom)

        resultado = metodo_func(A, b, x0, tol, int(max_iter))

        if resultado["status"] == "Error":
            st.error(resultado["mensaje"])
        else:
            st.success(resultado["mensaje"])

            # --- Solucion ---
            st.markdown("**Solucion encontrada:**")
            sol_cols = st.columns(n)
            for i, val in enumerate(resultado["solucion"]):
                sol_cols[i].metric(f"x{i+1}", f"{val:.8f}")

            # --- Grafica de convergencia ---
            fig = graficar_convergencia(
                resultado["historial"],
                titulo=f"Convergencia — {nombre}"
            )
            st.plotly_chart(fig, use_container_width=True)

            # --- Tabla de iteraciones ---
            with st.expander("Ver tabla de iteraciones", expanded=True):
                filas = []
                for h in resultado["historial"]:
                    fila = {"Iteracion": h["iteracion"], "Error": h["error"]}
                    for i, val in enumerate(h["x"]):
                        fila[f"x{i+1}"] = val
                    filas.append(fila)
                df = pd.DataFrame(filas)
                st.dataframe(df, use_container_width=True, hide_index=True)


def _render_lu():
    """Renderiza la interfaz para la descomposicion LU."""

    # --- Selector de ejemplo ---
    ejemplo_lu = st.selectbox(
        "Ejemplos rapidos",
        options=["Seleccionar ejemplo...", "Matriz 3x3 simple", "Matriz tridiagonal"],
        key="ejemplo_lu"
    )

    n = st.number_input(
        "Tamano del sistema (n x n)",
        min_value=2, max_value=10, value=3,
        key="n_lu"
    )

    st.markdown("**Matriz A:**")
    cols_a = st.columns(n)
    A = []
    for i in range(n):
        fila = []
        for j in range(n):
            with cols_a[j]:
                val = st.number_input(
                    f"A[{i+1},{j+1}]",
                    value=float(2 if i == j else -1 if abs(i-j) == 1 else 0),
                    key=f"a_lu_{i}_{j}",
                    label_visibility="collapsed" if i > 0 else "visible"
                )
                fila.append(val)
        A.append(fila)

    # --- Vector b ---
    st.markdown("**Vector b (terminos independientes):**")
    cols_b = st.columns(n)
    b = []
    for i in range(n):
        with cols_b[i]:
            val = st.number_input(
                f"b[{i+1}]",
                value=float(1),
                key=f"b_lu_{i}"
            )
            b.append(val)

    if st.button("DESCOMPONER LU Y RESOLVER", key="btn_lu", type="primary"):
        valido, msg = validar_matriz(A, b)
        if not valido:
            st.error(msg)
            return

        resultado = lu_doolittle(A, b)

        if resultado["status"] == "Error":
            st.error(resultado["mensaje"])
        else:
            st.success(resultado["mensaje"])

            # --- Mostrar matrices L y U lado a lado ---
            col_l, col_u = st.columns(2)
            with col_l:
                st.markdown("**Matriz L (triangular inferior):**")
                L_arr = np.array(resultado["L"])
                df_L = pd.DataFrame(
                    L_arr,
                    columns=[f"Col {j+1}" for j in range(n)],
                    index=[f"Fila {i+1}" for i in range(n)]
                )
                st.dataframe(df_L.style.format("{:.6f}"), use_container_width=True)

            with col_u:
                st.markdown("**Matriz U (triangular superior):**")
                U_arr = np.array(resultado["U"])
                df_U = pd.DataFrame(
                    U_arr,
                    columns=[f"Col {j+1}" for j in range(n)],
                    index=[f"Fila {i+1}" for i in range(n)]
                )
                st.dataframe(df_U.style.format("{:.6f}"), use_container_width=True)

            # --- Mostrar solucion ---
            if "solucion" in resultado:
                st.markdown("**Solucion del sistema:**")
                sol_cols = st.columns(n)
                for i, val in enumerate(resultado["solucion"]):
                    sol_cols[i].metric(f"x{i+1}", f"{val:.8f}")

            # --- Verificacion: A = L*U ---
            with st.expander("Verificacion A = L x U"):
                LU_prod = np.array(resultado["L"]) @ np.array(resultado["U"])
                df_verif = pd.DataFrame(
                    LU_prod,
                    columns=[f"Col {j+1}" for j in range(n)],
                    index=[f"Fila {i+1}" for i in range(n)]
                )
                st.dataframe(df_verif.style.format("{:.6f}"), use_container_width=True)
                error_lu = np.max(np.abs(np.array(A) - LU_prod))
                st.metric("Error maximo |A - LU|", f"{error_lu:.2e}")


# ══════════════════════════════════════════════════════════════════
# SECCION 16: VISTA: INTERPOLACION (views/interpolacion.py)
# ══════════════════════════════════════════════════════════════════

EJEMPLOS_INTERPOLACION = {
    "Seleccionar ejemplo...": {"x": [1, 2, 3, 4], "y": [1, 4, 9, 16]},
    "Cuadratica: y = x^2": {"x": [1, 2, 3, 4], "y": [1, 4, 9, 16]},
    "Cubica: y = x^3": {"x": [0, 1, 2, 3], "y": [0, 1, 8, 27]},
    "Seno: y = sin(x)": {"x": [0.0, 0.5, 1.0, 1.5, 2.0], "y": [0.0, 0.479, 0.841, 0.997, 0.909]},
    "Datos experimentales": {"x": [0, 1, 3, 5, 7], "y": [2.0, 3.1, 5.8, 9.2, 14.1]},
}


def vista_interpolacion():
    """Renderiza la vista completa de interpolacion."""

    # ============================================================
    # HEADER: Titulo y boton reiniciar
    # ============================================================
    col_titulo, col_reset = st.columns([5, 1])
    with col_titulo:
        st.title("Interpolacion")
        st.markdown("Construye polinomios que pasan por un conjunto de puntos")
    with col_reset:
        st.markdown("")
        st.markdown("")
        if st.button("Reiniciar", key="reset_interp", help="Limpia todos los campos y resultados"):
            for key in list(st.session_state.keys()):
                if any(s in key for s in ["interp", "xi_", "yi_", "lag", "newt", "spline"]):
                    del st.session_state[key]
            st.rerun()

    # ============================================================
    # SELECTOR DE EJEMPLO
    # ============================================================
    ejemplo_sel = st.selectbox(
        "Ejemplos rapidos",
        options=list(EJEMPLOS_INTERPOLACION.keys()),
        key="ejemplo_interp",
        help="Selecciona datos de ejemplo para cargar automaticamente"
    )
    ej = EJEMPLOS_INTERPOLACION[ejemplo_sel]

    # ============================================================
    # ENTRADA DE PUNTOS
    # ============================================================
    st.markdown("### Ingrese los puntos (x, y)")

    n_puntos = st.number_input(
        "Numero de puntos",
        min_value=2, max_value=20, value=len(ej["x"]),
        key="n_puntos_interp"
    )

    col_x, col_y = st.columns(2)
    xi = []
    yi = []

    for i in range(n_puntos):
        with col_x:
            x_val = st.number_input(
                f"x{i}",
                value=float(ej["x"][i] if i < len(ej["x"]) else i),
                key=f"xi_{i}",
                label_visibility="collapsed" if i > 0 else "visible"
            )
            xi.append(x_val)
        with col_y:
            y_val = st.number_input(
                f"y{i}",
                value=float(ej["y"][i] if i < len(ej["y"]) else i**2),
                key=f"yi_{i}",
                label_visibility="collapsed" if i > 0 else "visible"
            )
            yi.append(y_val)

    # ============================================================
    # TABS: Selector de metodo
    # ============================================================
    tab_lagrange, tab_newton, tab_spline, tab_comparar = st.tabs([
        "Lagrange",
        "Newton",
        "Trazadores Cubicos",
        "Comparar Metodos"
    ])

    # ============================================================
    # TAB 1: LAGRANGE
    # ============================================================
    with tab_lagrange:
        st.latex(latex_metodo_descripcion("Lagrange"))
        st.divider()

        if st.button("CALCULAR LAGRANGE", key="btn_lag", type="primary"):
            valido, msg = validar_puntos_interpolacion(xi, yi)
            if not valido:
                st.error(msg)
                return

            resultado = lagrange(xi, yi)

            if resultado["status"] == "OK":
                st.success(resultado["mensaje"])

                st.markdown("**Polinomio interpolante:**")
                st.code(resultado["polinomio_expandido"], language="text")

                fig = graficar_interpolacion(
                    xi, yi,
                    [resultado["funcion_eval"]],
                    ["Lagrange"],
                    titulo="Interpolacion de Lagrange"
                )
                st.plotly_chart(fig, use_container_width=True)

                with st.expander("Ver polinomios base L_i(x)"):
                    for paso in resultado["pasos"]:
                        st.latex(
                            f"L_{{{paso['i']}}}(x) = {paso['Li']}, \\quad "
                            f"y_{{{paso['i']}}} \\cdot L_{{{paso['i']}}} = {paso['termino']}"
                        )

    # ============================================================
    # TAB 2: NEWTON (DIFERENCIAS DIVIDIDAS)
    # ============================================================
    with tab_newton:
        st.latex(latex_metodo_descripcion("Newton Interpolacion"))
        st.divider()

        if st.button("CALCULAR NEWTON", key="btn_newt_interp", type="primary"):
            valido, msg = validar_puntos_interpolacion(xi, yi)
            if not valido:
                st.error(msg)
                return

            resultado = newton_interpolacion(xi, yi)

            if resultado["status"] == "OK":
                st.success(resultado["mensaje"])

                st.markdown("**Polinomio interpolante:**")
                st.code(resultado["polinomio_expandido"], language="text")

                st.markdown("**Coeficientes (diferencias divididas):**")
                for i, coef in enumerate(resultado["coeficientes"]):
                    st.latex(f"a_{{{i}}} = {coef:.8f}")

                with st.expander("Tabla de diferencias divididas"):
                    tabla = resultado["tabla_diferencias"]
                    n = len(tabla)
                    cols = ["f[]"] + [f"f[{',' .join([''] * (j+1))}]" for j in range(1, n)]
                    df = pd.DataFrame(tabla, columns=cols[:n])
                    st.dataframe(df.style.format("{:.6f}"), use_container_width=True)

                fig = graficar_interpolacion(
                    xi, yi,
                    [resultado["funcion_eval"]],
                    ["Newton"],
                    titulo="Interpolacion de Newton"
                )
                st.plotly_chart(fig, use_container_width=True)

    # ============================================================
    # TAB 3: TRAZADORES CUBICOS NATURALES
    # ============================================================
    with tab_spline:
        st.latex(latex_metodo_descripcion("Trazador Cubico"))
        st.divider()

        if st.button("CALCULAR TRAZADORES CUBICOS", key="btn_spline", type="primary"):
            valido, msg = validar_puntos_interpolacion(xi, yi)
            if not valido:
                st.error(msg)
                return

            orden = np.argsort(xi)
            xi_ord = [xi[i] for i in orden]
            yi_ord = [yi[i] for i in orden]

            resultado = trazador_cubico_natural(xi_ord, yi_ord)

            if resultado["status"] == "OK":
                st.success(resultado["mensaje"])

                st.markdown("**Ecuaciones por tramo:**")
                for trazo in resultado["trazos"]:
                    st.code(trazo["ecuacion"], language="text")

                fig = graficar_interpolacion(
                    xi_ord, yi_ord,
                    [resultado["funcion_eval"]],
                    ["Trazador Cubico"],
                    titulo="Trazadores Cubicos Naturales"
                )
                st.plotly_chart(fig, use_container_width=True)

                with st.expander("Tabla de coeficientes por tramo"):
                    filas = []
                    for t in resultado["trazos"]:
                        filas.append({
                            "Intervalo": f"[{t['intervalo'][0]:.2f}, {t['intervalo'][1]:.2f}]",
                            "a": t["a"], "b": t["b"], "c": t["c"], "d": t["d"]
                        })
                    df = pd.DataFrame(filas)
                    st.dataframe(df, use_container_width=True, hide_index=True)

    # ============================================================
    # TAB 4: COMPARACION DE METODOS
    # ============================================================
    with tab_comparar:
        st.markdown("### Comparacion lado a lado")
        st.markdown("Ejecuta los tres metodos sobre los mismos puntos y compara las curvas resultantes.")

        if st.button("COMPARAR TODOS LOS METODOS", key="btn_comp_interp", type="primary"):
            valido, msg = validar_puntos_interpolacion(xi, yi)
            if not valido:
                st.error(msg)
                return

            funciones = []
            nombres = []

            res_lag = lagrange(xi, yi)
            if res_lag["status"] == "OK":
                funciones.append(res_lag["funcion_eval"])
                nombres.append("Lagrange")

            res_newt = newton_interpolacion(xi, yi)
            if res_newt["status"] == "OK":
                funciones.append(res_newt["funcion_eval"])
                nombres.append("Newton")

            orden = np.argsort(xi)
            xi_ord = [xi[i] for i in orden]
            yi_ord = [yi[i] for i in orden]
            res_spline = trazador_cubico_natural(xi_ord, yi_ord)
            if res_spline["status"] == "OK":
                funciones.append(res_spline["funcion_eval"])
                nombres.append("Trazador Cubico")

            if funciones:
                fig = graficar_interpolacion(
                    xi, yi, funciones, nombres,
                    titulo="Comparacion: Lagrange vs Newton vs Trazadores Cubicos"
                )
                st.plotly_chart(fig, use_container_width=True)

                st.info(
                    "Nota: Lagrange y Newton producen el mismo polinomio "
                    "(pueden verse superpuestos). Los trazadores cubicos "
                    "usan polinomios de grado 3 por tramo, evitando las "
                    "oscilaciones de Runge."
                )


# ══════════════════════════════════════════════════════════════════
# SECCION 17: VISTA: INTEGRACION NUMERICA (views/integracion.py)
# ══════════════════════════════════════════════════════════════════

EJEMPLOS_INTEGRACION = {
    "Seleccionar ejemplo...": {"func": "x^2 + 1", "a": 0.0, "b": 2.0, "n": 10},
    "Polinomio: x^2 + 1": {"func": "x^2 + 1", "a": 0.0, "b": 2.0, "n": 10},
    "Trigonometrica: sin(x)": {"func": "sin(x)", "a": 0.0, "b": 3.14159, "n": 20},
    "Exponencial: e^(-x^2)": {"func": "exp(-x^2)", "a": 0.0, "b": 3.0, "n": 30},
    "Racional: 1/(1 + x^2)": {"func": "1/(1 + x^2)", "a": 0.0, "b": 5.0, "n": 20},
    "Logaritmica: ln(x+1)": {"func": "ln(x+1)", "a": 0.0, "b": 2.0, "n": 10},
}


def vista_integracion():
    """Renderiza la vista completa de integracion numerica."""

    # ============================================================
    # HEADER: Titulo y boton reiniciar
    # ============================================================
    col_titulo, col_reset = st.columns([5, 1])
    with col_titulo:
        st.title("Integracion Numerica")
        st.markdown("Calcula integrales definidas de funciones")
    with col_reset:
        st.markdown("")
        st.markdown("")
        if st.button("Reiniciar", key="reset_int", help="Limpia todos los campos y resultados"):
            for key in list(st.session_state.keys()):
                if any(s in key for s in ["func_int", "n_sub", "a_int", "b_int", "ejemplo_int",
                                          "trap", "s13", "s38", "comp_int"]):
                    del st.session_state[key]
            st.rerun()

    # ============================================================
    # SELECTOR DE EJEMPLO
    # ============================================================
    ejemplo_sel = st.selectbox(
        "Ejemplos rapidos",
        options=list(EJEMPLOS_INTEGRACION.keys()),
        key="ejemplo_int",
        help="Selecciona un problema clasico"
    )
    ej = EJEMPLOS_INTEGRACION[ejemplo_sel]

    # ============================================================
    # ENTRADA COMUN: Funcion y limites
    # ============================================================
    col1, col2 = st.columns([2, 1])
    with col1:
        func_int = st.text_input(
            "Funcion f(x)",
            value=ej["func"],
            key="func_int",
            help="Ejemplo: x^2, sin(x), exp(-x^2), ln(x)"
        )
    with col2:
        n_sub = st.slider(
            "Subintervalos (N)",
            min_value=2, max_value=200, value=ej["n"],
            key="n_sub",
            help="Mas subintervalos = mayor precision"
        )

    col3, col4 = st.columns(2)
    with col3:
        a_int = st.number_input("Limite inferior (a)", value=ej["a"], key="a_int")
    with col4:
        b_int = st.number_input("Limite superior (b)", value=ej["b"], key="b_int")

    # ============================================================
    # TABS: Selector de metodo
    # ============================================================
    tab_trap, tab_s13, tab_s38, tab_comp = st.tabs([
        "Trapecio",
        "Simpson 1/3",
        "Simpson 3/8",
        "Comparar Metodos"
    ])

    # ============================================================
    # TAB 1: REGLA DEL TRAPECIO
    # ============================================================
    with tab_trap:
        st.latex(latex_metodo_descripcion("Trapecio"))
        st.divider()

        if st.button("CALCULAR CON TRAPECIO", key="btn_trap", type="primary"):
            _ejecutar_integracion("Trapecio", func_int, a_int, b_int, n_sub, trapecio)

    # ============================================================
    # TAB 2: SIMPSON 1/3
    # ============================================================
    with tab_s13:
        st.latex(latex_metodo_descripcion("Simpson 1/3"))
        st.divider()

        if st.button("CALCULAR CON SIMPSON 1/3", key="btn_s13", type="primary"):
            _ejecutar_integracion("Simpson 1/3", func_int, a_int, b_int, n_sub, simpson_13)

    # ============================================================
    # TAB 3: SIMPSON 3/8
    # ============================================================
    with tab_s38:
        st.latex(latex_metodo_descripcion("Simpson 3/8"))
        st.divider()

        if st.button("CALCULAR CON SIMPSON 3/8", key="btn_s38", type="primary"):
            _ejecutar_integracion("Simpson 3/8", func_int, a_int, b_int, n_sub, simpson_38)

    # ============================================================
    # TAB 4: COMPARACION DE METODOS
    # ============================================================
    with tab_comp:
        st.markdown("### Comparacion de los 3 metodos")
        st.markdown("Ejecuta Trapecio, Simpson 1/3 y Simpson 3/8 con los mismos parametros.")

        if st.button("COMPARAR METODOS DE INTEGRACION", key="btn_comp_int", type="primary"):
            try:
                expr = parsear_funcion(func_int)
                func_str = str(expr)
                f_eval = crear_funcion_numerica(expr)

                metodos = [
                    ("Trapecio", trapecio),
                    ("Simpson 1/3", simpson_13),
                    ("Simpson 3/8", simpson_38)
                ]

                resultados = []
                for nombre, metodo in metodos:
                    res = metodo(func_str, a_int, b_int, n_sub)
                    res["nombre"] = nombre
                    resultados.append(res)

                # --- Tabla comparativa ---
                filas = []
                for res in resultados:
                    if res["status"] == "OK":
                        fila = {
                            "Metodo": res["nombre"],
                            "Integral aprox.": res["area"],
                            "h": res["h"],
                            "N usado": res["n"]
                        }
                        if res.get("integral_exacta") is not None:
                            fila["Exacta"] = res["integral_exacta"]
                            fila["Error"] = res["error_absoluto"]
                        filas.append(fila)

                if filas:
                    st.dataframe(
                        pd.DataFrame(filas),
                        use_container_width=True,
                        hide_index=True
                    )

                # --- Grafica del primer resultado ---
                if resultados and resultados[0]["status"] == "OK":
                    fig = graficar_integracion(
                        f_eval,
                        resultados[0]["x_puntos"],
                        resultados[0]["y_puntos"],
                        metodo="Comparacion",
                        a=a_int, b=b_int
                    )
                    st.plotly_chart(fig, use_container_width=True)

            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Error: {e}")


def _ejecutar_integracion(nombre, func_str_raw, a, b, n, metodo_func):
    """
    Funcion auxiliar que ejecuta un metodo de integracion
    y muestra los resultados. Se reutiliza para los 3 metodos.
    """
    try:
        expr = parsear_funcion(func_str_raw)
        func_str = str(expr)
        f_eval = crear_funcion_numerica(expr)

        resultado = metodo_func(func_str, a, b, n)

        if resultado["status"] == "Error":
            st.error(resultado["mensaje"])
            return

        st.success(resultado["mensaje"])

        # --- Metricas ---
        cols = st.columns(4)
        cols[0].metric("Integral aprox.", f"{resultado['area']:.10f}")
        cols[1].metric("h", f"{resultado['h']:.6f}")
        cols[2].metric("N subintervalos", resultado["n"])
        if resultado.get("integral_exacta") is not None:
            cols[3].metric("Error absoluto", f"{resultado['error_absoluto']:.2e}")

        # --- Comparacion con valor exacto ---
        if resultado.get("integral_exacta") is not None:
            st.info(f"Valor exacto (SymPy): {resultado['integral_exacta']:.10f}")

        # --- Grafica ---
        fig = graficar_integracion(
            f_eval, resultado["x_puntos"], resultado["y_puntos"],
            metodo=nombre, a=a, b=b
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- Tabla de puntos ---
        with st.expander("Ver puntos evaluados"):
            df = pd.DataFrame({
                "x": resultado["x_puntos"],
                "f(x)": resultado["y_puntos"]
            })
            st.dataframe(df, use_container_width=True, hide_index=True)

    except ValueError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"Error: {e}")


# ══════════════════════════════════════════════════════════════════
# SECCION 18: VISTA: EDOs (views/edo.py)
# ══════════════════════════════════════════════════════════════════

EJEMPLOS_EDO = {
    "Seleccionar ejemplo...": {"func": "-2*y + t", "t0": 0.0, "tf": 5.0, "y0": 1.0, "N": 50, "sol": ""},
    "Decaimiento: dy/dt = -2y + t": {"func": "-2*y + t", "t0": 0.0, "tf": 5.0, "y0": 1.0, "N": 50, "sol": "exp(-2*t) + t/2 - 1/4"},
    "Crecimiento: dy/dt = y": {"func": "y", "t0": 0.0, "tf": 2.0, "y0": 1.0, "N": 20, "sol": "exp(t)"},
    "Oscilacion: dy/dt = -sin(t)": {"func": "-sin(t)", "t0": 0.0, "tf": 10.0, "y0": 1.0, "N": 100, "sol": "cos(t)"},
    "No lineal: dy/dt = t*y": {"func": "t*y", "t0": 0.0, "tf": 2.0, "y0": 1.0, "N": 50, "sol": ""},
}

EJEMPLOS_VERLET = {
    "Seleccionar ejemplo...": {"func": "-x", "t0": 0.0, "tf": 10.0, "x0": 1.0, "v0": 0.0, "N": 100},
    "Oscilador armonico: x'' = -x": {"func": "-x", "t0": 0.0, "tf": 10.0, "x0": 1.0, "v0": 0.0, "N": 100},
    "Caida libre: x'' = -9.8": {"func": "-9.8", "t0": 0.0, "tf": 3.0, "x0": 100.0, "v0": 0.0, "N": 50},
    "Pendulo simple: x'' = -sin(x)": {"func": "-sin(x)", "t0": 0.0, "tf": 15.0, "x0": 0.5, "v0": 0.0, "N": 200},
}


def vista_edo():
    """Renderiza la vista completa de EDOs."""

    # ============================================================
    # HEADER: Titulo y boton reiniciar
    # ============================================================
    col_titulo, col_reset = st.columns([5, 1])
    with col_titulo:
        st.title("Ecuaciones Diferenciales Ordinarias")
        st.markdown("Resuelve EDOs de la forma **dy/dt = f(t, y)**")
    with col_reset:
        st.markdown("")
        st.markdown("")
        if st.button("Reiniciar", key="reset_edo", help="Limpia todos los campos y resultados"):
            for key in list(st.session_state.keys()):
                if any(s in key for s in ["euler", "rk2", "rk4", "verlet", "orden", "comp",
                                          "func_", "ejemplo_edo"]):
                    del st.session_state[key]
            st.rerun()

    # ============================================================
    # TABS: Selector de metodo
    # ============================================================
    tab_euler, tab_rk2, tab_rk4, tab_verlet, tab_orden, tab_comp = st.tabs([
        "Euler",
        "RK2",
        "RK4",
        "Verlet",
        "Analisis de Orden",
        "Comparar"
    ])

    # ============================================================
    # TAB 1: METODO DE EULER
    # ============================================================
    with tab_euler:
        st.latex(latex_metodo_descripcion("Euler"))
        st.divider()
        _render_edo_metodo("Euler", euler)

    # ============================================================
    # TAB 2: RUNGE-KUTTA 2DO ORDEN
    # ============================================================
    with tab_rk2:
        st.latex(latex_metodo_descripcion("RK2"))
        st.divider()
        _render_edo_metodo("RK2", rk2)

    # ============================================================
    # TAB 3: RUNGE-KUTTA 4TO ORDEN
    # ============================================================
    with tab_rk4:
        st.latex(latex_metodo_descripcion("RK4"))
        st.divider()
        _render_edo_metodo("RK4", rk4)

    # ============================================================
    # TAB 4: VERLET
    # ============================================================
    with tab_verlet:
        st.latex(latex_metodo_descripcion("Verlet"))
        st.divider()
        _render_verlet()

    # ============================================================
    # TAB 5: ANALISIS DE ORDEN DE CONVERGENCIA
    # ============================================================
    with tab_orden:
        st.markdown("### Analisis de Orden de Convergencia")
        st.markdown(
            "Ejecuta el metodo con diferentes tamanos de paso (h, h/2, h/4, ...) "
            "y grafica el error vs h en escala log-log. La pendiente indica el orden."
        )
        _render_analisis_orden()

    # ============================================================
    # TAB 6: COMPARACION DE METODOS
    # ============================================================
    with tab_comp:
        st.markdown("### Comparacion: Euler vs RK2 vs RK4")
        _render_comparacion()


def _render_edo_metodo(nombre, metodo_func):
    """
    Renderiza la interfaz para un metodo de EDO (Euler, RK2 o RK4).
    Se reutiliza para los tres metodos ya que la UI es identica.
    """
    key = nombre.lower()

    # --- Selector de ejemplo pre-cargado ---
    ejemplo_sel = st.selectbox(
        "Ejemplos rapidos",
        options=list(EJEMPLOS_EDO.keys()),
        key=f"ejemplo_edo_{key}",
        help="Selecciona un problema clasico"
    )
    ej = EJEMPLOS_EDO[ejemplo_sel]

    col1, col2 = st.columns(2)
    with col1:
        func_edo = st.text_input(
            "f(t, y) = dy/dt",
            value=ej["func"],
            key=f"func_{key}",
            help="Use 't' y 'y' como variables. Ejemplo: -2*y + t, t*y, sin(t)"
        )
    with col2:
        N_pasos = st.number_input(
            "Numero de pasos (N)",
            min_value=2, max_value=100000, value=ej["N"],
            key=f"N_{key}"
        )

    col3, col4, col5 = st.columns(3)
    with col3:
        t0 = st.number_input("t0 (tiempo inicial)", value=ej["t0"], key=f"t0_{key}")
    with col4:
        tf = st.number_input("t_f (tiempo final)", value=ej["tf"], key=f"tf_{key}")
    with col5:
        y0 = st.number_input("y0 (condicion inicial)", value=ej["y0"], key=f"y0_{key}")

    # --- Solucion exacta (opcional) ---
    sol_exacta = st.text_input(
        "Solucion exacta y(t) (opcional, para calcular error)",
        value=ej["sol"],
        key=f"sol_{key}",
        help="Si conoce la solucion exacta, ingresela para ver el error. Ej: exp(-2*t) + t/2 - 1/4"
    )

    if st.button(f"RESOLVER CON {nombre.upper()}", key=f"btn_{key}", type="primary"):
        try:
            resultado = metodo_func(str(parsear_funcion(func_edo)), t0, tf, y0, int(N_pasos))

            if resultado["status"] == "Error":
                st.error(resultado["mensaje"])
                return

            st.success(resultado["mensaje"])

            # --- Metricas ---
            m1, m2, m3 = st.columns(3)
            m1.metric(f"y({tf})", f"{resultado['y'][-1]:.10f}")
            m2.metric("Pasos", N_pasos)
            m3.metric("h", f"{resultado['h']:.6f}")

            # --- Grafica ---
            fig = graficar_edo([resultado], titulo=f"Solucion EDO — {nombre}")

            # Agregar solucion exacta si se proporciono
            if sol_exacta.strip():
                try:
                    t_sym = sp.Symbol('t')
                    y_exacta = sp.lambdify(t_sym, sp.sympify(sol_exacta), 'numpy')
                    t_arr = np.array(resultado["t"])
                    y_ex = y_exacta(t_arr)
                    fig.add_trace(go.Scatter(
                        x=t_arr, y=y_ex,
                        mode='lines',
                        name='Solucion Exacta',
                        line=dict(color='#ffea00', width=2, dash='dash')
                    ))
                except Exception:
                    st.warning("No se pudo evaluar la solucion exacta.")

            st.plotly_chart(fig, use_container_width=True)

            # --- Tabla de iteraciones ---
            with st.expander("Ver tabla de iteraciones", expanded=False):
                df = pd.DataFrame(resultado["historial"])
                st.dataframe(df, use_container_width=True, hide_index=True)

            # --- Pasos LaTeX (primeras 5) ---
            if nombre == "Euler":
                with st.expander("Ver pasos matematicos (LaTeX)"):
                    for h in resultado["historial"][:5]:
                        st.latex(latex_euler_paso(
                            h["paso"], h["t_n"], h["y_n"],
                            h["f(t_n, y_n)"], h["y_{n+1}"], resultado["h"]
                        ))
            elif nombre == "RK4":
                with st.expander("Ver pasos matematicos (LaTeX)"):
                    for h in resultado["historial"][:5]:
                        st.latex(latex_rk4_paso(
                            h["paso"], h["t_n"], h["y_n"],
                            h["k1"], h["k2"], h["k3"], h["k4"],
                            h["y_{n+1}"]
                        ))

        except ValueError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"Error: {e}")


def _render_verlet():
    """Renderiza la interfaz para el metodo de Verlet."""

    st.info("Verlet resuelve ecuaciones de 2do orden: x'' = a(t, x)")

    # --- Selector de ejemplo ---
    ejemplo_ver = st.selectbox(
        "Ejemplos rapidos",
        options=list(EJEMPLOS_VERLET.keys()),
        key="ejemplo_verlet",
        help="Selecciona un problema clasico"
    )
    ej = EJEMPLOS_VERLET[ejemplo_ver]

    col1, col2 = st.columns(2)
    with col1:
        a_func = st.text_input(
            "a(t, x) = x'' (aceleracion)",
            value=ej["func"],
            key="func_verlet",
            help="Ejemplo: -x (oscilador armonico), -9.8 (caida libre), -sin(x) (pendulo)"
        )
    with col2:
        N_ver = st.number_input("Pasos (N)", min_value=2, max_value=100000, value=ej["N"], key="N_ver")

    col3, col4, col5, col6 = st.columns(4)
    with col3:
        t0_v = st.number_input("t0", value=ej["t0"], key="t0_ver")
    with col4:
        tf_v = st.number_input("t_f", value=ej["tf"], key="tf_ver")
    with col5:
        x0_v = st.number_input("x0 (posicion inicial)", value=ej["x0"], key="x0_ver")
    with col6:
        v0_v = st.number_input("v0 (velocidad inicial)", value=ej["v0"], key="v0_ver")

    if st.button("RESOLVER CON VERLET", key="btn_verlet", type="primary"):
        try:
            resultado = verlet(str(parsear_funcion(a_func)), t0_v, tf_v, x0_v, v0_v, int(N_ver))

            if resultado["status"] == "Error":
                st.error(resultado["mensaje"])
                return

            st.success(resultado["mensaje"])

            m1, m2 = st.columns(2)
            m1.metric(f"x({tf_v})", f"{resultado['x'][-1]:.10f}")
            m2.metric("h", f"{resultado['h']:.6f}")

            res_plot = {"t": resultado["t"], "y": resultado["x"], "metodo": "Verlet"}
            fig = graficar_edo([res_plot], titulo="Solucion x(t) — Verlet")
            st.plotly_chart(fig, use_container_width=True)

            with st.expander("Ver tabla de iteraciones"):
                df = pd.DataFrame(resultado["historial"])
                st.dataframe(df, use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Error: {e}")


def _render_analisis_orden():
    """Renderiza el analisis de orden de convergencia."""

    col1, col2 = st.columns(2)
    with col1:
        func_orden = st.text_input(
            "f(t, y)",
            value="-2*y + t",
            key="func_orden"
        )
    with col2:
        metodo_sel = st.selectbox(
            "Metodo a analizar",
            ["Euler", "RK2", "RK4"],
            key="metodo_orden"
        )

    col3, col4, col5 = st.columns(3)
    with col3:
        t0_o = st.number_input("t0", value=0.0, key="t0_orden")
    with col4:
        tf_o = st.number_input("t_f", value=2.0, key="tf_orden")
    with col5:
        y0_o = st.number_input("y0", value=1.0, key="y0_orden")

    sol_exacta_o = st.text_input(
        "Solucion exacta y(t) (para calcular error exacto)",
        value="",
        key="sol_orden",
        help="Ej: exp(-2*t) + t/2 - 1/4"
    )

    if st.button("EJECUTAR ANALISIS DE ORDEN", key="btn_orden", type="primary"):
        try:
            metodos = {"Euler": euler, "RK2": rk2, "RK4": rk4}
            metodo_func = metodos[metodo_sel]
            func_str = str(parsear_funcion(func_orden))

            resultado = analisis_orden(
                metodo_func, func_str, t0_o, tf_o, y0_o,
                solucion_exacta_str=sol_exacta_o if sol_exacta_o.strip() else None
            )

            if resultado["status"] == "OK":
                st.success(resultado["mensaje"])

                ordenes_esperados = {"Euler": 1, "RK2": 2, "RK4": 4}
                st.metric("Orden estimado", f"{resultado['orden_promedio']:.2f}")
                st.info(f"Orden teorico de {metodo_sel}: {ordenes_esperados[metodo_sel]}")

                fig = graficar_analisis_orden(
                    resultado["h_values"],
                    resultado["errores"],
                    resultado["orden_promedio"],
                    titulo=f"Orden de Convergencia — {metodo_sel}"
                )
                st.plotly_chart(fig, use_container_width=True)

                with st.expander("Datos del analisis"):
                    filas = []
                    for i, (h, e) in enumerate(zip(resultado["h_values"], resultado["errores"])):
                        fila = {"h": h, "Error": e}
                        if i < len(resultado["ordenes_estimados"]):
                            fila["Orden estimado"] = resultado["ordenes_estimados"][i]
                        filas.append(fila)
                    df = pd.DataFrame(filas)
                    st.dataframe(df, use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Error: {e}")


def _render_comparacion():
    """Renderiza la comparacion de metodos EDO."""

    col1, col2 = st.columns(2)
    with col1:
        func_comp = st.text_input("f(t, y)", value="-2*y + t", key="func_comp")
    with col2:
        N_comp = st.number_input("Pasos (N)", min_value=2, value=20, key="N_comp")

    col3, col4, col5 = st.columns(3)
    with col3:
        t0_c = st.number_input("t0", value=0.0, key="t0_comp")
    with col4:
        tf_c = st.number_input("t_f", value=5.0, key="tf_comp")
    with col5:
        y0_c = st.number_input("y0", value=1.0, key="y0_comp")

    if st.button("COMPARAR EULER VS RK2 VS RK4", key="btn_comp_edo", type="primary"):
        try:
            func_str = str(parsear_funcion(func_comp))
            N = int(N_comp)

            res_euler = euler(func_str, t0_c, tf_c, y0_c, N)
            res_rk2 = rk2(func_str, t0_c, tf_c, y0_c, N)
            res_rk4 = rk4(func_str, t0_c, tf_c, y0_c, N)

            resultados = []
            for res in [res_euler, res_rk2, res_rk4]:
                if res["status"] != "Error":
                    resultados.append(res)

            if resultados:
                fig = graficar_edo(resultados, titulo="Comparacion: Euler vs RK2 vs RK4")
                st.plotly_chart(fig, use_container_width=True)

                filas = []
                for res in resultados:
                    filas.append({
                        "Metodo": res["metodo"],
                        f"y({tf_c})": res["y"][-1],
                        "Orden": res["orden"],
                        "h": res["h"]
                    })
                st.dataframe(
                    pd.DataFrame(filas),
                    use_container_width=True, hide_index=True
                )

                st.info(
                    "RK4 es significativamente mas preciso que Euler con el mismo N. "
                    "Observe como las curvas divergen al aumentar t."
                )

        except Exception as e:
            st.error(f"Error: {e}")


# ══════════════════════════════════════════════════════════════════
# SECCION 19: PUNTO DE ENTRADA PRINCIPAL
# ══════════════════════════════════════════════════════════════════

# ============================================================
# CONFIGURACION DE LA PAGINA
# ============================================================
st.set_page_config(
    page_title="Calculadora de Metodos Numericos | UNITEC",
    page_icon="assets/unitec_color.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CARGA DEL CSS (desde la variable CSS_GLOBAL)
# ============================================================
st.markdown(f"<style>{CSS_GLOBAL}</style>", unsafe_allow_html=True)

# ============================================================
# OCULTAR ELEMENTOS DEFAULT DE STREAMLIT
# ============================================================
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR: PANEL DE NAVEGACION LATERAL
# ============================================================
with st.sidebar:
    # --- Logo de UNITEC (blanco para fondo oscuro) ---
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "unitec_blanco.png")
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)

    st.markdown("")  # Espaciador

    # --- Titulo de la aplicacion ---
    st.markdown("""
    <div style="text-align: center; padding: 0 0 15px 0;">
        <h2 style="
            font-size: 1.3rem;
            background: linear-gradient(135deg, #00e5ff, #b388ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            line-height: 1.3;
        ">Calculadora de<br>Metodos Numericos</h2>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --- Selector de modulo (navegacion principal) ---
    modulo = st.radio(
        "Navegacion",
        options=[
            "Inicio",
            "Ecuaciones No Lineales",
            "Sistemas de Ecuaciones Lineales",
            "Interpolacion",
            "Integracion Numerica",
            "Ecuaciones Diferenciales (EDO)"
        ],
        index=0,
        label_visibility="collapsed",
        key="nav_principal"
    )

# ============================================================
# AREA PRINCIPAL: CARGA DEL MODULO SELECCIONADO
# ============================================================
if modulo == "Inicio":
    vista_inicio()
elif modulo == "Ecuaciones No Lineales":
    vista_no_lineales()
elif modulo == "Sistemas de Ecuaciones Lineales":
    vista_sistemas_lineales()
elif modulo == "Interpolacion":
    vista_interpolacion()
elif modulo == "Integracion Numerica":
    vista_integracion()
elif modulo == "Ecuaciones Diferenciales (EDO)":
    vista_edo()
