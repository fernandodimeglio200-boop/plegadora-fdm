import streamlit as st
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="FDM - Topes Especiales", layout="wide")
st.title("🛠️ FDM: Simulador con Giro y Tope Extendido")

# --- PARÁMETROS FÍSICOS ---
CUELLO_ANCHO = 18.0 #
LIMITE_TOPE_MIN = 7.0 #

with st.sidebar:
    st.header("⚙️ Configuración")
    esp = st.selectbox("Espesor (mm):", [0.5, 0.9, 1.25, 1.6, 2.0, 2.5, 3.18, 4.76, 6.35], index=2)
    v_matriz = st.number_input("V de Matriz (mm):", value=float(esp * 8))
    st.divider()
    input_alas = st.text_input("Medidas de alas (ej: 20, 40, 20):", "20, 40, 20")

try:
    lista_alas = [float(x.strip()) for x in input_alas.split(",") if x.strip()]
except:
    lista_alas = [20, 40, 20]

num_pliegues = len(lista_alas) - 1

# --- INTERFAZ DE GOLPES ---
st.subheader("📑 Estrategia de Plegado")
cols = st.columns(num_pliegues)
config_secuencia = []

for i in range(num_pliegues):
    with cols[i]:
        st.markdown(f"### GOLPE {i+1}")
        ang = st.number_input(f"Ángulo", 1, 179, 90, key=f"a_{i}")
        # Nueva opción de apoyo para el tope
        apoyo = st.selectbox("Apoyo de Tope", ["Ala actual", "Girar (Extremo opuesto)"], key=f"ap_{i}")
        sentido = st.selectbox("Sentido", ["Adentro (Giro)", "Afuera"], key=f"s_{i}")
        
        # Cálculo de deducción
        factor = (180 - ang) / 90
        deduc = ((2 * ((v_matriz/6) + esp)) - ((math.pi/2) * ((v_matriz/6) + (esp*0.45)))) * factor
        
        # LÓGICA DE TOPE SOLICITADA:
        # Si se apoya en el extremo opuesto, el tope es Ala + Centro + Espesor
        if "Extremo" in apoyo:
            posicion_tope = lista_alas[i] + lista_alas[i+1] + esp - (deduc/2)
        else:
            posicion_tope = lista_alas[i] - (deduc/2)
        
        config_secuencia.append({"angulo": ang, "tipo": sentido, "tope": posicion_tope})
        
        if posicion_tope < LIMITE_TOPE_MIN:
            st.error(f"🚨 TOPE CORTO: {posicion_tope:.2f}")
        else:
            st.metric("Setear Tope (X)", f"{posicion_tope:.2f} mm")

# --- ANÁLISIS DE COLISIÓN ---
st.divider()
alertas = []
es_realizable = True

for i in range(num_pliegues):
    if i > 0 and "Adentro" in config_secuencia[i]["tipo"]:
        ala_previa = lista_alas[i]
        if ala_previa > CUELLO_ANCHO:
            if (ala_previa - CUELLO_ANCHO) <= 3:
                alertas.append(f"⚠️ **GOLPE {i+1}:** Ala de {ala_previa}mm requiere maniobra en el cuello de {CUELLO_ANCHO}mm.")
            else:
                es_realizable = False
                alertas.append(f"❌ **GOLPE {i+1}:** Ala de {ala_previa}mm choca con pared vertical.")

if es_realizable:
    st.success("✅ PIEZA FACTIBLE")
else:
    st.error("🚫 REVISAR MEDIDAS")

for a in alertas: st.write(a)

# --- DIBUJO ---
fig, ax = plt.subplots(figsize=(10, 3))
cx, cy, a_acum = 0, 0, 0
for i, ala in enumerate(lista_alas):
    nx = cx + ala * math.cos(math.radians(a_acum))
    ny = cy + ala * math.sin(math.radians(a_acum))
    color = "#28a745" if es_realizable else "#dc3545"
    ax.plot([cx, nx], [cy, ny], linewidth=6, color=color, solid_capstyle='round')
    if i < num_pliegues:
        rot = (180 - config_secuencia[i]["angulo"])
        if "Adentro" in config_secuencia[i]["tipo"]: a_acum += rot
        else: a_acum -= rot
    cx, cy = nx, ny
ax.set_aspect('equal')
plt.axis('off')
st.pyplot(fig)
