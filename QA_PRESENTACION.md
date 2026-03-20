# GUIA Q&A - MECATON 2026
# Calculadora de Metodos Numericos
---

## SECCION 1: LAS LIBRERIAS

### P: "Que librerias usaste y por que?"

**R:** Usamos 7 librerias principales. Cada una tiene un proposito especifico:

| Libreria | Para que la usamos | Por que esa y no otra |
|----------|-------------------|----------------------|
| **Streamlit** | Crear la interfaz web (botones, inputs, sidebar, tabs) | Es la mas rapida para hacer apps de datos en Python. No necesitas HTML/CSS/JS manual — todo se hace con Python |
| **SymPy** | Matematica simbolica: parsear funciones del usuario, derivar automaticamente, simplificar expresiones | Es el estandar en Python para algebra simbolica. Permite que el usuario escriba `x^2 + 3x` y nosotros lo convertimos a una funcion evaluable |
| **NumPy** | Calculos numericos: arrays, operaciones vectorizadas, evaluacion rapida de funciones | Es 100x mas rapido que hacer loops en Python puro. Todas las iteraciones de los metodos usan NumPy |
| **Plotly** | Graficas interactivas (zoom, pan, hover con valores) | A diferencia de Matplotlib, las graficas de Plotly son interactivas en el navegador sin codigo extra |
| **Pandas** | Mostrar tablas de iteraciones (DataFrames) | Streamlit muestra DataFrames de Pandas nativamente con scroll, sort, etc. |
| **fpdf2** | Generar reportes PDF descargables con los resultados | Es ligera (no necesita LaTeX instalado) y permite crear PDFs programaticamente |
| **SciPy** | Funciones auxiliares para interpolacion (trazadores cubicos) | Tiene implementaciones optimizadas de splines cubicos que nosotros usamos como referencia |

### P: "Como instalaste las librerias?"

**R:** Todas estan en el archivo `requirements.txt`. Con un solo comando:
```
pip install -r requirements.txt
```
Streamlit Cloud las instala automaticamente al hacer deploy.

### P: "Que version de Python usaron?"

**R:** Python 3.14.2 (la version que esta instalada en la computadora). Pero funciona con cualquier Python 3.9+.

---

## SECCION 2: ARQUITECTURA DEL CODIGO

### P: "Como esta organizado el codigo?"

**R:** Todo esta en UN SOLO archivo `app.py` (~4,400 lineas) dividido en 19 secciones claramente marcadas:

```
SECCION 1:  Imports globales (todas las librerias)
SECCION 2:  CSS del tema visual (glassmorphism oscuro)
SECCION 3:  Parser de expresiones (convierte texto del usuario a matematica)
SECCION 4:  Validacion de entradas (verifica que los datos sean correctos)
SECCION 5:  Generador de reportes PDF
SECCION 6:  Generador de pasos en LaTeX (formulas bonitas)
SECCION 7:  Graficas con Plotly (6 tipos de graficas)
SECCION 8:  Metodos - Ecuaciones no lineales (Biseccion, Newton, Punto Fijo)
SECCION 9:  Metodos - Sistemas lineales (Jacobi, Gauss-Seidel, LU)
SECCION 10: Metodos - Interpolacion (Lagrange, Newton, Splines)
SECCION 11: Metodos - Integracion (Trapecio, Simpson 1/3, Simpson 3/8)
SECCION 12: Metodos - EDOs (Euler, RK2, RK4, Verlet)
SECCION 13-18: Vistas de la interfaz (una por modulo)
SECCION 19: Punto de entrada principal (sidebar, navegacion)
```

### P: "Por que un solo archivo y no muchos?"

**R:** Para facilitar la auditoria. Un solo archivo en VS Code permite:
- Buscar cualquier metodo con Ctrl+F
- Ver todo el codigo de un vistazo
- Compartir con el equipo copiando UN archivo
- Verificar que no hay codigo oculto en otros archivos

### P: "Cuantas lineas de codigo son?"

**R:** Aproximadamente 4,400 lineas, de las cuales:
- ~350 lineas son CSS (tema visual)
- ~1,500 lineas son los metodos numericos puros (la matematica)
- ~1,800 lineas son las vistas (interfaz de usuario)
- ~400 lineas son utilidades (parser, validacion, PDF)
- ~350 lineas son graficas

