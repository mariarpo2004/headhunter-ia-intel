# Headhunter IA · Búsqueda del próximo CEO de Intel

Proyecto de Fundamentos de IA. App en Streamlit que unifica los cuatro sprints:

1. **Filtro de requisitos** (lista de chequeo estricta)
2. **Comparación de opciones y reacción de la competencia** (teoría de juegos)
3. **Asistente de IA** para el diagnóstico de la empresa
4. **Lógica difusa**: grado de cumplimiento y regla del eslabón más débil

Flujo: Diagnóstico → Perfil del CEO → Candidatos → Filtro clásico vs difuso → Comparación → Recomendación.

## Ejecutar en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Asistente de IA (opcional)

En Streamlit Cloud: *Settings → Secrets* y agrega

```toml
ANTHROPIC_API_KEY = "tu_clave"
```

Sin clave, la app funciona igual con el diagnóstico base.

## Datos

Candidatos, puntajes, umbrales y pagos están al inicio de `app.py` (`CANDIDATOS`, `CRITERIOS`, `PAGOS`). Edítalos con los datos de tus sprints.

## Despliegue

Sube `app.py`, `requirements.txt` y `README.md` a un repositorio de GitHub y conéctalo en https://share.streamlit.io.
