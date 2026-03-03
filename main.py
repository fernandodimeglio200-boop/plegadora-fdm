import streamlit as st
import matplotlib.pyplot as plt
import math

# Configuración básica
st.set_page_config(page_title="FDM Plegado", layout="wide")

# Título principal
st.title("🛠️ Sistema de Plegado Dinámico - FDM")

# 1. ENTRADA DE DATOS (Panel Lateral)
with st.sidebar:
    st.header("Configuración de Taller")
    # Usamos keys únicas para que Streamlit no se confunda
    esp_maquina = st.selectbox("Espesor de Chapa (mm):", 
                               [0.5, 0.9, 1.25, 1.6, 2.0, 2.5, 3.18, 4.76, 6.35], 
                               key="f_esp_1")
    
    v_matriz_maquina = st.number_input("V de Matriz (mm):", 
                                       value=float(esp_maquina * 8), 
                                       key="f_v_1")
    
    st.divider()
    st.subheader("Medidas de la Pieza")
    input_alas_maquina = st.text_input("Ingresá las alas (separadas por coma):", 
                                       "20, 40, 20", 
                                       key="f_alas_1")

# 2. PROCESAMIENTO
try:
    lista_alas = [float(x.strip()) for x in input_alas_maquina.split(",") if x.strip()]
except:
    st.error("Error: Por favor usá solo números y comas.")
    lista_alas = [10, 10]

num_pliegues = len(lista_alas) - 1
r_int = v_matriz_maquina / 6
# Cálculo de estiramiento (Deducción)
deduccion = (2 * (r_int + esp_maquina)) - ((math.pi/2) * (r_int + (esp_maquina*0.45)))
desarrollo = sum(lista_alas) - (deduccion * num_pliegues)

# 3. RESULTADOS Y GRÁFICO
st.success(f"📏 LARGO PARA CORTAR: **{desarrollo:.2f} mm**")

st.subheader("✍️ Esquema de Plegado")
fig, ax = plt.subplots(figsize=(12, 3))
acumulado = 0

for i, ala in enumerate(lista_alas):
    # Dibujo proporcional de las alas
    ax.plot([acumulado, acumulado + ala], [0, 0], linewidth=10, solid_capstyle='round')
    ax.text(acumulado + (ala/2), -0.4, f"{ala}mm", ha='center', weight='bold')
    
    if i < num_pliegues:
        punto = acumulado + ala
        ax.plot(punto, 0, 'ro', markersize=12) # Punto de golpe
        ax.text(punto, 0.5, f"GOLPE {i+1}", color='red', ha='center', weight='bold')
        
        # Alerta de choque con punzón de 18mm
        if ala > 18.0:
            ax.text(punto, 1.0, "⚠️ CUIDADO", color='orange', ha='center', weight='bold')
    
    acumulado += ala

ax.set_ylim(-1.5, 2)
ax.axis('off')
st.pyplot(fig)
