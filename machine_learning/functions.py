import pandas as pd
import re
import nltk 
from pandas import *
import csv
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import math
import numpy as np

nltk.download('stopwords')
n = stopwords.words("english")
stemmer = PorterStemmer()


def minusculas(lista):
    tit = []
    for token in lista:
        tit.append(token.lower())
    return tit

def caracter_especiales(lista):
    tit = []
    for token in lista:
        tit.append(re.sub('[^A-Za-z0-9]+', ' ', token))
    return tit

def importacion_columnas(columna):
    url = "https://raw.githubusercontent.com/Freddy8-C/Proyecto_MachineLearning/master/csv/Proyecto.csv"
    data = pd.read_csv(url)
    columna = data[columna].tolist()
    return columna

def import_data_set():
    global url_archivo
    url = url_archivo
    data = pd.read_csv(url)
    return data

def importacion_columnas_serve(data,columna):
    columna = data[columna].tolist()
    return columna

def tokenizacion(lista):
    tit = []
    aux = []
    for token in lista:
        aux.append(token.split())   
    tit = aux
    return tit

def comprobar_stop_words(lista):
    global n
    for cadena in lista:
        for word in cadena:
            if (word in n):
               return True
    return False

def eliminar_stop_words(lista):
    global n
    while (comprobar_stop_words(lista)):
        for cadena in lista:
            for word in cadena:
                if (word in n):
                    cadena.remove(word)
    return lista

def stemming(lista):
    global stemmer
    tit = []
    aux = []
    for cadena in lista:
        aux = []
        for token in cadena:
            aux.append(stemmer.stem(token))
        tit.append(aux)
    return tit

def jacard (titulos,matriz):
    union = []
    aux = []
    interseccion = []
    cont = 0
    vector = []
    palabras_unidas =""
    vectoraux_titulos=[]
    vector_titulos = []
    #Se eliminan las palabras repetidas
    for lista in titulos:
        for palabra in lista:
            if palabra not in vectoraux_titulos:
                vectoraux_titulos.append(palabra)
       
        vector_titulos.append(vectoraux_titulos)
        vectoraux_titulos = []
    
    #se vuelve a unir las palabras
    for frase in vector_titulos:
        for palabra in frase:
            if ( palabras_unidas ==""):
                palabras_unidas = palabra
            else:
                palabras_unidas = palabras_unidas +" " +palabra
        vector.append(palabras_unidas)
        palabras_unidas = ""

    for i in range(len(vector)-1):
        for j in range(i+1,len(vector)):
            frase=""
            lista = []
            frase = vector[i] +" "+ vector[j]
            nueva_frase = ""
            lista = frase.split(" ")
            aux.append(len(lista))
           
            for element in lista:
               if element not in nueva_frase:
                   nueva_frase= nueva_frase +" "+element
            lista =nueva_frase.split(" ")
            lista.pop(0)
            union.append(len(lista))
            interseccion.append(aux[cont]- len(lista))
            cont +=1
    indice =0
    for i in range(len(matriz[1])):
        for j in range(len(matriz[1])):
            if (j > i):
                matriz[i][j]=round(interseccion[indice]/union[indice],2)
                indice +=1
    for i in range(len(matriz[1])):
         for j in range(len(matriz[1])):
             if (j < i):  
                matriz[i][j] = matriz[j][i]
                
def llenar_identidad(matriz):
    for i in range(len(matriz[1])):
        for j in range(len(matriz[1])):
            if(i == j):
                matriz[i][j]=1  

def generar_vocabulario(documentos,vocabulario):
    for documento in documentos:
        for palabra in documento:
            if(palabra not in vocabulario):
                vocabulario.append(palabra)

def frecuencias (vocabulario,abstract,frecuencia):
    lista_aux = []
  
    for lista in abstract:
        for palabra in vocabulario:
                lista_aux.append(lista.count(palabra))
        frecuencia.append(lista_aux)
        lista_aux = []
def llenar_palabras_documentos (vocabulario,abstract,matriz_df_idf):
    for i in range(len(matriz_df_idf)):
        
        for j in range(len(matriz_df_idf[1])):
            if(j== 0):
                if(i == 0):
                    matriz_df_idf[i][j]= "Terminos"
                else:
                    matriz_df_idf[i][j]= str(vocabulario[i-1])
            if(i==0 and j!=0):
                matriz_df_idf[i][j]= "Doc: "+ str(j)

