import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='Anuncios de coches', page_icon='🚗', layout='wide')


@st.cache_data
def load_data():
    """Lee el CSV y hace una limpieza ligera para poder graficar."""
    data = pd.read_csv('vehicles_us.csv')
    data['date_posted'] = pd.to_datetime(data['date_posted'])
    data['is_4wd'] = data['is_4wd'].fillna(0).astype(int)
    data['paint_color'] = data['paint_color'].fillna('desconocido')
    data['manufacturer'] = data['model'].str.split().str[0]
    return data


car_data = load_data()

# ---------- Encabezado ----------
st.header('Anuncios de venta de coches 🚗')
st.write(
    'Explora un conjunto de más de 51,000 anuncios de coches usados. '
    'Usa los filtros de la barra lateral y activa las casillas para '
    'construir los gráficos.'
)

# ---------- Filtros (barra lateral) ----------
st.sidebar.header('Filtros')

price_max = int(car_data['price'].quantile(0.99))
price_range = st.sidebar.slider(
    'Rango de precio (USD)', 0, price_max, (0, price_max), step=500
)

year_min = int(car_data['model_year'].min())
year_max = int(car_data['model_year'].max())
year_range = st.sidebar.slider(
    'Año del modelo', year_min, year_max, (1990, year_max)
)

types = sorted(car_data['type'].unique())
selected_types = st.sidebar.multiselect('Tipo de vehículo', types, default=types)

conditions = ['new', 'like new', 'excellent', 'good', 'fair', 'salvage']
selected_conditions = st.sidebar.multiselect(
    'Condición', conditions, default=conditions
)

filtered = car_data[
    car_data['price'].between(*price_range)
    & car_data['type'].isin(selected_types)
    & car_data['condition'].isin(selected_conditions)
    & (
        car_data['model_year'].between(*year_range)
        | car_data['model_year'].isna()
    )
]

if filtered.empty:
    st.warning('Ningún anuncio cumple con los filtros. Amplía los rangos.')
    st.stop()

# ---------- Métricas ----------
col1, col2, col3 = st.columns(3)
col1.metric('Anuncios', f'{len(filtered):,}')
col2.metric('Precio mediano', f"${filtered['price'].median():,.0f}")
col3.metric('Odómetro mediano', f"{filtered['odometer'].median():,.0f} mi")

st.divider()

# ---------- Gráficos con casillas ----------
st.subheader('Gráficos')

show_hist_odo = st.checkbox('Histograma del odómetro')
show_hist_price = st.checkbox('Histograma del precio')
show_scatter = st.checkbox('Gráfico de dispersión: precio vs. odómetro')
show_box = st.checkbox('Precio por tipo de vehículo (caja)')
show_table = st.checkbox('Mostrar tabla de datos')

if show_hist_odo:
    st.write('Distribución del odómetro de los coches filtrados')
    fig = px.histogram(
        filtered.dropna(subset=['odometer']),
        x='odometer',
        nbins=60,
        labels={'odometer': 'Odómetro (millas)'},
    )
    fig.update_layout(title_text='Distribución del odómetro')
    st.plotly_chart(fig)

if show_hist_price:
    st.write('Distribución del precio, separada por condición')
    fig = px.histogram(
        filtered,
        x='price',
        color='condition',
        nbins=60,
        labels={'price': 'Precio (USD)', 'condition': 'Condición'},
    )
    fig.update_layout(title_text='Distribución del precio por condición')
    st.plotly_chart(fig)

if show_scatter:
    st.write('Relación entre el odómetro y el precio')
    scatter_data = filtered.dropna(subset=['odometer'])
    if len(scatter_data) > 5000:
        st.caption('Se muestra una muestra aleatoria de 5,000 anuncios.')
        scatter_data = scatter_data.sample(5000, random_state=42)
    fig = px.scatter(
        scatter_data,
        x='odometer',
        y='price',
        color='condition',
        opacity=0.6,
        hover_data=['model', 'model_year'],
        labels={
            'odometer': 'Odómetro (millas)',
            'price': 'Precio (USD)',
            'condition': 'Condición',
        },
    )
    fig.update_layout(title_text='Precio vs. odómetro')
    st.plotly_chart(fig)

if show_box:
    st.write('Precio de los anuncios según el tipo de vehículo')
    fig = px.box(
        filtered,
        x='type',
        y='price',
        labels={'type': 'Tipo de vehículo', 'price': 'Precio (USD)'},
    )
    fig.update_layout(title_text='Precio por tipo de vehículo')
    st.plotly_chart(fig)

if show_table:
    st.write('Primeros 100 anuncios que cumplen con los filtros')
    st.dataframe(filtered.head(100))
