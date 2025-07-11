""" 

                        Análisis de datos Proyecto Tech

   (1) Canasta Generación de energía eléctrica


Data sacada de: "Canasta de Generación de Energía Eléctrica - Sistema Interconectado Nacional (SIN)"
(https://datos.integrame.gov.co/publicdataset-detail/558f4e7d-4551-4f5f-8991-d920f5891ca6)

"""

# Librerías necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Cargar archivo csv
file_path="data/yuzcggxs.csv"
df=pd.read_csv(file_path)
# print(df.head())


"""  Exploración inicial """
print("Dimensiones dataset: ",df.shape)


"""    Tipo de data   """
# print(df.dtypes)

"""  Verificacíon de data(que no hayan datos nulos o vacios)"""
# print(df.isnull().sum())

"""  Elimina valores duplicados """
df=df.drop_duplicates()
#print("Dimensiones dataset: ",df.shape)


""" se validan datos nulos y con la media se rellenan para no alterar tanto la data """
num_cols=df.select_dtypes(include=["int64","float64"]).columns
df_clean=df.copy()
for col in num_cols:
    if df_clean[col].isnull().sum()>0:
        df_clean[col]=df_clean[col].fillna(df_clean[col].mean())
print("Dimension dataset limpio: ", df_clean.shape)


""" Identificación de Outliers """
# Calcular los cuartiles Q1(25%) y Q3(75%) de las columnas numéricas

q1=df_clean[num_cols].quantile(0.25)
q3=df_clean[num_cols].quantile(0.75)

# Calcular el rango intercuartílico (IRQ)
irq=q3-q1

# Identificar Outliers (Máscara booleana = oum) (verdadero o falso)
oum=(df_clean[num_cols]<(q1-1.5*irq))|(df_clean[num_cols]>(q3+1.5*irq))

# Contador de valores outliers 
outliers_counts=oum.sum()
print("Cantidad de valores outliers")
print(outliers_counts)
print(df_clean.head())

# Dataset sin outliers
df_clean_olr=df_clean.copy()

""" for col in num_cols:
    lower=q1[col]-1.5*irq[col] # Calcula el menor rango
    upper=q3[col]+1.5*irq[col] # Calcula el mayor rango
    df_clean_olr=df_clean_olr[(df_clean_olr[col]>=lower)&(df_clean_olr[col]<=upper)] """

print("Outlier del datsel limpio: ",df_clean_olr.shape)

#obtener data de x columna y mostrar los elementos sin repetirlos
#print(df_clean_olr["EnerSource"].unique())

# Sumar Bagazo y Biomasa
#df=df_clean_olr.copy()
df_clean_olr.loc[df["EnerSource"]=="BAGAZO","VALOR"]+=df_clean_olr.loc[df["EnerSource"]=="BIOMASA","VALOR"].sum()

# Sumar "JET-A1" y "GLP" en "COMBUSTOLEO"

df_clean_olr.loc[df["EnerSource"]=="COMBUSTOLEO","VALOR"]+=df_clean_olr.loc[df["EnerSource"].isin(["JET-A1","GLP"]),"VALOR"].sum()

# Eliminar "BIOMASA" , "JET-A1" y "GLP"
#dfuentes=df_clean_olr.copy()
dfuentes=df_clean_olr[~df_clean_olr["EnerSource"].isin(["BIOMASA","JET-A1","GLP"])]

#comprobacion de columnas eliminadas
#print(dfuentes["EnerSource"].unique())

print(dfuentes.EnerSource.value_counts())
dfuentes.EnerSource.value_counts()

#print(dfuentes["EnerSource"].unique())


"""                 Gráfico de Torta             """

fig, ax=plt.subplots(figsize=(12,14))
dfuentes.EnerSource.value_counts().plot(
    kind="pie",
    #labels=["Agua","Rad Solar","Gas","Carbon","Bagazo","Combustoleo","ACPM","Biogas"],
    ax=ax,
    wedgeprops={"edgecolor":"black","linewidth":0.5}
)

plt.ylabel("")
plt.legend(loc="upper right")
plt.title("Tipos de energía generada",fontsize=20)

plt.show()


