import math
import sys
import csv
from turtle import *
import numpy as np
import matplotlib.pyplot as plt

asociados = dict()
nombres = dict()
asociados = {"Cante": "20162032003", "Monrroy": "20152032010",}
nombres = {"Cante": "Daniel", "Monrroy": "Paula",}
#################################################################################################################################
#[CARTERA DE CALCULO DE POLIGONAL POR EL METODO DE LA BRUJULA]

def rosa():
    theta = []          #Theta define los centros mediante ángulos en radianes
    Amplitud = []
    Contraccion = []
    print("D I B U J O   D E L    D I A G R A M A   D E   O B S T A C U L O S")
    #N = int(input("Numero de obstaculos: ")) # este es le numero de sombras
    i = 1
    fin = 0
    while fin <= 359:
        print(" ")
        print("Obstaculo #",i)
        if i == 1:
            inicio = 0
            print(" ")
            print("ALERTA: Inicio desde el norte (0)")
        else:
            inicio = float(input("¿Desde donde inicia? (ángulo en grados): "))
        fin = float(input("¿Donde finaliza? (ángulo en grados): "))
        centro = (((inicio + fin)/2) * np.pi)/180
        theta.append(centro)
        Amp = ((inicio - fin) * np.pi)/180
        Amplitud.append(Amp)
        Cont = float(input("¿Angulo de elevación?  (ángulo en grados): "))   #La contracción
        Contraccion.append(Cont)
        i += 1

    ax = plt.subplot(111, projection='polar')
    ax.bar(theta, Contraccion, Amplitud, bottom=0, color= "red", alpha=0.5)
    ax.set_ylim(90,0)
    plt.title("Diagrama de obstáculos")

    ax.set_theta_zero_location("N")  #Define el 0 en el norte, como lo conocen los topográfos
    ax.set_theta_direction(-1) #Los ángulos se mueven con las manecillas del reloj
    #ax.grid(False) #Quita los ejes

    plt.show()

def graficame(entrada):
    datos = entrada
    estePLACE = len(datos[2]) - 2
    nortePLACE = len(datos[2]) - 1
    title("Graficación de la poligonal")  #Ponle titulo a la ventana
    setup(600, 500, 0, 0)  #Defines el tamaño de la ventana (ancho,alto)
    screensize(150, 150)
    colormode(255) #color de los puntos, desde 1 hasta 255 (despues o antes da error)
    pensize(15) #Ajusta el grosor del lápiz, aunque en grandes extensiones no se nota, pero tampoco importa mucho
    tortuga = Turtle() #Recuerda definir siempre tortuga.FUNCION puesto que si no, no tomará las características dadas
    mineste = 700000000
    minnorte = 700000000
    maxeste = 0             #se definen las variables para hallar valores max y minimos
    maxnorte = 0
    n = 0  #inicia un contador
    for lista in datos: #este pequeño bucle busca las coordenadas este y norte maximas y minimas para definir la escala
        if n == 0:
            n += 1
            continue   #la primera lista contiene las palabras "delta, norte y este" asi que la salto porque no sirve para nada
        esteobs = datos[n][estePLACE]
        if esteobs > maxeste:
            maxeste = esteobs
        if esteobs < mineste:
            mineste = esteobs
        norteobs = datos[n][nortePLACE]
        if norteobs > maxnorte:
            maxnorte = norteobs
        if norteobs < minnorte:
            minnorte = norteobs
        n += 1

    setworldcoordinates(mineste, minnorte, maxeste, maxnorte) #define la escala (x1 min, y1 min, x2 max, y2 max)


    tortuga.penup()  #este comnando levanta el lápiz para llevarlo hasta las coordenadas de inicio
    tortuga.speed(0)  #este comando activa el turbo del lapiz para que llegue rapido a las coordenadas de inicio de la poligonal, ya que siempre inicia en 0,0
    tortuga.goto(datos[1][estePLACE],datos[1][nortePLACE])   #este comando dirige el lápiz hacia las coordenadas de inicio
    tortuga.pendown()  #este comando pone el lápiz en el papel, de acá empieza a dibujar
    deltas = len(datos) - 1   #hacemos un conteo de deltas a dibujar
    n = 1 #inicia un contador
    while n <= deltas:
        tortuga.goto(datos[n][estePLACE],datos[n][nortePLACE])   #grafica cada linea
        tortuga.dot(8,255,0,0)                  #pone un punto en el vertice para señalar el sitio del delta
        tortuga.write(datos[n][0])              # escribe el nombre del delta
        n += 1                                  #aumenta el contador para graficar lasiguiente linea


    tortuga.hideturtle() #Esta linea esconde el cursor que dibuja la figura
    done() #Este comando finaliza el codigo

def archivoniv():
    datos= [] #Crea una lista vacia para almacenar los datos del archivo
    datos.append(["PUNTO","HS","HM","HI","HS","HM","HI","PUNTO","V+","V-"])
    print(" ")
    print("Digite a continuación la ruta del archivo (Con el archivo, en formato CSV) [O pulse enter para ejecutar el archivo de ejemplo adjunto en el mismo directorio]")
    ruta = input("ruta: ") #se introduce la ruta del archivo
    print(" ")
    sep = input("Defina ahora el separador del archivo .csv (digite '.' o bien ',' o bien ';' [o también enter para ';']: )") #Se define el separador del csv
    if len(sep) <1:  #se define el valor por defecto si se pulsó enter para el separador
        sep = ';'
    if len(ruta) <1: #se define el valor por defecto si se pulsó enter para el archivo a trabajar
        ruta = 'niv.csv' #Archivo de ejemplo debe estar en la misma carpeta que este documento
    rutaR = open(ruta) #establece una conexion

    n = 0  #iniciamos un contador
    for linea in rutaR:      #un bucle para analizar cada linea del archivo
        linea = linea.split(sep)   #separador del archivo csv

        if n == 0: #se salta la primera linea ya que solo contiene los titulos de los campos
            n += 1
            continue

########## # Nivelación # ######################################################

        puntovmas = linea[0]                                        #0 Nombre cambio
        try:
            vmasnhs = float(linea[1].replace(",", "."))             #1 V+ Hilo superior
            vmasnhm = float(linea[2].replace(",", "."))             #2 V+ Hilo medio
            vmasnhi = float(linea[3].replace(",", "."))             #3 V+ Hilo inferior
        except:
            vmasnhs = 0             #1 V+ Hilo superior
            vmasnhm = 0             #2 V+ Hilo medio
            vmasnhi = 0             #3 V+ Hilo inferior
        try:
            vmennhs = float(linea[4].replace(",", "."))             #4 V- Hilo superior
            vmennhm = float(linea[5].replace(",", "."))             #5 V- Hilo medio
            vmennhi = float(linea[6].replace(",", "."))             #6 V- Hilo inferior
        except:
            vmennhs = 0             #4 V- Hilo superior
            vmennhm = 0            #5 V- Hilo medio
            vmennhi = 0            #6 V- Hilo inferior
