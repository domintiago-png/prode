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
    
    # Obtenemos los valores actuales de los selectores para filtrar los demás
    val_c1 = st.session_state.get("c1", None)
    val_c2 = st.session_state.get("c2", None)
    val_c3 = st.session_state.get("c3", None)
    
    opciones_1 = [j for j in jugadores if j != val_c2 and j != val_c3]
    c_1 = st.selectbox("1º Lugar (+3 pts)", [None] + opciones_1, key="c1")
    
    opciones_2 = [j for j in jugadores if j != c_1 and j != val_c3]
    c_2 = st.selectbox("2º Lugar (+2 pts)", [None] + opciones_2, key="c2")
    
    opciones_3 = [j for j in jugadores if j != c_1 and j != c_2]
    c_3 = st.selectbox("3º Lugar (+1 pt)", [None] + opciones_3, key="c3")

    if st.button("Siguiente ➡️"):
        if not c_1 or not c_2 or not c_3:
            st.warning("⚠️ Por favor completa todos los puestos.")
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
    
    val_b1 = st.session_state.get("b1", None)
    val_b2 = st.session_state.get("b2", None)
    val_b3 = st.session_state.get("b3", None)
    
    opciones_b1 = [j for j in jugadores if j != val_b2 and j != val_b3]
    b_1 = st.selectbox("1º Ganador Bingo (+3 pts)", [None] + opciones_b1, key="b1")
    
    opciones_b2 = [j for j in jugadores if j != b_1 and j != val_b3]
    b_2 = st.selectbox("2º Ganador Bingo (+3 pts)", [None] + opciones_b2, key="b2")
    
    opciones_b3 = [j for j in jugadores if j != b_1 and j != b_2]
    b_3 = st.selectbox("3º Ganador Bingo (+3 pts)", [None] + opciones_b3, key="b3")

    if st.button("Siguiente ➡️"):
        if not b_1 or not b_2 or not b_3:
            st.warning("⚠️ Por favor completa todos los ganadores.")
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

    # Obtenemos los estados actuales de las selecciones para filtrar de forma cruzada
    val_jp1 = st.session_state.get("j_p1", [])
    val_jp2 = st.session_state.get("j_p2", [])
    val_mp1 = st.session_state.get("m_p1", [])
    val_mp2 = st.session_state.get("m_p2", [])
    val_qp1 = st.session_state.get("q_p1", [])
    val_qp2 = st.session_state.get("q_p2", [])
    val_cp1 = st.session_state.get("c_p1", [])
    val_cp2 = st.session_state.get("c_p2", [])

    # Recolectamos todo lo usado EXCEPTO lo que pertenece al campo actual
    opc_jp1 = [j for j in jugadores if j not in val_jp2 + val_mp1 + val_mp2 + val_qp1 + val_qp2 + val_cp1 + val_cp2]
    j_p1 = st.multiselect("Pareja 1 (Jenga)", opc_jp1, max_selections=2, key="j_p1")

    opc_jp2 = [j for j in jugadores if j not in j_p1 + val_mp1 + val_mp2 + val_qp1 + val_qp2 + val_cp1 + val_cp2]
    j_p2 = st.multiselect("Pareja 2 (Jenga)", opc_jp2, max_selections=2, key="j_p2")
    
    opc_mp1 = [j for j in jugadores if j not in j_p1 + j_p2 + val_mp2 + val_qp1 + val_qp2 + val_cp1 + val_cp2]
    memo_p1 = st.multiselect("Pareja 1 (Memotest)", opc_mp1, max_selections=2, key="m_p1")

    opc_mp2 = [j for j in jugadores if j not in j_p1 + j_p2 + memo_p1 + val_qp1 + val_qp2 + val_cp1 + val_cp2]
    memo_p2 = st.multiselect("Pareja 2 (Memotest)", opc_mp2, max_selections=2, key="m_p2")
    
    opc_qp1 = [j for j in jugadores if j not in j_p1 + j_p2 + memo_p1 + memo_p2 + val_qp2 + val_cp1 + val_cp2]
    qeq_p1 = st.multiselect("Pareja 1 (¿Quién es Quién?)", opc_qp1, max_selections=2, key="q_p1")

    opc_qp2 = [j for j in jugadores if j not in j_p1 + j_p2 + memo_p1 + memo_p2 + qeq_p1 + val_cp1 + val_cp2]
    qeq_p2 = st.multiselect("Pareja 2 (¿Quién es Quién?)", opc_qp2, max_selections=2, key="q_p2")
    
    opc_cp1 = [j for j in jugadores if j not in j_p1 + j_p2 + memo_p1 + memo_p2 + qeq_p1 + qeq_p2 + val_cp2]
    c4_p1 = st.multiselect("Pareja 1 (Conecta 4)", opc_cp1, max_selections=2, key="c_p1")

    opc_cp2 = [j for j in jugadores if j not in j_p1 + j_p2 + memo_p1 + memo_p2 + qeq_p1 + qeq_p2 + c4_p1]
    c4_p2 = st.multiselect("Pareja 2 (Conecta 4)", opc_cp2, max_selections=2, key="c_p2")

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
            for pareja in [g_jenga_pareja, g_memo_pareja, g_qeq_pareja, g_c4_pareja]:
                for jugador in pareja:
                    puntos[jugador] += 2
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
    
    val_tt1 = st.session_state.get("tt1", None)
    val_tt2 = st.session_state.get("tt2", None)
    val_tt3 = st.session_state.get("tt3", None)
    
    op_tt1 = [j for j in jugadores if j != val_tt2 and j != val_tt3]
    tt_1 = st.selectbox("1º Lugar (+3 pts)", [None] + op_tt1, key="tt1")
    
    op_tt2 = [j for j in jugadores if j != tt_1 and j != val_tt3]
    tt_2 = st.selectbox("2º Lugar (+2 pts)", [None] + op_tt2, key="tt2")
    
    op_tt3 = [j for j in jugadores if j != tt_1 and j != tt_2]
    tt_3 = st.selectbox("3º Lugar (+1 pt)", [None] + op_tt3, key="tt3")

    if st.button("Siguiente ➡️"):
        if not tt_1 or not tt_2 or not tt_3:
            st.warning("⚠️ Completa los tres puestos.")
        else:
            puntos[tt_1] += 3; puntos[tt_2] += 2; puntos[tt_3] += 1
            st.session_state["paso"] = 5
            st.rerun()

