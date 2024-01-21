from operator import truediv
from random import randint
from xml.etree.ElementTree import tostring

#Función para pasar un número de decimal a binario, teniendo cada número 6 dígitos
def dec_bin(n):
    bin = 0
    mult = 1
    while n != 0:
        bin = bin + n%2*mult
        n //= 2
        mult *= 10
            
    #Si el número en binario tiene menos de 6 dígitos se le añaden 0 a la izquierda
    toStr = str(bin)
    while (len(toStr) < 6):
        toStr = '0' + toStr 
   
    return toStr


def drum():
    while True:
        sumaTot=0
        lista = []  #Almacenará la clave
        #Quiero obtener 6 números "random" entre 1 y 14
        while (sumaTot!=27):
            lista.clear()
            for i in range(6):  
                lista.append(randint(1,14))

            #Debo comprobar que su suma es 27
            suma=0
            for n in lista:
                suma += n
            if (suma==27):
                sumaTot=27

        #Hago una lista con los números del 1 al 64 en binario
        listaBin = []
        for i in range(64):
            listaBin.append(dec_bin(i))

        #Con el algoritmo de las sumas compruebo que sea adecuado
        sumaVerify = []
        for i in range(64):
            sumaVerify.append(0)
            caracteres = list(listaBin[i])
            pos = 0

            for c in caracteres:
                if (c == '1'):
                    sumaVerify[i] += lista[pos]
                pos += 1
                    
            if (sumaVerify[i] > 25):
                sumaVerify[i] -= 26

        todos=0
        for i in range(25):
            if i in sumaVerify:
                todos = todos+1
        
        if todos == 25:
            #Si llega aquí ya tengo una clave adecuada según el algoritmo
            #luego puedo salir del while
            break   
   

    #Creamos el diccionario que definirá el estado del tambor indicando las orejetas colocadas
    tambor = {}
    orejetas = []
    necesarias = 0
    counter = 0
    for i in range(6):
        necesarias = lista[i] + counter
        for j in range(27):
            if(counter <= j < necesarias):
                orejetas.append(1)  
                counter += 1
            else:
                orejetas.append(0)
        tambor[i] = orejetas.copy()
        orejetas.clear()

    # Añadimos las barras de movimiento juntos con sus orejetas (seguimos un lug setting adecuado)
    tambor[0] += [1,1,1,1,1]
    tambor[1] += [0,1,1,1,1]
    tambor[2] += [0,0,1,1,1]
    tambor[3] += [0,0,0,1,1]
    tambor[4] += [0,0,0,0,1]
    tambor[5] += [0,0,0,0,0]            
    #La posicion 0 se corresponde con la primera columna por la izquierda y el array son las orejetas de las 32 barras de esa columna
    
    return tambor

# Para saber el número de orejetas en una columna (sin tener en cuenta las barras de desplazamiento)
def orejetasInCol(orejetas):
    num = 0
    for i in range(27):
        num += orejetas[i]
    return num

# Para saber el número de orejetas en barras de desplazamiento en una columna
def orejetasInColDespl(orejetas):
    num = 0
    for i in range(27, len(orejetas)):
        num += orejetas[i]
    return num