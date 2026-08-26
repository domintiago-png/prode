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
    elementos = [arg for arg in args if arg]
    return len(elementos) != len(set(elementos))

# Inicializamos el sistema de puntos y el control de pasos en la sesión de Streamlit
if "puntos" not in st.session_state:
    st.session_state["puntos"] = {j: 0 for j in jugadores}
if "paso" not in st.session_state:
    st.session_state["paso"] = 1

puntos = st.session_state["puntos"]

# ==========================================
# PASO 1: CAPI DICE
# ==========================================
if st.session_state["paso"] == 1:
    st.header("1️⃣ Fase Regular: Capi Dice")
    
    c_1 = st.selectbox("1º Lugar (+3 pts)", [None] + jugadores, key="c1")
    c_2 = st.selectbox("2º Lugar (+2 pts)", [None] + jugadores, key="c2")
    c_3 = st.selectbox("3º Lugar (+1 pt)", [None] + jugadores, key="c3")

    if st.button("Siguiente ➡️"):
        if not c_1 or not c_2 or not c_3:
            st.warning("⚠️ Por favor completa todos los puestos.")
        elif hay_repetidos(c_1, c_2, c_3):
            st.warning("⚠️ No puedes repetir jugadores en el podio.")
        else:
            puntos[c_1] += 3
            puntos[c_2] += 2
            puntos[c_3] += 1
            st.session_state["paso"] = 2
            st.rerun()

# ==========================================
# PASO 2: BINGO
# ==========================================
elif st.session_state["paso"] == 2:
    st.header("2️⃣ Fase Regular: Bingo")
    
    b_1 = st.selectbox("1º Ganador Bingo (+3 pts)", [None] + jugadores, key="b1")
    b_2 = st.selectbox("2º Ganador Bingo (+3 pts)", [None] + jugadores, key="b2")
    b_3 = st.selectbox("3º Ganador Bingo (+3 pts)", [None] + jugadores, key="b3")

    if st.button("Siguiente ➡️"):
        if not b_1 or not b_2 or not b_3:
            st.warning("⚠️ Por favor completa todos los ganadores.")
        elif hay_repetidos(b_1, b_2, b_3):
            st.warning("⚠️ No puedes repetir jugadores en Bingo.")
        else:
            puntos[b_1] += 3
            puntos[b_2] += 3
            puntos[b_3] += 3
            st.session_state["paso"] = 3
            st.rerun()

