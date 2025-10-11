"""
Empleando el ejercicio visto en clase de Procesamiento con Ficheros. 
Supongamos que el precio brindado en el archivo “ventas.csv”  ha sido dato en dolares. 
Deberá solarizar el precio según la fecha de compra, 
para esto deberá leer la información almacenada de tipo de cambio de la base mongodb o sqlite (elegir una). 
Posteriormente debera obtener el precio total vendido (solarizado) por producto. 

Finalmente almacene dicha información en una colección de mongo db.
"""

from pymongo import MongoClient
from pymongoarrow.api import Schema
from pymongoarrow.monkey import patch_all
import pyarrow as pa
import pandas as pd
import requests
import re

# leo cadena de conexion
ruta_archivo = '/workspaces/ProgramacionPython202508/Modulo4/src/ventas.csv'
RUTA_CADENA_CONEXION = "/workspaces/ProgramacionPython202508/Modulo5/cadena_conexion_mongo_db.txt"
mongo_uri = open(RUTA_CADENA_CONEXION).read().strip()

# Aplica el monkey patch para usar pymongoarrow
patch_all()


def obtener_df_ventas(ruta_archivo:str)->pd.DataFrame:
    """ Lee el archivo ventas.csv y retorna un dataframe de pandas """
    
    df_ventas =  pd.read_csv(ruta_archivo, sep=',', header=None)
    df_ventas.columns = ['fecha_venta', 'product_name', 'cantidad', 'precio']

    print('Lectura de archivo ventas.csv finalizada')
    return df_ventas

def obtener_df_sunat(mongo_uri:str)->pd.DataFrame:
    """ Lee la coleccion sunat_julio y retorna un dataframe de pandas """

    with MongoClient(mongo_uri) as client:
        # Selecciona la base de datos y la colección
        db = client['my_db']
        collection = db['sunat']

        # Lee los datos desde MongoDB en un DataFrame de pandas usando pymongoarrow
        df = collection.find_pandas_all({})
        pass
    print('Lectura de coleccion sunat finalizada')
    return df

def procesamiento(df_ventas: pd.DataFrame, df_sunat: pd.DataFrame) -> pd.DataFrame:
    """ Procesa los datos de ventas y sunat para obtener el precio solarizado """

    # merge ventas_df y df_sunat
    df_ventas_consolidado = pd.merge(df_ventas, df_sunat, how='left', left_on='fecha_venta', right_on='fecha')
    df_ventas_consolidado.drop(columns=['origen','moneda','fecha'], inplace=True, axis=0)

    # calculos adicionales
    df_ventas_consolidado['precio_solarizado'] = df_ventas_consolidado.precio * df_ventas_consolidado.venta
    df_ventas_consolidado['subtotal'] = df_ventas_consolidado.precio_solarizado * df_ventas_consolidado.cantidad
    
    # agrupacion por producto
    df_agrupago = df_ventas_consolidado.groupby(['product_name']).agg(
        {'subtotal': 'sum'}
    )
    df_agrupago.reset_index(inplace=True, drop=False)

    print('Procesamiento finalizado ...')
    return df_agrupago


def envio_correo():
    return NotImplementedError



def main():
    # lectura df ventas
    df_ventas = obtener_df_ventas(ruta_archivo)
    df_sunat = obtener_df_sunat(mongo_uri)

    # procesamiento
    df_procesado = procesamiento(df_ventas, df_sunat)

    # guardamos el resultado en un archivo csv
    df_procesado.to_csv('/workspaces/ProgramacionPython202508/Modulo5/src/ventas_solarizadas.csv', index=False)

    # enviar por correo
    envio_correo()

    print('Proceso finalizado')


if __name__ == "__main__":
    main()
