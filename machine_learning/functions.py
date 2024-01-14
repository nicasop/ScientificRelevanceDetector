import pandas as pd
import re
import nltk 
from pandas import *
import csv
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import math
import numpy as np
import time
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from sklearn.manifold import MDS
from sklearn.cluster import KMeans

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

def eliminar_stop_words_test(document):
    global n
    # while (comprobar_stop_words(lista)):
    # for cadena in lista:
    for token in document:
        if (token in n):
            document.remove(token)
    return document

def stemming_test(document):
    global stemmer
    # tit = []
    # aux = []
    # for cadena in lista:
    aux = []
    for token in document:
        aux.append(stemmer.stem(token))
        # tit.append(aux)
    return aux

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
    vector_titulos = []
    #Se eliminan las palabras repetidas
    for lista in titulos:
        vector_titulos.append(list(set(lista)))
    # print('\nlimpiar palabras repetidas: ',vector_titulos)

    #se vuelve a unir las palabras
    vector = [" ".join(frase) for frase in vector_titulos]
    # print('\ntitulos unidos: ',vector)

    for i in range(len(vector)-1):
        for j in range(i+1,len(vector)):
            # nueva_frase = ""
            lista = vector[i].split() + vector[j].split()
            # print('>>>>>>>>>lista: ',lista)
            aux.append(len(lista))

            lista1 = []
            for element in lista:
               if element not in lista1:
                   lista1.append(element)

            union.append(len(lista1))
            interseccion.append(aux[cont]- len(lista1))

            cont +=1
    indice = 0
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


def clean_collection(collection):
    collection_token = []
    for document in collection:
        documentaux = re.sub('[^A-Za-z0-9]+',' ', document) #eliminar caracteres especiales
        documentaux = documentaux.lower() # minusculas
        documentaux = documentaux.split() # tokenizacion
        documentaux = eliminar_stop_words_test(documentaux) # stop words
        documentaux = stemming_test(documentaux) # stemming
        collection_token.append(documentaux)
    
    return collection_token

def matricesDistancia(collections):
    inicio = time.time()
    titulos = collections['Titles'].tolist()
    keyword = collections['Keywords'].tolist()
    abstract = collections['Abstract'].tolist()

    ### limpiar documentos
    titulosTK = clean_collection(titulos)
    keywordTK = clean_collection(keyword)
    abstractTK = clean_collection(abstract)

    ### obtener matrices
    ### jaccard
    matriz = np.zeros((len(titulosTK), len(titulosTK)))
    matriz_keywords = np.zeros((len(keywordTK), len(keywordTK)))
    llenar_identidad(matriz)
    llenar_identidad(matriz_keywords)
    jacard(titulosTK,matriz)
    jacard(keywordTK,matriz_keywords)

    ###TFIDF
    vocabulario = []
    generar_vocabulario(abstractTK, vocabulario)
    matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstractTK)+1),dtype=object)
    frecuencia = []
    lista_wtf = [] 
    lista_df = []   
    lista_idf = []  
    lista_tf_idf = []  
    lista_modulo = [] 
    lista_normal = []   
    lista_abstract_final =[]   
    frecuencias(vocabulario, abstractTK,frecuencia)
    #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
    llenar_palabras_documentos(vocabulario, abstractTK, matriz_df_idf)
    llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
    #########Term Frecuency#############")
    #print(matriz_df_idf)
    print()
    #########Weight Document Frecuency#############")
    matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstractTK)+1),dtype=object)
    calcular_wtf(frecuencia, lista_wtf)
    llenar_palabras_documentos(vocabulario, abstractTK, matriz_wtf)
    llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
    #print(matriz_wtf)
    print()
    #########Document Frecuency#############")
    matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
    calcular_df(lista_wtf, lista_df,vocabulario)
    llenar_palabras_documentos(vocabulario, abstractTK, matriz_df)
    llenar_matriz2(lista_df,matriz_df,"DF: ")
    #print(matriz_df)
    print()
    #########Inverse Document Frecuency#############")
    matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
    calcular_idf(lista_df, abstractTK, lista_idf)
    llenar_palabras_documentos(vocabulario, abstractTK, matriz_idf)
    llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
    #print(matriz_idf)
    print()
    ######### TF - IDF#############")
    matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstractTK)+1),dtype=object)
    calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
    lista_tf_idf =redondear(lista_tf_idf)
    llenar_palabras_documentos(vocabulario, abstractTK, matriz_tf_idf)
    llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
    #print(matriz_tf_idf)
    print()
    ######### Matriz de distancias abstract #############")
    ####Modulo de la raiz normalizacion
    modulo_raiz(lista_wtf, lista_modulo, vocabulario)
    lista_normalizada(lista_wtf, lista_modulo,lista_normal)
    lista_normal =redondear(lista_normal)

    ###### Matriz de distancias Abstract #######
    matriz_distancia_abstrac(lista_normal,lista_abstract_final)
    matriz_distancia_abs = np.zeros((len(abstractTK),len(abstractTK)))
    llenar_matriz_Distancias(matriz_distancia_abs)
    llenar_valores_matriz_Distancias(matriz_distancia_abs,lista_abstract_final)
    llenar_valores_matriz_Distancias_re(matriz_distancia_abs,lista_abstract_final)
    #print(matriz_distancia_abs)
    print()
    ##### Matriz de distancias de titulos con 20%  ########")
    matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
    #print(matriz_tit_20)
    print()
    ##### Matriz de distancias de keywords con 30%  ########")
    matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
    #print(matriz_key_30)
    print()
    ######### Matriz de distancias abstract 50%#############")
    matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
    #print(matriz_abs_50)
    print()
    matriz_aux = np.add(matriz_tit_20,matriz_key_30)
    matriz_resultante = np.add(matriz_aux,matriz_abs_50)
    # print('++++++++++++++++++++++++++++++')
    # print(matriz_resultante)
    fin = time.time()
    print('tiempo de ejecucion: ', fin - inicio)

    return matriz,matriz_keywords,matriz_distancia_abs, matriz_resultante
    # return False,False,False,False