######### # Contranivelación # #################################################
        puntovmen = linea[7]                                        #7 Nombre cambio
        try:
            vmas = float(linea[8].replace(",", "."))                #8 V+ contranivelación
        except:
            vmas = 0
        try:
            vmen = linea[9].rstrip()
            vmen = float(vmen.replace(",", "."))                    #9 V- contranivelacións
        except:
            vmen = 0
        datos_linea = [puntovmas, vmasnhs, vmasnhm, vmasnhi, vmennhs, vmennhm, vmennhi, puntovmen, vmas, vmen]
        datos.append(datos_linea.copy())

        n += 1
    return datos

#Halla el error de la nivelación
def error(lista):
    n = 0
    Svmasniv = 0
    Svmenosniv = 0
    Svmasc = 0
    Svmenosc = 0
    for minilista in lista:
        if n ==0:
            n += 1
            continue
        vmasniv = minilista[2]
        vmenosniv = minilista[5]
        vmasc = minilista[8]
        vmenosc = minilista[9]
###### # Nivelación # ######################################
        Svmasniv += vmasniv
        Svmenosniv += vmenosniv
        Svmasc += vmasc
        Svmenosc += vmenosc
    Nerr = Svmasniv - Svmenosniv
    Cerr = Svmasc - Svmenosc
    if Nerr < Cerr:
        error = Nerr + Cerr
        m = -1
    else:
        error = Nerr - Cerr
        m = 1
    error = round(error,3)
    ERROR = [error, Svmasniv, Svmenosniv, Svmasc, Svmenosc, m]
    return ERROR

def brujMAN:
    print("En proceso")

def brujArchivo:
    print("En proceso")
#Resuelve la nivelación por el metodo de los cambios
def NivCambios(lista):
    nivelacion = []
    nivelacion.append(["PUNTO", "V+", "ALT INS", "V-", "COTA"])
    cota = float(input("Cota de inicio de la nivelación?: "))
    puntoN = 0
    VmasN = 0
    altN = 0
    VmenN = 0
    n = 0
    cont = len(lista)
    for minilista in lista:
        if n ==0:
            n += 1
            continue
        puntoN = minilista[0]
        VmasN = minilista[2]
        VmenN = minilista[5]
        if n == 1:
            cotaN = cota
        else:
            cotaN = altN - VmenN
            cotaN = round(cotaN,3)
        altN = VmasN + cotaN
        altN = round(altN,3)
        if n == (cont-1):
            altN = 0
        datos_minilista = [puntoN, VmasN, altN, VmenN, cotaN]
        nivelacion.append(datos_minilista.copy())
        n += 1
####### # Contranivelación # ###################################################
    cnivelacion = []
    cnivelacion.append(["PUNTO", "V+", "ALT INS", "V-", "COTA"])
    cotac = nivelacion[n-1][4]
    print("cota de la contra: ",cotac)
    puntoN = 0
    VmasN = 0
    altN = 0
    VmenN = 0
    n = 0
    cont = len(lista)
    for minilista in lista:
        if n ==0:
            n += 1
            continue
        puntoN = minilista[7]
        VmasN = minilista[8]
        VmenN = minilista[9]
        if n == 1:
            cotaN = cotac
        else:
            cotaN = altN - VmenN
            cotaN = round(cotaN,3)
        altN = VmasN + cotaN
        altN = round(altN,3)
        if n == (cont-1):
            altN = 0
        datos_cminilista = [puntoN, VmasN, altN, VmenN, cotaN]
        cnivelacion.append(datos_cminilista.copy())
        n += 1

    ERR = error(lista)
    print(" ")

    print('='*150)
    print('{:^100}'.format('PARAMETROS NIVELACIÓN Y CONTRANIVELACIÓN'))
    print('='*150)
    print('{:^25}'.format('NIVELACIÓN'), '{:^40}'.format('CONTRANIVELACIÓN'), sep='\t')
    print('='*150)

    print('{:^10}'.format("∑V+"),'{:^10}'.format(round(ERR[1],3)), '{:^20}'.format("∑V+"), '{:^10}'.format(round(ERR[3],3)),  sep='\t')
    print('{:^10}'.format("∑V-"),'{:^10}'.format(round(ERR[2],3)), '{:^20}'.format("∑V-"), '{:^10}'.format(round(ERR[4],3)),  sep='\t')
    print('{:^8}'.format("∆h"),'{:^10}'.format(round(ERR[1]-ERR[2],3)), '{:^18}'.format("∆h"), '{:^10}'.format(round(ERR[3]-ERR[4],3)),  sep='\t')
    print(" ")
    print('{:^10}'.format("Error de la nivelación: "),'{:^5}'.format(ERR[0]),  sep='\t')
    print('{:^10}'.format("Corrección: "),'{:^30}'.format(ERR[0]/cont),  sep='\t')

    print('='*150)
    print(' ')
    #print(nivelacion)
##### # Corrección # ###########################################################
    corrindividual = (ERR[0]/cont)
    m = ERR[5]
    correccion = []
    correccion.append(["PUNTO", "V+", "ALT INS", "V-", "COTA", "CORRECCION", "COTA CORR"])
    puntoN = 0
    VmasN = 0
    altN = 0
    VmenN = 0
    n = 0
    for minilista in lista:
        if n ==0:
            n += 1
            continue
        puntoN = minilista[0]
        VmasN = minilista[2]
        VmenN = minilista[5]
        if n == 1:
            cotaN = cota
        else:
            cotaN = (altN - VmenN)
            cotaN = round(cotaN,3)
        altN = VmasN + cotaN
        altN = round(altN,3)
        if n == (cont-1):
            altN = 0
        correcc = round((n-1)*corrindividual,3)
        cotacorr = round( cotaN + m*correcc ,3)
        datos_minilista = [puntoN, VmasN, altN, VmenN, cotaN, correcc, cotacorr]
        correccion.append(datos_minilista.copy())
        n += 1

    print('='*150)
    print('{:^15}'.format('PUNTO'), '{:^10}'.format('V+'), '{:^10}'.format('ALT INS'), '{:^10}'.format('V-'), '{:^10}'.format('COTA'), '{:^10}'.format('CORRECCION'),'{:^10}'.format('COTA CORREGIDA'), sep='\t')
    print('='*150)

    i = 0

    for dato in correccion: #imprime cada dato de las listas pequeñas
        if i == 0:
            i += 1
            continue

        print('{:^15}'.format(dato[0]),'{:^10}'.format(dato[1]), '{:^10}'.format(dato[2]), '{:^10}'.format(dato[3]), '{:^10}'.format(dato[4]),'{:^10}'.format(dato[5]),'{:^10}'.format(dato[6]), sep='\t')

        i += 1

    print('='*150)

    return correccion

