import streamlit as st

st.set_page_config(page_title="Predicciones Capi Games", page_icon="🏆", layout="centered")

st.title("🏆 Predicciones Oficiales - Capi Games")
st.markdown("¡Arma tu pronóstico paso a paso!")

jugadores = [
    "Naza", "Santy", "Enzo", "Raúl", "Amu", "Gabriel", "Torres", "Gahel", 
    "Santino", "Joa", "Mariano", "Victoria", "Mía", "Agustín", "Juan", "Mora"
]

# Función para verificar si hay nombres repetidos en una lista de opciones
def hay_repetidos(*args):
    # Filtramos valores vacíos si los hubiera y comparamos el tamaño con un conjunto (set)
    elementos = [arg for arg in args if arg]
    return len(elementos) != len(set(elementos))

# Inicializamos el sistema de puntos y el control de pasos en la sesión de Streamlit
if "puntos" not in st.session_state:
    st.session_state["puntos"] = {j: 0 for j in jugadores}
if "paso" not in st.session_state:
    st.session_state["paso"] = 1

puntos = st.session_state["puntos"]

# ==========================================
# PASO 1: CAPI DICE Y BINGO
# ==========================================
if st.session_state["paso"] == 1:
    st.header("1️⃣ Fase Regular: Capi Dice y Bingo")
    
    st.subheader("Juego 1: Capi Dice")
    c_1 = st.selectbox("1º Lugar (+3 pts)", jugadores, key="c1")
    c_2 = st.selectbox("2º Lugar (+2 pts)", jugadores, key="c2")
    c_3 = st.selectbox("3º Lugar (+1 pt)", jugadores, key="c3")
    
    st.subheader("Juego 2: Bingo (¡3 ganadores de 3 pts!)")
    b_1 = st.selectbox("1º Ganador Bingo (+3 pts)", jugadores, key="b1")
    b_2 = st.selectbox("2º Ganador Bingo (+3 pts)", jugadores, key="b2")
    b_3 = st.selectbox("3º Ganador Bingo (+3 pts)", jugadores, key="b3")

    if st.button("Siguiente ➡️"):
        puntos[c_1] += 3; puntos[c_2] += 2; puntos[c_3] += 1
        puntos[b_1] += 3; puntos[b_2] += 3; puntos[b_3] += 3
        st.session_state["paso"] = 2
        st.rerun()

# ==========================================
# PASO 2: DUELOS 2VS2 (4 JUEGOS Y CRUCES)
# ==========================================
elif st.session_state["paso"] == 2:
    st.header("2️⃣ Fase Regular: Duelos 2vs2")
    st.markdown("Selecciona los ganadores de la 1ª ronda de cada juego:")
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        g_jenga = st.selectbox("Ganador Jenga", jugadores, key="gj")
        g_memo = st.selectbox("Ganador Memotest", jugadores, key="gm")
        g_qeq = st.selectbox("Ganador ¿Quién es Quién?", jugadores, key="gq")
        g_c4 = st.selectbox("Ganador Conecta 4", jugadores, key="gc4")
    with col_d2:
        p_jenga = st.selectbox("Perdedor Jenga", jugadores, key="pj")
        p_memo = st.selectbox("Perdedor Memotest", jugadores, key="pm")
        p_qeq = st.selectbox("Perdedor ¿Quién es Quién?", jugadores, key="pq")
        p_c4 = st.selectbox("Perdedor Conecta 4", jugadores, key="pc4")

    st.markdown("---")
    st.markdown("### 🔄 2ª Ronda de Duelos (Cruces)")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("**Jenga:** Ganador QEQ vs Ganador Memo")
        r_jenga = st.selectbox("Ganador de este cruce de Jenga", [g_qeq, g_memo], key="rj")
        
        st.markdown("**Conecta 4:** Perdedor QEQ vs Perdedor Memo")
        r_c4 = st.selectbox("Ganador de este cruce de Conecta 4", [p_qeq, p_memo], key="rc4")
    with col_c2:
        st.markdown("**Memotest:** Ganador Jenga vs Ganador C4")
        r_memo = st.selectbox("Ganador de este cruce de Memotest", [g_jenga, g_c4], key="rm")
        
        st.markdown("**¿Quién es Quién?:** Perdedor Jenga vs Perdedor C4")
        r_qeq = st.selectbox("Ganador de este cruce de QEQ", [p_jenga, p_c4], key="rq")

    if st.button("Siguiente ➡️"):
        # Otorgamos puntos por los cruces ganados en la ronda 2
        for ganador_cruce in [r_jenga, r_c4, r_memo, r_qeq]:
            if ganador_cruce: puntos[ganador_cruce] += 3
        st.session_state["paso"] = 3
        st.rerun()

