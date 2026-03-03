import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math

st.set_page_config(page_title="FDM - Simulador Pro", layout="wide")
st.title("🚀 FDM Fase 2: Simulador de Ángulos y Formas (U/Z)")

# 1. PARÁMETROS DE MÁQUINA
CUELLO = 18.0

with st.sidebar:
    st.header("⚙️ Configuración Global")
    esp = st.selectbox("Espesor (mm):", [0.5, 0.9, 1.25, 1.6, 2.0, 2.5, 3.18, 4.76, 6.35], key="esp_f2")
    v_matriz = st.number_input("V de Matriz (mm):", value=float(esp * 8), key="v_f2")
    
    st.divider()
    st.subheader("📐 Medidas de las Alas")
    input_alas = st.text_input("Alas (ej: 20, 40, 20):", "20, 40, 20", key="alas_f2")

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
        ang = st.number_input(f"Ángulo (°)", 1, 90, 90, key=f"ang_{i}")
        tipo = st.selectbox(f"Sentido", ["Mismo lado (U)", "Lado opuesto (Z)"], key=f"tipo_{i}")
        config_golpes.append({"angulo": ang, "tipo": tipo})

# 3. CÁLCULOS TÉCNICOS (Desarrollo dinámico por ángulo)
desarrollo = sum(lista_alas)
r_int = v_matriz / 6
for golpe in config_golpes:
    # Fórmula de deducción ajustada por ángulo
    # A menor ángulo, menos descuento de chapa
    factor_ang = golpe["angulo"] / 90
    deduccion = ((2 * (r_int + esp)) - ((math.pi/2) * (r_int + (esp*0.45)))) * factor_ang
    desarrollo -= deduccion

st.success(f"📏 LARGO TOTAL PARA CORTAR: **{desarrollo:.2f} mm**")

# 4. REPRESENTACIÓN DE LA FORMA FINAL (Esquema de la pieza)
st.subheader("🎨 Representación Visual de la Pieza")
fig_shape, ax_s = plt.subplots(figsize=(8, 6))

curr_x, curr_y = 0, 0
curr_angle = 0 # Horizontal inicial

points_x = [0]
points_y = [0]

for i, ala in enumerate(lista_alas):
    # Dibujar ala
    new_x = curr_x + ala * math.cos(math.radians(curr_angle))
    new_y = curr_y + ala * math.sin(math.radians(curr_angle))
    ax_s.plot([curr_x, new_x], [curr_y, new_y], linewidth=4, color="blue")
    
    # Si hay un pliegue después
    if i < num_pliegues:
        g = config_golpes[i]
        # Si es tipo U, el ángulo suma. Si es Z, resta.
        if "U" in g["tipo"]:
            curr_angle += (180 - g["angulo"])
        else:
            curr_angle -= (180 - g["angulo"])
            
    curr_x, curr_y = new_x, new_y
    points_x.append(new_x)
    points_y.append(new_y)

ax_s.set_aspect('equal')
ax_s.axis('off')
st.pyplot(fig_shape)

# 5. ALERTAS DE CUELLO DE CISNE
st.subheader("📋 Hoja de Ruta e Instrucciones")
for i, ala in enumerate(lista_alas[:-1]):
    if ala > CUELLO:
        st.warning(f"⚠️ GOLPE {i+1}: El ala de {ala}mm es mayor que el cuello ({CUELLO}mm). ¡Verificar orientación!")
    else:
        st.info(f"✅ GOLPE {i+1}: Ala de {ala}mm libre.")