#Resuelve la nivelación por el metodo de las distancias
def NivDistancias(lista):
    nivelacionD = []
    nivelacionD.append(["PUNTO", "V+", "ALT INS", "V-", "COTA", "Dist", "Dist Acum"])
    cota = float(input("Cota de inicio de la nivelación?: "))
    puntoN = 0
    VmasN = 0
    altN = 0
    VmenN = 0
    n = 0
    cont = len(lista)
    dist = 0
    distvmas = 0
    distvmen = 0
    distA = 0
    for minilista in lista:
        if n ==0:
            n += 1
            continue
        puntoN = minilista[0]
        VmasN = minilista[2]
        VmenN = minilista[5]
        if n == 1:
            cotaN = cota
        else:
            cotaN = altN - VmenN
            cotaN = round(cotaN,3)
        altN = VmasN + cotaN
        altN = round(altN,3)

        if n == (cont-1):
            altN = 0

        if n == 1:
            distvmen = 0
        else:
            distvmen = (minilista[4] - minilista[6])*100
            dist = round( distvmas + distvmen ,3)
            distA += dist
            distA = round(distA,3)
        distvmas = ( minilista[1] - minilista[3] )*100

        datos_minilista = [puntoN, VmasN, altN, VmenN, cotaN, dist, distA]
        nivelacionD.append(datos_minilista.copy())
        n += 1

    nivelacionDist = []
    nivelacionDist.append(["PUNTO", "V+", "ALT INS", "V-", "COTA", "Dist", "Dist Acum", "COTA CORR"])
    err = error(lista)
    errorniv = err[0]
    disttot = nivelacionD[n-1][6]
    n = 0
    for minilista in nivelacionD:
        if n ==0:
            n += 1
            continue
        corr = (errorniv * minilista[6])/disttot
        cotacorr = minilista[4] - corr
        minilista.append(round(cotacorr,3))
        nivelacionDist.append(minilista.copy())
        n += 1


    print("error: ",errorniv,"distancia total: ", disttot)
    #print(lista)
    print('='*150)
    print('{:^10}'.format('PUNTO'), '{:^5}'.format('V+'), '{:^10}'.format('ALT INS'), '{:^10}'.format('V-'), '{:^10}'.format('COTA'), '{:^10}'.format('Dist'), '{:^10}'.format('Dist acum'),  '{:^10}'.format('COTA CORREGIDA'), sep='\t')
    print('='*150)

    i = 0

    for dato in nivelacionDist: #imprime cada dato de las listas pequeñas
        if i == 0:
            i += 1
            continue

        print('{:^10}'.format(dato[0]),'{:^5}'.format(dato[1]), '{:^10}'.format(dato[2]), '{:^10}'.format(dato[3]), '{:^10}'.format(dato[4]), '{:^10}'.format(dato[5]), '{:^10}'.format(dato[6]), '{:^10}'.format(dato[7]), sep='\t')

        i += 1

    print('='*150)

    return nivelacionDist

#Entra al menu de resolución de la nivelación
def niv():
    #datos.append (['DELTA', 'PUNTO', 'DIST', 'AZIMUTH', 'PRY X', 'PRY Y','L2','D2','LD','LD2', 'PRY X COREG', 'PRY Y COREG', 'COORD X', 'COORD Y'])

    print()
    print('='*168)
    print()
    print('{:^173}'.format('CARTERA DE CALCULO DE NIVELACIÓN'))
    print()
    print('='*168)
    print()
    datos = archivoniv()
    print("Cartera cargada satisfactoriamente")
    print(" ")
    cambios = len(datos) - 1
    print("Cambios de la nivelación: ", cambios)

############ # Menú de resolución # ############################################
    print('{:^10}'.format('='*168))
    print('{:^43}'.format('¿CÓMO DESEA AJUSTAR LA NIVELACIÓN?')) #menu principal
    print(" ")
    print('{:^58}'.format('0) AJUSTE POR CAMBIOS'))
    print('{:^60}'.format('1) AJUSTE POR DISTANCIAS'))
    print(" ")
    w = int(input("Digite opción: "))
    print(" ")
    if w == 0:
        Nivelacion = NivCambios(datos)
        d = 0
    elif w == 1:
        Nivelacion = NivDistancias(datos)
        d = 1
    else:
        print("No ha seleccionado una opción válida")


    print(" ")
    w = int(input("¿Desea graficar el perfil del circuito? (1:Sí - 0:No): "))
    if w == 0:
        w = 5
    else:
        if d == 0:
            PLACE = len(Nivelacion[1]) - 1
            circ = []
            circ.append(["Nombre", "Dist", "Cota"])
            n = 0
            for minilista in Nivelacion:
                if n == 0:
                    n += 1
                    continue
                nombre = minilista[0]
                cota = minilista[PLACE]
                circuito = [nombre, d, cota]
                d += 10
                n += 1
                circ.append(circuito.copy())
        else :
            PLACE = len(Nivelacion[1]) - 1
            circ = []
            circ.append(["Nombre", "Dist", "Cota"])
            n = 0
            for minilista in Nivelacion:
                if n == 0:
                    n += 1
                    continue
                nombre = minilista[0]
                cota = minilista[PLACE]
                d = minilista[PLACE-1]
                circuito = [nombre, d, cota]
                n += 1
                circ.append(circuito.copy())
        graficame(circ)

    print(" ")
    w = int(input("¿Desea imprimir los resultados en un archivo plano? (1:Sí - 0:No): "))
    if w == 0:
        w = 5
    else:
        plano(Nivelacion, "nivelacionRESULTADOS")

#Le da formato a los numeros para que salgan en g m s
def gms2dec(angulo):
    grados = int(angulo)
    auxiliar = (angulo - grados) * 100
    minutos = int(auxiliar)
    segundos = (auxiliar - minutos)*100

    angulo_dec = grados + minutos / 60 + segundos / 3600

    return angulo_dec

