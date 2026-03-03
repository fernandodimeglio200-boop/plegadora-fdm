import streamlit as st
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="FDM - Secuenciador", layout="wide")
st.title("🛡️ FDM Fase 3: Verificador de Colisión (Adentro / Afuera)")

# --- PARÁMETROS FÍSICOS DE METALÚRGICA FDM ---
CUELLO_PUNZON = 18.0  # Profundidad máxima para pliegues hacia ADENTRO

with st.sidebar:
    st.header("⚙️ Configuración")
    esp = st.selectbox("Espesor (mm):", [0.5, 0.9, 1.25, 1.6, 2.0, 2.5, 3.18, 4.76, 6.35], index=2)
    v_matriz = st.number_input("V de Matriz (mm):", value=float(esp * 8))
    st.divider()
    st.subheader("📐 Medidas de las Alas")
    # Ejemplo solicitado: 5 alas para generar 4 pliegues
    input_alas = st.text_input("Ingresá las alas separadas por coma:", "20, 30, 60, 30, 20")

# Procesamiento de datos
try:
    lista_alas = [float(x.strip()) for x in input_alas.split(",") if x.strip()]
except:
    lista_alas = [10, 10, 10, 10, 10]

num_pliegues = len(lista_alas) - 1

# --- CONFIGURACIÓN DE SECUENCIA ---
st.subheader("📑 Configuración de la Secuencia de Plegado")
cols = st.columns(num_pliegues)
config_secuencia = []

# Mapeo solicitado: Golpes 1 y 2 AFUERA, Golpes 3 y 4 ADENTRO
for i in range(num_pliegues):
    with cols[i]:
        st.markdown(f"**Plegado {i+1}**")
        ang = st.number_input(f"Ángulo {i+1} (°)", 1, 179, 90, key=f"a_{i}")
        # Cambiamos U/Z por Adentro/Afuera
        # Ponemos por defecto Afuera para los primeros dos y Adentro para el resto
        default_idx = 1 if i < 2 else 0 
        tipo = st.selectbox(f"Sentido {i+1}", ["Adentro (U)", "Afuera (Z)"], 
                            index=default_idx, key=f"t_{i}")
        config_secuencia.append({"angulo": ang, "tipo": tipo})

# --- ANÁLISIS DE FACTIBILIDAD ---
st.divider()
st.subheader("🔍 Análisis de Realizabilidad en Plegadora")

es_realizable = True
mensajes_alerta = []

for i in range(num_pliegues):
    ala_izq = lista_alas[i]
    sentido = config_secuencia[i]["tipo"]
    
    # Lógica de choque: Si es hacia ADENTRO, el ala no puede superar el cuello del punzón
    if "Adentro" in sentido:
        if ala_izq > CUELLO_PUNZON:
            es_realizable = False
            mensajes_alerta.append(f"❌ **GOLPE {i+1} (Adentro):** El ala de {ala_izq}mm choca con el cuello de {CUELLO_PUNZON}mm.")
    
    # Si es hacia AFUERA, avisamos si es muy larga para la mesa
    if "Afuera" in sentido:
        if ala_izq > 50.0:
            mensajes_alerta.append(f"⚠️ **GOLPE {i+1} (Afuera):** Ala de {ala_izq}mm es larga, verificar que no toque la mesa o la estructura.")

if es_realizable:
    st.success("✅ **PIEZA REALIZABLE:** La secuencia no presenta choques con el punzón de 18mm.")
else:
    st.error("🚫 **PIEZA NO REALIZABLE:** Se detectaron colisiones críticas.")

for m in mensajes_alerta:
    st.write(m)

# --- DIBUJO DE LA FORMA FINAL ---
st.subheader("🎨 Simulación de Forma Final")
fig, ax = plt.subplots(figsize=(10, 5))
cx, cy, ang_actual = 0, 0, 0

for i, ala in enumerate(lista_alas):
    nx = cx + ala * math.cos(math.radians(ang_actual))
    ny = cy + ala * math.sin(math.radians(ang_actual))
    
    # Color verde si pasa, rojo si choca
    color_pieza = "#28a745" if es_realizable else "#dc3545"
    ax.plot([cx, nx], [cy, ny], linewidth=6, color=color_pieza, solid_capstyle='round')
    
    # Texto de medida de ala
    ax.text((cx+nx)/2, (cy+ny)/2 + 2, f"{ala}", ha='center', fontsize=9)
    
    if i < num_pliegues:
        rot = (180 - config_secuencia[i]["angulo"])
        # Adentro suma ángulo (cierra), Afuera resta ángulo (abre/Z)
        if "Adentro" in config_secuencia[i]["tipo"]:
            ang_actual += rot
        else:
            ang_actual -= rot
    cx, cy = nx, ny

ax.set_aspect('equal')
plt.axis('off')
st.pyplot(fig)

# Desarrollo al final
r_int = v_matriz / 6
desarrollo = sum(lista_alas)
for g in config_secuencia:
    factor = (180 - g["angulo"]) / 90
    deduccion = ((2 * (r_int + esp)) - ((math.pi/2) * (r_int + (esp*0.45)))) * factor
    desarrollo -= deduccion

st.info(f"📏 **LARGO TOTAL PARA CORTAR: {desarrollo:.
