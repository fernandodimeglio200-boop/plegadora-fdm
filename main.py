import streamlit as st
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="FDM - Lógica de Taller", layout="wide")
st.title("🛠️ FDM: Simulador Inteligente de Plegado")

# --- PARÁMETROS FÍSICOS ---
CUELLO_ANCHO = 18.0 #
LIMITE_TOPE_MIN = 7.0 #

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

# --- INTERFAZ ---
st.subheader("📑 Secuencia de Plegado")
cols = st.columns(num_pliegues)
config_secuencia = []

for i in range(num_pliegues):
    with cols[i]:
        st.markdown(f"### GOLPE {i+1}")
        ang = st.number_input(f"Ángulo {i+1}", 1, 179, 90, key=f"a_{i}")
        tipo = st.selectbox(f"Sentido {i+1}", ["Adentro", "Afuera"], key=f"s_{i}")
        
        # Cálculo de tope (X)
        factor = (180 - ang) / 90
        deduc = ((2 * ( (v_matriz/6) + esp)) - ((math.pi/2) * ( (v_matriz/6) + (esp*0.45)))) * factor
        posicion_tope = lista_alas[i] - (deduc / 2)
        
        config_secuencia.append({"angulo": ang, "tipo": tipo, "tope": posicion_tope})
        
        if posicion_tope < LIMITE_TOPE_MIN:
            st.error(f"🚨 TOPE: {posicion_tope:.2f}mm")
        else:
            st.metric("Tope (X)", f"{posicion_tope:.2f}")

# --- ANÁLISIS DE COLISIÓN (CORREGIDO) ---
st.divider()
alertas = []
realizable = True

for i in range(num_pliegues):
    # LÓGICA: En el GOLPE 1 no hay nada doblado que choque. 
    # El choque ocurre si en el GOLPE 2 o más, el ala previa (i) entra al punzón.
    if i > 0: # Solo chequear colisión desde el segundo golpe en adelante
        ala_previa = lista_alas[i]
        if "Adentro" in config_secuencia[i]["tipo"] and ala_previa > CUELLO_ANCHO:
            realizable = False
            alertas.append(f"❌ **GOLPE {i+1}:** El ala ya plegada de {ala_previa}mm choca con el punzón.")

if realizable:
    st.success("✅ PIEZA REALIZABLE")
else:
    st.error("🚫 COLISIÓN DETECTADA")

for a in alertas: st.write(a)

# --- DIBUJO ---
fig, ax = plt.subplots(figsize=(10, 3))
cx, cy, a_acum = 0, 0, 0
for i, ala in enumerate(lista_alas):
    nx = cx + ala * math.cos(math.radians(a_acum))
    ny = cy + ala * math.sin(math.radians(a_acum))
    ax.plot([cx, nx], [cy, ny], linewidth=6, color=("#28a745" if realizable else "#dc3545"), solid_capstyle='round')
    if i < num_pliegues:
        rot = (180 - config_secuencia[i]["angulo"])
        if "Adentro" in config_secuencia[i]["tipo"]: a_acum += rot
        else: a_acum -= rot
    cx, cy = nx, ny
ax.set_aspect('equal')
plt.axis('off')
st.pyplot(fig)