# ==========================================
# PASO 3: DUELOS 2VS2 (8 PAREJAS / 2 RONDAS CON FILTRADO BIDIRECCIONAL)
# ==========================================
elif st.session_state["paso"] == 3:
    st.header("3️⃣ Fase Regular: Duelos 2vs2")
    st.markdown("Arma los 4 enfrentamientos (Pareja A vs Pareja B) para cada juego. (Los jugadores seleccionados en cualquier campo se bloquean automáticamente en los demás):")

    # Recolectamos todas las selecciones actuales para filtrar dinámicamente
    j_p1 = st.multiselect("Pareja 1 (Jenga)", jugadores, max_selections=2, key="j_p1")
    j_p2 = st.multiselect("Pareja 2 (Jenga)", [j for j in jugadores if j not in j_p1], max_selections=2, key="j_p2")
    
    usados_jenga = j_p1 + j_p2
    memo_p1 = st.multiselect("Pareja 1 (Memotest)", [j for j in jugadores if j not in usados_jenga], max_selections=2, key="m_p1")
    usados_memo1 = usados_jenga + memo_p1
    memo_p2 = st.multiselect("Pareja 2 (Memotest)", [j for j in jugadores if j not in usados_memo1], max_selections=2, key="m_p2")
    
    usados_memo = usados_memo1 + memo_p2
    qeq_p1 = st.multiselect("Pareja 1 (¿Quién es Quién?)", [j for j in jugadores if j not in usados_memo], max_selections=2, key="q_p1")
    usados_qeq1 = usados_memo + qeq_p1
    qeq_p2 = st.multiselect("Pareja 2 (¿Quién es Quién?)", [j for j in jugadores if j not in usados_qeq1], max_selections=2, key="q_p2")
    
    usados_qeq = usados_qeq1 + qeq_p2
    c4_p1 = st.multiselect("Pareja 1 (Conecta 4)", [j for j in jugadores if j not in usados_qeq], max_selections=2, key="c_p1")
    usados_c41 = usados_qeq + c4_p1
    c4_p2 = st.multiselect("Pareja 2 (Conecta 4)", [j for j in jugadores if j not in usados_c41], max_selections=2, key="c_p2")

    st.markdown("---")

    parejas_completas = (
        len(j_p1) == 2 and len(j_p2) == 2 and
        len(memo_p1) == 2 and len(memo_p2) == 2 and
        len(qeq_p1) == 2 and len(qeq_p2) == 2 and
        len(c4_p1) == 2 and len(c4_p2) == 2
    )

    if parejas_completas:
        st.markdown("### 🏆 Ronda 1: Selecciona las 4 parejas ganadoras")
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            ganador_jenga = st.selectbox("Ganador Jenga", ["Pareja 1", "Pareja 2"], format_func=lambda x: f"{j_p1[0]} & {j_p1[1]}" if x == "Pareja 1" else f"{j_p2[0]} & {j_p2[1]}", key="gj_select")
            ganador_memo = st.selectbox("Ganador Memotest", ["Pareja 1", "Pareja 2"], format_func=lambda x: f"{memo_p1[0]} & {memo_p1[1]}" if x == "Pareja 1" else f"{memo_p2[0]} & {memo_p2[1]}", key="gm_select")
        with col_g2:
            ganador_qeq = st.selectbox("Ganador ¿Quién es Quién?", ["Pareja 1", "Pareja 2"], format_func=lambda x: f"{qeq_p1[0]} & {qeq_p1[1]}" if x == "Pareja 1" else f"{qeq_p2[0]} & {qeq_p2[1]}", key="gq_select")
            ganador_c4 = st.selectbox("Ganador Conecta 4", ["Pareja 1", "Pareja 2"], format_func=lambda x: f"{c4_p1[0]} & {c4_p1[1]}" if x == "Pareja 1" else f"{c4_p2[0]} & {c4_p2[1]}", key="gc4_select")

        g_jenga_pareja = j_p1 if ganador_jenga == "Pareja 1" else j_p2
        p_jenga_pareja = j_p2 if ganador_jenga == "Pareja 1" else j_p1

        g_memo_pareja = memo_p1 if ganador_memo == "Pareja 1" else memo_p2
        p_memo_pareja = memo_p2 if ganador_memo == "Pareja 1" else memo_p1

        g_qeq_pareja = qeq_p1 if ganador_qeq == "Pareja 1" else qeq_p2
        p_qeq_pareja = qeq_p2 if ganador_qeq == "Pareja 1" else qeq_p1

        g_c4_pareja = c4_p1 if ganador_c4 == "Pareja 1" else c4_p2
        p_c4_pareja = c4_p2 if ganador_c4 == "Pareja 1" else c4_p1

        st.markdown("---")
        st.markdown("### 🔄 Ronda 2: Cruces de 2vs2")

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("**Jenga:** Ganador QEQ vs Ganador Memotest")
            opciones_jenga_r2 = [f"{g_qeq_pareja[0]} & {g_qeq_pareja[1]}", f"{g_memo_pareja[0]} & {g_memo_pareja[1]}"]
            r_jenga_eleccion = st.selectbox("Ganador Jenga (R2)", opciones_jenga_r2, key="rj")
            r_jenga = g_qeq_pareja if r_jenga_eleccion == opciones_jenga_r2[0] else g_memo_pareja
            
            st.markdown("**Conecta 4:** Perdedor QEQ vs Perdedor Memotest")
            opciones_c4_r2 = [f"{p_qeq_pareja[0]} & {p_qeq_pareja[1]}", f"{p_memo_pareja[0]} & {p_memo_pareja[1]}"]
            r_c4_eleccion = st.selectbox("Ganador Conecta 4 (R2)", opciones_c4_r2, key="rc4")
            r_c4 = p_qeq_pareja if r_c4_eleccion == opciones_c4_r2[0] else p_memo_pareja

        with col_c2:
            st.markdown("**Memotest:** Ganador Jenga vs Ganador Conecta 4")
            opciones_memo_r2 = [f"{g_jenga_pareja[0]} & {g_jenga_pareja[1]}", f"{g_c4_pareja[0]} & {g_c4_pareja[1]}"]
            r_memo_eleccion = st.selectbox("Ganador Memotest (R2)", opciones_memo_r2, key="rm")
            r_memo = g_jenga_pareja if r_memo_eleccion == opciones_memo_r2[0] else g_c4_pareja
            
            st.markdown("**¿Quién es Quién?:** Perdedor Jenga vs Perdedor Conecta 4")
            opciones_qeq_r2 = [f"{p_jenga_pareja[0]} & {p_jenga_pareja[1]}", f"{p_c4_pareja[0]} & {p_c4_pareja[1]}"]
            r_qeq_eleccion = st.selectbox("Ganador QEQ (R2)", opciones_qeq_r2, key="rq")
            r_qeq = p_jenga_pareja if r_qeq_eleccion == opciones_qeq_r2[0] else p_c4_pareja

        if st.button("Siguiente ➡️"):
            # Sumamos puntos Ronda 1 (+2 a cada integrante)
            for pareja in [g_jenga_pareja, g_memo_pareja, g_qeq_pareja, g_c4_pareja]:
                for jugador in pareja:
                    puntos[jugador] += 2
            # Sumamos puntos Ronda 2 (+2 a cada integrante)
            for pareja in [r_jenga, r_c4, r_memo, r_qeq]:
                for jugador in pareja:
                    puntos[jugador] += 2
            
            st.session_state["paso"] = 4
            st.rerun()
    else:
        st.info("ℹ️ Asigna exactamente 2 integrantes distintos a cada una de las 8 parejas para continuar.")

