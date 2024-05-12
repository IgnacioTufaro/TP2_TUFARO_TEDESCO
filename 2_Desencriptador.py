#Importo librerias y funciones
import numpy as np 
from PIL import Image
import matplotlib.pyplot as plt
from Funciones import*


#COMIENZO DEL PROGRAMA

#Defino la imagen a desencriptar
img = defino_imagen_a_desencriptar()

#Obtengo la lista de numeros encriptados en la imagen
lista_num_encriptados = desencriptar_img(img)

#Desencripto la lista y obtengo el mensaje
msg_encriptado = desencriptador(lista_num_encriptados)

#Imprimo el mensaje en la terminal
print(msg_encriptado)
