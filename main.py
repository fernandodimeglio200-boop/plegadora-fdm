import streamlit as st
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="FDM - Control de Topes", layout="wide")
st.title("📏 FDM Fase 4: Posición de Topes y Seguridad")

# --- PARÁMETROS FÍSICOS CALIBRADOS ---
CUELLO_ANCHO = 18.0  # Según tu plano
LIMITE_TOPE_MIN = 7.0 # Tu límite de seguridad para no golpear el punzón

with st.sidebar:
    st.header("⚙️ Configuración")
    esp = st.selectbox("Espesor (mm):", [0.5, 0.9, 1.25, 1.6, 2.0, 2.5, 3.18, 4.76, 6.35], index=2)
    v_matriz = st.number_input("V de Matriz (mm):", value=float(esp * 8))
    st.divider()
    input_alas = st.text_input("Medidas de alas:", "20, 40, 20")

try:
    lista_alas = [float(x.strip()) for x in input_alas.split(",") if x.strip()]
except:
    lista_alas = [10, 10]

num_pliegues = len(lista_alas) - 1

# --- CÁLCULO DE DESARROLLO Y DEDUCCIÓN ---
r_int = v_matriz / 6
def calcular_deduccion(angulo):
    factor = (180 - angulo) / 90
    return ((2 * (r_int + esp)) - ((math.pi/2) * (r_int + (esp*0.45)))) * factor

# --- INTERFAZ DE GOLPES Y TOPES ---
st.subheader("📑 Hoja de Configuración de Máquina")
cols = st.columns(num_pliegues)
config_secuencia = []

for i in range(num_pliegues):
    with cols[i]:
        st.markdown(f"### GOLPE {i+1}")
        ang = st.number_input(f"Ángulo {i+1}", 1, 179, 90, key=f"a_{i}")
        tipo = st.selectbox(f"Sentido {i+1}", ["Adentro", "Afuera"], key=f"s_{i}")
        
        # Cálculo de posición del tope (X)
        # El tope se apoya en el ala anterior. Se resta la mitad de la deducción.
        deduc = calcular_deduccion(ang)
        posicion_tope = lista_alas[i] - (deduc / 2)
        
        config_secuencia.append({"angulo": ang, "tipo": tipo, "tope": posicion_tope})
        
        # Validación de seguridad del tope
        if posicion_tope < LIMITE_TOPE_MIN:
            st.error(f"🚨 TOPE PELIGROSO: {posicion_tope:.2f}mm. ¡El punzón golpeará el tope!")
        else:
            st.metric("Tope (X)", f"{posicion_tope:.2f} mm")

# --- ANÁLISIS DE COLISIÓN DEL PUNZÓN ---
st.divider()
alertas_punzon = []
for i in range(num_pliegues):
    if "Adentro" in config_secuencia[i]["tipo"] and lista_alas[i] > CUELLO_ANCHO:
        alertas_punzon.append(f"❌ **GOLPE {i+1}:** Ala de {lista_alas[i]}mm choca pared de 18mm.")

if alertas_punzon:
    for a in alertas_punzon: st.error(a)
else:
    st.success("✅ Geometría de punzón respetada.")

# --- DIBUJO ---
fig, ax = plt.subplots(figsize=(10, 3))
cx, cy, a_acum = 0, 0, 0
for i, ala in enumerate(lista_alas):
    nx = cx + ala * math.cos(math.radians(a_acum))
    ny = cy + ala * math.sin(math.radians(a_acum))
    ax.plot([cx, nx], [cy, ny], linewidth=6, color="#1f77b4", solid_capstyle='round')
    if i < num_pliegues:
        rot = (180 - config_secuencia[i]["angulo"])
        if "Adentro" in config_secuencia[i]["tipo"]: a_acum += rot
        else: a_acum -= rot
    cx, cy = nx, ny
ax.set_aspect('equal')
plt.axis('off')
st.pyplot(fig)
