import streamlit as st
import matplotlib.pyplot as plt
import math

# Configuración básica de FDM
st.set_page_config(page_title="FDM - Golpes", layout="wide")

st.title("🛠️ Sistema de Plegado Dinámico con Mapa de Golpes - FDM")

# 1. PARÁMETROS DE MÁQUINA Y PIEZA
# Estos datos definen los límites de choque
CUELLO_CISNE_MM = 18.0 

with st.sidebar:
    st.header("⚙️ Configuración")
    # Selectores únicos para evitar errores
    esp_maquina = st.selectbox("Espesor (mm):", 
                               [0.5, 0.9, 1.25, 1.6, 2.0, 2.5, 3.18, 4.76, 6.35], 
                               key="f_esp_1")
    
    v_matriz_maquina = st.number_input("V de Matriz (mm):", 
                                       value=float(esp_maquina * 8), 
                                       key="f_v_1")
    
    st.divider()
    st.subheader("📐 Medidas de la Pieza")
    input_alas_maquina = st.text_input("Ingresá las alas (separadas por coma):", 
                                       "20, 40, 20", 
                                       key="f_alas_1")

# 2. PROCESAMIENTO Y CÁLCULOS
try:
    # Convertimos el texto a una lista de números reales
    lista_alas = [float(x.strip()) for x in input_alas_maquina.split(",") if x.strip()]
except:
    st.error("Error: Usá solo números y comas.")
    lista_alas = [10, 10]

num_pliegues = len(lista_alas) - 1
r_int = v_matriz_maquina / 6
# Cálculo de estiramiento (Deducción)
deduccion = (2 * (r_int + esp_maquina)) - ((math.pi/2) * (r_int + (esp_maquina*0.45)))
desarrollo = sum(lista_alas) - (deduccion * num_pliegues)

# 3. RESULTADOS EN PANTALLA
st.success(f"📏 LARGO PARA CORTAR: **{desarrollo:.2f} mm**")

# 4. GRÁFICO CON MAPA DE GOLPES
st.subheader("✍️ Mapa de Secuencia de Plegado (Proporcional)")
fig, ax = plt.subplots(figsize=(12, 4))
acumulado = 0

# Colores para distinguir cada ala proporcionalmente
colores_alas = plt.cm.get_cmap('tab10', len(lista_alas))

for i, ala in enumerate(lista_alas):
    # Dibuja la línea proporcional del ala según la medida
    ax.plot([acumulado, acumulado + ala], [0, 0], 
            color=colores_alas(i), linewidth=10, solid_capstyle='round')
    
    # Etiqueta con la medida del ala en el centro de la línea
    ax.text(acumulado + (ala/2), -0.4, f"{ala}mm", ha='center', weight='bold')
    
    # Si hay un pliegue después de esta ala, dibujamos el punto de golpe
    if i < num_pliegues:
        punto_pliegue = acumulado + ala
        
        # Círculo rojo que marca el lugar exacto del plegado
        ax.plot(punto_pliegue, 0, 'ro', markersize=14) 
        # Número de golpe secuencial
        ax.text(punto_pliegue, 0.6, f"GOLPE {i+1}", color='red', 
                ha='center', fontsize=12, weight='bold')
        
        # ALERTA DE CHOQUE CON CUELLO DE 18mm
        if ala > CUELLO_CISNE_MM:
            # Ponemos el triángulo y el texto en color naranja
            ax.text(punto_pliegue, 1.2, "⚠️ CUIDADO CON EL CUELLO", 
                    color='orange', ha='center', fontsize=11, weight='bold')
    
    # Avanzamos para el siguiente segmento
    acumulado += ala

# Ajustes de visualización del gráfico
ax.set_ylim(-1.5, 2.5)
ax.set_xlim(-5, sum(lista_alas) + 5)
ax.axis('off') # Ocultamos los ejes para que parezca un plano de taller
st.pyplot(fig)
