# Hackea la participación: Datos que construyen democracia

Dashboard desarrollado por el equipo **Código IPK** para visualizar la participación electoral histórica de las mujeres en México y hacer más accesible el análisis de los Conteos de Participación Ciudadana (CCPC) del INE.

## Características

- Exploración histórica de 2009 a 2024 mediante un selector de año.
- Mapa coroplético de participación por entidad federativa.
- Comparación de la participación entre estados y años.
- Ranking de los 15 estados con mayor número de votos emitidos.

## Estructura del proyecto

```text
codigo_ipk_ine_hackathon_2026/
├── app.py
├── README.md
├── requirements.txt
├── scripts/
│   └── generate_summary_file.py
└── steps/
    ├── compress_ccpc_data_1/
    └── process_geo_data_2/
        ├── voting_data.parquet
        └── matched_geo_data.geojson
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

## Uso

1. Abre la aplicación en el navegador.
2. Selecciona un año en el panel lateral, entre 2009 y 2024.
3. Consulta el mapa y el ranking actualizados para ese año.
4. Usa el mapa de calor para comparar la participación histórica entre entidades.

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

