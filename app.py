import streamlit as st

st.set_page_config(page_title="Predicciones del Torneo Capi Games", page_icon="🏆", layout="centered")

st.title("🏆 Predicciones del Torneo")
st.markdown("¡Arma tu pronóstico para el torneo de Capi Games! Selecciona los ganadores de cada etapa y descubre quién se lleva la gloria.")

jugadores = [
    "Naza", "Santy", "Enzo", "Raúl", "Amu", "Gabriel", "Torres", "Gahel", 
    "Santino", "Joa", "Mariano", "Victoria", "Mía", "Agustín", "Juan", "Mora"
]

# Inicializamos el diccionario de puntos para los pronósticos
puntos = {j: 0 for j in jugadores}

# ==========================================
# FASE 1: FASE REGULAR (JUEGOS 1 AL 6)
# ==========================================
st.header("1️⃣ Fase Regular (Acumulación de Puntos)")
st.write("Selecciona a los ganadores de cada juego de la primera fase:")

col1, col2 = st.columns(2)
with col1:
    g_capi = st.selectbox("Capi Dice (1º Lugar - 3 pts)", jugadores, key="capi")
    g_bingo = st.selectbox("Bingo (Ganador - 3 pts)", jugadores, key="bingo")
    g_memo = st.selectbox("Duelos 2vs2 / Memotest (Ganador)", jugadores, key="memo")
with col2:
    g_tictac = st.selectbox("Tic Tac (1º Lugar - 3 pts)", jugadores, key="tictac")
    g_mimica = st.selectbox("Dígalo con Mímica (Equipo Ganador)", jugadores, key="mimica")
    g_nota = st.selectbox("En Una Nota (1º Lugar - 5 pts)", jugadores, key="nota")

# Otorgamos puntos según las elecciones
puntos[g_capi] += 3
puntos[g_bingo] += 3
puntos[g_memo] += 2
puntos[g_tictac] += 3
puntos[g_mimica] += 3
puntos[g_nota] += 5

# Botón para procesar el corte de Fase 1
if st.button("📊 Calcular Corte de Fase 1 (Top 8)"):
    # Ordenamos a los jugadores por los puntos acumulados en las predicciones
    tabla_fase1 = sorted(puntos.items(), key=lambda x: x[1], reverse=True)
    top_8 = [j[0] for j in tabla_fase1[:8]]
    
    st.success("¡Corte realizado con éxito!")
    st.write("### 🏅 Top 8 Clasificados a Fase 2:")
    for i, (jugador, pts) in enumerate(tabla_fase1[:8], 1):
        st.write(f"**{i}º** - {jugador} ({pts} pts)")
        
    # Guardamos los 8 mejores en la sesión de Streamlit para usarlos después
    st.session_state["top_8"] = top_8
    st.session_state["puntos_fase1"] = tabla_fase1

# ==========================================
# FASE 2 Y FINALES (Solo si ya se calculó el Top 8)
# ==========================================
if "top_8" in st.session_state:
    top_8 = st.session_state["top_8"]
    
    st.markdown("---")
    st.header("2️⃣ Fase 2 y Etapa Final")
    st.write("Selecciona los ganadores de los juegos de la Fase 2 (Tuttifrutti, Barquito, Juicio Matemático, UNO):")

    col3, col4 = st.columns(2)
    with col3:
        g_tutti = st.selectbox("Tuttifrutti (1º Lugar)", top_8, key="tutti")
        g_barquito = st.selectbox("Barquito (1º Lugar)", top_8, key="barquito")
    with col4:
        g_juicio = st.selectbox("Juicio Matemático (1º Lugar)", top_8, key="juicio")
        g_uno = st.selectbox("UNO (1º Lugar)", top_8, key="uno")

    # Copiamos puntos de fase 1 y sumamos fase 2
    puntos_f2 = {j: dict(st.session_state["puntos_fase1"])[j] for j in top_8}
    puntos_f2[g_tutti] += 3
    puntos_f2[g_barquito] += 3
    puntos_f2[g_juicio] += 5
    puntos_f2[g_uno] += 3

    # Ordenamos finalistas de Fase 2
    ranking_f2 = sorted(puntos_f2.items(), key=lambda x: x[1], reverse=True)
    
    finalista_directo = ranking_f2[0][0]
    semifinalistas_posibles = [j[0] for j in ranking_f2[1:5]]

    st.write(f"🌟 **Pase Directo a la Final (Mayor puntaje F2):** **{finalista_directo}**")
    
    st.markdown("### ⚔️ Semifinal: Liar's Bar (4 Jugadores)")
    st.write("De estos 4 semifinalistas, elige a los 2 que superan el juego:")
    
    # Selectores múltiples para la semifinal
    clasificados_liars = st.multiselect(
        "Selecciona exactamente a los 2 ganadores de Liar's Bar:",
        semifinalistas_posibles,
        max_selections=2
    )

    if len(clasificados_liars) == 2:
        st.markdown("---")
        st.header("3️⃣ 🏆 Gran Final: Pasapalabra")
        
        participantes_final = [finalista_directo] + clasificados_liars
        st.write(f"Los 3 finalistas absolutos son: **{', '.join(participantes_final)}**")
        
        campeon = st.selectbox("¿Quién gana Pasapalabra y se consagra Campeón?", participantes_final)
        
        if st.button("🎉 ¡Enviar mi Predicción y Ver Resultado!"):
            st.balloons()
            st.success(f"¡Predicción guardada! Apuestas a que **{campeon}** gana todo el torneo.")
            st.info("¡Copia la URL de esta página de tu navegador y compártela en las historias de Instagram para que tus amigos armen la suya!")
