import streamlit as st

st.set_page_config(page_title="Predicciones Capi Games", page_icon="🏆", layout="centered")

st.title("🏆 Predicciones Oficiales - Capi Games")
st.markdown("Arma tu pronóstico completo: define equipos, podios por juego, descubre quiénes llegan a la final y elige al campeón.")

jugadores = [
    "Naza", "Santy", "Enzo", "Raúl", "Amu", "Gabriel", "Torres", "Gahel", 
    "Santino", "Joa", "Mariano", "Victoria", "Mía", "Agustín", "Juan", "Mora"
]

puntos = {j: 0 for j in jugadores}

# ==========================================
# FASE 1: FASE REGULAR (JUEGOS 1 AL 6)
# ==========================================
st.header("1️⃣ Fase Regular (Acumulación de Puntos)")

# --- JUEGO 1: CAPI DICE ---
st.subheader("1. Capi Dice")
c_1 = st.selectbox("1º Lugar (+3 pts)", jugadores, key="cd_1")
c_2 = st.selectbox("2º Lugar (+2 pts)", jugadores, key="cd_2")
c_3 = st.selectbox("3º Lugar (+1 pt)", jugadores, key="cd_3")
puntos[c_1] += 3
puntos[c_2] += 2
puntos[c_3] += 1

# --- JUEGO 2: BINGO ---
st.subheader("2. Bingo")
b_1 = st.selectbox("1º Lugar / 1ª Línea (+3 pts)", jugadores, key="bg_1")
b_2 = st.selectbox("2º Lugar (+2 pts)", jugadores, key="bg_2")
b_3 = st.selectbox("3º Lugar (+1 pt)", jugadores, key="bg_3")
puntos[b_1] += 3
puntos[b_2] += 2
puntos[b_3] += 1

# --- JUEGO 3: DUELOS 2VS2 (Armado de equipos) ---
st.subheader("3. Duelos 2vs2 (Memotest / Juegos de Dos)")
st.write("Arma la pareja ganadora:")
col_d1, col_d2 = st.columns(2)
with col_d1:
    duelo_p1 = st.selectbox("Jugador 1 del equipo ganador", jugadores, key="dp1")
with col_d2:
    duelo_p2 = st.selectbox("Jugador 2 del equipo ganador", jugadores, key="dp2")
# Otorgamos puntos a ambos integrantes si se seleccionan distintos
if duelo_p1 and duelo_p2:
    puntos[duelo_p1] += 2
    puntos[duelo_p2] += 2

# --- JUEGO 4: TIC TAC ---
st.subheader("4. Tic Tac")
t_1 = st.selectbox("1º Lugar Tic Tac (+3 pts)", jugadores, key="tt_1")
t_2 = st.selectbox("2º Lugar Tic Tac (+2 pts)", jugadores, key="tt_2")
puntos[t_1] += 3
puntos[t_2] += 2

# --- JUEGO 5: DÍGALO CON MÍMICA (Equipos) ---
st.subheader("5. Dígalo con Mímica (Equipos de 3 o 4)")
st.write("Selecciona a los integrantes del equipo ganador:")
mimica_equipo = st.multiselect("Integrantes del equipo ganador de Mímica (+3 pts c/u):", jugadores, key="mimica_eq")
for miembro in mimica_equipo:
    puntos[miembro] += 3

# --- JUEGO 6: EN UNA NOTA ---
st.subheader("6. En Una Nota (Top 5)")
n_1 = st.selectbox("1º Lugar (+5 pts)", jugadores, key="nota_1")
n_2 = st.selectbox("2º Lugar (+4 pts)", jugadores, key="nota_2")
n_3 = st.selectbox("3º Lugar (+3 pts)", jugadores, key="nota_3")
n_4 = st.selectbox("4º Lugar (+2 pts)", jugadores, key="nota_4")
n_5 = st.selectbox("5º Lugar (+1 pt)", jugadores, key="nota_5")
puntos[n_1] += 5
puntos[n_2] += 4
puntos[n_3] += 3
puntos[n_4] += 2
puntos[n_5] += 1

