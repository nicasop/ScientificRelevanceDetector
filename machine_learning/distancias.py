import numpy as np
import time

from . import nlp
from . import jaccard
from . import tfIdf as tdf
from . import cosenoVectorial as cosV

def matrizDistanciaPonderada(matriz1,matriz2,matriz3,ponderacines):
    matrizDistancias = np.zeros((len(matriz1),len(matriz1)))
    i = j = 0
    while True:
        matrizDistancias[i][j] = matriz1[i][j]*ponderacines[0] + matriz2[i][j]*ponderacines[1] + matriz3[i][j]*ponderacines[2]
        j += 1
        if j ==  len(matriz1):
            j = 0
            i += 1
        if i == len(matriz1):
            break
    return matrizDistancias

def matricesDistancia (datos):
    # print('===========================')
    # print(datos)
    # print('+++++++++++++++++++++++++++')
    inicio = time.time()
    # titulos = datos['titulo'].tolist()
    # keywords = datos['keywords'].tolist()
    # abstracts = datos['abstract'].tolist()
    titulos = datos['Titles'].tolist()
    keywords = datos['Keywords'].tolist()
    abstracts = datos['Abstract'].tolist()

    ##NLP
    titulosL = nlp.limpiarDocumento(titulos,'en')
    keywordsL = nlp.limpiarDocumento(keywords,'en')
    abstractsL = nlp.limpiarDocumento(abstracts,'en')
    ##JACCARD
    #TITULOS
    matrizTit = jaccard.matrizJaccard(titulosL)
    #KEYWORDS
    matrizKey = jaccard.matrizJaccard(keywordsL)
    ##FULL INVERTED INDEX -- TF-IDF -- COSENO VECTORIAL
    #FULL INVERTED INDEX
    diccionario={'tokens':[],'ocurrencias':[]}
    diccionario['tokens']= nlp.indexacionToken(abstractsL)
    diccionario['ocurrencias'] = nlp.ocurrencias(diccionario['tokens'],abstractsL)
    #TF-IDF
    # matriz = tdf.bagWords(diccionario,abstractsL)
    wtf = tdf.matrizPTF(tdf.bagWords(diccionario,abstractsL))
    idf = tdf.IDF(tdf.documentF(wtf),len(abstractsL))
    tf_idf = tdf.TFIDF(wtf,idf)
    #Coseno Vectorial
    matrizAbs = cosV.matrizDistacias(cosV.matrizNormal(tf_idf))
    ##MATRIZ DE DISTACIAS
    ponderacion = [0.5,0.3,0.2]
    Distancias = matrizDistanciaPonderada(matrizAbs,matrizKey,matrizTit,ponderacion)
    fin = time.time()
    print('Tiempo de ejecución :',fin - inicio)
    return matrizTit,matrizKey,matrizAbs,Distancias