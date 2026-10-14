import pandas as pd

input_path = "steps/process_geo_data_2/voting_data.parquet"

print("Cargando archivo parquet desde una subcarpeta...")
df_raw_parquet = pd.read_parquet(input_path)

print(f"Cantidad de filas originales: {len(df_raw_parquet):,}")

summary_df = (
    df_raw_parquet.groupby(["AELEC", "EDOCVE", "EDONOM", "SEXO", "EDAD"])[["SV", "NV"]]
    .sum()
    .reset_index()
)

print(f"Cantidad de filas en el archivo de resumen: {len(summary_df):,}")

# Guarda el nuevo archivo de resumen
output_path = "summary_voting_data.parquet"
summary_df.to_parquet(output_path, compression="snappy", index=False)

print(f"Se guardó exitosamente el archivo de resumen. Nombre: '{output_path}'")
