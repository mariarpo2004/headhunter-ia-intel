"""Headhunter IA · Búsqueda del próximo CEO de Intel
Proyecto de Fundamentos de IA — Sprints 1 a 4 unificados en una sola app.

Sprint 1: filtro de requisitos (lista de chequeo, reglas estrictas)
Sprint 2: comparación de opciones y reacción de la competencia (teoría de juegos)
Sprint 3: asistente de IA para el diagnóstico de la empresa
Sprint 4: lógica difusa (grado de cumplimiento, "eslabón más débil")
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Headhunter IA · CEO de Intel",
    page_icon="🎯",
    layout="wide",
)

# ───────────────────────── Estilo minimalista ─────────────────────────
st.markdown(
    """
    <style>
    .block-container {max-width: 1100px; padding-top: 2rem;}
    h1, h2, h3 {letter-spacing: -0.01em;}
    .muted {color: #6b7280; font-size: 0.95rem;}
    .card {border: 1px solid #e5e7eb; border-radius: 10px; padding: 1rem 1.2rem; background: #fafafa;}
    .pill {display:inline-block; padding: 2px 10px; border-radius: 999px; font-size: 0.8rem; font-weight: 600;}
    .ok {background:#dcfce7; color:#166534;}
    .mid {background:#fef9c3; color:#854d0e;}
    .no {background:#fee2e2; color:#991b1b;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ───────────────────────── Datos del proyecto ─────────────────────────
# NOTA: puntajes 0-10 y años son estimaciones de trabajo. Reemplázalos por
# los datos exactos de tus sprints editando este bloque.

CRITERIOS = {
    # clave: (etiqueta, umbral por defecto, tolerancia por defecto, unidad)
    "tecnologia": ("Tecnología (semiconductores / IA)", 8.0, 2.0, "pts"),
    "transformacion": ("Capacidad de transformación", 7.0, 3.0, "pts"),
    "gobernanza": ("Gobernanza y disciplina de ejecución", 7.0, 3.0, "pts"),
    "experiencia": ("Experiencia como CEO", 5.0, 3.0, "años"),
    "disponibilidad": ("Disponibilidad y viabilidad de fichaje", 5.0, 3.0, "pts"),
}

CANDIDATOS = pd.DataFrame(
    [
        # nombre, empresa actual, tec, transf, gob, exp, disp, foundry (fit), IA (fit), cultura (fit)
        ["Lip-Bu Tan", "Ex-CEO Cadence", 8.5, 8.5, 8.5, 12, 9, 9, 7, 8],
        ["Rene Haas", "CEO Arm", 9.2, 8.0, 8.0, 4, 7, 6, 8, 7],
        ["Pat Gelsinger", "Ex-CEO Intel / VMware", 9.0, 3.0, 3.0, 12, 8, 8, 6, 5],
        ["Sanjay Mehrotra", "CEO Micron", 8.2, 7.5, 8.5, 10, 6, 8, 7, 7],
        ["Lisa Su", "CEO AMD", 9.5, 9.5, 9.0, 12, 1, 5, 9, 8],
        ["Hock Tan", "CEO Broadcom", 7.0, 8.5, 7.5, 15, 3, 6, 6, 5],
    ],
    columns=[
        "Candidato", "Cargo actual", "tecnologia", "transformacion", "gobernanza",
        "experiencia", "disponibilidad", "fit_foundry", "fit_ia", "fit_cultura",
    ],
)

TRAYECTORIA = {
    "Lip-Bu Tan": (
        "Llevó a Cadence a un crecimiento sostenido durante más de una década; conoce el ecosistema de diseño y de clientes de foundry.",
        "No ha dirigido una fabricación a escala de Intel.",
    ),
    "Rene Haas": (
        "Consolidó a Arm como estándar para IA y móvil; muy fuerte en tecnología y alianzas.",
        "Solo ~4 años como CEO y sin operar fábricas propias.",
    ),
    "Pat Gelsinger": (
        "Conoce Intel por dentro y lanzó el plan IDM 2.0 y la inversión en fábricas.",
        "Su ejecución y gobernanza fueron cuestionadas: retrasos, pérdidas y recortes tardíos.",
    ),
    "Sanjay Mehrotra": (
        "Gestión disciplinada de Micron en un negocio intensivo en fábricas y ciclos.",
        "Menos experiencia en diseño de procesadores y en IA de cómputo.",
    ),
    "Lisa Su": (
        "Rescató a AMD y la puso a competir con Intel y NVIDIA; referente del sector.",
        "Es cabeza de un competidor directo: fichaje prácticamente inviable.",
    ),
    "Hock Tan": (
        "Maestro en adquisiciones y márgenes en Broadcom.",
        "Perfil financiero más que tecnológico y difícil de contratar.",
    ),
}

DIAGNOSTICO = {
    "Problemas": [
        "Perdió el liderazgo en proceso de manufactura frente a TSMC.",
        "Llegó tarde al mercado de IA: NVIDIA domina los aceleradores para centros de datos.",
        "Su negocio de fundición (foundry) pierde dinero y aún no atrae suficientes clientes externos.",
        "Márgenes y flujo de caja bajo presión; dividendo y gastos recortados.",
    ],
    "Errores de líderes anteriores": [
        "Retrasos repetidos en nodos de manufactura sin corregir a tiempo.",
        "Recompra de acciones en lugar de invertir en tecnología y fábricas.",
        "Subestimar la IA y las GPU mientras NVIDIA tomaba ventaja.",
        "Planes ambiciosos sin disciplina de ejecución ni gobernanza clara.",
    ],
    "Hacia dónde va el mercado": [
        "La demanda de cómputo para IA crece más rápido que el resto del sector.",
        "Los clientes buscan una alternativa a TSMC fuera de Asia (resiliencia de cadena).",
        "Los gobiernos subsidian la manufactura local de chips.",
        "Se abre espacio para chips por encargo y arquitecturas especializadas.",
    ],
}

PERFIL_CEO = [
    ("Tecnología", "Dominio profundo de semiconductores e IA para recuperar credibilidad ante clientes e ingenieros."),
    ("Transformación", "Haber reestructurado una empresa o un negocio en dificultad."),
    ("Gobernanza", "Disciplina de ejecución: cumplir plazos, controlar costos y rendir cuentas."),
    ("Experiencia como CEO", "Haber dirigido una compañía grande durante varios años."),
    ("Disponibilidad", "Que sea realista contratarlo: no estar atado a un competidor directo."),
]

# Estrategias de Intel vs reacción de la competencia (utilidad para Intel, 0-10)
ESTRATEGIAS = [
    "Foundry primero (atraer clientes externos)",
    "IA primero (aceleradores y CPU para IA)",
    "Eficiencia y enfoque (recortar y priorizar)",
]
REACCIONES = [
    "TSMC baja precios",
    "NVIDIA acelera su ecosistema",
    "AMD/Arm atacan el servidor",
]
PAGOS = pd.DataFrame(
    [[6, 7, 7], [5, 3, 5], [5, 5, 6]],
    index=ESTRATEGIAS,
    columns=REACCIONES,
)
PROB_REACCION = pd.Series([0.3, 0.4, 0.3], index=REACCIONES)
AFINIDAD = {
    "Foundry primero (atraer clientes externos)": "fit_foundry",
    "IA primero (aceleradores y CPU para IA)": "fit_ia",
    "Eficiencia y enfoque (recortar y priorizar)": "fit_cultura",
}

# ───────────────────────── Lógica ─────────────────────────


def membresia(valor, umbral, tolerancia):
    """Grado de cumplimiento 0-1. 1 si alcanza el umbral; baja linealmente
    hasta 0 cuando está a 'tolerancia' o más por debajo."""
    if valor >= umbral:
        return 1.0
    if tolerancia <= 0 or valor <= umbral - tolerancia:
        return 0.0
    return (valor - (umbral - tolerancia)) / tolerancia


def evaluar(df, umbrales, tolerancias):
    filas = []
    for _, r in df.iterrows():
        fila = {"Candidato": r["Candidato"]}
        grados, clasicos = [], []
        for k in CRITERIOS:
            g = membresia(r[k], umbrales[k], tolerancias[k])
            fila[f"mu_{k}"] = g
            fila[f"ok_{k}"] = r[k] >= umbrales[k]
            grados.append(g)
            clasicos.append(r[k] >= umbrales[k])
        fila["clasico"] = all(clasicos)
        fila["difuso"] = min(grados)
        fila["limitante"] = list(CRITERIOS)[grados.index(min(grados))]
        filas.append(fila)
    return pd.DataFrame(filas)


def etiqueta(g):
    if g >= 0.999:
        return "Apto"
    if g > 0:
        return "Parcialmente apto"
    return "No apto"


def pill(g):
    clase = "ok" if g >= 0.999 else ("mid" if g > 0 else "no")
    return f'<span class="pill {clase}">{etiqueta(g)}</span>'


def ajuste(r):
    """Ajuste a los problemas de Intel (0-10): foundry, IA y gobernanza/cultura."""
    return round(0.4 * r["fit_foundry"] + 0.3 * r["fit_ia"] + 0.3 * r["fit_cultura"], 2)


def seguridad_y_esperado():
    maximin = PAGOS.min(axis=1)
    esperado = PAGOS.mul(PROB_REACCION, axis=1).sum(axis=1)
    return maximin, esperado


# ───────────────────────── Estado compartido ─────────────────────────
if "umbrales" not in st.session_state:
    st.session_state.umbrales = {k: v[1] for k, v in CRITERIOS.items()}
    st.session_state.tolerancias = {k: v[2] for k, v in CRITERIOS.items()}

PASOS = [
    "1 · Diagnóstico de Intel",
    "2 · Perfil del CEO",
    "3 · Candidatos",
    "4 · Filtro: clásico vs difuso",
    "5 · Comparación y competencia",
    "6 · Recomendación",
]

with st.sidebar:
    st.markdown("### 🎯 Headhunter IA")
    st.caption("Búsqueda del próximo CEO de Intel")
    paso = st.radio("Flujo de trabajo", PASOS, label_visibility="collapsed")
    st.divider()
    st.caption("Proyecto de Fundamentos de IA")

UMB = st.session_state.umbrales
TOL = st.session_state.tolerancias
RES = evaluar(CANDIDATOS, UMB, TOL).merge(CANDIDATOS[["Candidato"]], on="Candidato")
CAND = CANDIDATOS.copy()
CAND["Ajuste Intel"] = CAND.apply(ajuste, axis=1)

# ───────────────────────── Páginas ─────────────────────────
if paso == PASOS[0]:
    st.title("Diagnóstico de Intel")
    st.markdown(
        '<p class="muted">Un buen headhunter empieza entendiendo a la empresa, no buscando candidatos.</p>',
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    for col, (titulo, items) in zip((c1, c2, c3), DIAGNOSTICO.items()):
        with col:
            st.subheader(titulo)
            for it in items:
                st.markdown(f"- {it}")

    st.divider()
    st.subheader("Asistente de IA")
    st.caption(
        "Genera un análisis inicial actualizado. Requiere ANTHROPIC_API_KEY en los secretos de Streamlit; "
        "sin clave se muestra el diagnóstico base de arriba."
    )
    pregunta = st.text_area(
        "Pregunta para el asistente",
        "Resume la situación actual de Intel frente a NVIDIA y qué debe priorizar un nuevo CEO.",
        height=80,
    )
    if st.button("Analizar con IA"):
        clave = st.secrets.get("ANTHROPIC_API_KEY", None) if hasattr(st, "secrets") else None
        if not clave:
            st.info("No hay clave configurada. Agrega ANTHROPIC_API_KEY en Settings → Secrets.")
        else:
            try:
                import anthropic

                cliente = anthropic.Anthropic(api_key=clave)
                with st.spinner("Analizando..."):
                    r = cliente.messages.create(
                        model=st.secrets.get("ANTHROPIC_MODEL", "claude-sonnet-5-5"),
                        max_tokens=900,
                        system=(
                            "Eres un consultor de búsqueda de ejecutivos. Analiza a Intel de forma breve, "
                            "concreta y estructurada: problemas, errores previos, tendencias de mercado "
                            "y cualidades que necesita su próximo CEO. Responde en español."
                        ),
                        messages=[{"role": "user", "content": pregunta}],
                    )
                st.markdown(r.content[0].text)
            except Exception as e:  # noqa: BLE001
                st.error(f"No se pudo consultar al asistente: {e}")

elif paso == PASOS[1]:
    st.title("Perfil del CEO ideal")
    st.markdown(
        '<p class="muted">Del diagnóstico salen las cualidades indispensables. Son los requisitos que usaremos para filtrar.</p>',
        unsafe_allow_html=True,
    )
    for nombre, desc in PERFIL_CEO:
        st.markdown(f"**{nombre}** — {desc}")
    st.divider()
    st.subheader("Umbrales mínimos")
    st.caption("Puedes ajustarlos; todo el resto de la app se recalcula.")
    cols = st.columns(len(CRITERIOS))
    for col, (k, (et, _, _, unidad)) in zip(cols, CRITERIOS.items()):
        with col:
            maximo = 20.0 if unidad == "años" else 10.0
            UMB[k] = st.number_input(
                f"{et.split(' (')[0]} (mín., {unidad})", 0.0, maximo, float(UMB[k]), 0.5, key=f"umb_{k}"
            )
    with st.expander("Tolerancia de la lógica difusa"):
        st.caption("Cuánto por debajo del umbral aún cuenta como cumplimiento parcial. Con 0 se vuelve un filtro estricto.")
        cols = st.columns(len(CRITERIOS))
        for col, (k, (et, _, _, unidad)) in zip(cols, CRITERIOS.items()):
            with col:
                TOL[k] = st.number_input(
                    f"{et.split(' (')[0]}", 0.0, 10.0, float(TOL[k]), 0.5, key=f"tol_{k}"
                )

elif paso == PASOS[2]:
    st.title("Candidatos")
    st.markdown(
        '<p class="muted">Ejecutivos reconocidos de la industria y lo que lograron (o no) en las empresas que dirigieron.</p>',
        unsafe_allow_html=True,
    )
    tabla = CAND[["Candidato", "Cargo actual", "tecnologia", "transformacion", "gobernanza", "experiencia", "disponibilidad"]].rename(
        columns={k: v[0].split(" (")[0] for k, v in CRITERIOS.items()}
    )
    st.dataframe(tabla, hide_index=True, width="stretch")
    st.divider()
    elegido = st.selectbox("Ver trayectoria de", CAND["Candidato"])
    logro, limite = TRAYECTORIA[elegido]
    a, b = st.columns(2)
    a.success(f"**Lo que logró**\n\n{logro}")
    b.warning(f"**Lo que no logró / riesgo**\n\n{limite}")

elif paso == PASOS[3]:
    st.title("Filtro de requisitos")
    st.markdown(
        '<p class="muted">Sprint 1 pregunta “¿cumple o no cumple?”. Sprint 4 pregunta “¿qué tanto cumple?”.</p>',
        unsafe_allow_html=True,
    )
    t1, t2, t3 = st.tabs(["Clásico (pasa / no pasa)", "Lógica difusa", "Cómo funciona"])

    with t1:
        pasan = RES[RES["clasico"]]["Candidato"].tolist()
        tabla = pd.DataFrame(
            {
                "Candidato": RES["Candidato"],
                **{
                    CRITERIOS[k][0].split(" (")[0]: RES[f"ok_{k}"].map({True: "✔", False: "✘"})
                    for k in CRITERIOS
                },
                "Resultado": RES["clasico"].map({True: "Pasa", False: "Descartado"}),
            }
        )
        st.dataframe(tabla, hide_index=True, width="stretch")
        if pasan:
            st.success(f"Pasan el filtro estricto: {', '.join(pasan)}")
        else:
            st.error("Nadie pasa. Antes se necesitaba la “regla de relajación” para bajar los umbrales.")
        quedan_cerca = RES[(~RES["clasico"]) & (RES["difuso"] > 0)]["Candidato"].tolist()
        if quedan_cerca:
            st.caption(
                "Descartados por el filtro clásico pero cercanos a cumplir: " + ", ".join(quedan_cerca) + "."
            )

    with t2:
        orden = RES.sort_values("difuso", ascending=False)
        tabla = pd.DataFrame(
            {
                "Candidato": orden["Candidato"],
                **{
                    CRITERIOS[k][0].split(" (")[0]: orden[f"mu_{k}"].map(lambda x: f"{x:.0%}")
                    for k in CRITERIOS
                },
                "Aptitud global": orden["difuso"].map(lambda x: f"{x:.0%}"),
                "Estado": orden["difuso"].map(etiqueta),
                "Requisito que frena": orden.apply(
                    lambda r: "—" if r["difuso"] >= 0.999 else CRITERIOS[r["limitante"]][0].split(" (")[0], axis=1
                ),
            }
        )
        st.dataframe(tabla, hide_index=True, width="stretch")
        fig = go.Figure(
            go.Bar(
                x=orden["difuso"],
                y=orden["Candidato"],
                orientation="h",
                marker_color=["#16a34a" if v >= 0.999 else "#ca8a04" if v > 0 else "#dc2626" for v in orden["difuso"]],
                text=[f"{v:.0%}" for v in orden["difuso"]],
                textposition="outside",
            )
        )
        fig.update_layout(
            xaxis=dict(range=[0, 1.15], tickformat=".0%", title="Aptitud global (mínimo de los requisitos)"),
            yaxis=dict(autorange="reversed"),
            height=320,
            margin=dict(l=0, r=0, t=10, b=0),
            plot_bgcolor="white",
        )
        st.plotly_chart(fig, width="stretch")
        for nombre in ("Rene Haas", "Pat Gelsinger"):
            fila = RES[RES["Candidato"] == nombre].iloc[0]
            st.markdown(
                f"**{nombre}** {pill(fila['difuso'])} — aptitud {fila['difuso']:.0%}",
                unsafe_allow_html=True,
            )

    with t3:
        st.markdown(
            "Cada requisito tiene un **umbral** y una **tolerancia**. Si el candidato lo alcanza, cumple 100 %. "
            "Si está por debajo, el cumplimiento baja de forma gradual hasta 0 % cuando la distancia iguala la tolerancia.\n\n"
            "La aptitud global es el **mínimo** de los grados: una cadena es tan fuerte como su eslabón más débil."
        )
        k = st.selectbox("Requisito a visualizar", list(CRITERIOS), format_func=lambda x: CRITERIOS[x][0])
        u, t = UMB[k], TOL[k]
        xs = [u - t - 1 + i * 0.1 for i in range(int((t + 2) * 10) + 1)]
        ys = [membresia(x, u, t) for x in xs]
        fig = go.Figure(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color="#111827", width=3)))
        for _, r in CAND.iterrows():
            fig.add_trace(
                go.Scatter(
                    x=[r[k]], y=[membresia(r[k], u, t)], mode="markers+text",
                    text=[r["Candidato"].split()[-1]], textposition="top center",
                    marker=dict(size=9), showlegend=False,
                )
            )
        fig.update_layout(
            xaxis_title=CRITERIOS[k][0], yaxis=dict(title="Grado de cumplimiento", range=[-0.05, 1.2], tickformat=".0%"),
            height=340, margin=dict(l=0, r=0, t=10, b=0), plot_bgcolor="white", showlegend=False,
        )
        st.plotly_chart(fig, width="stretch")

elif paso == PASOS[4]:
    st.title("Comparación y reacción de la competencia")
    st.markdown(
        '<p class="muted">Entre los candidatos aptos (total o parcialmente) no solo importa quién es mejor, sino quién encaja con los problemas de Intel.</p>',
        unsafe_allow_html=True,
    )
    base = RES[["Candidato", "difuso"]].merge(CAND[["Candidato", "Ajuste Intel", "fit_foundry", "fit_ia", "fit_cultura"]], on="Candidato")
    base = base[base["difuso"] > 0].copy()
    base["Puntaje final"] = (base["difuso"] * base["Ajuste Intel"]).round(2)
    base = base.sort_values("Puntaje final", ascending=False)

    st.subheader("Ajuste a los problemas de Intel")
    st.caption("Ajuste = 40 % foundry + 30 % IA + 30 % cultura/ejecución. Puntaje final = ajuste × aptitud difusa.")
    mostrar = base.rename(
        columns={"difuso": "Aptitud difusa", "fit_foundry": "Foundry", "fit_ia": "IA", "fit_cultura": "Cultura"}
    )
    mostrar["Aptitud difusa"] = mostrar["Aptitud difusa"].map(lambda x: f"{x:.0%}")
    st.dataframe(mostrar, hide_index=True, width="stretch")

    st.divider()
    st.subheader("¿Cómo reaccionaría la competencia?")
    st.caption("Utilidad para Intel (0–10) según su estrategia y la respuesta de los rivales. Puedes editar los pagos.")
    editado = st.data_editor(PAGOS, width="stretch")
    PAGOS.loc[:, :] = editado
    maximin, esperado = seguridad_y_esperado()
    resumen = pd.DataFrame(
        {"Peor escenario (maximin)": maximin, "Valor esperado": esperado.round(2)}
    )
    st.dataframe(resumen, width="stretch")
    mejor_seg = maximin.idxmax()
    mejor_esp = esperado.idxmax()
    st.markdown(
        f"Estrategia más segura: **{mejor_seg}**. Mayor valor esperado: **{mejor_esp}**."
    )

    st.subheader("Mejor estrategia por candidato")
    filas = []
    for _, r in base.iterrows():
        cand = CAND[CAND["Candidato"] == r["Candidato"]].iloc[0]
        valores = {e: esperado[e] * cand[AFINIDAD[e]] / 10 for e in ESTRATEGIAS}
        mejor = max(valores, key=valores.get)
        filas.append({"Candidato": r["Candidato"], "Estrategia que mejor ejecutaría": mejor, "Valor": round(valores[mejor], 2)})
    st.dataframe(pd.DataFrame(filas), hide_index=True, width="stretch")

else:
    st.title("Recomendación")
    st.markdown(
        '<p class="muted">Candidato ideal, plan B y la razón de la elección.</p>',
        unsafe_allow_html=True,
    )
    base = RES[["Candidato", "difuso", "limitante"]].merge(CAND[["Candidato", "Ajuste Intel"]], on="Candidato")
    base["Puntaje final"] = (base["difuso"] * base["Ajuste Intel"]).round(2)
    base = base[base["difuso"] > 0].sort_values("Puntaje final", ascending=False).reset_index(drop=True)

    if len(base) == 0:
        st.error("Ningún candidato alcanza el mínimo. Reduce los umbrales o aumenta la tolerancia en el paso 2.")
    else:
        ideal = base.iloc[0]
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Candidato ideal")
            st.markdown(f"## {ideal['Candidato']}")
            st.markdown(pill(ideal["difuso"]), unsafe_allow_html=True)
            st.metric("Puntaje final", f"{ideal['Puntaje final']:.2f} / 10")
        with c2:
            st.markdown("#### Plan B")
            if len(base) > 1:
                b = base.iloc[1]
                st.markdown(f"## {b['Candidato']}")
                st.markdown(pill(b["difuso"]), unsafe_allow_html=True)
                st.metric("Puntaje final", f"{b['Puntaje final']:.2f} / 10")
            else:
                st.write("No hay un segundo candidato viable.")

        logro, limite = TRAYECTORIA[ideal["Candidato"]]
        st.divider()
        st.subheader("Por qué")
        st.markdown(
            f"- **Aptitud:** {ideal['difuso']:.0%} de cumplimiento global de los requisitos.\n"
            f"- **Ajuste a Intel:** {ideal['Ajuste Intel']:.1f}/10 según foundry, IA y ejecución.\n"
            f"- **Lo que logró:** {logro}\n"
            f"- **Riesgo a vigilar:** {limite}"
        )
        st.subheader("Ranking completo")
        completo = base.rename(columns={"difuso": "Aptitud difusa"})[["Candidato", "Aptitud difusa", "Ajuste Intel", "Puntaje final"]]
        completo["Aptitud difusa"] = completo["Aptitud difusa"].map(lambda x: f"{x:.0%}")
        st.dataframe(completo, hide_index=True, width="stretch")

        descartados = RES[RES["difuso"] == 0]["Candidato"].tolist()
        if descartados:
            st.caption("Descartados (0 % en algún requisito): " + ", ".join(descartados) + ".")
        st.caption(
            "Los puntajes de los candidatos son estimaciones de trabajo; actualízalos con los datos de tus sprints en app.py."
        )
