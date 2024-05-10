import numpy as np 
from PIL import Image
import matplotlib.pyplot as plt

#ARCHIVO CON LAS FUNCIONES DEL TP2

def filtro_kuwahara(img):
    '''
    Recibe como argumento una imagen y devuelve una nueva con el filtro kuwahara aplicado

    '''
    img_extendida = np.pad(img,((2,2),(2,2),(0,0)),mode="edge")     #Aplico padding de la imagen original
    filas, columnas, dimension = img_extendida.shape                #Obtengo las filas y columnas de la misma
    img_filtro =  np.copy(img)                        #Creo una imagen similar a la original que va a ser la modificada por el filtro  
    
    for fil in range(2,filas-2):             #Recorro la imagen pixel por pixel (sin contar los bordes extras del padding)
        for col in range(2, columnas-2):

            #Creo los cuadrantes a, b, c, d alrededor del pixel (utilizamos slicings de array)
            a = img_extendida[fil-2:fil+1 , col-2:col+1] 
            b = img_extendida[fil-2:fil+1 , col:col+3]
            c = img_extendida[fil:fil+3 , col:col+3] 
            d = img_extendida[fil:fil+3 , col-2:col+1]

            #Creo una lista con la suma de las varianzas de cada canal de color para cada cuadrante a, b, c, d
            varianzas = [ sum([np.var(cuadrante[:,:,dim]) for dim in range(3)]) for cuadrante in [a,b,c,d]]

            #Recorro las varianzas para obtener el cuadrante con menor variacion 
            min_varianza = 999999           
            cuadrante_min_varianza = a                              #seteo valores iniciales
            for cuadrante,varianza in zip([a,b,c,d],varianzas):     #Recorro los cuadrantes y sus varianzas
                if varianza < min_varianza:
                    min_varianza = varianza
                    cuadrante_min_varianza = cuadrante

            #Creo el nuevo pixel calculando la media de cada color del cuadrante con menor varianza
            pixel_media_colores = np.mean(cuadrante_min_varianza, (0,1)) 

            img_filtro[fil-2,col-2] = pixel_media_colores #Asigno el pixel creado a la imagen con filtro
    
    return img_filtro

def encriptador(msg):
    '''
    La funcion recibe un mensaje tipo string y lo devuelve codificado como una secuencia de numeros enteros.
    El metodo de encriptacion toma el mensaje a ocultar, lo pasa a minusculas y se convierte a una secuencia de números según el diccionario escrito. Se divide cada número en sus dígitos, y a cada digito se le suma 1. Se agrega un 0 al final del mensaje.
    '''
    dic = {
        'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12, 'm': 13,
        'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23, 'x': 24, 'y': 25, 'z': 26,
        ' ': 27, '.': 28, ',': 29, '?': 30, '!': 31, '¿': 32, '¡': 33, '(': 34, ')': 35, ':': 36, ';': 37, '-': 38, '“': 39,
        '‘': 40, 'á': 41, 'é': 42, 'í': 43, 'ó': 44, 'ú': 45, 'ü': 46, 'ñ': 47}
    
    #Creo que una lista con el codigo correspondiente para cada letra del mensaje
    lista_codigos = [dic[letra] for letra in (msg.lower())]

    lista_msg_encriptado = []
    for codigo in lista_codigos:                        #Recorro cada codigo de la lista
            for num in str(codigo):                     #Recorro cada digito del codigo
                lista_msg_encriptado.append(int(num)+1) #Le sumo uno y lo agrego a la lista final del msg encriptado
            lista_msg_encriptado.append(-1)             #Agrego un -1 al final de cada letra
    lista_msg_encriptado.append(0)                      #Agrego un 0 al final del mensaje
    msg_final = " ".join((str(digito) for digito in lista_msg_encriptado)) #Creo el string final con el mensaje codificado
    return msg_final