st.markdown("---")

# Botón para procesar el corte de Fase 1
if st.button("📊 Calcular Corte de Fase 1 (Top 8)"):
    tabla_fase1 = sorted(puntos.items(), key=lambda x: x[1], reverse=True)
    top_8 = [j[0] for j in tabla_fase1[:8]]
    
    st.success("¡Corte realizado con éxito!")
    st.write("### 🏅 Top 8 Clasificados a Fase 2:")
    for i, (jugador, pts) in enumerate(tabla_fase1[:8], 1):
        st.write(f"**{i}º** - {jugador} ({pts} pts)")
        
    st.session_state["top_8"] = top_8
    st.session_state["puntos_fase1"] = tabla_fase1

# ==========================================
# FASE 2 Y FINALES
# ==========================================
if "top_8" in st.session_state:
    top_8 = st.session_state["top_8"]
    
    st.markdown("---")
    st.header("2️⃣ Fase 2 y Etapa Final (Top 8)")
    st.write("Define los podios para los juegos de la Fase 2:")

    col3, col4 = st.columns(2)
    with col3:
        st.write("**Tuttifrutti**")
        tf_1 = st.selectbox("1º Tutti (+3)", top_8, key="tf1")
        tf_2 = st.selectbox("2º Tutti (+2)", top_8, key="tf2")
        
        st.write("**Barquito**")
        bar_1 = st.selectbox("1º Barquito (+3)", top_8, key="bar1")
        bar_2 = st.selectbox("2º Barquito (+2)", top_8, key="bar2")
    with col4:
        st.write("**Juicio Matemático**")
        jm_1 = st.selectbox("1º Juicio (+5)", top_8, key="jm1")
        jm_2 = st.selectbox("2º Juicio (+3)", top_8, key="jm2")
        
        st.write("**UNO (Juego 10)**")
        uno_1 = st.selectbox("1º UNO (+3)", top_8, key="u1")
        uno_2 = st.selectbox("2º UNO (+2)", top_8, key="u2")

    # Copiamos puntos de fase 1 y sumamos fase 2 con podios
    puntos_f2 = {j: dict(st.session_state["puntos_fase1"])[j] for j in top_8}
    puntos_f2[tf_1] += 3; puntos_f2[tf_2] += 2
    puntos_f2[bar_1] += 3; puntos_f2[bar_2] += 2
    puntos_f2[jm_1] += 5; puntos_f2[jm_2] += 3
    puntos_f2[uno_1] += 3; puntos_f2[uno_2] += 2

    # Ordenamos finalistas de Fase 2
    ranking_f2 = sorted(puntos_f2.items(), key=lambda x: x[1], reverse=True)
    
    finalista_directo = ranking_f2[0][0]
    semifinalistas_posibles = [j[0] for j in ranking_f2[1:5]]

    st.write(f"🌟 **Pase Directo a la Final:** **{finalista_directo}** ({ranking_f2[0][1]} pts)")
    
    st.markdown("### ⚔️ Semifinal: Liar's Bar (4 Jugadores)")
    st.write(f"Candidatos: {', '.join(semifinalistas_posibles)}")
    
    clasificados_liars = st.multiselect(
        "Selecciona a los 2 que ganan la semifinal de Liar's Bar:",
        semifinalistas_posibles,
        max_selections=2
    )

    if len(clasificados_liars) == 2:
        st.markdown("---")
        st.header("3️⃣ 🏆 Gran Final: Pasapalabra")
        
        participantes_final = [finalista_directo] + clasificados_liars
        st.write(f"Los 3 finalistas absolutos son: **{', '.join(participantes_final)}**")
        
        campeon = st.selectbox("¿Quién gana Pasapalabra y se consagra Campeón?", participantes_final)
        
        if st.button("🎉 ¡Enviar mi Predicción y Ver Resultado Final!"):
            st.balloons()
            st.success(f"¡Predicción guardada con éxito! Apuestas a que **{campeon}** levanta el trofeo.")
