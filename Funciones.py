import numpy as np 
from PIL import Image
import matplotlib.pyplot as plt

#ARCHIVO CON LAS FUNCIONES DEL TP2

def filtro_kuwahara(img : Image.Image) -> np.ndarray:
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

def encriptador() -> list:
    '''
    La funcion le pide al usuario un mensaje tipo string y lo devuelve codificado como una secuencia de numeros enteros.
    El metodo de encriptacion toma el mensaje a ocultar, lo pasa a minusculas y se convierte a una secuencia de números según el diccionario escrito. Se divide cada número en sus dígitos, y a cada digito se le suma 1. Se agrega un 0 al final del mensaje.
    '''
    dic = {
        'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12, 'm': 13,
        'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23, 'x': 24, 'y': 25, 'z': 26,
        ' ': 27, '.': 28, ',': 29, '?': 30, '!': 31, '¿': 32, '¡': 33, '(': 34, ')': 35, ':': 36, ';': 37, '-': 38, '“': 39,
        '‘': 40, 'á': 41, 'é': 42, 'í': 43, 'ó': 44, 'ú': 45, 'ü': 46, 'ñ': 47}
    
    msg =  input("Ingrese el mensaje a esconder: ") #Le pido al usuario que escriba un mensaje a encriptar

    #Creo que una lista con el codigo correspondiente para cada letra del mensaje
    lista_codigos = [dic[letra] for letra in (msg.lower())]

    lista_msg_encriptado = []
    for codigo in lista_codigos:                        #Recorro cada codigo de la lista
            for num in str(codigo):                     #Recorro cada digito del codigo
                lista_msg_encriptado.append(int(num)+1) #Le sumo uno y lo agrego a la lista final del msg encriptado
            lista_msg_encriptado.append(-1)             #Agrego un -1 al final de cada letra
    lista_msg_encriptado.append(0)                      #Agrego un 0 al final del mensaje
    # msg_final = " ".join((str(digito) for digito in lista_msg_encriptado)) #Creo el string final con el mensaje codificado
    return lista_msg_encriptado

def desencriptador(lista_encriptados : list) -> str:
    '''
    La funcion toma como parametro la lista de numeros encriptados que se extrajo de la imagen.
    Devuelve un string que seria el mensaje encriptado oculto
    '''
    dic = {
        1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e' , 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j', 11: 'k', 12: 'l', 13: 'm',
        14: 'n', 15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 's', 20: 't', 21: 'u' , 22: 'v', 23: 'w', 24: 'x', 25: 'y', 26: 'z',
        27: ' ', 28: '.', 29: ',', 30: '?', 31: '!' , 32: '¿' , 33: '¡', 34: '(', 35: ')', 36: ':' , 37: ';',38:  '-', 39: '“',
        40: '‘', 41: 'á', 42: 'é', 43: 'í', 44: 'ó', 45: 'ú', 46: 'ü', 47: 'ñ'}
    
    secuencia=[]
    sublista=[]
    for i in lista_encriptados:
        if i != -1:
            numero_real= i - 1
            secuencia.append(str(numero_real)) 
        else:
            secuencia.append(str(sublista))
            sublista = []
    if sublista:
        secuencia.append(str(sublista))

    valores=''.join(secuencia)

    valores_final=valores.split('[]')

    W=[int(j) for j in valores_final]

    desencriptado=''
    for n in W:
        if n in dic.keys():
            desencriptado += dic[n]

    return desencriptado

def defino_imagen_a_encriptar() -> np.ndarray:
    nombre_img = input("Ingrese nombre de la imagen a utilizar como base: ") #Le pido al usuario que ingrese el nombre de la imagen
    imagen = Image.open(nombre_img)                                          #Abro la imagen a encriptar
    img_arrey = np.array(imagen)                                             #La transformo en un array para poder trabajarla
    img_filtro = (filtro_kuwahara(img_arrey)) 
    return img_filtro

def defino_imagen_a_desencriptar() -> np.ndarray:
    '''
    Le solicita al usuario el nombre (y extension) de la imagen que se quiere desencriptar
    Devuelve el array de la imagen para poder trabajar
    '''
    nombre_img = input("Ingrese nombre a desencriptar: ")
    imagen = Image.open(nombre_img)
    img = np.array(imagen)
    return img

def guardar_img(img : np.ndarray) -> None:
    '''
    Recibe como argumento una imagen, le solicita al usuario un nombre y extension, y la guarda en la carpeta.
    '''
    nombre_img = input("Ingrese nombre del archivo de salida: ") #solicito al ususario un nombre para guardarla
    img_encriptada = Image.fromarray(img)                 #Convierto el array con el que estaba trabajando a formato img
    img_encriptada.save(nombre_img)                              #Guardo la imagen