---

## SECCION 3: LOS METODOS NUMERICOS

### P: "Que metodos implementaron?"

**R:** 15+ metodos en 5 modulos:

**Modulo 1 - Ecuaciones No Lineales** (encontrar raices de f(x) = 0):
- **Biseccion**: Divide el intervalo a la mitad repetidamente
- **Newton-Raphson**: Usa la tangente (derivada) para converger rapido
- **Punto Fijo**: Transforma f(x)=0 en x=g(x) e itera

**Modulo 2 - Sistemas Lineales** (resolver Ax = b):
- **Jacobi**: Metodo iterativo, calcula cada variable independientemente
- **Gauss-Seidel**: Como Jacobi pero usa valores actualizados inmediatamente
- **LU (Doolittle)**: Descompone A en L*U para resolver directo

**Modulo 3 - Interpolacion** (pasar curva por puntos):
- **Lagrange**: Polinomio unico que pasa por todos los puntos
- **Newton (diferencias divididas)**: Construye el polinomio incrementalmente
- **Trazadores Cubicos**: Splines suaves entre cada par de puntos

**Modulo 4 - Integracion** (calcular areas bajo curvas):
- **Trapecio**: Aproxima con trapecios
- **Simpson 1/3**: Usa parabolas (mas preciso)
- **Simpson 3/8**: Usa cubicas (aun mas preciso)

**Modulo 5 - EDOs** (ecuaciones diferenciales ordinarias):
- **Euler**: El mas simple, paso a paso con la pendiente
- **RK2 (Runge-Kutta 2)**: Usa 2 evaluaciones por paso
- **RK4 (Runge-Kutta 4)**: Usa 4 evaluaciones, muy preciso
- **Verlet**: Especial para problemas de fisica (conserva energia)
- **Analisis de Orden**: Compara precision vs tamanio de paso

### P: "Explicame el metodo de Biseccion"

**R:** Es como buscar una palabra en el diccionario:
1. Tienes un intervalo [a, b] donde sabes que hay una raiz (porque f(a) y f(b) tienen signos opuestos)
2. Calculas el punto medio c = (a+b)/2
3. Evaluas f(c)
4. Si f(a)*f(c) < 0, la raiz esta entre a y c → nuevo intervalo [a, c]
5. Si f(a)*f(c) > 0, la raiz esta entre c y b → nuevo intervalo [c, b]
6. Repites hasta que el intervalo sea menor que la tolerancia

**Ventaja:** SIEMPRE converge (si hay cambio de signo)
**Desventaja:** Es lento (convergencia lineal)

### P: "Explicame Newton-Raphson"

**R:** Usa la recta tangente para "apuntar" hacia la raiz:
1. Empiezas con un valor inicial x0
2. Trazas la tangente de f(x) en x0
3. Donde esa tangente cruza el eje x, ese es x1
4. Formula: x_{n+1} = x_n - f(x_n) / f'(x_n)
5. Repites hasta convergencia

**Ventaja:** Convergencia cuadratica (MUCHO mas rapido que Biseccion)
**Desventaja:** Puede diverger si x0 esta lejos o si f'(x) = 0

### P: "Explicame Simpson 1/3"

**R:** En vez de aproximar con rectangulos o trapecios, usa PARABOLAS:
1. Divide [a,b] en N subintervalos (N debe ser par)
2. En cada par de subintervalos, ajusta una parabola
3. Calcula el area bajo cada parabola
4. Formula: (h/3)[f(x0) + 4f(x1) + 2f(x2) + 4f(x3) + ... + f(xn)]

**Por que es mejor:** Una parabola se ajusta mejor a curvas que una linea recta

### P: "Que es RK4 y por que es tan usado?"

**R:** Runge-Kutta de orden 4. Para resolver y' = f(t,y):
1. Calcula 4 "pendientes" en cada paso:
   - k1 = f(t, y) — pendiente al inicio
   - k2 = f(t+h/2, y+h*k1/2) — pendiente a la mitad (usando k1)
   - k3 = f(t+h/2, y+h*k2/2) — pendiente a la mitad (usando k2)
   - k4 = f(t+h, y+h*k3) — pendiente al final