# ==========================================
# PASO 3: TIC TAC Y DÍGALO CON MÍMICA
# ==========================================
elif st.session_state["paso"] == 3:
    st.header("3️⃣ Fase Regular: Tic Tac y Mímica")
    
    st.subheader("Juego 4: Tic Tac")
    tt_1 = st.selectbox("1º Lugar Tic Tac (+3 pts)", jugadores, key="tt1")
    tt_2 = st.selectbox("2º Lugar Tic Tac (+2 pts)", jugadores, key="tt2")
    tt_3 = st.selectbox("3º Lugar Tic Tac (+1 pt)", jugadores, key="tt3")
    
    st.subheader("Juego 5: Dígalo con Mímica (Equipos de 4)")
    st.write("Selecciona los integrantes de cada podio:")
    eq_1 = st.multiselect("Equipo 1º Puesto (+3 pts c/u):", jugadores, key="eq1")
    eq_2 = st.multiselect("Equipo 2º Puesto (+2 pts c/u):", jugadores, key="eq2")
    eq_3 = st.multiselect("Equipo 3º Puesto (+1 pt c/u):", jugadores, key="eq3")

    if st.button("Siguiente ➡️"):
        puntos[tt_1] += 3; puntos[tt_2] += 2; puntos[tt_3] += 1
        for m in eq_1: puntos[m] += 3
        for m in eq_2: puntos[m] += 2
        for m in eq_3: puntos[m] += 1
        st.session_state["paso"] = 4
        st.rerun()

# ==========================================
# PASO 4: EN UNA NOTA Y CORTE DE FASE 1
# ==========================================
elif st.session_state["paso"] == 4:
    st.header("4️⃣ Fase Regular: En Una Nota & Corte Top 8")
    
    st.subheader("Juego 6: En Una Nota (Top 5)")
    n_1 = st.selectbox("1º Lugar (+5 pts)", jugadores, key="n1")
    n_2 = st.selectbox("2º Lugar (+4 pts)", jugadores, key="n2")
    n_3 = st.selectbox("3º Lugar (+3 pts)", jugadores, key="n3")
    n_4 = st.selectbox("4º Lugar (+2 pts)", jugadores, key="n4")
    n_5 = st.selectbox("5º Lugar (+1 pt)", jugadores, key="n5")

    if st.button("📊 Calcular Top 8 y Avanzar a Fase 2"):
        puntos[n_1] += 5; puntos[n_2] += 4; puntos[n_3] += 3; puntos[n_4] += 2; puntos[n_5] += 1
        
        tabla_f1 = sorted(puntos.items(), key=lambda x: x[1], reverse=True)
        top_8 = [j[0] for j in tabla_f1[:8]]
        st.session_state["top_8"] = top_8
        st.session_state["puntos_f1"] = tabla_f1
        
        st.session_state["paso"] = 5
        st.rerun()

