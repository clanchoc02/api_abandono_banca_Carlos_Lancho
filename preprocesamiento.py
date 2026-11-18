import numpy as np
import pandas as pd

def _descartar_columnas_no_utilizables(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina columnas no predictivas o con fuga de datos."""
    columnas_descarte = ['id_cliente', 'salario_mensual_aprox', 'comentarios_cliente', 'motivo_cancelacion']
    return df.drop(columns=columnas_descarte, errors='ignore')


def _sanitizar_centinelas_numericos(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte los centinelas o errores numéricos en np.nan."""
    df_res = df.copy()
    if 'edad' in df_res.columns:
        df_res.loc[(df_res['edad'] <= 0) | (df_res['edad'] > 120), 'edad'] = np.nan
    if 'ingresos_anuales' in df_res.columns:
        df_res.loc[df_res['ingresos_anuales'] <= 0, 'ingresos_anuales'] = np.nan
    if 'saldo_cuenta' in df_res.columns:
        df_res['saldo_cuenta'] = df_res['saldo_cuenta'].replace(-999, np.nan)
    return df_res

def _sanitizar_categoricos(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia la tipografía de los textos y unifica nulos categóricos."""
    df_res = df.copy()
    if 'tipo_cuenta' in df_res.columns:
        df_res['tipo_cuenta'] = df_res['tipo_cuenta'].astype(str).str.strip().str.capitalize()
        df_res['tipo_cuenta'] = df_res['tipo_cuenta'].replace({'Desconocido': np.nan, '?': np.nan, 'Nan': np.nan, 'nan': np.nan})

    if 'canal_preferido' in df_res.columns:
        df_res['canal_preferido'] = df_res['canal_preferido'].astype(str).str.strip()
        df_res['canal_preferido'] = df_res['canal_preferido'].replace({'???': np.nan, 'Nan': np.nan, 'nan': np.nan})

    if 'nivel_estudios' in df_res.columns:
        df_res['nivel_estudios'] = df_res['nivel_estudios'].astype(str).str.strip()
        df_res['nivel_estudios'] = df_res['nivel_estudios'].replace({'Nan': np.nan, 'nan': np.nan})

    return df_res

def _feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """Genera las nuevas variables de negocio y ajusta escalas temporales."""
    df_res = df.copy()
    if 'saldo_cuenta' in df_res.columns and 'ingresos_anuales' in df_res.columns:
        df_res['ratio_saldo_ingresos'] = df_res['saldo_cuenta'] / (df_res['ingresos_anuales'] + 1)

    if 'saldo_cuenta' in df_res.columns and 'num_productos' in df_res.columns:
        df_res['saldo_por_producto'] = df_res['saldo_cuenta'] / df_res['num_productos']

    if 'edad' in df_res.columns:
        limites_edad = [0, 30, 55, 120]
        etiquetas_edad = ['Joven', 'Adulto', 'Senior']
        df_res['grupo_edad'] = pd.cut(df_res['edad'], bins=limites_edad, labels=etiquetas_edad).astype(str)

    if 'antiguedad_meses' in df_res.columns:
        df_res['antiguedad_anios'] = df_res['antiguedad_meses'] / 12.0
        df_res = df_res.drop(columns=['antiguedad_meses'])

    return df_res

def preparar_datos_crudos(df_entrada: pd.DataFrame) -> pd.DataFrame:
    """Función unificadora que ejecuta las 4 operaciones de limpieza y FE."""
    df = df_entrada.copy()
    df = _descartar_columnas_no_utilizables(df)
    df = _sanitizar_centinelas_numericos(df)
    df = _sanitizar_categoricos(df)
    df = _feature_engineering(df)
    return df