def matricesDistancia_exper(csv_path):
    #leer csv
    collections = pd.read_csv(csv_path)

    titulos = collections['Titles'].tolist()
    keyword = collections['Keywords'].tolist()
    abstract = collections['Abstract'].tolist()

    inicio = time.time()
    ### limpiar documentos
    titulosTK = clean_collection(titulos)
    keywordTK = clean_collection(keyword)
    abstractTK = clean_collection(abstract)

    ### obtener matrices
    ### jaccard
    matriz = np.zeros((len(titulosTK), len(titulosTK)))
    matriz_keywords = np.zeros((len(keywordTK), len(keywordTK)))
    llenar_identidad(matriz)
    llenar_identidad(matriz_keywords)
    jacard(titulosTK,matriz)
    jacard(keywordTK,matriz_keywords)

    ###TFIDF
    vocabulario = []
    generar_vocabulario(abstractTK, vocabulario)
    matriz_df_idf =  np.zeros((len(vocabulario)+1, len(abstractTK)+1),dtype=object)
    frecuencia = []
    lista_wtf = [] 
    lista_df = []   
    lista_idf = []  
    lista_tf_idf = []  
    lista_modulo = [] 
    lista_normal = []   
    lista_abstract_final =[]   
    frecuencias(vocabulario, abstractTK,frecuencia)
    #frecuencia = [[115,10,2,0],[58,7,0,0],[20,11,6,38]]
    llenar_palabras_documentos(vocabulario, abstractTK, matriz_df_idf)
    llenar_matriz(frecuencia, matriz_df_idf,"Fr: ")
    #########Term Frecuency#############")
    #print(matriz_df_idf)
    print()
    #########Weight Document Frecuency#############")
    matriz_wtf =  np.zeros((len(vocabulario)+1, len(abstractTK)+1),dtype=object)
    calcular_wtf(frecuencia, lista_wtf)
    llenar_palabras_documentos(vocabulario, abstractTK, matriz_wtf)
    llenar_matriz(lista_wtf, matriz_wtf,"WTF: ")
    #print(matriz_wtf)
    print()
    #########Document Frecuency#############")
    matriz_df = np.zeros((len(vocabulario)+1, 2),dtype=object)
    calcular_df(lista_wtf, lista_df,vocabulario)
    llenar_palabras_documentos(vocabulario, abstractTK, matriz_df)
    llenar_matriz2(lista_df,matriz_df,"DF: ")
    #print(matriz_df)
    print()
    #########Inverse Document Frecuency#############")
    matriz_idf = np.zeros((len(vocabulario)+1, 2),dtype=object)
    calcular_idf(lista_df, abstractTK, lista_idf)
    llenar_palabras_documentos(vocabulario, abstractTK, matriz_idf)
    llenar_matriz2(lista_idf,matriz_idf,"IDF: ")
    #print(matriz_idf)
    print()
    ######### TF - IDF#############")
    matriz_tf_idf = np.zeros((len(vocabulario)+1, len(abstractTK)+1),dtype=object)
    calcular_Tf_Idf(lista_idf, lista_wtf, lista_tf_idf)
    lista_tf_idf =redondear(lista_tf_idf)
    llenar_palabras_documentos(vocabulario, abstractTK, matriz_tf_idf)
    llenar_matriz(lista_tf_idf, matriz_tf_idf, "TF-IDF: ")
    #print(matriz_tf_idf)
    print()
    ######### Matriz de distancias abstract #############")
    ####Modulo de la raiz normalizacion
    modulo_raiz(lista_wtf, lista_modulo, vocabulario)
    lista_normalizada(lista_wtf, lista_modulo,lista_normal)
    lista_normal =redondear(lista_normal)

    ###### Matriz de distancias Abstract #######
    matriz_distancia_abstrac(lista_normal,lista_abstract_final)
    matriz_distancia_abs = np.zeros((len(abstractTK),len(abstractTK)))
    llenar_matriz_Distancias(matriz_distancia_abs)
    llenar_valores_matriz_Distancias(matriz_distancia_abs,lista_abstract_final)
    llenar_valores_matriz_Distancias_re(matriz_distancia_abs,lista_abstract_final)
    #print(matriz_distancia_abs)
    print()
    ##### Matriz de distancias de titulos con 20%  ########")
    matriz_tit_20 = np.around(np.matrix(matriz*0.20),2)
    #print(matriz_tit_20)
    print()
    ##### Matriz de distancias de keywords con 30%  ########")
    matriz_key_30 = np.around(np.matrix(matriz_keywords*0.30),2)
    #print(matriz_key_30)
    print()
    ######### Matriz de distancias abstract 50%#############")
    matriz_abs_50 =np.around(np.matrix(matriz_distancia_abs*0.50),2)
    #print(matriz_abs_50)
    print()
    matriz_aux = np.add(matriz_tit_20,matriz_key_30)
    matriz_resultante = np.add(matriz_aux,matriz_abs_50)
    # print('++++++++++++++++++++++++++++++')
    # print(matriz_resultante)
    fin = time.time()
    print('tiempo de ejecucion: ', fin - inicio)

    return matriz,matriz_keywords,matriz_distancia_abs, matriz_resultante



