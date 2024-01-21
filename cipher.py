from drum import *
from impressionWheel import *
from wheels import *

#La rueda normal imprime y luego imprime la de cifrado con un desplazamiento que viene dado por el numero de dientes en el engranaje,
# el numero de dientes se corresponde con el numero de barras del tambor que han sido desplazadas (las barras de desplazamineto no cuentan).
# Una barra es desplazada cuando, durante la revolución del tambor, una de sus orejetas hace contacto con un brazo guía activo.
# Un brazo guía está activo cuando la rueda que le corresponde (del 1 al 6 de izquierda a derecha) tiene un pin activo en esa posición de la rueda.
# Las barras de desplazamiento se encargan del avance de las ruedas (no añaden desplazamineto a la impresión). La 1ª rueda siempre avanza y 
# las demás dependerán de si hay un brazo guía activo en esa posición. Si está activo el de la posición 1 se moverán las 
# ruedas 2,3,4,5 y 6; si está activo el de la posición 2 se moverán la 3,4,5 y 6; etc. La barra 1 avanza la rueda 2, la barra 2 avanza la rueda 3...
# Luego está el desplazamiento de las ruedas de impresión entre sí usando el modo variable:
# primero imprime la primera y a la segunda se le aplica el desplazamiento,  en el modo variable este desplazamiento se aplica
# solo a la segundo rueda de impresión, mientras que en el constante se aplica a las dos.

#FUNCIÓN PARA CIFRAR/DESCIFRAR

def cipher_decipher(texto, texto1, texto2):
#En cifrado será texto, textoPlano, textoCifrado
#En descifrado será textoCifrado, textoPlano, textoDescifrado
    for letra in texto:
        texto1 += imprimeTextoR1(letra, ruedaImp1, ruedaImp2)

        # Comprobar el desplazamiento a aplicar empezando por la columna de la izquierda. También comprobamos las barras de desplazamiento
        barrasDesp = [1, 0, 0, 0, 0, 0]
        col = -1
        colDesp = 0
        barras = 0

        # ***Columnas 1-5***
        for i in range(5):
            col += 1    
            colDesp += 1
            # 1º miramos si el brazo guía está activo comprobando el pin de la posición de la rueda de esa columna
            if (isBrazoActivo(list(ruedas.values())[col], posRuedas[col])):
                # 2º si está activo comprobamos cuantas barras se verían desplazadas para añadir un paso a la rueda de impresión de cifrado
                barras += orejetasInCol(list(tambor.values())[col])
                # 3º comprobamos las barras de desplazaminto desplazadas a la izuqierda
                desplazamientos  = orejetasInColDespl(list(tambor.values())[col])
                for i in range(colDesp, len(barrasDesp)):
                    barrasDesp[i] += desplazamientos / (len(barrasDesp) - colDesp)
            # si no está activo pasamos a la siguiente columna
        
        # ***Columna 6***
        col += 1
        # 1º miramos si el brazo guía está activo comprobando el pin de la posición de la rueda de esa columna
        if (isBrazoActivo(list(ruedas.values())[col], posRuedas[col])):
            # 2º si está activo comprobamos cuantas barras se verían desplazadas para añadir un paso a la rueda de impresión de cifrado
            barras += orejetasInCol(list(tambor.values())[col])
            # En la última columna no es necesario comprobar las barras de desplazamiento

        # Tenemos el numero de pasos extra que se aplicarán a la rueda de impresión para el cifrado
        texto2 += imprimeTextoR2(ruedaImp1, ruedaImp2, barras, variable)

        # Tenemos el desplazamiento de cada rueda
        advanceWheels(ruedas, posRuedas, barrasDesp)

    return (texto, texto1, texto2)

#CONFIGURAMOS LAS RUEDAS Y EL TAMBOR

#Creamos las ruedas con sus pines y el tambor con sus orejetas. Tambien las ruedas de impresión con su desplazamiento inicial y se establece si 
#el modo será o no variable para las ruedas de impresión
ruedas, posRuedas = wheels()
tambor = drum()
n = int(input("\nDesplazamiento inicial de la rueda de impresión: "))
ruedaImp1, ruedaImp2 = impressionWheels(n)
variable = bool(input("\¿Quiere que sea variable? 1/0: "))  

#Debemos guardar la configuración inicial para cuando vayamos a descifrar
configInicial = {
    "ruedasI": ruedas,
    "posRuedasI": posRuedas.copy(), #Solamente es necesrio el .copy() en esta porque es la única que se modifica
    "tamborI": tambor,
    "ruedaImp": n
}

#CIFRADO 

print("\n-------> Proceso de cifrado")

#Se pide al usuario el texto a cifrar y se codifica pasándolo a mayúsculas y sustituyendo los espacios por 'X'
texto = input("Texto a cifrar: ").upper()
texto = texto.replace(" ", "X")

textoPlano = ""
textoCifrado = ""

#Al cifrar, esto se hace en grupos de 5 letras
#Para ello:
# 1. Separamos el texto en grupos de 5 caracteres
# 2. Aplicamos la función de cifrado a dichos grupos
# 3. Unimos el texto resultante


for i in range(0, len(texto), 5):   #for avanza de 5 en 5
    textoPlanoSeparado = ""
    textoCifradoSeparado = ""
    union = ""
    for j in range(i, i + 5):  #Ahora voy uniendo los caracteres de 5 en 5
        if j < len(texto):
            union = union + texto[j]
    union, textoPlanoSeparado, textoCifradoSeparado = cipher_decipher(union, textoPlanoSeparado, textoCifradoSeparado)

    #Uno al texto final los 5 caracteres nuevos
    textoPlano = textoPlano + textoPlanoSeparado
    textoCifrado = textoCifrado + textoCifradoSeparado

#texto, textoPlano, textoCifrado = cipher_decipher(texto, textoPlano, textoCifrado)

print("Texto codificado: ", textoPlano)
print("Texto cifrado: ", textoCifrado)

#DESCIFRADO

print("\n-------> Proceso de descifrado")

#Recuperamos la configuración inicial
ruedas = configInicial["ruedasI"] #no es realmente necesario porque no se modifica
posRuedas = configInicial["posRuedasI"]
tambor = configInicial["tamborI"] #no es realmente necesario porque no se modifica
ruedaImp1, ruedaImp2 = impressionWheels(configInicial["ruedaImp"])

textoDescifrado = ""

#El descifrado no se hace en grupos, sino directamente 
textoCifrado, textoPlano, textoDescifrado = cipher_decipher(textoCifrado, textoPlano, textoDescifrado)

print("Texto cifrado: ", textoCifrado)
print("Texto descifrado: ", textoDescifrado)
print("Texto original: ", textoDescifrado.replace("X", " "))