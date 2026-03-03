import streamlit as st
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="FDM - Validación Física", layout="wide")
st.title("🛠️ FDM: Simulador con Validación de Base (U)")

# --- PARÁMETROS FÍSICOS ---
CUELLO_ANCHO = 18.0 #
LIMITE_TOPE_MIN = 7.0 #

with st.sidebar:
    st.header("⚙️ Configuración")
    esp = st.selectbox("Espesor (mm):", [0.5, 0.9, 1.25, 1.6, 2.0, 2.5, 3.18, 4.76, 6.35], index=2)
    v_matriz = st.number_input("V de Matriz (mm):", value=float(esp * 8))
    st.divider()
    input_alas = st.text_input("Medidas de alas (ej: 20, 10, 20):", "20, 10, 20")

try:
    lista_alas = [float(x.strip()) for x in input_alas.split(",") if x.strip()]
except:
    lista_alas = [20, 10, 20]

num_pliegues = len(lista_alas) - 1

# --- ANÁLISIS DE FACTIBILIDAD DE BASE ---
st.divider()
error_base = False
if len(lista_alas) >= 3:
    # Chequeamos cada "U" posible en la secuencia
    for i in range(len(lista_alas) - 2):
        ala_1 = lista_alas[i]
        centro = lista_alas[i+1]
        ala_2 = lista_alas[i+2]
        # REGLA DE ORO: El centro debe ser mayor al ala para que no choque la matriz
        if centro <= ala_1 or centro <= ala_2:
            error_base = True
            st.error(f"🚫 **ERROR DE DISEÑO:** El centro de {centro}mm es muy chico para alas de {ala_1}mm o {ala_2}mm. La pieza chocará con la matriz o el punzón al intentar el segundo golpe.")

# --- INTERFAZ DE GOLPES ---
config_secuencia = []
if not error_base:
    st.subheader("📑 Estrategia de Plegado")
    cols = st.columns(num_pliegues)
    for i in range(num_pliegues):
        with cols[i]:
            st.markdown(f"### GOLPE {i+1}")
            ang = st.number_input(f"Ángulo", 1, 179, 90, key=f"a_{i}")
            apoyo = st.selectbox("Apoyo de Tope", ["Ala actual", "Girar (Extremo opuesto)"], key=f"ap_{i}")
            sentido = st.selectbox("Sentido", ["Adentro (Giro)", "Afuera"], key=f"s_{i}")
            
            factor = (180 - ang) / 90
            deduc = ((2 * ((v_matriz/6) + esp)) - ((math.pi/2) * ((v_matriz/6) + (esp*0.45)))) * factor
            
            if "Extremo" in apoyo:
                posicion_tope = lista_alas[i] + lista_alas[i+1] + esp - (deduc/2)
            else:
                posicion_tope = lista_alas[i] - (deduc/2)
            
            config_secuencia.append({"angulo": ang, "tipo": sentido, "tope": posicion_tope})
            st.metric("Setear Tope (X)", f"{posicion_tope:.2f} mm")

    # --- DIBUJO ---
    fig, ax = plt.subplots(figsize=(10, 3))
    cx, cy, a_acum = 0, 0, 0
    for i, ala in enumerate(lista_alas):
        nx = cx + ala * math.cos(math.radians(a_acum))
        ny = cy + ala * math.sin(math.radians(a_acum))
        ax.plot([cx, nx], [cy, ny], linewidth=6, color="#28a745", solid_capstyle='round')
        if i < num_pliegues:
            rot = (180 - config_secuencia[i]["angulo"])
            if "Adentro" in config_secuencia[i]["tipo"]: a_acum += rot
            else: a_acum -= rot
        cx, cy = nx, ny
    ax.set_aspect('equal')
    plt.axis('off')
    st.pyplot(fig)