# ==========================================
# PASO 5: DÍGALO CON MÍMICA
# ==========================================
elif st.session_state["paso"] == 5:
    st.header("5️⃣ Fase Regular: Dígalo con Mímica")
    st.markdown("Arma los 4 equipos de 4 jugadores cada uno. (Los jugadores seleccionados se bloquean automáticamente en los demás equipos):")

    val_eqa = st.session_state.get("eq_a", [])
    val_eqb = st.session_state.get("eq_b", [])
    val_eqc = st.session_state.get("eq_c", [])
    val_eqd = st.session_state.get("eq_d", [])

    op_eqa = [j for j in jugadores if j not in val_eqb + val_eqc + val_eqd]
    eq_a = st.multiselect("Equipo A (4 jugadores):", op_eqa, max_selections=4, key="eq_a")
    
    op_eqb = [j for j in jugadores if j not in eq_a + val_eqc + val_eqd]
    eq_b = st.multiselect("Equipo B (4 jugadores):", op_eqb, max_selections=4, key="eq_b")
    
    op_eqc = [j for j in jugadores if j not in eq_a + eq_b + val_eqd]
    eq_c = st.multiselect("Equipo C (4 jugadores):", op_eqc, max_selections=4, key="eq_c")
    
    op_eqd = [j for j in jugadores if j not in eq_a + eq_b + eq_c]
    eq_d = st.multiselect("Equipo D (4 jugadores):", op_eqd, max_selections=4, key="eq_d")

    st.markdown("---")

    equipos_completos = (
        len(eq_a) == 4 and 
        len(eq_b) == 4 and 
        len(eq_c) == 4 and 
        len(eq_d) == 4
    )

    if equipos_completos:
        st.markdown("### 🏆 Selecciona los puestos de los equipos")
        
        nombres_equipos = ["Equipo A", "Equipo B", "Equipo C", "Equipo D"]
        val_m1 = st.session_state.get("mimica_p1", None)
        val_m2 = st.session_state.get("mimica_p2", None)
        val_m3 = st.session_state.get("mimica_p3", None)

        op_m1 = [e for e in nombres_equipos if e != val_m2 and e != val_m3]
        eq_1_podio = st.selectbox("1º Puesto (+3 pts c/u):", [None] + op_m1, key="mimica_p1")
        
        op_m2 = [e for e in nombres_equipos if e != eq_1_podio and e != val_m3]
        eq_2_podio = st.selectbox("2º Puesto (+2 pts c/u):", [None] + op_m2, key="mimica_p2")
        
        op_m3 = [e for e in nombres_equipos if e != eq_1_podio and e != eq_2_podio]
        eq_3_podio = st.selectbox("3º Puesto (+1 pt c/u):", [None] + op_m3, key="mimica_p3")

        dic_equipos = {
            "Equipo A": eq_a,
            "Equipo B": eq_b,
            "Equipo C": eq_c,
            "Equipo D": eq_d
        }

        if st.button("Siguiente ➡️"):
            if not eq_1_podio or not eq_2_podio or not eq_3_podio:
                st.warning("⚠️ Completa los puestos del podio.")
            else:
                for m in dic_equipos[eq_1_podio]: puntos[m] += 3
                for m in dic_equipos[eq_2_podio]: puntos[m] += 2
                for m in dic_equipos[eq_3_podio]: puntos[m] += 1
                
                st.session_state["paso"] = 6
                st.rerun()
    else:
        st.info("ℹ️ Asigna exactamente 4 integrantes distintos a cada uno de los 4 equipos para que aparezca la opción de elegir el podio.")