2. Promedio ponderado: y_{n+1} = y_n + (h/6)(k1 + 2k2 + 2k3 + k4)

**Es tan usado porque:** Con solo 4 evaluaciones por paso logra precision de orden 4 (error proporcional a h^4). Es el "sweet spot" entre precision y costo computacional.

---

## SECCION 4: EL PARSER DE FUNCIONES

### P: "Como hace el usuario para ingresar una funcion?"

**R:** El usuario escribe en texto normal, como en una calculadora:
```
x^2 + 3x - 5
sen(x) + cos(2x)
e^x - ln(x)
sqrt(x+1)
```

Nuestro parser convierte automaticamente:
- `^` → `**` (potencia en Python)
- `sen` → `sin` (nombre en espanol a ingles)
- `3x` → `3*x` (multiplicacion implicita)
- `e^x` → `exp(x)`
- `ln` → `log`

Luego SymPy lo convierte a una expresion matematica evaluable.

### P: "Que pasa si el usuario escribe algo mal?"

**R:** Tenemos 8 funciones de validacion que verifican:
- Que la funcion sea valida matematicamente
- Que los intervalos sean correctos (a < b)
- Que la tolerancia sea positiva
- Que haya cambio de signo (para Biseccion)
- Que la matriz sea cuadrada (para sistemas)
- Que los puntos no se repitan (para interpolacion)
- Si algo falla, se muestra un mensaje de error claro en rojo

---

## SECCION 5: LA INTERFAZ VISUAL

### P: "Que es glassmorphism?"

**R:** Es un estilo de diseno moderno que simula vidrio esmerilado:
- Fondos semitransparentes con `rgba(255, 255, 255, 0.03)`
- Efecto de desenfoque con `backdrop-filter: blur(12px)`
- Bordes suaves con `border: 1px solid rgba(255,255,255,0.08)`
- Sombras con glow neon: `box-shadow: 0 0 20px rgba(0,229,255,0.1)`

Lo combinamos con un tema OSCURO para que se vea profesional.

### P: "Por que tema oscuro?"

**R:** Tres razones:
1. Se ve mas profesional y moderno para una presentacion
2. Reduce fatiga visual en presentaciones con proyector
3. Los colores neon (cyan, magenta) resaltan mas sobre fondo oscuro

### P: "Como forzaron el tema oscuro?"

**R:** En el archivo `.streamlit/config.toml` (configuracion de Streamlit):
```toml
[theme]
base = "dark"
```
Ademas, el CSS aplica colores oscuros directamente con `!important` para garantizar que no se filtre el tema claro.

### P: "Que tecnologias de frontend usaron?"

**R:** Streamlit genera el HTML/CSS/JS automaticamente. Nosotros solo:
- Escribimos CSS personalizado (350 lineas) para el tema glassmorphism
- Usamos Plotly para graficas interactivas (se renderizan con WebGL)
- Usamos KaTeX (integrado en Streamlit) para renderizar formulas LaTeX
- Un pequenio JavaScript para el boton flotante del sidebar

---

## SECCION 6: LAS GRAFICAS

### P: "Como funcionan las graficas interactivas?"

**R:** Usamos Plotly, que genera graficas con JavaScript en el navegador:
- **Zoom**: Scroll del mouse o seleccionar area
- **Pan**: Arrastrar la grafica
- **Hover**: Pasar el mouse muestra los valores exactos
- **Export**: Boton de camara para guardar como PNG

### P: "Por que las graficas no se cortan al hacer pan?"

**R:** Pre-calculamos los datos en un rango 10 veces mas amplio que lo visible:
- Si el usuario ve de x=-2 a x=5 (rango 7)
- Nosotros calculamos de x=-37 a x=40 (rango 77)
- Con 2000 puntos (suficiente resolucion)
- Plotly guarda todo en el navegador del cliente
- Al hacer pan, solo mueve la "ventana" — no hay llamada al servidor
- Por eso se siente infinito y fluido

### P: "Que es uirevision?"

**R:** Es un parametro de Plotly que le dice "no re-renderices desde cero cuando Streamlit actualiza la pagina". Preserva el zoom y pan actual del usuario.

---

## SECCION 7: EL DEPLOY Y EL QR

### P: "Como hicieron para que funcione en internet?"

