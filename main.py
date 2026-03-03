import streamlit as st
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="FDM - Simulador 179", layout="wide")
st.title("🚀 FDM Fase 2: Simulador con Ángulos (1° a 179°)")

# 1. PARÁMETROS DE MÁQUINA
CUELLO = 18.0

with st.sidebar:
    st.header("⚙️ Configuración Global")
    esp = st.selectbox("Espesor (mm):", [0.5, 0.9, 1.25, 1.6, 2.0, 2.5, 3.18, 4.76, 6.35], key="esp_f2")
    v_matriz = st.number_input("V de Matriz (mm):", value=float(esp * 8), key="v_f2")
    
    st.divider()
    st.subheader("📐 Medidas de las Alas")
    input_alas = st.text_input("Alas (ej: 30, 60, 30):", "30, 60, 30", key="alas_f2")

# Procesamiento de alas
try:
    lista_alas = [float(x.strip()) for x in input_alas.split(",") if x.strip()]
except:
    lista_alas = [10, 10]

num_pliegues = len(lista_alas) - 1

# 2. CONFIGURACIÓN INDIVIDUAL DE GOLPES
st.subheader("🛠️ Configuración de cada Plegado")
columnas = st.columns(num_pliegues)
config_golpes = []

for i in range(num_pliegues):
    with columnas[i]:
        st.markdown(f"**Golpe {i+1}**")
        ang = st.number_input(f"Ángulo (°)", 1, 179, 90, key=f"ang_{i}")
        tipo = st.selectbox(f"Sentido", ["Tipo U", "Tipo Z"], key=f"tipo_{i}")
        config_golpes.append({"angulo": ang, "tipo": tipo})

# 3. CÁLCULO DE DESARROLLO (Ajustado por ángulo)
r_int = v_matriz / 6
desarrollo = sum(lista_alas)

for i in range(num_pliegues):
    ang_plegado = config_golpes[i]["angulo"]
    # A mayor ángulo (más abierto), menos descuento. 180° = 0 descuento.
    factor_correccion = (180 - ang_plegado) / 90
    deduccion = ((2 * (r_int + esp)) - ((math.pi/2) * (r_int + (esp*0.45)))) * factor_correccion
    desarrollo -= deduccion

st.success(f"📏 LARGO PARA CORTAR: **{desarrollo:.2f} mm**")

# 4. REPRESENTACIÓN GRÁFICA DE LA FORMA
st.subheader("🎨 Forma Final de la Pieza (Simulación)")
fig_shape, ax_s = plt.subplots(figsize=(10, 6))

cx, cy = 0, 0  # Coordenadas de inicio
angulo_actual = 0 

for i, ala in enumerate(lista_alas):
    # Calcular el siguiente punto
    proximo_x = cx + ala * math.cos(math.radians(angulo_actual))
    proximo_y = cy + ala * math.sin(math.radians(angulo_actual))
    
    # Dibujar el ala
    ax_s.plot([cx, proximo_x], [cy, proximo_y], linewidth=6, color="#1f77b4", solid_capstyle='round')
    
    # Etiqueta de largo de ala
    ax_s.text((cx + proximo_x)/2, (cy + proximo_y)/2 + 1, f"{ala}mm", ha='center', fontsize=9)
    
    # Si hay un pliegue, calcular el nuevo ángulo para la siguiente ala
    if i < num_pliegues:
        g = config_golpes[i]
        rotacion = (180 - g["angulo"])
        
        # Etiqueta del ángulo en el vértice
        ax_s.text(proximo_x, proximo_y + 2, f"{g['angulo']}°", color="red", fontweight="bold")
        
        if g["tipo"] == "Tipo U":
            angulo_actual += rotacion
        else:
            angulo_actual -= rotacion
            
    cx, cy = proximo_x, proximo_y

ax_s.set_aspect('equal')
ax_s.axis('off')
st.pyplot(fig_shape)

# 5. ALERTAS DE CHOQUE
st.divider()
for i, ala in enumerate(lista_alas[:-1]):
    if ala > CUELLO:
        st.warning(f"⚠️ GOLPE {i+1}: El ala de {ala}mm es larga. ¡Cuidado con el cuello de 18mm!")
