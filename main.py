import streamlit as st
import math

# Configuración de Metalúrgica FDM
st.set_page_config(page_title="FDM Plegados", layout="centered")
st.title("🛠️ Simulador Metalúrgica FDM")

# 1. Base de Datos (Tus medidas reales)
espesores = [0.5, 0.9, 1.25, 1.6, 2.0, 2.5, 3.18, 4.76, 6.35]
CUELLO_PUNZON = 18.0
RADIO_CUBO = 95 / 2

# 2. Interfaz de Usuario
with st.expander("1. Configuración de Material", expanded=True):
    esp = st.selectbox("Espesor de Chapa (mm)", espesores)
    v_sugerida = esp * 8
    v_matriz = st.number_input("V de la Matriz (mm)", value=float(v_sugerida))

with st.expander("2. Datos del Pliegue", expanded=True):
    ala = st.number_input("Largo de ala deseada (mm)", value=30.0)
    angulo = st.slider("Ángulo de plegado (grados)", 30, 150, 90)
    sentido = st.radio("¿El ala va hacia el cuello del punzón?", ["Sí", "No"])

# 3. Cálculos Técnicos
radio_interno = v_matriz / 6
# Cálculo de Deducción de Pliegue (Simplificado para taller)
descuento = (2 * (radio_interno + esp)) - (math.pi/2 * (radio_interno + (esp/2)))

# 4. Resultados y Alertas
st.subheader("📋 Resultado del Análisis")

if sentido == "Sí" and ala > CUELLO_PUNZON:
    st.error(f"❌ ¡CHOQUE! El ala de {ala}mm es mayor al cuello de {CUELLO_PUNZON}mm.")
elif ala > RADIO_CUBO:
    st.warning(f"⚠️ CUIDADO: El ala de {ala}mm puede tocar el lateral del cubo de 95mm.")
else:
    st.success("✅ Pliegue físicamente posible.")

st.metric("Cortar chapa con este descuento:", f"- {descuento:.2f} mm")
st.info(f"Para obtener un ala de {ala}mm, marcá la chapa a {ala - (descuento/2):.2f}mm.")