#Halla el azimut mediante las coordenadas
def acimut_linea(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dy != 0:
        rumbo = math.degrees(math.atan(dx/dy))

        if dx > 0 and dy > 0:
            acimut = rumbo
        elif dx > 0 and dy < 0:
            acimut = 180 + rumbo
        elif dx < 0 and dy < 0:
            acimut = 180 + rumbo
        elif dx < 0 and dy > 0:
            acimut = 360 + rumbo
        elif dx == 0 and dy > 0:
            acimut = 0
        elif dx == 0 and dy > 0:
            acimut = 180
    else:
        if dx > 0:
            acimut = 90
        elif dx < 0:
            acimut = 270
        else:
            acimut = -1

    return acimut

#[PASAR ANGULOS EN DECIMALES A ANGULOS EN SISTEMA SEXAGESIMAL]
def dec2gms(angulo_dec):
    grados = int(angulo_dec)
    auxiliar = (angulo_dec - grados)*60
    minutos = int(auxiliar)
    segundos = round((auxiliar - minutos)*60,0)

    angulo_gms = '{:03d}'.format(grados) + '° ' + '{:02d}'.format(minutos) + "' " + '{:04.1f}'.format(segundos) + '"'

    return angulo_gms

#[CALCULAR ACIMUT ENTRE CADA DELTA]
def acimut_poligonal(acimut_anterior, angulo_observ):
    if acimut_anterior >= 180:
        contra_acimut = acimut_anterior - 180
    else:
        contra_acimut = acimut_anterior + 180

    acimut = contra_acimut + angulo_observ

    if acimut >= 360:
        acimut = acimut - 360

    return acimut

#Calcula las proyecciones
def proyecciones(acimut, distancia):

    acimut = math.radians(acimut)

    valor_proyecciones = []
    valor_proyecciones.append(math.sin(acimut)*distancia)
    valor_proyecciones.append(math.cos(acimut)*distancia)

    return valor_proyecciones

def brujula():
    print()
    print('='*110)
    print()
    print('{:^173}'.format('CARTERA DE CALCULO DE POLIGONAL POR EL METODO DE LA BRUJULA'))
    print()
    print('='*110)
    print()
##############################################3
    datos= [] #crea una lista para trabajar
    datos.append (['DELTA', 'PUNTO', 'DIST', 'AZIMUTH', 'PRY X', 'PRY Y','L2','D2','LD','LD2', 'PRY X COREG', 'PRY Y COREG', 'COORD X', 'COORD Y'])


    print('{:^10}'.format('='*168))
    print('{:^43}'.format('¿QUE DESEA HACER?')) #menu principal
    print(" ")
    print('{:^58}'.format('0) Introducir datos manualmente'))
    print('{:^60}'.format('1) Introducir datos desde archivo'))
    print(" ")
    w = int(input("Digite opción: "))

    if w > 0:
        print(" ")
        print("ADVERTENCIA: para ejecutar correctamente el programa los datos deben estar en el orden de DELTA, PUNTO, ANGULO Y DISTANCIA")
        datos = archivoCR()
    else:
        datos = manualCR()




###########################################
    deltas = int(input('Digite el numero de deltas en la poligonal: '))
    ang_externos = int(input('¿Angulos externos [1 = SI] [0 = NO]: '))

    #[CALCULO Y AJUSTE DE LOS ANGULOS DE LA POLIGONAL]
    if ang_externos == 1:
        suma_teorica_ang = (deltas + 2) *180
    else:
        suma_teorica_ang = (deltas - 2) *180

    #[SE LE SOLICITAN LAS COORDENADAS AL USUARIO]
    x_inicio = float(input('Digite la coordenada X (E) del punto de inicio: '))
    y_inicio = float(input('DIgite la coordenada Y (N) del punto de inicio: '))
    x_referencia = float(input('Digite la coordena X (E) del punto de referencia: '))
    y_referencia = float(input('Digite la coordena Y (N) del punto de referencia: '))

    #[CALCULAR ACIMUT DE ENTRADA]
    acimut_ref = acimut_linea(x_inicio, y_inicio, x_referencia, y_referencia)
    print('\n', f'El acimut calculado es: {dec2gms(acimut_ref)}')

    #[IMPRIME EL VALOR DE LA SUMATORIA TEORICA ANGULAR]
    print(f'La sumatoria teórica de ángulos es: {suma_teorica_ang}°')

    #[]
    datos_medidos = []
    datos_medidos.append (['DELTA','ANG OBSER', 'DIST', 'ANG OBSERV DEC', 'ANG OBSER CORREG', 'AZIMUTH', 'PRY X', 'PRY Y', 'PRY X COREG', 'PRY Y COREG', 'COORD X', 'COORD Y'])

    j = 0
    sumang = 0.0
    sumdist = 0.0

    #[SE LE SOLICITA AL USUARIO EL NOMBRE DEL DELTA, EL ANGULO OBSERVADO Y LA RESPECTIVA DISTANCIA PARA CALCULAR EL ERROR ANGULAR Y LA CORRECCION ANGULAR]
    for delta in (range(deltas+1)):
        print('='*80)

        nombre_delta = input(f'Digite el nombre del delta {delta+1}: ')
        ang_observado = float(input(f'Digite el angulo observado {delta+1}: '))
        distancia = float(input(f'Digite la dista de la linea {delta+1}: '))

        print('='*80)

        datos_linea = [nombre_delta, ang_observado, distancia, gms2dec(ang_observado)]
        datos_medidos.append(datos_linea.copy())

        if j != 0:
            sumdist = sumdist + distancia
            sumang = sumang + datos_linea[3]
            j += 1
        else:
            j += 1

    error_angular = suma_teorica_ang - sumang
    correccion_angular = error_angular / deltas

    print('El error angular es:', error_angular)
    print('La corrección angular es:', correccion_angular)

    datos_medidos[1].append(datos_medidos[1][3])
    datos_medidos[1].append(acimut_ref + datos_medidos[1][3])

    #[QUE HACE ESTE BLOQUE DE CÓDIGO]
    i = 0
    suma_px = 0.0
    suma_py = 0.0
    proyec_punto = []

    #[QUE HACE ESTE BLOQUE DE CÓDIGO]
    for dato in datos_medidos:

        if i < 2:
            i += 1
            continue

        datos_medidos[i].append(datos_medidos[i][3] + correccion_angular)

        if datos_medidos[i-1][4] >= 180:
            acimut_deltas = datos_medidos[i-1][5] - 180 + datos_medidos[i][4]
        else:
            acimut_deltas = datos_medidos[i-1][5] + 180 + datos_medidos[i][4]

        if acimut_deltas >= 360:
            acimut_deltas -= 360

        datos_medidos[i].append(acimut_deltas)

        proyec_punto = proyecciones(acimut_deltas, datos_medidos[i][2])

        datos_medidos[i].append(proyec_punto[0])
        datos_medidos[i].append(proyec_punto[1])

        suma_px += datos_medidos[i][6]
        suma_py += datos_medidos[i][7]

        i += 1

    print()

    datos_medidos [1][:] += [0, 0, 0, 0, x_inicio, y_inicio]

    #[QUE HACE ESTE BLOQUE DE CÓDIGO]
    i = 0

    for dato in datos_medidos:

        if i < 2:
            i += 1
            continue

        #[QUE HACE ESTE BLOQUE DE CÓDIGO]
        datos_medidos[i].append(datos_medidos[i][6] - (suma_px / sumdist)*datos_medidos[i][2])
        datos_medidos[i].append(datos_medidos[i][7] - (suma_py / sumdist)*datos_medidos[i][2])

        #[QUE HACE ESTE BLOQUE DE CÓDIGO]
        datos_medidos[i].append(datos_medidos[i-1][10] + datos_medidos[i][8])
        datos_medidos[i].append(datos_medidos[i-1][11] + datos_medidos[i][9])

        i += 1

    #[QUE HACE ESTE BLOQUE DE CÓDIGO]
    print()

    print('='*173)
    print('{:^10}'.format('DELTA'), '{:^8}'.format('ANGULO'), '{:^8}'.format('DISTANC'), '{:^10}'.format('ANGULO'), '{:^10}'.format('AZIMUTH'), '{:^10}'.format('PROYECC'), '{:^10}'.format('PROYECC'), '{:^10}'.format('PROYECC'), '{:^10}'.format('PROYECC'), '{:^11}'.format('COORDEN'), '{:^11}'.format('COORDEN'), sep='\t')

    print('{:^10}'.format(''), '{:^8}'.format('OBSERV'), '{:^8}'.format('(m)'), '{:^10}'.format('CORREGIDO'), '{:^10}'.format(''), '{:^10}'.format('X'), '{:^10}'.format('Y'), '{:^10}'.format('CORR X'), '{:^10}'.format('CORR Y'), '{:^11}'.format('X'), '{:^11}'.format('Y'), sep='\t')
    print('='*173)

    i = 0

    for dato in datos_medidos:
        if i == 0:
            i += 1
            continue

        print('{:^10}'.format(dato[0]),'{:8.4f}'.format(dato[1]), '{:8.4f}'.format(dato[2]), '{:10}'.format(dec2gms(dato[4])), '{:10}'.format(dec2gms(dato[5])), '{:+010.3f}'.format(dato[6]), '{:+010.3f}'.format(dato[7]), '{:+010.3f}'.format(dato[8]), '{:+010.3f}'.format(dato[9]), '{:11.3f}'.format(dato[10]), '{:11.3f}'.format(dato[11]), sep='\t')

        i += 1

    print('='*173)
    print(" ")
    w = int(input("¿Desea graficar la poligonal? (1:Sí - 0:No): "))
    if w == 0:
        w = 5
    else:
        graficame(datos_medidos)
    print(" ")
    w = int(input("¿Desea imprimir los resultados en un archivo plano? (1:Sí - 0:No): "))
    if w == 0:
        w = 5
    else:
        plano(datos_medidos,"resultadosBRUJULA")

#[BUSCA EL ARCHIVO DE LOS DATOS DELA POLIGONAL]
def archivoCR():
    datos= [] #Crea una lista vacia para almacenar lso datos del archivo
    datos.append (['DELTA', 'PUNTO', 'DIST', 'AZIMUTH', 'PRY X', 'PRY Y','L2','D2','LD','LD2', 'PRY X COREG', 'PRY Y COREG', 'COORD X', 'COORD Y'])

    print(" ")
    print("Digite a continuación la ruta del archivo (Con el archivo, en formato CSV) [O pulse enter para ejecutar el archivo de ejemplo adjunto en el mismo directorio]")
    ruta = input("ruta: ") #se introduce la ruta del archivo
    print(" ")
    sep = input("Defina ahora el separador del archivo .csv (digite '.' o bien ',' o bien ';' [o también enter para ';']: )") #Se define el separador del csv
    if len(sep) <1:  #se define el valor por defecto si se pulsó enter para el separador
        sep = ';'
    if len(ruta) <1: #se define el valor por defecto si se pulsó enter para el archivo a trabajar
        ruta = 'crandall.csv' #Archivo de ejemplo debe estar en la misma carpeta que este documento
    rutaR = open(ruta) #establece una conexion

    n = 0  #iniciamos un contador
    for linea in rutaR:      #un bucle para analizar cada linea del archivo
        linea = linea.split(sep)   #separador del archivo csv

        if n == 0: #se salta la primera linea ya que solo contiene los titulos de los campos
            n += 1
            continue

        delta = linea[0]                              #0 Nombre delta
        punto = linea[1]                              #1 Nombre punto visado
        #angulo = linea[2]
        angulo = linea[2].replace(",", ".")
        angulo = float(angulo)                        #2 angulo AZIMUT DIRECTO
        dist = linea[3].replace(",", ".")             #3 distancia
        dist = dist.rstrip()
        dist = float(dist)
        datos_linea = [delta,punto, angulo, dist]
        datos.append(datos_linea.copy())

        n += 1
    return datos #la función devuelve este archivo de trabajo

def manualCR():
    datos= [] #inicia una lista vacia para almacenar los datos
    datos.append (['DELTA', 'PUNTO', 'AZIMUTH', 'DIST', 'PRY X', 'PRY Y','L2','D2','LD','LD2', 'PRY X COREG', 'PRY Y COREG', 'COORD X', 'COORD Y'])

    n = int(input("¿Cuantos deltas tiene la poligonal?")) #define el numero de deltas de la poligonal
    i = 1 #inicia un contador
    for cambio in (range(n)): #este bucle introducira datos por el numero de deltas
        print('Cambio numero',i) #solo imprime el numero de delta
        d = input('Nombre del delta:')  #guarda el nombre del delta
        v = input('Punto visado: ') #guarda el punto siguiente
        d = float(input("distancia: ")) #guarda la distancia
        a = float(input('azimut directo DECIMAL: ')) #guarda elangulo
        datos_linea = [d,v, a, d] #introduce todos los datos en una lista aparte
        datos.append(datos_linea.copy()) #guarda dicha lista en la que creamos previamente
        i += 1 #aumenta el contador en 1
        print(" ") #añade un espacio para que se vea estetico

    return datos #la función devuelve este archivo de trabajo

def archivoTR():
    datos= [] #Crea una lista vacia para almacenar lso datos del archivo
    datos.append (['DELTA', "ÁNGULO", 'DIST', 'AZIMUTH', 'PRY X', 'PRY Y',"CORR X","CORR Y",'PRY X COREG', 'PRY Y COREG', 'COORD X', 'COORD Y'])

    print(" ")
    print("Digite a continuación la ruta del archivo (Con el archivo, en formato CSV) [O pulse enter para ejecutar el archivo de ejemplo adjunto en el mismo directorio]")
    ruta = input("ruta: ") #se introduce la ruta del archivo
    print(" ")
    sep = input("Defina ahora el separador del archivo .csv (digite '.' o bien ',' o bien ';' [o también enter para ';']: )") #Se define el separador del csv
    if len(sep) <1:  #se define el valor por defecto si se pulsó enter para el separador
        sep = ';'
    if len(ruta) <1: #se define el valor por defecto si se pulsó enter para el archivo a trabajar
        ruta = 'transito.csv' #Archivo de ejemplo debe estar en la misma carpeta que este documento
    rutaR = open(ruta) #establece una conexion

    n = 0  #iniciamos un contador
    for linea in rutaR:      #un bucle para analizar cada linea del archivo
        linea = linea.split(sep)   #separador del archivo csv

        if n == 0: #se salta la primera linea ya que solo contiene los titulos de los campos
            n += 1
            continue

        delta = linea[0]                              #0 Nombre delta
        #angulo = linea[2]
        angulo = float(linea[1].replace(",", "."))    #1 angulo AZIMUT DIRECTO
        dist = linea[2].replace(",", ".")             #2 distancia
        dist = float(dist.rstrip())
        datos_linea = [delta, angulo, dist]
        datos.append(datos_linea.copy())

        n += 1
    return datos #la función devuelve este archivo de trabajo

def manualTR():
    datos= [] #inicia una lista vacia para almacenar los datos
    datos.append (['DELTA', 'PUNTO', 'AZIMUTH', 'DIST', 'PRY X', 'PRY Y','L2','D2','LD','LD2', 'PRY X COREG', 'PRY Y COREG', 'COORD X', 'COORD Y'])

    n = int(input("¿Cuantos deltas tiene la poligonal?")) #define el numero de deltas de la poligonal
    i = 1 #inicia un contador
    for cambio in (range(n)): #este bucle introducira datos por el numero de deltas
        print('Cambio numero',i) #solo imprime el numero de delta
        dt = input('Nombre del delta:')  #guarda el nombre del delta
        a = float(input('azimut directo DECIMAL: ').replace(",", ".")) #guarda elangulo
        d = float(input("distancia: ").replace(",", ".")) #guarda la distancia
        datos_linea = [dt,a,d] #introduce todos los datos en una lista aparte
        datos.append(datos_linea.copy()) #guarda dicha lista en la que creamos previamente
        i += 1 #aumenta el contador en 1
        print(" ") #añade un espacio para que se vea estetico

    return datos #la función devuelve este archivo de trabajo

#[ESTA FUNCIÓN DEFINE EL ARCHIVO DE SALIDA]
def plano(entrada, nombre):
    salida = [] #crea una lista para trabajar
    resumen = [] #lo de arriba x2
    for lista in entrada: #este bucle analiza cada lista pequeña dentro de la lista grande
        for cosa in lista: #y este analiza cada dato dentro de la lista pequeña
            cosa = str(cosa) #volvemos el dato una cadena de texto
            cosa = cosa.replace(".", ",") #reemplazamos el punto por la coma, si lo tiene
            salida.append(cosa) #añade lso datos a una lista
        resumen.append(salida.copy()) #hace una copia de esa lista y la añade a la lista final
        del salida[:] #borra la lista de trabajo para introducir mas datos organizadamente

    print(" ")
    print("Defina a continuación la ruta de salida [O pulse enter para guardar en el mismo directorio que este archivo python]")
    ruta = input("ruta: ") #se define la ruta de salida
    if len(ruta) < 1: #se define un valor por defecto en el mismo directorio
        ruta = nombre + '.csv'
    plano = open(ruta, 'w') #abre ese archivo y le indica al computador que va a escribir algo
    with plano:
        escribir = csv.writer(plano, delimiter=";") #indica el archivo y el separador
        escribir.writerows(resumen) #escribe el archivo

    print("Archivo escrito satisfactoriamente en:",ruta)

def transito():
    #datos= [] #crea una lista para trabajar
    #datos.append (['DELTA', 'PUNTO', 'DIST', 'AZIMUTH', 'PRY X', 'PRY Y','PRY X COREG', 'PRY Y COREG', 'COORD X', 'COORD Y'])

    print()
    print('='*168)
    print()
    print('{:^173}'.format('CARTERA DE CALCULO DE POLIGONAL POR EL METODO DE TRÁNSITO'))
    print()
    print('='*168)
    print()

    print('{:^10}'.format('='*168))
    print('{:^43}'.format('¿QUE DESEA HACER?')) #menu principal
    print(" ")
    print('{:^58}'.format('0) Introducir datos manualmente'))
    print('{:^60}'.format('1) Introducir datos desde archivo'))
    print(" ")
    w = int(input("Digite opción: "))

    if w > 0:
        print(" ")
        print("ADVERTENCIA: para ejecutar correctamente el programa los datos deben estar en el orden de PUNTO, ANGULO Y DISTANCIA")
        datos = archivoTR()
    else:
        datos = manualTR()

    y_inicio = float(input('Digite la coordenada Y (N) del punto de inicio: '))
    x_inicio = float(input('Digite la coordenada X (E) del punto de inicio: '))
    azimut = input("Introduzca el Azimut de inicio: ")
    azimut = float(azimut.replace(",", "."))
    n = 0
    for lista in datos:
        if n ==0:
            n += 1
            continue
        if n == 1:
            azlinea = azimut
            datos[n].append(azlinea)
            n += 1
            continue
        azlinea = acimut_poligonal(datos[n-1][3], lista[1])
        datos[n].append(azlinea)
        n += 1

    suma_px = 0
    suma_py = 0
    ABSsuma_px = 0
    ABSsuma_py = 0
    n = 0
    distACUM = 0
    for lista in datos: #comienza a visualizar cada lista para hacer calculos
        if n ==0:
            n += 1
            continue
        pry = proyecciones((lista[3]), (lista[2])) #calcula las proyecciones

        datos[n].append(pry[0]) #4 proyeccion este
        datos[n].append(pry[1]) #5 proyeccion norte

        distACUM += datos[n][2] #Acumulamos las distancias
        suma_px += datos[n][4]  #Acumulamos las proyeciones
        suma_py += datos[n][5]
        ABSsuma_px += abs(datos[n][4])  #Acumulamos las proyeciones absolutas
        ABSsuma_py += abs(datos[n][5])
        n += 1

    ECL = math.sqrt((suma_px ** 2)+(suma_py ** 2))
    PREL = ECL/distACUM
    n = 0
    for lista in datos:
        if n == 0:
            n += 1
            continue
        corrx = (suma_px * abs(datos[n][4]))/ABSsuma_px #6 corr este
        corry = (suma_py * abs(datos[n][5]))/ABSsuma_py #7 corr norte

        pry_corrx = datos[n][4] - corrx #8 proy corregida este
        pry_corry = datos[n][5] - corry #8 proy corregida norte
        datos[n].append(corrx)
        datos[n].append(corry)
        datos[n].append(pry_corrx)
        datos[n].append(pry_corry)
        n += 1

    datos[1].append(x_inicio)
    datos[1].append(y_inicio)

    n = 0
    for lista in datos:
        if n < 2:
            n += 1
            continue
        cordx = datos[n-1][8] + datos[n-1][10]
        cordy = datos[n-1][9] + datos[n-1][11]
        datos[n].append(cordx)
        datos[n].append(cordy)
        n += 1

    print()

    #ENTREGA TODO EN UN FORMATO VISUALMENTE ATRACTIVO
    print('='*150)
    print('{:^5}'.format('DELTA'), '{:^10}'.format('ÁNGULO'), '{:^9}'.format('DISTANC'), '{:^1}'.format('AZIMUT'), '{:^25}'.format('PROYECCIÓN'), '{:^20}'.format('CORRECCIÓN'), '{:^1}'.format('PROYECCIÓN CORREGIDA'), '{:^25}'.format('COORDENADAS'), sep='\t')

    print('{:^5}'.format(''), '{:^10}'.format('OBSERV'), '{:^25}'.format(''), '{:^1}'.format('X'), '{:^10}'.format('Y'), '{:^5}'.format('Xc'), '{:^0}'.format('Yc'), '{:^16}'.format('X'), '{:^1}'.format('Y'),  '{:^16}'.format('X'), '{:^1}'.format('Y'), sep='\t')
    print('='*150)

    i = 0

    for dato in datos: #imprime cada dato de las listas pequeñas
        if i == 0:
            i += 1
            continue

        print('{0:>5}'.format(dato[0]),'{0:>5}'.format(dec2gms(dato[1])), '{0:>3.3f}'.format(dato[2]), '{0:>5}'.format(dec2gms(dato[3])), '{0:>9.3f}'.format(dato[4]), '{0:>9.3f}'.format(dato[5]), '{0:>4.3f}'.format(dato[6]),'{0:>4.3f}'.format(dato[7]), '{0:>8.3f}'.format(dato[8]), '{0:>8.3f}'.format(dato[9]), '{0:>9.3f}'.format(dato[10]), '{0:>9.3f}'.format(dato[11]), sep='\t')

        i += 1

    print('='*150)
    print(" ")
    w = int(input("¿Desea graficar la poligonal? (1:Sí - 0:No): "))
    if w == 0:
        w = 5
    else:
        graficame(datos)
    print(" ")
    w = int(input("¿Desea imprimir los resultados en un archivo plano? (1:Sí - 0:No): "))
    if w == 0:
        w = 5
    else:
        plano(datos,"resultadosTRANSITO")

def crandall():

    datos= [] #crea una lista para trabajar
    datos.append (['DELTA', 'PUNTO', 'DIST', 'AZIMUTH', 'PRY X', 'PRY Y','L2','D2','LD','LD2', 'PRY X COREG', 'PRY Y COREG', 'COORD X', 'COORD Y'])

    print()
    print('='*168)
    print()
    print('{:^173}'.format('CARTERA DE CALCULO DE POLIGONAL ABIERTA POR EL METODO DE CRANDALL'))
    print()
    print('='*168)
    print()

    print('{:^10}'.format('='*168))
    print('{:^43}'.format('¿QUE DESEA HACER?')) #menu principal
    print(" ")
    print('{:^58}'.format('0) Introducir datos manualmente'))
    print('{:^60}'.format('1) Introducir datos desde archivo'))
    print(" ")
    w = int(input("Digite opción: "))

    if w > 0:
        print(" ")
        print("ADVERTENCIA: para ejecutar correctamente el programa los datos deben estar en el orden de DELTA, PUNTO, ANGULO Y DISTANCIA")
        datos = archivoCR()
    else:
        datos = manualCR()

    y_inicio = float(input('Digite la coordenada Y (N) del punto de inicio: '))
    x_inicio = float(input('Digite la coordenada X (E) del punto de inicio: '))

    #[Este bloque de código no se utilizó jamás...]
    #y_referencia = float(input('Digite la coordena Y (N) del punto de referencia: '))
    #x_referencia = float(input('Digite la coordena X (E) del punto de referencia: '))
    #acimut_ref = acimut_linea(x_inicio, y_inicio, x_referencia, y_referencia)
    #print('\n', f'El acimut calculado es: {dec2gms(acimut_ref)}')

    suma_px = 0 #definimos las variables para las proyeciones
    suma_py = 0
    L2 = 0 #Definimos las variables para Crandall
    D2 = 0
    LD = 0
    LD2 = 0
    SL2 = 0
    SD2 = 0
    SLD = 0
    SLD2 = 0

    n = 0 #Reiniciamos el contador
    for dato in datos: #comienza a visualizar cada lista para hacer calculos
        if n ==0:
            n += 1
            continue
        pry = proyecciones((datos[n][2]), (datos[n][3])) #calcula las proyecciones

        datos[n].append(pry[0]) #4 proyeccion este
        datos[n].append(pry[1]) #5 proyeccion norte

        suma_px += datos[n][4]  #Acumulamos las proyeciones
        suma_py += datos[n][5]

        #[Calculo de las variables crandall (L2,D2 ETC)]

        L2 = ((pry[1]**2)/datos[n][3] )/100         #6
        D2 = ((pry[0]**2)/datos[n][3] )/100         #7
        LD = ((pry[1] + pry[0])/datos[n][3])/100    #8
        LD2 = LD**2                                 #9

        SL2 += L2 #acumulamos los parametros
        SD2 += D2
        SLD += LD
        SLD2 += LD2

        crandlist = [L2,D2,LD,LD2]
        datos[n].append(crandlist[0])
        datos[n].append(crandlist[1])
        datos[n].append(crandlist[2])
        datos[n].append(crandlist[3])

        n += 1

    A = ((suma_px*SLD)-(suma_py*SD2))/((SL2*SD2)-SLD2) #calculamos los parametros A Y C
    B = ((suma_py*SLD)-(suma_px*SL2))/((SL2*SD2)-SLD2)

    PRNC = 0 #definimos las variables para las proyecciones corregidas
    PREC = 0

    n = 0 #Reiniciamos el contador
    for dato in datos: #CORREGIMOS LAS PROYECCIONES y calculamos coordenadas en cada lista pequeña
        if n ==0:
            n += 1
            continue
        PREC = datos[n][4] + (((datos[n][7]*B + datos[n][8]*A))) #corregimos las proyecciones por el metodo crandall
        PRNC = datos[n][5] + ((datos[n][6]*A) + (datos[n][8]*B))

        datos[n].append(PREC)   #10
        datos[n].append(PRNC)   #11

        if n == 1: #hace esto si es la primera linea
            datos[n].append(x_inicio + PREC) #12 coordenada este
            datos[n].append(y_inicio + PRNC) #13 coordenada norte
        else: #hace esto si lalinea es distinta a la primera
            datos[n].append(datos[n-1][12] + PREC)
            datos[n].append(datos[n-1][13] + PRNC)

        n += 1

    print()

    #ENTREGA TODO EN UN FORMATO VISUALMENTE ATRACTIVO
    print('='*168)
    print('{:^10}'.format('DELTA'), '{:^8}'.format('PUNTO'), '{:^15}'.format('AZIMUT'), '{:^18}'.format('DISTANC'), '{:^18}'.format('PROYECCION'), '{:^32}'.format('PROYECCION CORREGIDA'), '{:^15}'.format('COORDENADAS'), sep='\t')

    print('{:^10}'.format(''), '{:^8}'.format('OBSERV'), '{:^10}'.format(''), '{:^17}'.format('(m)'), '{:^1}'.format('X'), '{:^15}'.format('Y'), '{:^18}'.format('Xc'), '{:^0}'.format('Yc'), '{:^16}'.format('X'), '{:^1}'.format('Y'), sep='\t')
    print('='*168)

    i = 0

    for dato in datos: #imprime cada dato de las listas pequeñas
        if i == 0:
            i += 1
            continue

        print('{:^10}'.format(dato[0]),'{:^8}'.format(dato[1]), '{:^0}'.format(dec2gms(dato[2])), '{:11.3f}'.format(dato[3]), '{:11.3f}'.format(dato[4]), '{:11.3f}'.format(dato[5]), '{:11.3f}'.format(dato[10]), '{:11.3f}'.format(dato[11]), '{:11.3f}'.format(dato[12]), '{:11.3f}'.format(dato[13]), sep='\t')

        i += 1

    print('='*168)

    print('{:^100}'.format('PARAMETROS CRANDALL'))
#PARAMETROS CRANDALL
    print()

    print('='*168)
    print('{:^20}'.format('L2'), '{:^18}'.format('D2'), '{:^20}'.format('LD'), '{:^20}'.format('LD2'), sep='\t')
    print('='*168)

    i = 0

    for dato in datos: #imprime los parametros crandall utilizados
        if i == 0:
            i += 1
            continue

        print('{:^10}'.format(dato[6]),'{:^10}'.format(dato[7]), '{:^10}'.format(dato[8]), '{:^10}'.format(dato[9]),  sep='\t')

        i += 1

    print('='*168)
    print('{:^10}'.format('A: '),A,'{:^40}'.format('B: '),B) #imprime A y B de crandall que se utilizó
    print('='*168)

    print(" ")
    w = int(input("¿Desea graficar la poligonal? (1:Sí - 0:No): "))
    if w == 0:
        w = 5
    else:
        graficame(datos)
    print(" ")
    print(" ")
    v = float(input("¿Desea imprimir los resultados en un archivo plano? [SI =1, NO = 0]: "))
    if v >0:
        plano(datos, "resultadosCRANDALL")

#[IMPRIMIR EL TITULO Y SOLICITAR AL USUARIO NUMERO DE DELTAS Y QUE ESPECIFIQUE SI SON ANGULOS INTERNOS O EXTERNOS]
def main():
    print()
    print('='*110)
    print()
    print('{:^173}'.format('C A L C U L O   D E   C A R T E R A S   V 1.0 '))
    print()
    print('='*110)
    print()
    print("I N G R E S O   A L  S I S T E M A")
    print()
    n = 0
    print(asociados)
    while n <= 3:
        print(" ")
        name = input("ingresar apellido asociado: ")
        cod = input("Ingresar código: ")
        if name in asociados:
            vals = list(asociados.values())
            if cod in vals:
                n = 5
                print(" ")
                print("Credenciales correctas")
            else:
                n = n + 1
                print("Credenciales incorrectas, usted tiene",4 - n,"intentos más")
        else:
            n = n + 1
            print("Credenciales incorrectas, usted tiene",4 - n,"intentos más")
    if n == 4:
        print(" ")
        print("Credenciales incorrectas, comuniquese con el administrador")
        print("Programa terminado")
        sys.exit()
    else:
        print("Bienvenid@,",nombres[name],name)
        z = 1
    print('='*110)
    print("                                                                                         Menú principal      =")
    print('='*110)

    print('''                                        ===================================
                                        =        1) Brújula               =
                                        =        2) Tránsito              =
                                        =        3) Crandall              =
                                        =        4) Nivelación            =
                                        =           o Por cambios         =
                                        =           o Por distancias      =
                                        =        5) Diagrama de           =
                                        =           obstáculos            =
                                        ===================================
    ''')
    print('='*110)

    metodo = int(input("Seleccione el método: "))
    while metodo < 1 or metodo > 5:
        print(" ")
        print("No es válido, intente nuevamente.")
        metodo = int(input("Seleccione el método: "))

    if metodo == 1:
        brujula()
    elif metodo == 2:
        transito()
    elif metodo == 3:
        crandall()
    elif metodo == 4:
        niv()
    elif metodo == 5:
        rosa()
    else:
        print("No ha seleccionado una opción válida")

    new = int(input("¿Volver al menú? 1 SI, 0 NO: "))
    if new == 1:
        main()
    else:
        print("Finalizado")
    #print("                                                                                                             =")
    #print('='*110)

#[AQUI INICIA EL CODIGO, ESTA LINEA EJECUTA EL PROGRAMA AL INICIAR]
if __name__ == '__main__':
    main()
