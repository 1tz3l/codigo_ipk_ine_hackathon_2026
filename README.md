# Hackea la participación: Datos que construyen democracia

Dashboard desarrollado por el equipo **Código IPK** para visualizar la participación electoral histórica de las mujeres en México y hacer más accesible el análisis de los Conteos de Participación Ciudadana (CCPC) del INE.

<img width="1864" height="903" alt="dashboard-preview-2026-10-27" src="https://github.com/user-attachments/assets/48193de5-88cd-4f93-a422-e629cc073fa9" />

## Características

- Exploración de los procesos electorales de 2009, 2012, 2015, 2018, 2021 y 2024.
- Filtros por tipo de sección: urbana, mixta y rural, aplicables al mapa y al ranking.
- Mapa coroplético para comparar la participación por entidad federativa.
- Mapa de calor con la participación histórica de cada estado por año electoral.
- Ranking de las 12 entidades con más votos emitidos para el año y los filtros seleccionados.

## Estructura del proyecto

```text
codigo_ipk_ine_hackathon_2026/
├── app.py
├── assets/
│    ├── fonts/
│    │   ├── averia_sans
│    │   └── league-spartan
│    └── ine_200px.png
├── constants.py
├── ccpc_data/
│    ├── 2009/
│    ├── 2012/
│    ├── 2015/
│    ├── 2018/
│    ├── 2021/
│    └── 2024/
├── README.md
├── requirements.txt
│
└── steps/
│    ├── compress_ccpc_data_1/
│    └── process_geo_data_2/
│       ├── voting_data.parquet
│       └── matched_geo_data.geojson
└── style.css
```

## Requisitos

- Python 3.10 o una versión compatible.
- Acceso desde la raíz del proyecto a los archivos de datos procesados.

## Instalación y ejecución

Desde una terminal, ubícate en la raíz del proyecto:

```bash
cd codigo_ipk_ine_hackathon_2026
```

Crea y activa un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instala las dependencias:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Ejecuta la aplicación con Streamlit:

```bash
streamlit run app.py
```

Streamlit mostrará una URL local, normalmente `http://localhost:8501`, que puedes abrir en tu navegador.

### Comandos Bash

Desde la raíz del proyecto, puedes ejecutar la instalación completa en una terminal Bash:

```bash
cd codigo_ipk_ine_hackathon_2026
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app.py
```

## Uso

1. Abre la aplicación en el navegador.
2. Selecciona un año electoral en el panel lateral.
3. Opcionalmente, filtra por tipo de sección: urbana, mixta o rural. Si no seleccionas ninguna, se incluyen todos los tipos.
4. Consulta el mapa y el ranking de las 12 entidades con más votos emitidos, actualizados según el año y el filtro.
5. Usa el mapa de calor para comparar la participación histórica entre estados y años electorales.

## Datos

El dashboard utiliza información de los Conteos Censales de Participación Ciudadana (CCPC) del INE. Los datos y los polígonos geográficos procesados se encuentran en:

```text
steps/process_geo_data_2/voting_data.parquet
steps/process_geo_data_2/matched_geo_data.geojson
```

Los archivos dentro de `steps/` contienen los notebooks utilizados para comprimir los datos, asociar las entidades con el GeoJSON y revisar la información geográfica.

## Detener la aplicación

Presiona `Ctrl+C` en la terminal donde se está ejecutando Streamlit.

Para salir del entorno virtual:

```bash
deactivate
```

---

**Equipo Código IPK · 2026**

