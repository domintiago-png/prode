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
        # Validamos usando la función que creamos arriba
        if hay_repetidos(c_1, c_2, c_3):
            st.warning("⚠️ No puedes repetir jugadores en el podio de Capi Dice.")
        elif hay_repetidos(b_1, b_2, b_3):
            st.warning("⚠️ No puedes repetir jugadores en los ganadores de Bingo.")
        else:
            puntos[c_1] += 3
            puntos[c_2] += 2
            puntos[c_3] += 1
            puntos[b_1] += 3
            puntos[b_2] += 3
            puntos[b_3] += 3
            st.session_state["paso"] = 2
            st.rerun()

# ==========================================
# PASO 2: DUELOS 2VS2 (8 PAREJAS / 4 ENFRENTAMIENTOS)
# ==========================================
elif st.session_state["paso"] == 2:
    st.header("2️⃣ Fase Regular: Duelos 2vs2")
    st.markdown("Arma los 4 enfrentamientos (Pareja A vs Pareja B) para cada juego. (¡Asegúrate de usar a los 16 jugadores sin repetir!):")

    # --- JENGA ---
    st.subheader("🪵 Jenga")
    col_j1, col_j2 = st.columns(2)
    with col_j1:
        jenga_p1 = st.multiselect("Pareja 1 (Jenga)", jugadores, max_selections=2, key="j_p1")
    with col_j2:
        jenga_p2 = st.multiselect("Pareja 2 (Jenga)", jugadores, max_selections=2, key="j_p2")

    # --- MEMOTEST ---
    st.subheader("🧠 Memotest")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        memo_p1 = st.multiselect("Pareja 1 (Memotest)", jugadores, max_selections=2, key="m_p1")
    with col_m2:
        memo_p2 = st.multiselect("Pareja 2 (Memotest)", jugadores, max_selections=2, key="m_p2")

    # --- ¿QUIÉN ES QUIÉN? ---
    st.subheader("🕵️ ¿Quién es Quién?")
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        qeq_p1 = st.multiselect("Pareja 1 (QEQ)", jugadores, max_selections=2, key="q_p1")
    with col_q2:
        qeq_p2 = st.multiselect("Pareja 2 (QEQ)", jugadores, max_selections=2, key="q_p2")

    # --- CONECTA 4 ---
    st.subheader("🔴 Conecta 4")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        c4_p1 = st.multiselect("Pareja 1 (Conecta 4)", jugadores, max_selections=2, key="c_p1")
    with col_c2:
        c4_p2 = st.multiselect("Pareja 2 (Conecta 4)", jugadores, max_selections=2, key="c_p2")

    st.markdown("---")

    # Validamos que todas las parejas tengan exactamente 2 integrantes
    parejas_completas = (
        len(jenga_p1) == 2 and len(jenga_p2) == 2 and
        len(memo_p1) == 2 and len(memo_p2) == 2 and
        len(qeq_p1) == 2 and len(qeq_p2) == 2 and
        len(c4_p1) == 2 and len(c4_p2) == 2
    )

    if parejas_completas:
        # Validar que no se repita ninguna persona en distintas parejas
        todas_las_parejas = jenga_p1 + jenga_p2 + memo_p1 + memo_p2 + qeq_p1 + qeq_p2 + c4_p1 + c4_p2
        
        if len(todas_las_parejas) != len(set(todas_las_parejas)):
            st.warning("⚠️ Hay jugadores repetidos entre los enfrentamientos. Cada jugador debe pertenecer a una sola pareja en toda la fase.")
        else:
            st.markdown("### 🏆 Paso 2: Selecciona las 4 parejas ganadoras de la 1ª Ronda")
            
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                ganador_jenga = st.selectbox("Ganador Jenga", ["Pareja 1", "Pareja 2"], format_func=lambda x: f"{jenga_p1[0]} & {jenga_p1[1]}" if x == "Pareja 1" else f"{jenga_p2[0]} & {jenga_p2[1]}", key="gj_select")
                ganador_memo = st.selectbox("Ganador Memotest", ["Pareja 1", "Pareja 2"], format_func=lambda x: f"{memo_p1[0]} & {memo_p1[1]}" if x == "Pareja 1" else f"{memo_p2[0]} & {memo_p2[1]}", key="gm_select")
            with col_g2:
                ganador_qeq = st.selectbox("Ganador ¿Quién es Quién?", ["Pareja 1", "Pareja 2"], format_func=lambda x: f"{qeq_p1[0]} & {qeq_p1[1]}" if x == "Pareja 1" else f"{qeq_p2[0]} & {qeq_p2[1]}", key="gq_select")
                ganador_c4 = st.selectbox("Ganador Conecta 4", ["Pareja 1", "Pareja 2"], format_func=lambda x: f"{c4_p1[0]} & {c4_p1[1]}" if x == "Pareja 1" else f"{c4_p2[0]} & {c4_p2[1]}", key="gc4_select")

            # Definir ganadores y perdedores individuales para los cruces de la Ronda 2
            g_jenga_pareja = jenga_p1 if ganador_jenga == "Pareja 1" else jenga_p2
            p_jenga_pareja = jenga_p2 if ganador_jenga == "Pareja 1" else jenga_p1

            g_memo_pareja = memo_p1 if ganador_memo == "Pareja 1" else memo_p2
            p_memo_pareja = memo_p2 if ganador_memo == "Pareja 1" else memo_p1

            g_qeq_pareja = qeq_p1 if ganador_qeq == "Pareja 1" else qeq_p2
            p_qeq_pareja = qeq_p2 if ganador_qeq == "Pareja 1" else qeq_p1

            g_c4_pareja = c4_p1 if ganador_c4 == "Pareja 1" else c4_p2
            p_c4_pareja = c4_p2 if ganador_c4 == "Pareja 1" else c4_p1

            st.markdown("---")
            st.markdown("### 🔄 2ª Ronda de Duelos (Cruces individuales o entre ganadores/perdedores)")
            st.markdown("Elige a un representante o ganador de cada cruce de la Ronda 2:")

            col_c1, col_c2 = st.columns(2)
            with col_c1:
                st.markdown("**Jenga:** Ganador QEQ vs Ganador Memotest")
                opciones_j = g_qeq_pareja + g_memo_pareja
                r_jenga = st.selectbox("¿Quién avanza/gana?", opciones_j, key="rj")
                
                st.markdown("**Conecta 4:** Perdedor QEQ vs Perdedor Memotest")
                opciones_c4 = p_qeq_pareja + p_memo_pareja
                r_c4 = st.selectbox("¿Quién avanza/gana?", opciones_c4, key="rc4")
            with col_c2:
                st.markdown("**Memotest:** Ganador Jenga vs Ganador Conecta 4")
                opciones_m = g_jenga_pareja + g_c4_pareja
                r_memo = st.selectbox("¿Quién avanza/gana?", opciones_m, key="rm")
                
                st.markdown("**¿Quién es Quién?:** Perdedor Jenga vs Perdedor Conecta 4")
                opciones_q = p_jenga_pareja + p_c4_pareja
                r_qeq = st.selectbox("¿Quién avanza/gana?", opciones_q, key="rq")

            if st.button("Siguiente ➡️"):
                # Otorgamos puntos por los cruces ganados en la ronda 2
                for ganador_cruce in [r_jenga, r_c4, r_memo, r_qeq]:
                    if ganador_cruce: puntos[ganador_cruce] += 3
                st.session_state["paso"] = 3
                st.rerun()
    else:
        st.info("ℹ️ Completa exactamente 2 integrantes en cada una de las 8 parejas para desbloquear las selecciones de ganadores y la Ronda 2.")

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
    st.write("Selecciona los integrantes de cada podio (no repitas personas entre equipos):")
    eq_1 = st.multiselect("Equipo 1º Puesto (+3 pts c/u):", jugadores, key="eq1")
    eq_2 = st.multiselect("Equipo 2º Puesto (+2 pts c/u):", jugadores, key="eq2")
    eq_3 = st.multiselect("Equipo 3º Puesto (+1 pt c/u):", jugadores, key="eq3")

    if st.button("Siguiente ➡️"):
        todos_mimica = eq_1 + eq_2 + eq_3
        if hay_repetidos(tt_1, tt_2, tt_3):
            st.warning("⚠️ No puedes repetir jugadores en el podio de Tic Tac.")
        elif len(todos_mimica) != len(set(todos_mimica)):
            st.warning("⚠️ Un jugador no puede estar en dos equipos distintos de Mímica a la vez.")
        else:
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
        if hay_repetidos(n_1, n_2, n_3, n_4, n_5):
            st.warning("⚠️ No puedes repetir jugadores en el Top 5 de En Una Nota.")
        else:
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
        if hay_repetidos(tf_1, tf_2, tf_3) or hay_repetidos(bar_1, bar_2, bar_3) or hay_repetidos(jm_1, jm_2, jm_3, jm_4, jm_5) or hay_repetidos(u_1, u_2, u_3):
            st.warning("⚠️ Hay jugadores repetidos en los podios de la Fase 2. Revisa las selecciones.")
        else:
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
            
    # Botón de reinicio fuera del botón de guardar para que funcione bien
    st.markdown("---")
    if st.button("🔄 Reiniciar y armar otra predicción"):
        st.session_state["paso"] = 1
        st.session_state["puntos"] = {j: 0 for j in jugadores}
        st.rerun()
