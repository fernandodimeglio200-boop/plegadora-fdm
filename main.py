import streamlit as st
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="FDM - Simulador 179", layout="wide")
st.title("🚀 FDM Fase 2: Ángulos de 1° a 179° (U/Z)")

# 1. PARÁMETROS DE MÁQUINA
CUELLO = 18.0

with st.sidebar:
    st.header("⚙️ Configuración Global")
    esp = st.selectbox("Espesor (mm):", [0.5, 0.9, 1.25, 1.6, 2.0, 2.5, 3.18, 4.76, 6.35], key="esp_f2")
    v_matriz = st.number_input("V de Matriz (mm):", value=float(esp * 8), key="v_f2")
    
    st.divider()
    st.subheader("📐 Medidas de las Alas")
    input_alas = st.text_input("Alas (ej: 20, 50, 20):", "20, 50, 20", key="alas_f2")

# Procesamiento de alas
lista_alas = [float(x.strip()) for x in input_alas.split(",") if x.strip()]
num_pliegues = len(lista_alas) - 1

# 2. CONFIGURACIÓN INDIVIDUAL DE GOLPES
st.subheader("🛠️ Configuración de cada Plegado")
columnas = st.columns(num_pliegues)
config_golpes = []

for i in range(num_pliegues):
    with columnas[i]:
        st.markdown(f"**Golpe {i+1}**")
        # Cambio de rango: ahora de 1 a 179 grados
        ang = st.number_input(f"Ángulo (°)", 1, 179, 90, key=f"ang_{i}")
        tipo = st.selectbox(f"Sentido", ["Tipo U", "Tipo Z"], key=f"tipo_{i}")
        config_golpes.append({"angulo": ang, "tipo": tipo})

# 3. CÁLCULO DE DESARROLLO (Ajustado por ángulo)
r_int = v_matriz / 6
desarrollo = sum(lista_alas)

for i in range(num_pliegues):
    ang_plegado = config_golpes[i]["angulo"]
    # Cálculo de deducción de pliegue según ángulo (Fórmula empírica)
    # A 180° la deducción es 0, a 90° es la máxima.
    factor_correccion = (180 - ang_plegado) / 90
    deduccion = ((2 * (r_int + esp)) - ((math.pi/2) * (r_int + (esp*0.45)))) * factor_correccion
    desarrollo -= deduccion

st.success(f"📏 LARGO PARA CORTAR: **{desarrollo:.2f} mm**")

# 4. REPRESENTACIÓN GRÁFICA DE LA FORMA
st.subheader("🎨 Forma Final de la Pieza (Simulación)")
fig_shape, ax_s = plt.subplots(figsize=(10, 6))

curr_x, curr_y = 0, 0
curr_angle = 0  # Horizontal inicial

for i, ala in enumerate(lista_alas):
    # Calculamos el final de la línea actual
    new_x = curr_x + ala * math.cos(math.radians(curr_angle))
    new_y = curr_y + ala * math.sin(math.radians(curr_angle))
    
    # Dibujamos el ala
    ax_s.plot([curr_x, new_x], [curr_y, new_y], linewidth=5, color="#1f77b4", solid_capstyle='round')
    ax_s.text((curr_x + new_x)/2, (curr_y + new_y)/2 + 2, f"{ala}", color="black", fontsize=10)
    
    # Si hay un pliegue después de esta ala, rotamos el ángulo para la siguiente
    if i < num_pliegues:
        g = config_golpes[i]
        # Rotación según el ángulo de plegado ingresado
        rotacion = (180 - g["angulo"])
        if g["tipo"] == "Tipo U":
            curr_