# ==========================================
# PASO 6: EN UNA NOTA Y CORTE DE FASE 1
# ==========================================
elif st.session_state["paso"] == 6:
    st.header("6️⃣ Fase Regular: En Una Nota")
    
    val_n1 = st.session_state.get("n1", None)
    val_n2 = st.session_state.get("n2", None)
    val_n3 = st.session_state.get("n3", None)
    val_n4 = st.session_state.get("n4", None)
    val_n5 = st.session_state.get("n5", None)

    op_n1 = [j for j in jugadores if j != val_n2 and j != val_n3 and j != val_n4 and j != val_n5]
    n_1 = st.selectbox("1º Lugar (+5 pts)", [None] + op_n1, key="n1")
    
    op_n2 = [j for j in jugadores if j != n_1 and j != val_n3 and j != val_n4 and j != val_n5]
    n_2 = st.selectbox("2º Lugar (+4 pts)", [None] + op_n2, key="n2")
    
    op_n3 = [j for j in jugadores if j != n_1 and j != n_2 and j != val_n4 and j != val_n5]
    n_3 = st.selectbox("3º Lugar (+3 pts)", [None] + op_n3, key="n3")
    
    op_n4 = [j for j in jugadores if j != n_1 and j != n_2 and j != n_3 and j != val_n5]
    n_4 = st.selectbox("4º Lugar (+2 pts)", [None] + op_n4, key="n4")
    
    op_n5 = [j for j in jugadores if j != n_1 and j != n_2 and j != n_3 and j != n_4]
    n_5 = st.selectbox("5º Lugar (+1 pt)", [None] + op_n5, key="n5")

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
    
    val_tf1 = st.session_state.get("tf1", None)
    val_tf2 = st.session_state.get("tf2", None)
    val_tf3 = st.session_state.get("tf3", None)

    op_tf1 = [j for j in top_8 if j != val_tf2 and j != val_tf3]
    tf_1 = st.selectbox("1º Tuttifrutti (+3 pts)", [None] + op_tf1, key="tf1")
    
    op_tf2 = [j for j in top_8 if j != tf_1 and j != val_tf3]
    tf_2 = st.selectbox("2º Tuttifrutti (+2 pts)", [None] + op_tf2, key="tf2")
    
    op_tf3 = [j for j in top_8 if j != tf_1 and j != tf_2]
    tf_3 = st.selectbox("3º Tuttifrutti (+1 pt)", [None] + op_tf3, key="tf3")

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
    
    val_bar1 = st.session_state.get("bar1", None)
    val_bar2 = st.session_state.get("bar2", None)
    val_bar3 = st.session_state.get("bar3", None)

    op_bar1 = [j for j in top_8 if j != val_bar2 and j != val_bar3]
    bar_1 = st.selectbox("1º Barquito (+3 pts)", [None] + op_bar1, key="bar1")
    
    op_bar2 = [j for j in top_8 if j != bar_1 and j != val_bar3]
    bar_2 = st.selectbox("2º Barquito (+2 pts)", [None] + op_bar2, key="bar2")
    
    op_bar3 = [j for j in top_8 if j != bar_1 and j != bar_2]
    bar_3 = st.selectbox("3º Barquito (+1 pt)", [None] + op_bar3, key="bar3")

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
    
    val_jm1 = st.session_state.get("jm1", None)
    val_jm2 = st.session_state.get("jm2", None)
    val_jm3 = st.session_state.get("jm3", None)
    val_jm4 = st.session_state.get("jm4", None)
    val_jm5 = st.session_state.get("jm5", None)

    op_jm1 = [j for j in top_8 if j != val_jm2 and j != val_jm3 and j != val_jm4 and j != val_jm5]
    jm_1 = st.selectbox("1º Juicio Matemático (+5 pts)", [None] + op_jm1, key="jm1")
    
    op_jm2 = [j for j in top_8 if j != jm_1 and j != val_jm3 and j != val_jm4 and j != val_jm5]
    jm_2 = st.selectbox("2º Juicio Matemático (+4 pts)", [None] + op_jm2, key="jm2")
    
    op_jm3 = [j for j in top_8 if j != jm_1 and j != jm_2 and j != val_jm4 and j != val_jm5]
    jm_3 = st.selectbox("3º Juicio Matemático (+3 pts)", [None] + op_jm3, key="jm3")
    
    op_jm4 = [j for j in top_8 if j != jm_1 and j != jm_2 and j != jm_3 and j != val_jm5]
    jm_4 = st.selectbox("4º Juicio Matemático (+2 pts)", [None] + op_jm4, key="jm4")
    
    op_jm5 = [j for j in top_8 if j != jm_1 and j != jm_2 and j != jm_3 and j != jm_4]
    jm_5 = st.selectbox("5º Juicio Matemático (+1 pt)", [None] + op_jm5, key="jm5")

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
    
    val_u1 = st.session_state.get("u1", None)
    val_u2 = st.session_state.get("u2", None)
    val_u3 = st.session_state.get("u3", None)

    op_u1 = [j for j in top_8 if j != val_u2 and j != val_u3]
    u_1 = st.selectbox("1º UNO No Mercy (+3 pts)", [None] + op_u1, key="u1")
    
    op_u2 = [j for j in top_8 if j != u_1 and j != val_u3]
    u_2 = st.selectbox("2º UNO No Mercy (+2 pts)", [None] + op_u2, key="u2")
    
    op_u3 = [j for j in top_8 if j != u_1 and j != u_2]
    u_3 = st.selectbox("3º UNO No Mercy (+1 pt)", [None] + op_u3, key="u3")

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
