#Importo librerias y funciones
import numpy as np 
from PIL import Image
import matplotlib.pyplot as plt
from Funciones import*


#COMIENZO DEL PROGRAMA

#Defino la imagen y le aplico el filtro
img_filtro = defino_imagen_a_encriptar()

#Defino el mensaje encriptado
msg_encriptado = encriptador()   

#Oculto el mensaje encriptado en la imagen
img_encriptada = encriptar_en_img(img_filtro,msg_encriptado)

#Exporto la imagen encriptada
guardar_img(img_encriptada)