**R:** Usamos **Streamlit Community Cloud** (gratis):
1. Subimos el codigo a un repositorio en **GitHub**
2. Conectamos ese repositorio a **Streamlit Cloud**
3. Streamlit automaticamente:
   - Descarga el codigo
   - Instala las librerias del `requirements.txt`
   - Ejecuta `streamlit run app.py`
   - Genera una URL publica (ej: `https://mecaton-2026.streamlit.app`)

### P: "Como funciona el QR?"

**R:** El QR es simplemente la URL publica codificada en formato QR:
1. Streamlit Cloud nos da una URL (ej: `https://xxxx.streamlit.app`)
2. Usamos un generador de QR (como qr-code-generator.com)
3. Se genera una imagen PNG con el QR
4. Cualquier persona que escanee el QR con su celular abre la URL
5. La app corre en el navegador del celular (es responsive)

### P: "Si cambio el codigo, se actualiza?"

**R:** Si. El flujo es:
1. Editas `app.py` en tu computadora
2. Haces `git add . && git commit -m "cambio" && git push`
3. Streamlit Cloud detecta el cambio en ~30 segundos
4. Redeploy automatico
5. La URL y el QR siguen siendo los mismos

### P: "Cuantas personas pueden usar la app al mismo tiempo?"

**R:** Streamlit Cloud permite multiples usuarios simultaneos. Cada usuario tiene su propia "sesion" — los datos de uno no afectan al otro.

### P: "Necesitan servidor propio?"

**R:** No. Streamlit Cloud provee el servidor gratis. Solo necesitamos:
- Una cuenta de GitHub (gratis)
- Una cuenta de Streamlit Cloud (gratis, se conecta con GitHub)

---

## SECCION 8: LOS REPORTES PDF

### P: "Como generan los PDFs?"

**R:** Usamos la libreria `fpdf2`:
1. Se crea un objeto `ReportePDF` (clase propia)
2. Se agrega titulo, fecha, datos del metodo
3. Se agrega la tabla de iteraciones
4. Se agrega el resultado final
5. Se genera el PDF en memoria (no se guarda en disco)
6. Streamlit lo ofrece como descarga con `st.download_button`

### P: "Que contiene el PDF?"

**R:**
- Titulo del metodo usado
- Fecha y hora del calculo
- Parametros de entrada (funcion, intervalo, tolerancia, etc.)
- Tabla completa de iteraciones
- Resultado final (raiz, error, numero de iteraciones)
- Es un reporte profesional listo para entregar

---

## SECCION 9: CONCEPTOS TECNICOS CLAVE

### P: "Que es SymPy?"

**R:** Es una libreria de Python para matematica simbolica. A diferencia de NumPy que trabaja con numeros, SymPy trabaja con simbolos:
- Puede derivar: `diff(x**2, x)` → `2*x`
- Puede integrar: `integrate(x**2, x)` → `x**3/3`
- Puede simplificar: `simplify((x**2-1)/(x-1))` → `x+1`
- Puede resolver: `solve(x**2-4, x)` → `[-2, 2]`

Nosotros lo usamos para:
- Parsear funciones del usuario
- Calcular derivadas automaticamente (Newton-Raphson)
- Convertir strings a funciones evaluables con `lambdify`

### P: "Que es lambdify?"

**R:** Es una funcion de SymPy que convierte una expresion simbolica en una funcion numerica rapida:
```python
x = sp.Symbol('x')
expr = sp.sympify("x**2 + 1")   # expresion simbolica
f = sp.lambdify(x, expr, 'numpy')  # funcion numerica
f(3)  # → 10.0 (rapido, usa NumPy)
```

### P: "Que es un DataFrame?"

**R:** Es una tabla de datos de la libreria Pandas. Como una hoja de Excel en Python. Lo usamos para mostrar las tablas de iteraciones con columnas como "iteracion", "x_n", "f(x_n)", "error".

### P: "Que es LaTeX?"

**R:** Es un sistema de tipografia para formulas matematicas. En vez de escribir `x_(n+1) = x_n - f(x_n)/f'(x_n)` mostramos:

$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$

Streamlit renderiza LaTeX automaticamente con `st.latex()`.

---

## SECCION 10: PREGUNTAS DIFICILES

### P: "Por que no usaron MATLAB?"