def get_heat_map_data(matriz):
    xAxis = [] #vector eje x
    yAxis = [] #vector eje y
    data = [] #vector data
    for i in range(len(matriz)):
        xAxis.append({
            'xaxis': 'D'+str(i+1)
        })

        yAxis.append({
            'yaxis': 'D'+str(i+1)
        })
        for j in range(len(matriz)):
            data.append({
                'yaxis': 'D'+str(i+1),
                'xaxis': 'D'+str(j+1),
                'value': matriz[i][j]
            })
    return xAxis, yAxis, data

def get_cluster_data(matriz, grupos=4):
    data = {
        'name': 'Classified Documents',
        'value': len(matriz)
    }

    #clusters
    clusters = []
    hc = AgglomerativeClustering(n_clusters = grupos, 
                        metric = 'euclidean', 
                        linkage = 'ward')
    y_hc = hc.fit_predict(matriz)

    y_hc_unique = list(set(y_hc))
    for cluster in y_hc_unique:
        filtered = list(filter(lambda element: element[1] == cluster,enumerate(y_hc)))
        children = [{'name': 'D' + str(child[0] + 1), 'value': int(child[1]),'children': []} for child in filtered]

        clusters.append({
            'name': 'Group '+str(cluster + 1),
            'value': len(filtered),
            'children': children
        })
    data.update({
        'children': clusters
    })
    return data

def get_scatter_data(matriz, tipoDis='euclidean',grupos=4):

    hc = AgglomerativeClustering(n_clusters = grupos, 
                        metric = 'euclidean', 
                        linkage = 'ward')
    y_hc = hc.fit_predict(matriz)

    mds = MDS(metric=True, dissimilarity=tipoDis, random_state=0)
    coordenadas = mds.fit_transform(matriz)

    colores = ['#0000FF', '#FFFF00', '#800080', '#008000']

    print('-------------------------------------')
    print(coordenadas)
    print('-------------------------------------')

    data = []
    for i in range(len(y_hc)):
        data.append({
            'x': coordenadas[i][0],
            'y':coordenadas[i][1],
            'color': colores[y_hc[i]],
            'value': 'D'+str(i+1)
        })

    return data