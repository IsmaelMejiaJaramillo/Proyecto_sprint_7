# Anuncios de venta de coches 🚗

Aplicación web interactiva para explorar un conjunto de más de 51,000 anuncios de coches usados en Estados Unidos. Está hecha con **Streamlit** y **Plotly**, y desplegada en **Render**.

🔗 **Aplicación desplegada:** https://TU-APP.onrender.com

> Nota: en el plan gratuito de Render la app se "duerme" tras unos minutos de inactividad. Si tarda en cargar, espera unos 30–60 segundos y actualiza la página.

## ¿Qué hace la aplicación?

- Muestra métricas rápidas: número de anuncios, precio mediano y odómetro mediano.
- Permite filtrar los anuncios por **rango de precio**, **año del modelo**, **tipo de vehículo** y **condición** desde la barra lateral.
- Construye gráficos interactivos al activar las casillas:
  - Histograma del odómetro.
  - Histograma del precio, separado por condición.
  - Gráfico de dispersión de precio contra odómetro.
  - Diagrama de cajas del precio por tipo de vehículo.
  - Tabla con los primeros anuncios que cumplen los filtros.

## Estructura del proyecto

```
├── app.py                  # aplicación web (Streamlit)
├── vehicles_us.csv         # datos utilizados
├── requirements.txt        # librerías necesarias
├── notebooks/
│   └── EDA.ipynb           # análisis exploratorio de datos
└── README.md
```

## Cómo ejecutarla localmente

```bash
python -m venv vehicles_env
# Windows: .\vehicles_env\Scripts\Activate.ps1   |   Mac/Linux: source vehicles_env/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

La app se abre en `http://localhost:8501`.

## Datos

Se usa el archivo `vehicles_us.csv`, con 13 columnas (precio, año del modelo, modelo, condición, cilindros, combustible, odómetro, transmisión, tipo, color, tracción 4x4, fecha de publicación y días publicado). Hay valores ausentes en algunas columnas; el análisis completo está en `notebooks/EDA.ipynb`.