# ==========================================
# PASO 4: TIC TAC
# ==========================================
elif st.session_state["paso"] == 4:
    st.header("4️⃣ Fase Regular: Tic Tac")
    
    tt_1 = st.selectbox("1º Lugar (+3 pts)", [None] + jugadores, key="tt1")
    tt_2 = st.selectbox("2º Lugar (+2 pts)", [None] + jugadores, key="tt2")
    tt_3 = st.selectbox("3º Lugar (+1 pt)", [None] + jugadores, key="tt3")

    if st.button("Siguiente ➡️"):
        if not tt_1 or not tt_2 or not tt_3:
            st.warning("⚠️ Completa los tres puestos.")
        elif hay_repetidos(tt_1, tt_2, tt_3):
            st.warning("⚠️ No puedes repetir jugadores en el podio.")
        else:
            puntos[tt_1] += 3; puntos[tt_2] += 2; puntos[tt_3] += 1
            st.session_state["paso"] = 5
            st.rerun()

# ==========================================
# PASO 5: DÍGALO CON MÍMICA
# ==========================================
elif st.session_state["paso"] == 5:
    st.header("5️⃣ Fase Regular: Dígalo con Mímica")
    
    # Verificamos si ya armaron los equipos o si estamos en la fase de podio
    if "mimica_fase_podio" not in st.session_state:
        st.session_state["mimica_fase_podio"] = False

    if not st.session_state["mimica_fase_podio"]:
        st.markdown("### 👥 Armado de Equipos (4 equipos de 4 jugadores)")
        
        eq_a = st.multiselect("Equipo A (Máx. 4 jugadores):", jugadores, max_selections=4, key="eq_a")
        
        disponibles_b = [j for j in jugadores if j not in eq_a]
        eq_b = st.multiselect("Equipo B (Máx. 4 jugadores):", disponibles_b, max_selections=4, key="eq_b")
        
        disponibles_c = [j for j in disponibles_b if j not in eq_b]
        eq_c = st.multiselect("Equipo C (Máx. 4 jugadores):", disponibles_c, max_selections=4, key="eq_c")
        
        disponibles_d = [j for j in disponibles_c if j not in eq_c]
        eq_d = st.multiselect("Equipo D (Máx. 4 jugadores):", disponibles_d, max_selections=4, key="eq_d")

        if st.button("Siguiente: Definir Podio ➡️"):
            if len(eq_a) != 4 or len(eq_b) != 4 or len(eq_c) != 4 or len(eq_d) != 4:
                st.warning("⚠️ Cada uno de los 4 equipos debe tener exactamente 4 jugadores.")
            else:
                # Guardamos los equipos en la sesión
                st.session_state["mimica_equipos"] = {
                    "Equipo A": eq_a,
                    "Equipo B": eq_b,
                    "Equipo C": eq_c,
                    "Equipo D": eq_d
                }
                st.session_state["mimica_fase_podio"] = True
                st.rerun()
    else:
        st.markdown("### 🏆 Resultados de Dígalo con Mímica")
        nombres_equipos = ["Equipo A", "Equipo B", "Equipo C", "Equipo D"]
        
        eq_1_podio = st.selectbox("1º Puesto (+3 pts c/u):", [None] + nombres_equipos, key="mimica_p1")
        
        opciones_p2 = [e for e in nombres_equipos if e != eq_1_podio]
        eq_2_podio = st.selectbox("2º Puesto (+2 pts c/u):", [None] + opciones_p2, key="mimica_p2")
        
        opciones_p3 = [e for e in opciones_p2 if e != eq_2_podio]
        eq_3_podio = st.selectbox("3º Puesto (+1 pt c/u):", [None] + opciones_p3, key="mimica_p3")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Volver a armar equipos"):
                st.session_state["mimica_fase_podio"] = False
                st.rerun()
        with col2:
            if st.button("Siguiente ➡️", key="btn_sig_mimica"):
                if not eq_1_podio or not eq_2_podio or not eq_3_podio:
                    st.warning("⚠️ Completa los puestos del podio.")
                else:
                    equipos = st.session_state["mimica_equipos"]
                    
                    # Sumamos puntos a los integrantes de cada equipo según su puesto
                    for m in equipos[eq_1_podio]: puntos[m] += 3
                    for m in equipos[eq_2_podio]: puntos[m] += 2
                    for m in equipos[eq_3_podio]: puntos[m] += 1
                    
                    # Limpiamos las variables temporales de mímica para la próxima
                    del st.session_state["mimica_fase_podio"]
                    del st.session_state["mimica_equipos"]
                    
                    st.session_state["paso"] = 6
                    st.rerun()