**R:** Python es:
- Gratis (MATLAB cuesta $$$)
- Tiene mas librerias para web (Streamlit, Plotly)
- Se puede deployar gratis en la nube
- Mas usado en la industria actual
- Los metodos numericos son igual de precisos

### P: "Como verificaron que los resultados son correctos?"

**R:**
1. Comparamos con soluciones analiticas conocidas (ej: raiz de x^2-4 debe ser 2)
2. Verificamos convergencia (el error debe disminuir en cada iteracion)
3. El analisis de orden confirma que cada metodo converge al orden teorico esperado
4. Comparamos entre metodos (ej: Biseccion, Newton y Punto Fijo deben dar la misma raiz)

### P: "Que limitaciones tiene la app?"

**R:**
- Solo funciones de una variable (no multivariable)
- Precision limitada por punto flotante (16 digitos)
- Algunos metodos pueden diverger con malas entradas
- Las graficas son 2D (no 3D)
- Depende de internet para acceso remoto (Streamlit Cloud)

### P: "Si Streamlit Cloud se cae, que pasa?"

**R:** La app tambien se cae. Pero:
- El codigo sigue en GitHub (nunca se pierde)
- Se puede correr localmente con `streamlit run app.py`
- Streamlit Cloud tiene 99.9% de uptime

### P: "Cuanto tiempo les tomo?"

**R:** El desarrollo del proyecto incluyo:
- Diseno de la arquitectura y seleccion de metodos
- Implementacion de los 15+ metodos numericos
- Diseno de la interfaz glassmorphism
- Integracion de graficas interactivas
- Deploy en la nube con QR
- Pruebas y depuracion

### P: "Que es el orden de convergencia?"

**R:** Es que tan rapido un metodo se acerca a la solucion:
- **Orden 1 (lineal)**: Biseccion — cada iteracion gana ~1 digito de precision
- **Orden 2 (cuadratico)**: Newton-Raphson — cada iteracion DUPLICA los digitos correctos
- **Orden 4**: RK4 — si reduces h a la mitad, el error se reduce 16 veces (2^4)

### P: "Que es tolerancia?"

**R:** Es el margen de error que el usuario acepta. Si pones tolerancia = 0.0001, el metodo se detiene cuando el error es menor a 0.0001. Menor tolerancia = mas precision pero mas iteraciones.

---

## SECCION 11: COMO EXPLICAR EL CODIGO EN VIVO

Si te piden que muestres el codigo, abre `app.py` en VS Code y:

1. **Ctrl+G** → Ir a linea. Usa estos numeros de referencia:
   - Linea ~70: CSS del tema
   - Linea ~430: Parser de funciones
   - Linea ~530: Validaciones
   - Linea ~1060: Graficas Plotly
   - Linea ~1470: Biseccion
   - Linea ~1640: Sistemas Lineales
   - Linea ~2520: Vista de Inicio
   - Linea ~4280: Punto de entrada principal

2. **Ctrl+F** → Buscar. Escribe el nombre del metodo:
   - "def biseccion" → te lleva directo al codigo
   - "def newton_raphson" → te lleva directo
   - "CSS_GLOBAL" → te lleva al tema visual

3. Muestra la **TABLA DE CONTENIDOS** al inicio del archivo (lineas 26-48)

4. Muestra los **comentarios** — cada seccion tiene banners claros:
   ```
   # ══════════════════════════════════════════════════════════
   # SECCION 8: ECUACIONES NO LINEALES
   # ══════════════════════════════════════════════════════════
   ```

---

## TIPS PARA LA PRESENTACION

1. **Si no sabes algo:** "Esa parte la implemento mi companero/a, pero el concepto general es..."
2. **Si te preguntan algo muy tecnico:** Abre el codigo y muestralo — los comentarios explican todo
3. **Si te preguntan por que Python:** "Es el lenguaje mas usado en ciencia de datos e ingenieria, es gratis, y tiene las mejores librerias para esto"
4. **Muestra la app en vivo:** Es mas impactante que slides
5. **Ten el QR listo:** Imprimelo o muestralo en pantalla para que los jueces lo escaneen
6. **Demuestra interactividad:** Cambia la funcion, el intervalo, la tolerancia — muestra que es una herramienta REAL, no un demo estatico
