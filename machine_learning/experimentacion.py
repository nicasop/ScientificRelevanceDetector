from functions import matricesDistancia_exper
import pandas as pd
import io
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def graficoMapaCalor(m,m1,m2,m3):
    ##matriz exactas
    labels = [i for i in range(1,len(m)+1)]
    data = pd.DataFrame(m,columns=labels,index=labels)
    ##matriz computacion
    labels1 = [i for i in range(1,len(m1)+1)]
    data1 = pd.DataFrame(m1,columns=labels1,index=labels1)
    ##matriz medicina
    labels2 = [i for i in range(1,len(m2)+1)]
    data2 = pd.DataFrame(m2,columns=labels2,index=labels2)
    ##matriz sociales
    labels3 = [i for i in range(1,len(m3)+1)]
    data3 = pd.DataFrame(m3,columns=labels3,index=labels3)

    blue_cmap = sns.color_palette("Blues")
    red_cmap = sns.color_palette("Reds")
    green_cmap = sns.color_palette("Greens")
    
    
    fig, axs = plt.subplots(2, 2, figsize=(27, 10))

    sns.heatmap(data, ax=axs[0, 0], cmap=blue_cmap)
    axs[0, 0].set_title('Ciencias Exactas')

    sns.heatmap(data1, ax=axs[0, 1], cmap=red_cmap)
    axs[0, 1].set_title('Ciencias de la Computación')

    sns.heatmap(data2, ax=axs[1, 0], cmap=green_cmap)
    axs[1, 0].set_title('Medicina')

    sns.heatmap(data3, ax=axs[1, 1], cmap=blue_cmap)
    axs[1, 1].set_title('Ciencias Sociales')

    # Ajusta el diseño
    plt.tight_layout()

    plt.savefig('heatmap_general_multicolor.png', dpi=300, bbox_inches='tight')
    plt.show()

def graficoMapaCalor1(m):
    ##matriz total
    labels = [i for i in range(1,len(m)+1)]
    data = pd.DataFrame(m,columns=labels,index=labels)

    blue_cmap = sns.color_palette("Blues")
    red_cmap = sns.color_palette("Reds")
    green_cmap = sns.color_palette("Greens")
    
    
    plt.figure(figsize = (27,10) )

    sns.heatmap(data, cmap=blue_cmap)
    
    plt.title("Mapa de Calor General")

    # Ajusta el diseño
    plt.tight_layout()

    plt.savefig('heatmap_total.png', dpi=300, bbox_inches='tight')
    plt.show()

def boxplot(m,m1,m2,m3):
    distancias_flatten = m[np.triu_indices(m.shape[0], k=1)]
    distancias_flatten1 = m1[np.triu_indices(m1.shape[0], k=1)]
    distancias_flatten2 = m2[np.triu_indices(m2.shape[0], k=1)]
    distancias_flatten3 = m3[np.triu_indices(m3.shape[0], k=1)]

    data = {"Distancias": distancias_flatten}
    df = pd.DataFrame(data)

    data1 = {"Distancias": distancias_flatten1}
    df1 = pd.DataFrame(data1)

    data2 = {"Distancias": distancias_flatten2}
    df2 = pd.DataFrame(data2)

    data3 = {"Distancias": distancias_flatten3}
    df3 = pd.DataFrame(data3)

    fig, axs = plt.subplots(2, 2, figsize=(27, 10))

    # Crea un boxplot con Seaborn
    sns.boxplot(x="Distancias", data=df, ax=axs[0, 0], color="#add8e6")
    axs[0, 0].set_title('Ciencias Exactas')

    sns.boxplot(x="Distancias", data=df1, ax=axs[0, 1], color="#ffb6c1")
    axs[0, 1].set_title('Ciencias de la Computación')

    sns.boxplot(x="Distancias", data=df2, ax=axs[1, 0], color="#98fb98")
    axs[1, 0].set_title('Medicina')

    sns.boxplot(x="Distancias", data=df3, ax=axs[1, 1], color="#add8e6")
    axs[1, 1].set_title('Ciencias Sociales')
    
    # Ajusta el diseño
    plt.tight_layout()

    plt.savefig('boxplot.png', dpi=300, bbox_inches='tight')
    plt.show()

def vector_etiquetado(m,m1,m2,m3):
    matrix = []
    distancias_flatten = m[np.triu_indices(m.shape[0], k=1)]
    for distance in distancias_flatten:
        matrix.append(['Ciencias Exactas',distance])
    
    distancias_flatten1 = m1[np.triu_indices(m1.shape[0], k=1)]
    for distance in distancias_flatten1:
        matrix.append(['Ciencias de la Computación',distance])
    
    distancias_flatten2 = m2[np.triu_indices(m2.shape[0], k=1)]
    for distance in distancias_flatten2:
        matrix.append(['Medicina',distance])
    
    distancias_flatten3 = m3[np.triu_indices(m3.shape[0], k=1)]
    for distance in distancias_flatten3:
        matrix.append(['Ciencias Sociales',distance])
    
    print(matrix)

    datos = pd.DataFrame(matrix, columns=['Area del Conocimiento', 'Distancia'])

    # datos.to_csv('distancias.csv', index=False)
    datos.to_excel('distancias.xlsx', index=False, sheet_name='Hoja1')


mT,mK,mA,M = matricesDistancia_exper('./experimentacion/Exactas.csv')
mT1,mK1,mA1,M1 = matricesDistancia_exper('./experimentacion/Computacion.csv')
mT2,mK2,mA2,M2 = matricesDistancia_exper('./experimentacion/Medicina.csv')
mT3,mK3,mA3,M3 = matricesDistancia_exper('./experimentacion/Sociales.csv')
# mT_tot,mK_tot,mA_tot,M_tot = matricesDistancia_exper('./experimentacion/DataSet.csv')

# graficoMapaCalor(M,M1,M2,M3)
# boxplot(M,M1,M2,M3)
# graficoMapaCalor1(M_tot)
vector_etiquetado(M,M1,M2,M3)