# ==========================================
# PASO 6: EN UNA NOTA Y CORTE DE FASE 1
# ==========================================
elif st.session_state["paso"] == 6:
    st.header("6️⃣ Fase Regular: En Una Nota")
    
    n_1 = st.selectbox("1º Lugar (+5 pts)", [None] + jugadores, key="n1")
    
    opciones_n2 = [j for j in jugadores if j != n_1]
    n_2 = st.selectbox("2º Lugar (+4 pts)", [None] + opciones_n2, key="n2")
    
    opciones_n3 = [j for j in opciones_n2 if j != n_2]
    n_3 = st.selectbox("3º Lugar (+3 pts)", [None] + opciones_n3, key="n3")
    
    opciones_n4 = [j for j in opciones_n3 if j != n_3]
    n_4 = st.selectbox("4º Lugar (+2 pts)", [None] + opciones_n4, key="n4")
    
    opciones_n5 = [j for j in opciones_n4 if j != n_4]
    n_5 = st.selectbox("5º Lugar (+1 pt)", [None] + opciones_n5, key="n5")

    if st.button("📊 Calcular Puntos y Ver Tabla de Fase 1"):
        if not n_1 or not n_2 or not n_3 or not n_4 or not n_5:
            st.warning("⚠️ Completa los 5 puestos.")
        else:
            puntos[n_1] += 5; puntos[n_2] += 4; puntos[n_3] += 3; puntos[n_4] += 2; puntos[n_5] += 1
            
            tabla_f1 = sorted(puntos.items(), key=lambda x: x[1], reverse=True)
            st.session_state["puntos_f1_temporal"] = tabla_f1
            st.session_state["mostrar_tabla_f1"] = True

    if st.session_state.get("mostrar_tabla_f1", False):
        st.markdown("---")
        st.subheader("📈 Tabla de Posiciones - Final Fase Regular")
        tabla = st.session_state["puntos_f1_temporal"]
        
        for i, (jugador, pts) in enumerate(tabla, 1):
            st.write(f"**{i}º** {jugador}: **{pts} pts**")
            
        octavo_puntaje = tabla[7][1]
        candidatos_corte = [j for j, p in tabla if p >= octavo_puntaje]
        clasificados_fijos = [j for j, p in tabla if p > octavo_puntaje][:7]
        empatados_octavo = [j for j, p in tabla if p == octavo_puntaje]
        
        st.markdown("---")
        if len(candidatos_corte) > 8:
            st.warning(f"⚠️ ¡Hay un empate en el corte del Top 8! Se necesitan definir los clasificados finales.")
            st.write(f"Jugadores ya clasificados de forma directa (Top 7): **{', '.join(clasificados_fijos)}**")
            st.write(f"Jugadores empatados peleando por los puestos restantes: **{', '.join(empatados_octavo)}**")
            
            vacantes = 8 - len(clasificados_fijos)
            elegidos_desempate = st.multiselect(f"Selecciona a los {vacantes} jugador(es) que avanzan por desempate:", empatados_octavo, max_selections=vacantes)
            
            if st.button("🚀 Confirmar Top 8 y Avanzar a Fase 2"):
                if len(elegidos_desempate) != vacantes:
                    st.error(f"Debes seleccionar exactamente {vacantes} jugador(es).")
                else:
                    top_8_final = clasificados_fijos + elegidos_desempate
                    st.session_state["top_8"] = top_8_final
                    st.session_state["puntos_f1"] = tabla
                    st.session_state["mostrar_tabla_f1"] = False
                    st.session_state["paso"] = 7
                    st.rerun()
        else:
            if st.button("🚀 Avanzar a Fase 2 (Top 8)"):
                top_8_final = [j[0] for j in tabla[:8]]
                st.session_state["top_8"] = top_8_final
                st.session_state["puntos_f1"] = tabla
                st.session_state["mostrar_tabla_f1"] = False
                st.session_state["paso"] = 7
                st.rerun()

