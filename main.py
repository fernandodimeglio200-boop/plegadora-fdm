import streamlit as st
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="FDM - Calibración Real", layout="wide")
st.title("📏 FDM: Simulador Calibrado con Punzón Real")

# --- DATOS DEL PLANO PROPORCIONADO ---
CUELLO_ANCHO = 18.0  # El ancho del cuerpo vertical
ALTURA_CUELLO = 95.0 # La altura libre antes del anclaje
ANGULO_PUNZON = 89.0 # Ángulo de la punta

with st.sidebar:
    st.header("⚙️ Configuración")
    esp = st.selectbox("Espesor (mm):", [0.5, 0.9, 1.25, 1.6, 2.0, 2.5, 3.18, 4.76, 6.35], index=2)
    v_matriz = st.number_input("V de Matriz (mm):", value=float(esp * 8))
    st.divider()
    input_alas = st.text_input("Medidas de alas (ej: 20, 40, 20):", "20, 40, 20")

# Procesamiento de alas
try:
    lista_alas = [float(x.strip()) for x in input_alas.split(",") if x.strip()]
except:
    lista_alas = [10, 10, 10]

num_pliegues = len(lista_alas) - 1

# --- INTERFAZ DE GOLPES ---
st.subheader("📑 Secuencia de Trabajo")
cols = st.columns(num_pliegues)
config_secuencia = []

for i in range(num_pliegues):
    with cols[i]:
        st.write(f"**GOLPE {i+1}**")
        ang = st.number_input(f"Ángulo (°)", 1, 179, 90, key=f"ang_{i}")
        sentido = st.selectbox(f"Sentido", ["Adentro (Hacia Cuerpo)", "Afuera (Libre)"], key=f"sen_{i}")
        config_secuencia.append({"angulo": ang, "tipo": sentido})

# --- ANÁLISIS TÉCNICO DE CHOQUE ---
st.divider()
realizable = True
alertas = []

for i in range(num_pliegues):
    ala_lado_punzon = lista_alas[i] 
    
    if "Adentro" in config_secuencia[i]["tipo"]:
        # Si el ala es mayor a los 18mm del plano, golpea la pared vertical
        if ala_lado_punzon > CUELLO_ANCHO:
            realizable = False
            alertas.append(f"❌ **CHOQUE EN GOLPE {i+1}:** El ala de {ala_lado_punzon}mm golpea la pared vertical del punzón (Límite {CUELLO_ANCHO}mm).")
        # Si el ángulo es muy cerrado y el ala es alta
        elif ala_lado_punzon > 40 and config_secuencia[i]["angulo"] < 45:
            alertas.append(f"⚠️ **RIESGO EN GOLPE {i+1}:** Con {config_secuencia[i]['angulo']}°, el ala podría tocar la parte superior del anclaje.")

if realizable:
    st.success("✅ PIEZA FACTIBLE: Las medidas respetan la geometría del punzón FDM.")
else:
    st.error("🚫 NO SE PUEDE PLEGAR: Revisar diseño o sentido de plegado.")

for a in alertas:
    st.write(a)

# --- DIBUJO DE LA PIEZA ---
fig, ax = plt.subplots(figsize=(10, 4))
cx, cy, a_acum = 0, 0, 0
for i, ala in enumerate(lista_alas):
    nx = cx + ala * math.cos(math.radians(a_acum))
    ny = cy + ala * math.sin(math.radians(a_acum))
    ax.plot([cx, nx], [cy, ny], linewidth=6, color=("#28a745" if realizable else "#dc3545"), solid_capstyle='round')
    ax.text((cx+nx)/2, (cy+ny)/2 + 2, f"{ala}", ha='center')
    if i < num_pliegues:
        rot = (180 - config_secuencia[i]["angulo"])
        if "Adentro" in config_secuencia[i]["tipo"]: a_acum += rot
        else: a_acum -= rot
    cx, cy = nx, ny
ax.set_aspect('equal')
plt.axis('off')
st.pyplot(fig)