def llenar_matriz (frecuencia,matriz_df_idf,texto):
    for i in range(len(frecuencia)):
        for j in range (len(frecuencia[i])):
            matriz_df_idf[j+1][i+1] = texto +str(frecuencia[i][j])
def llenar_matriz2 (frecuencia,matriz_df_idf,texto):
    
    for i in range(len(frecuencia)):
            matriz_df_idf[i+1][1] = texto +str(frecuencia[i])

def calcular_wtf (frecuencia,lista_wtf):
    lista_aux = []
    for lista_frecuencia in frecuencia:
        for dato in lista_frecuencia:
            if(dato > 0):
                lista_aux.append(round((math.log(dato,10))+1,2))
            else:
                lista_aux.append(0)
        lista_wtf.append(lista_aux)
        lista_aux=[]

def calcular_df (lista_wtf,lista_df,vocabulario):
    cont = 0
    index = 0
    for rep in range(len(vocabulario)):
        for lista in lista_wtf:
            if(lista[index]>0):
                cont+=1
        index+=1
        lista_df.append(cont)
        cont=0
def calcular_idf (lista_df,abstract,lista_idf):
    for dato in lista_df:
        #lista_idf.append(round(math.log(3/dato,10),2))
        lista_idf.append(round(math.log(len(abstract)/dato,10),2))

def calcular_Tf_Idf(lista_idf,lista_wtf,lista_tf_idf):
    for lista in lista_wtf:
        lista_tf_idf.append(np.multiply(lista,lista_idf))
     
def redondear(lista_tf_idf):
   lista = []
   lista_aux =[]
   for i in range(len(lista_tf_idf)):
       for j in range (len(lista_tf_idf[i])):
           lista_aux.append(round(lista_tf_idf[i][j],2))
       lista.append(lista_aux)
       lista_aux = []
   return lista


    
def modulo_raiz(lista_wtf,lista_modulo,vocabulario):
   
    acum = 0

    for lista in lista_wtf:
        for dato in lista:
            if(dato>0):
               acum = acum + dato**2
        lista_modulo.append(round(math.sqrt(acum),2))
        acum=0

def lista_normalizada(lista_wtf,lista_modulo,lista_normal):
    indice = 0
    for lista in lista_wtf:
        lista_normal.append(list(map(lambda x: x / lista_modulo[indice],lista)))
        indice+=1

def retorno_lista (array_lista):
    lista = []
    lista_aux= []
    for dato in array_lista:
        for lt in dato:
            lista_aux.append(lt)
        lista.append(lista_aux)
        lista_aux= []
    return lista

def matriz_distancia_abstrac(lista_normal,lista_abstract_final):
    lista_aux=[]
    for i in range(len(lista_normal)-1):
        for j in range(i+1,len(lista_normal)):
            lista_aux.append(np.multiply(lista_normal[i],lista_normal[j]))
        nueva = retorno_lista(lista_aux)
        for i in range(len(nueva)):
            lista_abstract_final.append(round(sum(nueva[i]),2))
        lista_aux=[]

def llenar_matriz_Distancias (matriz_distancia_abs):
    for i in range(len(matriz_distancia_abs)):
        for j in range(len(matriz_distancia_abs[1])):
            if( i== j ):
                matriz_distancia_abs[i][j]=1
                
def llenar_valores_matriz_Distancias(matriz_distancia_abs,lista_abstract_final):
    indice=0
    #print(len(matriz_distancia_abs)) len(matriz_distancia_abs)
    #print(len(lista_abstract_final)) len(matriz_distancia_abs[1])
    for i in range(0,len(matriz_distancia_abs)):
        for j in range(0,len(matriz_distancia_abs[1])):
            if (j > i):
                matriz_distancia_abs[i][j] =lista_abstract_final[indice]
                indice+=1
def llenar_valores_matriz_Distancias_re(matriz_distancia_abs,lista_abstract_final):

    indice=0
    for i in range(0,len(matriz_distancia_abs)):
        for j in range(0,len(matriz_distancia_abs[1])): 
            if (i < j):
                matriz_distancia_abs[j][i] =lista_abstract_final[indice]
                indice+=1

def llenardoc (tam,vector):
    for i in range(0,tam):
        vector.append("Doc "+str(i))