# ==========================================
# PASO 7: TUTTIFRUTTI
# ==========================================
elif st.session_state["paso"] == 7:
    top_8 = st.session_state["top_8"]
    st.header("7️⃣ Fase 2: Tuttifrutti")
    
    tf_1 = st.selectbox("1º Tuttifrutti (+3 pts)", [None] + top_8, key="tf1")
    opciones_tf2 = [j for j in top_8 if j != tf_1]
    tf_2 = st.selectbox("2º Tuttifrutti (+2 pts)", [None] + opciones_tf2, key="tf2")
    opciones_tf3 = [j for j in opciones_tf2 if j != tf_2]
    tf_3 = st.selectbox("3º Tuttifrutti (+1 pt)", [None] + opciones_tf3, key="tf3")

    if st.button("Siguiente ➡️"):
        if not tf_1 or not tf_2 or not tf_3:
            st.warning("⚠️ Completa el podio.")
        else:
            puntos[tf_1] += 3; puntos[tf_2] += 2; puntos[tf_3] += 1
            st.session_state["paso"] = 8
            st.rerun()

# ==========================================
# PASO 8: BARQUITO
# ==========================================
elif st.session_state["paso"] == 8:
    top_8 = st.session_state["top_8"]
    st.header("8️⃣ Fase 2: Barquito")
    
    bar_1 = st.selectbox("1º Barquito (+3 pts)", [None] + top_8, key="bar1")
    opciones_bar2 = [j for j in top_8 if j != bar_1]
    bar_2 = st.selectbox("2º Barquito (+2 pts)", [None] + opciones_bar2, key="bar2")
    opciones_bar3 = [j for j in opciones_bar2 if j != bar_2]
    bar_3 = st.selectbox("3º Barquito (+1 pt)", [None] + opciones_bar3, key="bar3")

    if st.button("Siguiente ➡️"):
        if not bar_1 or not bar_2 or not bar_3:
            st.warning("⚠️ Completa el podio.")
        else:
            puntos[bar_1] += 3; puntos[bar_2] += 2; puntos[bar_3] += 1
            st.session_state["paso"] = 9
            st.rerun()

