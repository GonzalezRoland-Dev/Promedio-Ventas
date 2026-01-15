import streamlit as st
import pandas as pd

st.title("📊 Promedio de Ventas - Reporte Automático")

# Subida de archivos
archivos = st.file_uploader(
    "Subí tus archivos Excel (.xlsx)", 
    type=["xlsx"], 
    accept_multiple_files=True
)

# Inputs para columnas
col_fecha = st.text_input("Nombre de la columna de fecha", "Fecha")
col_ventas = st.text_input("Nombre de la columna de ventas", "Ventas")

# Botón de ejecución
if st.button("Procesar"):
    if archivos:
        lista_df = [pd.read_excel(f) for f in archivos]
        df_total = pd.concat(lista_df, ignore_index=True)

        # Convertir fechas y ordenar
        df_total[col_fecha] = pd.to_datetime(df_total[col_fecha], errors="coerce")
        df_total = df_total.sort_values(by=col_fecha)

        # Calcular promedio
        promedio = df_total[col_ventas].mean()

        # Mostrar resultados
        st.success(f"✅ Promedio total de ventas: {promedio:.2f}")
        st.dataframe(df_total)

        # Descargar Excel final
        nombre_salida = "promedio_ventas.xlsx"
        with pd.ExcelWriter(nombre_salida, engine="openpyxl") as writer:
            df_total.to_excel(writer, index=False, sheet_name="Reporte")
            workbook = writer.book
            worksheet = writer.sheets["Reporte"]
            ultima_fila = len(df_total) + 2
            worksheet.cell(row=ultima_fila, column=1, value="PROMEDIO TOTAL:")
            worksheet.cell(row=ultima_fila, column=2, value=promedio)

        with open(nombre_salida, "rb") as f:
            st.download_button(
                label="⬇️ Descargar reporte Excel",
                data=f,
                file_name=nombre_salida,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.error("⚠️ Tenés que subir al menos un archivo Excel.")