# ==========================================
# PASO 5: FASE 2 (TUTTIFRUTTI, BARQUITO, JUICIO, UNO)
# ==========================================
elif st.session_state["paso"] == 5:
    top_8 = st.session_state["top_8"]
    st.header("5️⃣ Fase 2: Juegos Decisivos")
    st.write("Selecciona los podios del Top 8:")

    st.subheader("Tuttifrutti (3 al 1º, 2 al 2º, 1 al 3º)")
    tf_1 = st.selectbox("1º Tuttifrutti", top_8, key="tf1")
    tf_2 = st.selectbox("2º Tuttifrutti", top_8, key="tf2")
    tf_3 = st.selectbox("3º Tuttifrutti", top_8, key="tf3")

    st.subheader("Barquito (3 al 1º, 2 al 2º, 1 al 3º)")
    bar_1 = st.selectbox("1º Barquito", top_8, key="bar1")
    bar_2 = st.selectbox("2º Barquito", top_8, key="bar2")
    bar_3 = st.selectbox("3º Barquito", top_8, key="bar3")

    st.subheader("Juicio Matemático (Top 5: 5, 4, 3, 2, 1 pts)")
    jm_1 = st.selectbox("1º Juicio Matemático", top_8, key="jm1")
    jm_2 = st.selectbox("2º Juicio Matemático", top_8, key="jm2")
    jm_3 = st.selectbox("3º Juicio Matemático", top_8, key="jm3")
    jm_4 = st.selectbox("4º Juicio Matemático", top_8, key="jm4")
    jm_5 = st.selectbox("5º Juicio Matemático", top_8, key="jm5")

    st.subheader("UNO - Juego 10 (3 al 1º, 2 al 2º, 1 al 3º)")
    u_1 = st.selectbox("1º UNO", top_8, key="u1")
    u_2 = st.selectbox("2º UNO", top_8, key="u2")
    u_3 = st.selectbox("3º UNO", top_8, key="u3")

    if st.button("⚔️ Ver Clasificados a Semifinales y Final"):
        # Sumamos puntos Fase 2
        puntos_f2 = {j: dict(st.session_state["puntos_f1"])[j] for j in top_8}
        puntos_f2[tf_1] += 3; puntos_f2[tf_2] += 2; puntos_f2[tf_3] += 1
        puntos_f2[bar_1] += 3; puntos_f2[bar_2] += 2; puntos_f2[bar_3] += 1
        puntos_f2[jm_1] += 5; puntos_f2[jm_2] += 4; puntos_f2[jm_3] += 3; puntos_f2[jm_4] += 2; puntos_f2[jm_5] += 1
        puntos_f2[u_1] += 3; puntos_f2[u_2] += 2; puntos_f2[u_3] += 1

        ranking_f2 = sorted(puntos_f2.items(), key=lambda x: x[1], reverse=True)
        st.session_state["finalista_directo"] = ranking_f2[0][0]
        st.session_state["semifinalistas"] = [j[0] for j in ranking_f2[1:5]]
        
        st.session_state["paso"] = 6
        st.rerun()

# ==========================================
# PASO 6: SEMIFINAL (LIAR'S BAR) Y GRAN FINAL (PASAPALABRA)
# ==========================================
elif st.session_state["paso"] == 6:
    finalista_directo = st.session_state["finalista_directo"]
    semifinalistas = st.session_state["semifinalistas"]

    st.header("6️⃣ Etapa Final: Semifinal & Gran Final")
    st.markdown(f"🌟 **Pase directo a la Final:** **{finalista_directo}**")
    
    st.subheader("⚔️ Semifinal: Liar's Bar")
    st.write(f"Candidatos: {', '.join(semifinalistas)}")
    clasificados_liars = st.multiselect("Selecciona a los 2 que pasan a la final:", semifinalistas, max_selections=2)

    if len(clasificados_liars) == 2:
        st.markdown("---")
        st.subheader("🏆 Gran Final: Pasapalabra")
        participantes_final = [finalista_directo] + clasificados_liars
        st.write(f"Finalistas: **{', '.join(participantes_final)}**")
        
        campeon = st.selectbox("¿Quién se consagra Campeón Absoluto?", participantes_final)

        if st.button("🎉 ¡Guardar Pronóstico y Ver Resultado Final!"):
            st.balloons()
            st.success(f"¡Listo! Tu predicción indica que **{campeon}** gana el torneo.")
            if st.button("🔄 Reiniciar y armar otra predicción"):
                st.session_state["paso"] = 1
                st.session_state["puntos"] = {j: 0 for j in jugadores}
                st.rerun()
