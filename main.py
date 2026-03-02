import streamlit as st
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="FDM - Calculador Maestro", layout="wide")
st.title("📏 Planificador de Corte y Plegado - Metalúrgica FDM")

# 1. Parámetros Técnicos
CUELLO_PUNZON = 18.0
RADIO_CUBO = 47.5  # 95mm / 2

# 2. Configuración de Material
with st.sidebar:
    st.header("Datos de Corte")
    esp = st.selectbox("Espesor de Chapa (mm)", [0.5, 0.9, 1.25, 1.6, 2.0, 2.5, 3.18, 4.76, 6.35])
    v_matriz = st.number_input("V de Matriz usada (mm)", value=float(esp * 8))

# 3. Definición de la Pieza (Dibujo cargado)
alas = [20, 40, 60, 15, 30, 15, 40, 40, 20]
num_pliegues = 8

# 4. Cálculos de Desarrollo (Deducción de Pliegue)
# Usamos una fórmula de taller: radio interno aprox V/6
r_int = v_matriz / 6
# Cálculo de la deducción por cada pliegue de 90°
deduccion_por_pliegue = (2 * (r_int + esp)) - ( (math.pi/2) * (r_int + (esp*0.45)) )
desarrollo_total = sum(alas) - (deduccion_por_pliegue * num_pliegues)

# 5. Interfaz de Resultados
col_a, col_b = st.columns(2)
with col_a:
    st.metric("Largo total de chapa a CORTAR:", f"{desarrollo_total:.2f} mm")
with col_b:
    st.metric("Descuento total aplicado:", f"{deduccion_por_pliegue * num_pliegues:.2f} mm")

# 6. Mapa de Golpes y Orientación
st.divider()
st.subheader("🔢 Secuencia de Golpes y Posición del Punzón")

fig, ax = plt.subplots(figsize=(12, 5))
x_c = [0, 20, 20, 60, 60, 75, 105, 120, 120, 160, 160, 180]
y_c = [0, 0,  40, 40, 60, 60, 60,  60,  40, 40,  0,   0]
ax.plot(x_c, y_c, color='navy', linewidth=4)

# Datos de la secuencia
secuencia = [
    {"p": 1, "coord": (60, 60), "dir": "Derecha", "ala": 15},
    {"p": 2, "coord": (75, 60), "dir": "Izquierda", "ala": 30},
    {"p": 3, "coord": (105, 60), "dir": "Izquierda", "ala": 15},
    {"p": 4, "coord": (60, 40), "dir": "Derecha", "ala": 60},
    {"p": 5, "coord": (120, 60), "dir": "Izquierda", "ala": 40},
    {"p": 6, "coord": (20, 40), "dir": "Girar 180°", "ala": 40},
    {"p": 7, "coord": (120, 40), "dir": "Girar 180°", "ala": 40},
    {"p": 8, "coord": (20, 0), "dir": "Libre", "ala": 20}
]

for s in secuencia:
    ax.text(s["coord"][0], s["coord"][1], str(s["p"]), color='white', 
            bbox=dict(facecolor='red', boxstyle='circle'), fontsize=12)
    if s["ala"] > CUELLO_PUNZON:
        ax.text(s["coord"][0], s["coord"][1]-10, "⚠️ CHOQUE", color='red', fontsize=8)

ax.axis('off')
st.pyplot(fig)

st.table(secuencia)
