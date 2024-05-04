import streamlit as st
import pandas as pd
import plotly_express as px
import datetime


# Configurar o xlsx
df = pd.read_excel(
    io='supermarkt_sales.xlsx',
    engine='openpyxl',
    sheet_name='Sales',
    skiprows=3,
    usecols='B:R',
    nrows=1000,
)

st.set_page_config(layout='wide')

st.sidebar.title('Filters')

# Criar multiselect city
descriçao_city = st.sidebar.multiselect(
    'Select the City: ',
    options=df['City'].unique(),
    default=df['City'].unique()
)

# Criar data range
max_date = datetime.date(2021, 12, 31)
min_date = datetime.date(2021, 1, 1)
calendario = st.sidebar.date_input('Choose the Period: ', (min_date, max_date))

calendario_inicio = pd.to_datetime(calendario[0])
calendario_fim = pd.to_datetime(calendario[1])

calendario_filtro = df[(df['Date'] >= calendario_inicio)
                       & (df['Date'] <= calendario_fim)]

# Criar multiselect Gender
descriçao_gender = st.sidebar.multiselect(
    'Select the Gender: ',
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

# Criar multiselect Customer Type
descriçao_Customer = st.sidebar.multiselect(
    'Select the Customer Type: ',
    options=df['Customer_type'].unique(),
    default=df['Customer_type'].unique()
)

# Criar variável englobando todos filter
# Filtrar por cidade
df_select = df[df['City'].isin(descriçao_city)]

# Filtrar por tipo de cliente
df_select = df_select[df_select['Customer_type'].isin(descriçao_Customer)]

# Filtrar por gênero
df_select = df_select[df_select['Gender'].isin(descriçao_gender)]

# Filtrar por período
df_select = df_select[(df_select['Date'] >= calendario_inicio)
                      & (df_select['Date'] <= calendario_fim)]

# Se o sidebar estiver vazio
if df_select.empty:
    st.warning('No data available based on the current filter settings!')
    st.stop()

# Agora você pode calcular as métricas diretamente usando df_filtered

# Title
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# Criar métricas KPI
total_sales = int(df_select['Total'].sum())
avg_rating = round(df_select['Rating'].mean(), 1)
star_rating = ':star:' * int(round(avg_rating, 0))
avg_sales_by_transaction = round(df_select['Total'].mean(), 2)

# Colocar as métricas
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{avg_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {avg_sales_by_transaction}")

st.divider()

# Criar Gráfico fig1
st.header('Total $ x Product Line x Payment method')
fig1 = px.bar(df_select, x='Product line', y='Total', color='Payment')
fig1

# Criar Gráfico fig2
st.header('Sales Total x Product line')
fig2 = px.pie(df_select, values='Total', names='Product line', hole=0.5)
fig2

# Criar Gráfico fig3
st.header('Sales Quantity x Date')
fig3 = px.area(df_select, x='Date', y='Quantity', color='Product line')
fig3