def encriptar_en_img(img_filtro: np.ndarray ,msg_encriptado:list) -> np.ndarray:
    '''
    Se toma la imagen a encriptar con el filtro aplicado
    El metodo de encriptacion es el siguente:
    -De la imagen resultante se toman secciones de 2x2 pixeles.
    -En cada seccion se va a modificar el pixel de la esquina inferior derecha de la siguiente manera:
        -Se selecciona el canal de color con menor varianza entre los otros tres pixeles de la sección.
        -Se calcula el promedio del canal seleccionado de los mismos tres pixeles
        -Se suma el promedio calculado con el siguiente número del mensaje y se toma el módulo 256.
        -Se reemplaza el pixel con el nuevo valor.
    
    La funcion devuelve una imagen similar a la ingresada pero con ya el mensaje encriptado.
    '''
    filas, columnas, dimension = img_filtro.shape 

    #Compruebo que el mensage entre en la imagen
    capacidad_max = (filas//2)*(columnas//2)
    if len(msg_encriptado) > capacidad_max:
        raise ValueError("Error! El mensage es muy largo y no entra en la imagen") 

    for fil in range(1,filas,2):
        if len(msg_encriptado) == 0:        #Si ya se oculto todo el mensaje se termina el ciclo
            break
        for col in range(1,columnas,2):
            if len(msg_encriptado) == 0:    #Si ya se oculto todo el mensaje se termina el ciclo
                break

            #Creo un array en cada dimension del resto de los 3 pixeles del cuadrante 3x3
            canal_rojo = np.array([img_filtro[fil-1,col-1,0],img_filtro[fil-1,col,0],img_filtro[fil,col-1,0]])
            canal_verde = np.array([img_filtro[fil-1,col-1,1],img_filtro[fil-1,col,1],img_filtro[fil,col-1,1]])
            canal_azul = np.array([img_filtro[fil-1,col-1,2],img_filtro[fil-1,col,2],img_filtro[fil,col-1,2]])

            #Encuentro cual es la dimension con menor varianza
            min_varianza = 99999999999
            canal_min_varianza = canal_rojo
            dimension_canal = 0    
            for dim, canal in enumerate([canal_rojo,canal_verde,canal_azul]):
                if np.var(canal) < min_varianza:
                    min_varianza = np.var(canal)
                    canal_min_varianza = canal
                    dimension_canal = dim
            
            #Hago un promedio de colores con el canal de menor varianza
            prom_color = np.mean(canal_min_varianza)

            #Creo un nuevo valor de pixel con el prom de color mas el valor del msg encriptado
            nuevo_valor = prom_color + float(msg_encriptado.pop(0)) #Voy popeando uno por uno los valor del msg encriptado
            
            #Evaluo el modulo por si obtengo un valor fuera de rango
            (nuevo_valor - 255) if nuevo_valor > 255 else nuevo_valor

            #Le asigno el nuevo valor al pixel en el que me encuentro
            img_filtro[fil,col,dimension_canal] = nuevo_valor 

    return img_filtro          

def desencriptar_img(img : np.ndarray) -> list:
    '''
    Se toma la imagen a desencriptar y extraen los numeros ocultos en la misma.
    El metodo de desencriptacion es el siguiente:
    -Se empieza con una lista de números vacía.
   - Se toman secciones de 2x2 pixeles de la imagen encriptada.
    -En cada sección:
        -Calcular el canal de color con menor varianza entre los otros tres pixeles de la sección.
        -Calcular el promedio de los tres pixeles (todos menos inferior derecho) de la sección.
        -Restarle el promedio calculado al pixel inferior derecho.
        -En caso de quedar un número negativo distinto a -1, se le suma 256.
        -Se agrega este resultado a la lista de números.
        -Ir a la siguiente sección hasta encontrarse que el resultado sea 0.
    
    La funcion devuelve la lista con el los numeros del mensaje encriptado 
    '''
    filas, columnas, dimension = img.shape
    encriptado_numeros=[]

    for fil in range(1,filas,2):
        if encriptado_numeros and encriptado_numeros[-1] == 0:  #Si encuentra el ultimo digito "0" termina el ciclo
            break
        for col in range(1,columnas,2):
            if encriptado_numeros and encriptado_numeros[-1] == 0:   #Si encuentra el ultimo digito "0" termina el ciclo
                break

            #Creo un array en cada dimension del resto de los 3 pixeles del cuadrante 3x3
            canal_rojo = np.array([img[fil-1,col-1,0],img[fil-1,col,0],img[fil,col-1,0]])
            canal_verde = np.array([img[fil-1,col-1,1],img[fil-1,col,1],img[fil,col-1,1]])
            canal_azul = np.array([img[fil-1,col-1,2],img[fil-1,col,2],img[fil,col-1,2]])

            #Encuentro cual es la dimension con menor varianza
            min_varianza = 99999999999
            canal_min_varianza = canal_rojo
            dimension_canal = 0    
            for dim, canal in enumerate([canal_rojo,canal_verde,canal_azul]):
                if np.var(canal) < min_varianza:
                    min_varianza = np.var(canal)
                    canal_min_varianza = canal
                    dimension_canal = dim
            
            #Hago un promedio de colores con el canal de menor varianza
            prom_color = np.int64(np.mean(canal_min_varianza))
            
            #Obtengo el valor del pixel en el que estoy
            valor_pixel= img[fil,col,dimension_canal]
        
            #Obtengo el numero que estaba encriptado
            numero_encriptado = valor_pixel - prom_color

            #Compruebo que el valor no este fuera de rango
            (numero_encriptado + 256) if numero_encriptado < -1 else numero_encriptado
            
            #Lo agrego a la lista de numeros encriptados
            encriptado_numeros.append(numero_encriptado)

    return encriptado_numeros 
