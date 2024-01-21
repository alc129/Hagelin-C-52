from random import randint

#Creación de las ruedas y las posiciones iniciales de las mismas
def wheels():
    #Partimos de la definición de las ruedas
    ruedas = {
        25 : [],
        26 : [],
        29 : [],
        31 : [],
        34 : [],
        37 : [],
        38 : [],
        41 : [],
        42 : [],
        43 : [],
        46 : [],
        47 : []
    }

    #Rellenamos con el número de pines adecuado
    for x,y in ruedas.items():
        for i in range(x):
            y.append(0)

    #Se eligen 6 de las 12 ruedas al azar, con un orden también elegido al azar
    ruedasSelected = []
    for i in range(6): 
        esta = 1
        while (esta == 1):  #Si una rueda ya ha sido seleccionada no puede volver a seleccionarse
            newWheel = randint(0,11)
            if  not (newWheel in ruedasSelected):
                esta = 0
        ruedasSelected.append(newWheel)

    #Wheels almacena las ruedas seleccionadas junto con sus pines
    counter = 0
    wheels = {}
    for x,y in ruedas.items():
        if counter in ruedasSelected:
            wheels[x] = y
        counter += 1


    #Para elegir qué pines se dejan activos y cuales no, se hace lanzando una moneda
    #Hay que intentar tener aproximadamente el 50% de los pines activos
    #pero para eso podemos suponer que al elegir cada uno como si se lanzase
    #una moneda, se hará 50/50 aproximadamente
    for x,y in wheels.items():
        y[0] = randint(0,1)
        y[1] = randint(0,1)
        y[2] = randint(0,1)
        for i in range(3,x): 
            pin = randint(0,1)      #Como si se lanzase la moneda
            #No debe haber más de 3 pines activos seguidos
            if (y[i-1] != pin or y[i-2]!= pin or y[i-3] != pin):    
                y[i] = pin
            else:
                if (pin == 0):
                    y[i] = 1
                else:
                    y[i] = 0

    posWheels = [0,0,0,0,0,0]

    # Determina la posición inicial de cada rueda, recibiéndola por teclado
    message = ''
    i=0
    while i in range(6):
        message = "\nRango de 0 a " + str(list(wheels.keys())[i] - 1) + ' ---> Posicion inicial rueda ' + str(i + 1) + ': '
        ran = int(input(message))
        if 0 <= ran <= (list(wheels.keys())[i] - 1): #Comprueba que la posición esté en el rango adecuado
            posWheels[i] = ran                          #y establece la posición inicial de cada rueda
            i+=1
        else:
            print("ERROR. No pertenece al rango adecuado")
            
    return (wheels, posWheels)

#Avanza las ruedas el número de pasos necesarios
def advanceWheels(wheels, posWheels, steps):
    for i in range(len(posWheels)):
        posWheels[i] = int((posWheels[i] + steps[i]) % list(wheels.keys())[i]) 

#Comprueba si hay un pin activo en la posición actual
def isBrazoActivo(rueda, pos):
    if(rueda[pos]):
        return True
    else:
        return False