# ==========================================
# PASO 9: JUICIO MATEMÁTICO
# ==========================================
elif st.session_state["paso"] == 9:
    top_8 = st.session_state["top_8"]
    st.header("9️⃣ Fase 2: Juicio Matemático")
    
    jm_1 = st.selectbox("1º Juicio Matemático (+5 pts)", [None] + top_8, key="jm1")
    opciones_jm2 = [j for j in top_8 if j != jm_1]
    jm_2 = st.selectbox("2º Juicio Matemático (+4 pts)", [None] + opciones_jm2, key="jm2")
    opciones_jm3 = [j for j in opciones_jm2 if j != jm_2]
    jm_3 = st.selectbox("3º Juicio Matemático (+3 pts)", [None] + opciones_jm3, key="jm3")
    opciones_jm4 = [j for j in opciones_jm3 if j != jm_3]
    jm_4 = st.selectbox("4º Juicio Matemático (+2 pts)", [None] + opciones_jm4, key="jm4")
    opciones_jm5 = [j for j in opciones_jm4 if j != jm_4]
    jm_5 = st.selectbox("5º Juicio Matemático (+1 pt)", [None] + opciones_jm5, key="jm5")

    if st.button("Siguiente ➡️"):
        if not jm_1 or not jm_2 or not jm_3 or not jm_4 or not jm_5:
            st.warning("⚠️ Completa los 5 puestos.")
        else:
            puntos[jm_1] += 5; puntos[jm_2] += 4; puntos[jm_3] += 3; puntos[jm_4] += 2; puntos[jm_5] += 1
            st.session_state["paso"] = 10
            st.rerun()

# ==========================================
# PASO 10: UNO NO MERCY
# ==========================================
elif st.session_state["paso"] == 10:
    top_8 = st.session_state["top_8"]
    st.header("🔟 Fase 2: UNO No Mercy")
    
    u_1 = st.selectbox("1º UNO No Mercy (+3 pts)", [None] + top_8, key="u1")
    opciones_u2 = [j for j in top_8 if j != u_1]
    u_2 = st.selectbox("2º UNO No Mercy (+2 pts)", [None] + opciones_u2, key="u2")
    opciones_u3 = [j for j in opciones_u2 if j != u_2]
    u_3 = st.selectbox("3º UNO No Mercy (+1 pt)", [None] + opciones_u3, key="u3")

    if st.button("📊 Ver Tabla General y Definir Semifinalistas"):
        if not u_1 or not u_2 or not u_3:
            st.warning("⚠️ Completa el podio.")
        else:
            puntos[u_1] += 3; puntos[u_2] += 2; puntos[u_3] += 1
            
            tabla_f2 = sorted(puntos.items(), key=lambda x: x[1], reverse=True)
            st.session_state["puntos_f2_temporal"] = tabla_f2
            st.session_state["mostrar_tabla_f2"] = True

    if st.session_state.get("mostrar_tabla_f2", False):
        st.markdown("---")
        st.subheader("📈 Tabla General Actualizada (Fase 2)")
        tabla = st.session_state["puntos_f2_temporal"]
        
        for i, (jugador, pts) in enumerate(tabla, 1):
            st.write(f"**{i}º** {jugador}: **{pts} pts**")
            
        quinto_puntaje = tabla[4][1]
        candidatos_corte_f2 = [j for j, p in tabla if p >= quinto_puntaje]
        clasificados_fijos_f2 = [j for j, p in tabla if p > quinto_puntaje][:4]
        empatados_quinto = [j for j, p in tabla if p == quinto_puntaje]
        
        st.markdown("---")
        if len(candidatos_corte_f2) > 5:
            st.warning(f"⚠️ ¡Hay un empate en el corte del Top 5! Se debe definir quién avanza.")
            st.write(f"Jugadores asegurados arriba del corte: **{', '.join(clasificados_fijos_f2)}**")
            st.write(f"Jugadores empatados disputando el último lugar del Top 5: **{', '.join(empatados_quinto)}**")
            
            vacantes_f2 = 5 - len(clasificados_fijos_f2)
            elegidos_desempate_f2 = st.multiselect(f"Selecciona a los {vacantes_f2} jugador(es) que completan el Top 5:", empatados_quinto, max_selections=vacantes_f2)
            
            if st.button("🚀 Continuar a Semifinal y Gran Final"):
                if len(elegidos_desempate_f2) != vacantes_f2:
                    st.error(f"Debes seleccionar exactamente {vacantes_f2} jugador(es).")
                else:
                    top_5_final = clasificados_fijos_f2 + elegidos_desempate_f2
                    st.session_state["finalista_directo"] = top_5_final[0]
                    st.session_state["semifinalistas"] = top_5_final[1:]
                    st.session_state["mostrar_tabla_f2"] = False
                    st.session_state["paso"] = 11
                    st.rerun()
        else:
            if st.button("🚀 Continuar a Semifinal y Gran Final"):
                top_5_final = [j[0] for j in tabla[:5]]
                st.session_state["finalista_directo"] = top_5_final[0]
                st.session_state["semifinalistas"] = top_5_final[1:]
                st.session_state["mostrar_tabla_f2"] = False
                st.session_state["paso"] = 11
                st.rerun()

# ==========================================
# PASO 11: SEMIFINAL & GRAN FINAL
# ==========================================
elif st.session_state["paso"] == 11:
    finalista_directo = st.session_state["finalista_directo"]
    semifinalistas = st.session_state["semifinalistas"]

    st.header("1️⃣1️⃣ Etapa Final: Semifinal & Gran Final")
    st.markdown(f"🌟 **Pase directo a la Gran Final:** **{finalista_directo}**")
    
    st.subheader("⚔️ Semifinal: Liar's Bar")
    st.write(f"Candidatos: {', '.join(semifinalistas)}")
    clasificados_liars = st.multiselect("Selecciona a los 2 que pasan a la Gran Final:", semifinalistas, max_selections=2)

    if len(clasificados_liars) == 2:
        st.markdown("---")
        st.subheader("🏆 Gran Final")
        participantes_final = [finalista_directo] + clasificados_liars
        st.write(f"Finalistas: **{', '.join(participantes_final)}**")
        
        campeon = st.selectbox("¿Quién se consagra Campeón Absoluto?", participantes_final)

        if st.button("🎉 ¡Guardar Pronóstico y Ver Resultado Final!"):
            st.balloons()
            st.success(f"¡Listo! Tu predicción indica que **{campeon}** gana el torneo.")
            
            st.markdown("---")
            st.subheader("📊 Posiciones Finales del Torneo")
            
            # 1. 1º Puesto: El Campeón Absoluto
            puesto_1 = [campeon]
            
            # 2. 2º y 3º Puesto: Los otros dos perdedores de la Gran Final ordenados por puntos
            perdedores_final = [p for p in participantes_final if p != campeon]
            perdedores_final_ordenados = sorted(perdedores_final, key=lambda x: puntos[x], reverse=True)
            
            # 3. 4º y 5º Puesto: Los dos semifinalistas que no pasaron a la Gran Final
            semifinalistas_eliminados = [j for j in semifinalistas if j not in clasificados_liars]
            # Por si acaso queremos ordenarlos también por puntos o dejarlos tal cual
            semifinalistas_ordenados = sorted(semifinalistas_eliminados, key=lambda x: puntos[x], reverse=True)
            
            # 4. Agrupamos el Top 5 exacto según tus reglas
            top_5_final = puesto_1 + perdedores_final_ordenados + semifinalistas_ordenados
            
            # 5. Del 6º en adelante: El resto de los jugadores ordenados por puntos acumulados
            resto_jugadores = sorted(
                [j for j in jugadores if j not in top_5_final],
                key=lambda x: puntos[x],
                reverse=True
            )
            
            # Lista final unificada
            ranking_final = top_5_final + resto_jugadores

            for i, jugador in enumerate(ranking_final, 1):
                st.write(f"**{i}º** {jugador} (Puntaje acumulado: {puntos[jugador]} pts)")

    # Botón de reinicio
    st.markdown("---")
    if st.button("🔄 Reiniciar y armar otra predicción"):
        st.session_state["paso"] = 1
        st.session_state["puntos"] = {j: 0 for j in jugadores}
        st.rerun()
