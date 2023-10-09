#!/usr/bin/env python
#-*- coding: utf-8 -*-

import math
import pygame
import random

pygame.init()
pygame.font.init() 
pygame.mixer.music.load("assets/sounds/paseNivel.wav") 
pygame.display.set_caption("OFIRCA 2023 - Resolución de todas las rondas")
pantalla= pygame.display.set_mode((1152,648))
tipografia = pygame.font.SysFont('Arial', 18)
tipografiaGrande=pygame.font.SysFont('Arial', 24)

# -----> Variables Nuestras <-----#

global habitacionActual
global personaje
global crearMapa
global sala1
global sala2
global sala3

reloj = pygame.time.Clock()
dt = 0
movArriba, movAbajo, movDerecha, movIzquierda = False, False, False, False

posXjugador = 2
posYjugador = 5

zonaDeTransporte2 = 0

indexX = 0
indexY = 1

boolCambioSala = False

# -----> Variables Ofirca <-----#

global ticksAlComenzar
global cantidadDeMovimientosRestantes
global cantidadDeMovimientosActual
global zonaDeTransporte
global avatarRect
global nivelCompletado

contMovUAIBOT=0
contMovUAIBOTA=0
contMovUAIBOTINA=0

dt = 0
ticksAlComenzar=pygame.time.get_ticks()
personajeActual='UAIBOT'
tiempoParaSolucionarElNivel=55
cantidadDeMovimientosActual=0
cantidadDeMovimientosRestantes=10
colorVerde,colorAzul,colorBlanco,colorNegro, colorNaranja, colorBordeaux= (11,102,35), (0,0,255), (255,255,255), (0,0,0), (239,27,126), (102,41,53)
cantidadDeCasillasPorLado=8 # Debe ser número par ya que la zona es un cuadrado
cantPixelesPorLadoCasilla=64
salirJuego = False
lstAreaProtegida=[]

imgAvatar=pygame.transform.scale(pygame.image.load("assets/img/UAIBOT.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
avatarRect=imgAvatar.get_rect()   
imgMira=pygame.transform.scale(pygame.image.load("assets/img/mira.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
imgPared=pygame.transform.scale(pygame.image.load("assets/img/pared.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
imgParedAlternativa=pygame.transform.scale(pygame.image.load("assets/img/paredAlternativa.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
imgParedAlternativa=pygame.transform.scale(pygame.image.load("assets/img/paredAlternativa.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  

imgAreaProtegida=pygame.transform.scale(pygame.image.load("assets/img/areaprotegida.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
listaVirus  = ["assets/img/virus1.png","assets/img/virus2.png","assets/img/virus3.png","assets/img/virus4.png","assets/img/virus5.png","assets/img/virus6.png"]

imgVirus=pygame.transform.scale(pygame.image.load(str(random.choice(listaVirus))), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
imgVirusQueSeMueve=pygame.transform.scale(pygame.image.load(str(random.choice(listaVirus))), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
imgVirusSinusoidal=pygame.transform.scale(pygame.image.load(str(random.choice(listaVirus))), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))

# Colision de la mira
miraRect=imgMira.get_rect()

virusQueSeMueveRect = imgVirusQueSeMueve.get_rect()
virusQueSeMueveRect.left =cantPixelesPorLadoCasilla * cantidadDeCasillasPorLado
virusQueSeMueveRect.top = cantPixelesPorLadoCasilla * (cantidadDeCasillasPorLado - 1)

virusSinusoidalRect = imgVirusSinusoidal.get_rect()
virusSinusoidalRect.left =cantPixelesPorLadoCasilla * cantidadDeCasillasPorLado
virusSinusoidalRect.top = cantPixelesPorLadoCasilla * (cantidadDeCasillasPorLado - 1)

nombreJugador="Jugador1"
cantidadDeMovimientosRestantes=30
cantidadDeMovimientosDeterminada=30 
#nombreJugador=input("Ingresa tu nombre: ")
#cantidadDeMovimientosDeterminada=int(input("Ingresa la cantidad máxima de movimientos: "))
cantidadDeMovimientosRestantes=cantidadDeMovimientosDeterminada

def dibujarFondo():
    fondo = pygame.image.load("assets/img/fondo.png")
    pantalla.blit(fondo, (0, 0))


def hayAreaProtegidaEn(x,y):
    punto=(x,y)
    return lstAreaProtegida.__contains__(punto)

def actualizarContadorDeMovimientos(num):
    global cantidadDeMovimientosActual
    global cantidadDeMovimientosRestantes

       
    cantidadDeMovimientosActual=cantidadDeMovimientosActual+num
    cantidadDeMovimientosRestantes=cantidadDeMovimientosRestantes-1
    
    if cantidadDeMovimientosRestantes<0:
        cantidadDeMovimientosRestantes=0
    
    ancho=350
    alto=30
    x=75+(cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla)
    y=cantPixelesPorLadoCasilla*5
    pygame.draw.rect(pantalla,colorBordeaux,(x,y,ancho,alto))
    textoPasos = tipografiaGrande.render('Cantidad de movimientos: ' + str(cantidadDeMovimientosActual), False, colorBlanco)
    pantalla.blit(textoPasos,(x+5,y,ancho,alto))    
   
    y=cantPixelesPorLadoCasilla*6 
    pygame.draw.rect(pantalla,colorBordeaux,(x,y,ancho + 32,alto))
    textoMovimientosRestantes = tipografiaGrande.render('Cantidad de movimientos restantes: ' + str(cantidadDeMovimientosRestantes), False, colorBlanco)
    pantalla.blit(textoMovimientosRestantes,(x+5,y,ancho,alto))

    calculoPorcentajeMovimientos = round((100 * cantidadDeMovimientosRestantes)/cantidadDeMovimientosDeterminada) 
    textoPorcentaje = tipografiaGrande.render(str(calculoPorcentajeMovimientos) + ' %', False, colorBlanco)
    y=cantPixelesPorLadoCasilla*6+32
    pygame.draw.rect(pantalla,colorAzul,(x,y,200,alto))
    pygame.draw.rect(pantalla,colorNaranja,(x,y,calculoPorcentajeMovimientos*2,alto))

    pantalla.blit(textoPorcentaje,(x,y,ancho,alto))

    
# Clase del jugador
class jugador(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.surface = pygame.Surface((x, y))
        self.surface.fill('red')
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = x
        self.heigth = y

        self.rect = self.surface.get_rect()
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        self.rect.width = self.width
        self.rect.height = self.heigth

        self.x = 2
        self.y = 5
        
     #------------>Personaje: 1. Arrastrar Bloques<-------------#
    # Utilidad de las siguientes 4 funciones:  
    # Revisa si en la direccion contraria a la que se va a mover (Ej: Si se mueve para arriba, mira la casilla de abajo), tiene un virus para mover
    # Si es cierto, arrastra al virus hacia la posicion del jugador y se limpia (regresa a 0) la posicion del virus
    # Si NO lo es, limpia solo la posicion que tenia el jugador antes de moverse

    def ArrastrarVertical(self, simbolo, opuesto, lista):
        
        if eval(str(self.y) + simbolo + '1') < 9:
            if lista[eval(str(self.y) + simbolo + '1')][self.x] in [0, 6]:
                
                if eval(str(self.y) + opuesto + '1') < 9:

                    if lista[eval(str(self.y) + opuesto + '1')][self.x] == 4:

                        lista[eval(str(self.y) + opuesto + '1')][self.x] = 0
                        lista[self.y][self.x] = 4
                    
                    else:
                    
                        lista[self.y][self.x] = 0
                
                else:

                    lista[self.y][self.x] = 0 

                self.y = eval(str(self.y) + simbolo + '1')
            
    def ArrastrarHorizontal(self, simbolo, opuesto, lista):
        
        # Cada tanto da algunos errores con los resultados de la posicion en X y en Y ya que se salen del rango en index de la lista
        # Se soluciono solo (?
        if eval(str(self.x) + simbolo + '1') < 9:

            if lista[self.y][eval(str(self.x) + simbolo + '1')] in [0, 6]:

                if eval(str(self.x) + opuesto + '1') < 9:

                    if lista[self.y][eval(str(self.x) + opuesto + '1')] == 4:

                        lista[self.y][eval(str(self.x) + opuesto + '1')] = 0
                        lista[self.y][self.x] = 4

                    else:

                        lista[self.y][self.x] = 0

                else:

                    lista[self.y][self.x] = 0

                self.x = eval(str(self.x) + simbolo + '1')

    #------------>Personaje: 2. Saltar Bloques<-------------#

    def SaltarVertical(self, simbolo, lista):

        if not eval(str(self.y) + simbolo + '1') == 9:

            if lista[eval(str(self.y) + simbolo + '1')][self.x] in [0, 6]:

                
                lista[self.y][self.x] = 0
                self.y = eval(str(self.y) + simbolo + '1') 

            else:

                if eval(str(self.y) + simbolo + '2') < 9:

                    if lista[eval(str(self.y) + simbolo + '1')][self.x] in [1, 4, 5] and lista[eval(str(self.y) + simbolo + '2')][self.x] in [0, 6]:


                        lista[self.y][self.x] = 0
                        self.y = eval(str(self.y) + simbolo + '2')

             
    
    def SaltarHorizontal(self, simbolo, lista):

        if not eval(str(self.x) + simbolo + '1') == 9:

            if lista[self.y][eval(str(self.x) + simbolo + '1')] in [0, 6]:

                    
                lista[self.y][self.x] = 0
                self.x = eval(str(self.x) + simbolo + '1')

            else:

                if eval(str(self.x) + simbolo + '2') < 9:

                    if lista[self.y][eval(str(self.x) + simbolo + '1')] in [1, 4, 5] and lista[self.y][eval(str(self.x) + simbolo + '2')] in [0, 6]:


                        lista[self.y][self.x] = 0
                        self.x = eval(str(self.x) + simbolo + '2')

    #------------>Personaje: 3. Empujar Bloques<-------------#
    def EmpujarVertical(self, simbolo, lista):

        if eval(str(self.y) + simbolo + '1') < 9:
            if lista[eval(str(self.y) + simbolo + '1')][self.x] == 4 and lista[eval(str(self.y) + simbolo + '2')][self.x] in [0, 6]:


                lista[self.y][self.x] = 0
                self.y = eval(str(self.y) + simbolo + '1')
                lista[eval(str(self.y) + simbolo + '1')][self.x] = 4
                
            elif lista[eval(str(self.y) + simbolo + '1')][self.x] in [0, 6]:


                lista[self.y][self.x] = 0
                self.y = eval(str(self.y) + simbolo + '1')
        
    def EmpujarHorizontal(self, simbolo, lista):

        if eval(str(self.x) + simbolo + '1') < 9:
            
            if lista[self.y][eval(str(self.x) + simbolo + '1')] in [4, 5] and lista[self.y][eval(str(self.x) + simbolo + '2')] in [0, 6]:
                
                lista[self.y][self.x] = 0
                lista[self.y][eval(str(self.x) + simbolo + '2')] = lista[self.y][eval(str(self.x) + simbolo + '1')] 
                self.x = eval(str(self.x) + simbolo + '1')
                
            elif lista[self.y][eval(str(self.x) + simbolo + '1')] in [0, 6]:

                lista[self.y][self.x] = 0
                self.x = eval(str(self.x) + simbolo + '1')

    def mover(self, robot, bool = [], lista = []):
        
        global zonaActual, zonaDeTransporte, zonaDeTransporte2, indexY, indexX, boolCambioSala

        if pygame.key.get_pressed()[pygame.K_w]:

            if 'arriba' in bool and self.y == 1:
                lista[self.y][self.x] = 0
                indexY -= 1
                self.y = 8
                boolCambioSala = True
            else:
                match robot:
                        case "UAIBOT":
                            self.EmpujarVertical('-', lista)
                        case "UAIBOTA":
                            self.ArrastrarVertical('-', '+', lista)
                        case "UAIBOTINA":
                            self.SaltarVertical('-', lista)
                        case "UAIBOTINO":
                            self.SaltarVertical('-', lista)

        if pygame.key.get_pressed()[pygame.K_s]:

            if 'abajo' in bool and self.y == 8:
                lista[self.y][self.x] = 0
                indexY += 1
                self.y = 1
                boolCambioSala = True
            else:
                match personajeActual:
                        case "UAIBOT":
                            self.EmpujarVertical('+', lista)
                        case "UAIBOTA":
                            self.ArrastrarVertical('+', '-', lista)
                        case "UAIBOTINA":
                            self.SaltarVertical('+', lista)
                        case "UAIBOTINO":
                            self.SaltarVertical('+', lista)

        if pygame.key.get_pressed()[pygame.K_d]:

            if 'derecha' in bool and self.x == 8:
                lista[self.y][self.x] = 0
                indexX += 1
                self.x = 1
                boolCambioSala = True
            else:
                match personajeActual:
                        case "UAIBOT":
                            self.EmpujarHorizontal('+', lista)
                        case "UAIBOTA":
                            self.ArrastrarHorizontal('+', '-', lista)
                        case "UAIBOTINA":
                            self.SaltarHorizontal('+', lista)
                        case "UAIBOTINO":
                            self.SaltarHorizontal('+', lista)


        if pygame.key.get_pressed()[pygame.K_a]:

            if 'izquierda' in bool and self.x == 1:
                lista[self.y][self.x] = 0
                indexX -= 1
                self.x = 8
                boolCambioSala = True
            else:
                match personajeActual:
                        case "UAIBOT":
                            self.EmpujarHorizontal('-', lista)
                        case "UAIBOTA":
                            self.ArrastrarHorizontal('-', '+', lista)
                        case "UAIBOTINA":
                            self.SaltarHorizontal('-', lista)
                        case "UAIBOTINO":
                            self.SaltarHorizontal('-', lista)
            
        actualizarContadorDeMovimientos(1)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
        lista[self.y][self.x] = 3

    def reiniciar(self):
        
        self.y = 5
        self.x = 2


class virus(pygame.sprite.Sprite):

    def __init__(self, posX, posY):

        # Aca se heredan las propiedades
        pygame.sprite.Sprite.__init__(self) 
        self.posX = posX
        self.posY = posY
        self.surface = pygame.Surface((64, 64))
        self.rect = self.surface.get_rect()
        self.rect.x = self.posX
        self.rect.y = self.posY

    def update(self, rect):

        global movArriba, movAbajo, movDerecha, movIzquierda

        if self.rect.colliderect(rect):
            if movArriba:
                self.rect.top -= 64

            if movAbajo:
                self.rect.top += 64

            if movDerecha:
                self.rect.left += 64

            if movIzquierda:
                self.rect.left -= 64

        pygame.draw.rect(pantalla, 'white', self.rect) 

class pared(pygame.sprite.Sprite):

    def __init__(self, posX, posY):

        # Aca se heredan las propiedades
        pygame.sprite.Sprite.__init__(self)

        self.posX = posX
        self.posY = posY
        self.surface = pygame.Surface((64, 64))
        self.rect = self.surface.get_rect()
        self.rect.x = self.posX
        self.rect.y = self.posY

    def update(self):

        pygame.draw.rect(pantalla, 'white', self.rect, 2) 

class mapa:

    def __init__(self, totalSalas, totalCapaz, salas = []):
        self.totalSalas = totalSalas # Cantidad de salas totales que se tienen que procesar (mayor cantidad a medida que se pasan niveles)
        self.totalCapaz = totalCapaz
        self.salas = salas
        
        self.cantCapas = 3 # Elige la cantidad de capas (Valor de Y en index de lista) Por ahora lo hago en un valor fijo

    def agregar(self, sala, indexYmapa):
        self.salas[indexYmapa].append(sala)
    def definirForma(self):
        self.salas = [[] for filas in range(self.totalSalas) for columnas in range(self.totalCapaz)]
        

    def SeleccionarSala(self, indexYmapa, indexXmapa):
        return self.salas[indexYmapa][indexXmapa]
    
    def clearMapa(self):
        self.salas = []

    def dibujarMapa(self):

        esquinaDerecha = pantalla.get_width() - cantPixelesPorLadoCasilla
        esquinaArriba = 0 + cantPixelesPorLadoCasilla

        pygame.draw.rect(pantalla, 'white', [esquinaDerecha - (self.totalCapaz * 64), esquinaDerecha, esquinaArriba, esquinaArriba + (self.totalCapaz * 64)], 2)

class habitacion:

    def __init__(self, posZonaSeguras = [[]], posBloques = [], salaActual = False, salidas = []):

        self.posZonaSeguras = posZonaSeguras
        self.posBloques = posBloques
        self.salaActual = salaActual
        self.salidas = salidas

    def colocarZonaSegura(self):
        for y in self.posZonaSeguras:
            self.posBloques[y[0]][y[1]] = 6

    def get_Salidas(self):
        return self.salidas

def dibujarReglas():

    textoReglas = tipografia.render('Mueve a tu avatar con las flechas para que lleve los virus a las zonas protegidas.', False, colorBlanco)
    
    ancho=650
    alto=25
    x=64
    y=3
    pygame.draw.rect(pantalla,colorBordeaux,(x,y,ancho,alto))
    pantalla.blit(textoReglas,(x+5,y,ancho,alto))


def actualizarTiempoRestante():
    global segundosRestantes
    ancho=350
    alto=30
    x=75+(cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla)
    y=cantPixelesPorLadoCasilla*7
    pygame.draw.rect(pantalla,colorBordeaux,(x,y,ancho,alto))
    textoSegundosRestantes = tipografiaGrande.render('Tiempo restante: ' + str(round(segundosRestantes)), False, colorBlanco)
    pantalla.blit(textoSegundosRestantes,(x+5,y,ancho,alto))

    calculoPorcentajeTiempo = round((100 * segundosRestantes)/tiempoParaSolucionarElNivel) 
    textoPorcentaje = tipografiaGrande.render(str(calculoPorcentajeTiempo) + ' %', False, colorBlanco)
    y=cantPixelesPorLadoCasilla*7+32
    pygame.draw.rect(pantalla,colorAzul,(x,y,200,alto))
    pygame.draw.rect(pantalla,colorNaranja,(x,y,calculoPorcentajeTiempo*2,alto))

    pantalla.blit(textoPorcentaje,(x,y,ancho,alto))

def actualizarContadorMovUAIBOT():
    global contMovUAIBOT
    contMovUAIBOT=contMovUAIBOT+1

def actualizarContadorMovUAIBOTA():
    global contMovUAIBOTA
    contMovUAIBOTA=contMovUAIBOTA+1

def actualizarContadorMovUAIBOTINA():
    global contMovUAIBOTINA
    contMovUAIBOTINA=contMovUAIBOTINA+1

def actualizarTiempoDeJuegoActual():
      
    global segundosTranscurridos
    ancho=350
    alto=30
    x=75+(cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla)
    y=cantPixelesPorLadoCasilla*8
    pygame.draw.rect(pantalla,colorBordeaux,(x,y,ancho,alto))
    textoSegundos = tipografiaGrande.render('Segundos transcurridos: ' + str(round(segundosTranscurridos)), False, colorBlanco)
    pantalla.blit(textoSegundos,(x+5,y,ancho,alto))
   
def dibujarCartelIndicadorRonda():
    textoFelicitacion = tipografiaGrande.render('Ronda final', False, colorBlanco)
    ancho=160
    alto=50
    x=350+(cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla)
    y=5
    pygame.draw.rect(pantalla,colorBordeaux,(x,y,ancho,alto))
    pantalla.blit(textoFelicitacion,(x+5,y,ancho,alto))
    

def obtenerDelArchivo5ConMenosMovimientos():
  file = open("ranking.txt", "r")
  lstMovimientos=[]

  nombreAgregado=False
  par=[]
      
  lineas= file.readlines()
  lineas = [line.strip() for line in open('ranking.txt')]

  for line in lineas:
    
    if not (line==''):
        if (nombreAgregado==False):
            par=[]
            par.append(line)
            nombreAgregado=True
        else:    
            par.append(str(line))
            lstMovimientos.append(par)
            nombreAgregado=False
 
  lstMovimientos.sort(key=lambda x: x[1], reverse=False)

  lstMovimientos = lstMovimientos[:5]

  file.close() 
  
  return lstMovimientos

def dibujarRanking():
    lst5Jugadores=obtenerDelArchivo5ConMenosMovimientos()
    ancho=220
    alto=40
    x=75+(cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla)
    i=8
     
    for par in lst5Jugadores:
        y=(32*i)-135
        textoRanking = tipografiaGrande.render(str(par[0]) + ': ' + str(par[1]), False, colorBlanco)
        pygame.draw.rect(pantalla,colorBordeaux,(x,y,ancho,alto))
        pantalla.blit(textoRanking,(x+5,y,ancho,alto))
        i=i+1
    
def dibujarPorcentajeDeMovimientos():

    global cantidadDeMovimientosActual

    ancho=220
    alto=40
    x=850
    y=25

    if (cantidadDeMovimientosActual > 0):

        porcentajeMovUAIBOT=(100*contMovUAIBOT)/cantidadDeMovimientosActual
        porcentajeMovUAIBOTA=(100*contMovUAIBOTA)/cantidadDeMovimientosActual
        porcentajeMovUAIBOTINA=(100*contMovUAIBOTINA)/cantidadDeMovimientosActual
    
        textoPorcentajeMovUAIBOT=tipografiaGrande.render('UAIBOT: ' + str(round(porcentajeMovUAIBOT)) + ' %', False, colorBlanco)
        textoPorcentajeMovUAIBOTA=tipografiaGrande.render('UAIBOTA: ' + str(round(porcentajeMovUAIBOTA)) + ' %', False, colorBlanco)
        textoPorcentajeMovUAIBOTINA=tipografiaGrande.render('HIJOS: ' + str(round(porcentajeMovUAIBOTINA)) + ' %', False, colorBlanco)
    
        y=y+100
        pygame.draw.rect(pantalla,colorBordeaux,(x,y,ancho,alto))
        pantalla.blit(textoPorcentajeMovUAIBOT,(x+5,y,ancho,alto))
        y=y+60
        pygame.draw.rect(pantalla,colorBordeaux,(x,y,ancho,alto))
        pantalla.blit(textoPorcentajeMovUAIBOTA,(x+5,y,ancho,alto))
        y=y+60
        pygame.draw.rect(pantalla,colorBordeaux,(x,y,ancho,alto))
        pantalla.blit(textoPorcentajeMovUAIBOTINA,(x+5,y,ancho,alto))


def dibujarZonaDeTransporte(zona):

    global avatarRect
    # Los For arrancan a contar desde el 1 ya que despues se multiplican con los las coordenadas
    # Si arrancaran en 0, se dibujarian pegados a los bordes de la pantalla

    for y in range(1,cantidadDeCasillasPorLado+1):
        for x in range(1,cantidadDeCasillasPorLado+1):
            
            pygame.draw.rect(pantalla, colorVerde,[cantPixelesPorLadoCasilla*x,cantPixelesPorLadoCasilla*y,cantPixelesPorLadoCasilla,cantPixelesPorLadoCasilla])
            
            if zona[y][x] in [1, 3, 4, 5, 6]:

                totalImagenes = [0, imgPared, 0, imgAvatar, imgVirus, imgParedAlternativa, imgAreaProtegida]
                pantalla.blit(totalImagenes[zona[y][x]], (cantPixelesPorLadoCasilla*x,cantPixelesPorLadoCasilla*y))
           
 
                # El jugador se compone de dos partes:
                    # El sprite y la posicion en la que se dibuja
                    # El marco de la colision
                # Esto quiere decir que puede darse el error de que se dibuje en un lado y detecte que colisiona con algo de otra parte

    pygame.draw.rect(pantalla, colorBlanco, [cantPixelesPorLadoCasilla,cantPixelesPorLadoCasilla,cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla,cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla],1)       
    

def dibujarTodo(zona):
    dibujarFondo()
    dibujarZonaDeTransporte(zona)
    dibujarCartelIndicadorRonda()
    dibujarReglas()
    dibujarRanking()

def estaSolucionado(zona):

    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/paseNivel.wav"))

    dibujarCartelIndicadorRonda()
    dibujarReglas()
    escribirMovimientosEnArchivo(zona)
    dibujarPorcentajeDeMovimientos()

###################################### Clases #######################################################
# Empiezo a programar la clase del virus sinosuidal
class Sinosuidal: 

    def __init__(self, sprite):

        # Sprite aleatorio
        self.sprite = sprite
        self.marca = pygame.Rect(0, 0, 64,64)
        
        # Variables para las funciones de movimiento
        self.virusBool = True
        self.marca.top = 0
        self.marca.left = 0
        self.orientacionX = ''
        self.orientacionY = ''
        self.instancia = 0

        # Condiciones para la funcion de dibujo
        # Se va a empezar a usar cuando se agrege la funcionalidad de la mira
        self.spawnBool = True
        
    def establecerMov(self):
            
        if self.virusBool:

            # Decidir velocidad del virus.
            self.velocidadX = random.randrange(150, 250, 1)
            # Definir el ancho de curvas que va a dar en la pantalla, a mas anchas menos curvas va a dar
            self.curvaAncho = random.choice([100, 100, 150])

            # Decidir puntos de inicio, (posiciones posibles entre la altura de la grilla)
            self.marca.top = random.choice([64, 128, 192, 256, 320, 384, 448, 512])
            self.marca.left = random.choice([64, 512])
            if self.marca.left == 64:
                self.orientacionX = '+'
            if self.marca.left == 512:
                self.orientacionX = '-'

            self.virusBool = False

    def movVirus(self):
        
        if self.spawnBool:

            # Usa la funcion 'eval()' para calcular con texto 
            # el dt son los fps, hace un poquito mas fluido el movimiento del virus. Con las teclas no se nota mucho pero es mas claro con el mouse
            self.marca.left = eval(str(self.marca.left) + self.orientacionX + str(self.velocidadX * dt))

            # Explicacion del calculo.
                # 64 +: Se le suma 64 ya que no esta adherido a la parte superior de la pantalla, inicia unos 64 pixeles mas abajo, en la grilla
                # Parentesis:
                    # 1 +: Se le suma 1 para que el seno no tenga forma negativa (en un grafico es mas claro el porque)
                    # funcion math.sin: (Saca el seno de lo que este dentro del parentesis)
                        # self.marca.left: para que el virus se mueva a la par del valor X
                        # se divide con self.curvaAncho para que tarde un poco en cambiar la orientacion vertical
                # * 224: La altura maxima a la que sube y baja el virus, (es la mitad de pixeles que toma la grilla)
            self.marca.top = 64 + (1 + math.sin(self.marca.left/self.curvaAncho)) * 224

        if self.marca.left < 64 or self.marca.left + 64 > 576:
            self.virusBool = True

        if self.marca.top < 64:
            self.marca.top = 64
            

        elif self.marca.top > 512:
            self.marca.top = 512

    def dibujarVirus(self, tiempo):
        # pygame.draw.rect(pantalla, 'red', [self.marca.left, self.marca.top, 64, 64])

        # De momento es un cuadrado, despues le agrego un sprite.
        # Mas tarde agregar Collider
        if self.spawnBool or tiempo >= 250:
            self.spawnBool = True
            pantalla.blit(pygame.transform.scale(pygame.image.load(self.sprite), (64, 64)), (self.marca.left, self.marca.top))

# El atributo de sprite es un string, pero en realidad la clase
# todavia no usa ningun parametro mas que self.
virusSinosuidal = Sinosuidal(random.choice(listaVirus)) 
# Funciones para reestablecer las variables a su valor inicial. Funciones que corroboran si se cumplen condiciones de derrota o victoria.

#Clase de textos
class Textos:

    def __init__(self):
        
        self.posy = 0
        self.posx = 0
        self.color = "black"
        self.mensaje = "Lorem Ipsum"


    def mostrar(self, mensaje,posy,posx,colorBg,color="black"):

        self.mensaje = mensaje
        self.color = color
        self.posx = posx
        self.posy = posy

        ancho = 200
        alto = 200

        self.text = tipografia.render(self.mensaje, True, self.color)
        self.text2 = tipografia.render("█" * len(mensaje), True, colorBg)
        self.text_rect = self.text.get_rect(center=(self.posy, self.posx))
        pantalla.blit(self.text2, self.text_rect)
        pantalla.blit(self.text, self.text_rect)
        pygame.display.update()

#Clase de boton
class Button():
    def __init__(self, imagen, x_pos, y_pos, texto_boton, presionado):
        self.imagen = imagen
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.imagen.get_rect(center=(self.x_pos, self.y_pos))
        self.texto_boton = texto_boton
        self.text = tipografia.render(self.texto_boton, True, "black")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.presionado = presionado

    def Actualizar(self):
        pantalla.blit(self.imagen, self.rect)
        pantalla.blit(self.text, self.text_rect)
    
    def CambiarContenido(self,texto_boton):
        self.texto_boton = texto_boton
        self.text = tipografia.render(self.texto_boton, True, "black")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    #Detecta el input en el boton
    def DetectarInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
                        

    def CambiarColorBoton(self, position,color1,color2):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = tipografia.render(self.texto_boton, True, color1)
        else:
            self.text = tipografia.render(self.texto_boton, True, color2)

#Clase de inputs
class Input(pygame.sprite.Sprite):
    def __init__(self, x, y, width, font, bgColor):
        super().__init__()
        self.txtColor = (255, 255, 255)
        self.bgColor = None
        self.pos = (x, y) 
        self.width = width
        self.fuente = font
        self.bgColor = bgColor
        self.activo = False
        self.text = ""
        self.mostrarTexto()

    def mostrarTexto(self):
        t_surf = self.fuente.render(self.text, True, self.txtColor, self.bgColor)
        self.image = pygame.Surface((max(self.width, t_surf.get_width()+10), t_surf.get_height()+10), pygame.SRCALPHA)
        if self.bgColor:
            self.image.fill(self.bgColor)
        self.image.blit(t_surf, (5, 5))
        pygame.draw.rect(self.image, self.txtColor, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(topleft = self.pos)
        pygame.display.update()

    def update(self):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.activo:
            self.activo = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.activo:
            if event.key == pygame.K_RETURN:
                self.activo = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                if (self.text == ""):
                    #Hacer la funcion cagada de nuevo o cambiar la condicion 
                    #dibujarMenu()
                    pass
            else:
                self.text += event.unicode
            self.mostrarTexto()
            
    def redefinir(self):
        self.text = ""
        self.mostrarTexto()

################################################ Fin clases #############################################

# Aca defino el objeto de personaje, pero lo ideal seria que si agregamos mas clases las definamos en un espacio apropiado
# Añadir clase de paredes para collide y que no se empujen dos cosas a la vez

crearMapa = mapa(2, 2)
crearMapa.definirForma()

# ceacion del "tablero", se hizo un array que a su vez contiene 9 arrays, (solo se usan 8, evitando el primero) los cuales, se inician llenandolos de espacios vacios, despues se cambian esos 0s por valores de palabras

zonaDeTransporte1 = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 0, 1, 1, 1, 1],
                    [1, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 6, 0, 5, 0, 0, 0, 0],
                    [1, 1, 3, 0, 4, 1, 0, 0, 1],
                    [1, 1, 6, 0, 0, 4, 0, 0, 1],
                    [1, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1]]

zonaDeTransporte1[posYjugador][posXjugador] = 3

zonaDeTransporte2 = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 0, 0, 4, 0, 0, 0, 1],
                    [1, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 0, 1, 1, 1, 1]]

zonaDeTransporte3 = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 0, 0, 0, 1, 0, 0, 1],
                    [1, 1, 0, 0, 0, 1, 0, 0, 1],
                    [1, 1, 0, 0, 0, 1, 0, 4, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1]]

sala1 = habitacion([[4, 2], [6, 2]], zonaDeTransporte1, True, ['arriba', 'derecha'])
sala2 = habitacion([[2, 5]], zonaDeTransporte2, False, ['abajo'])
sala3 = habitacion([[4, 7]], zonaDeTransporte3, False, ['izquierda'])

crearMapa.agregar(sala1, 1)
crearMapa.agregar(sala2, 0)
crearMapa.agregar(sala3, 1)


for indexYmap in crearMapa.salas:
    for habitacionActual in indexYmap:
        if habitacionActual.salaActual:
            break

for numY, y in enumerate(habitacionActual.posBloques):
    for numX, x in enumerate(y):
        if x == 3:
            personaje = jugador(64 * numX, 64 * numY, 64, 64)

def definirMapa():

    # ceacion del "tablero", se hizo un array que a su vez contiene 9 arrays, (solo se usan 8, evitando el primero) los cuales, se inician llenandolos de espacios vacios, despues se cambian esos 0s por valores de palabras

    zonaDeTransporte1 = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 0, 1, 1, 1, 1],
                        [1, 1, 0, 0, 0, 0, 0, 0, 1],
                        [1, 1, 0, 0, 0, 0, 0, 0, 1],
                        [1, 1, 6, 0, 5, 0, 0, 0, 0],
                        [1, 1, 3, 0, 4, 1, 0, 0, 1],
                        [1, 1, 6, 0, 0, 4, 0, 0, 1],
                        [1, 1, 0, 0, 0, 0, 0, 0, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1]]

    zonaDeTransporte1[posYjugador][posXjugador] = 3

    zonaDeTransporte2 = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 0, 0, 4, 0, 0, 0, 1],
                        [1, 1, 0, 0, 0, 0, 0, 0, 1],
                        [1, 1, 0, 0, 0, 0, 0, 0, 1],
                        [1, 1, 0, 0, 0, 0, 0, 0, 1],
                        [1, 1, 0, 0, 0, 0, 0, 0, 1],
                        [1, 1, 0, 0, 0, 0, 0, 0, 1],
                        [1, 1, 1, 1, 0, 1, 1, 1, 1]]

    zonaDeTransporte3 = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 0, 0, 0, 0, 0, 0, 1],
                        [1, 1, 0, 0, 0, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0, 1],
                        [1, 1, 0, 0, 0, 1, 0, 0, 1],
                        [1, 1, 0, 0, 0, 1, 0, 0, 1],
                        [1, 1, 0, 0, 0, 1, 0, 4, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1]]

    global indexX, indexY

    indexX = 0
    indexY = 1

    crearMapa.clearMapa()
    crearMapa.definirForma()

    sala1 = habitacion([[4, 2], [6, 2]], zonaDeTransporte1, True, ['arriba', 'derecha'])
    sala2 = habitacion([[2, 5]], zonaDeTransporte2, False, ['abajo'])
    sala3 = habitacion([[4, 7]], zonaDeTransporte3, False, ['izquierda'])

    crearMapa.agregar(sala1, 1)
    crearMapa.agregar(sala2, 0)
    crearMapa.agregar(sala3, 1)
    
    personaje.reiniciar()

    for indexYmap in crearMapa.salas:
        for habitacionActual in indexYmap:
            if habitacionActual.salaActual:
                return habitacionActual


def resetearJuego():

    global zonaDeTransporte, cantidadDeMovimientosRestantes, cantidadDeMovimientosActual, ticksAlComenzar
    global contMovUAIBOT, contMovUAIBOTA, contMovUAIBOTINA

    contMovUAIBOT=0
    contMovUAIBOTA=0
    contMovUAIBOTINA=0

    virusQueSeMueveRect.left =cantPixelesPorLadoCasilla * cantidadDeCasillasPorLado
    virusQueSeMueveRect.top = cantPixelesPorLadoCasilla * (cantidadDeCasillasPorLado - 1)
           
    virusSinusoidalRect.left =cantPixelesPorLadoCasilla * cantidadDeCasillasPorLado
    virusSinusoidalRect.top = cantPixelesPorLadoCasilla * (cantidadDeCasillasPorLado - 1)

    cantidadDeMovimientosActual=0

    cantidadDeMovimientosRestantes=cantidadDeMovimientosDeterminada

    ticksAlComenzar=pygame.time.get_ticks()

def escribirEnArchivo(nombre, cantMovimientosUtilizados):
    file = open("ranking.txt", "a")
    file.write(nombre)
    file.write('\n')
    file.write(str(cantMovimientosUtilizados))
    file.write('\n')
    file.close()

def escribirMovimientosEnArchivo(zona):

    global cantidadDeMovimientosActual, nivelCompletado, nombreJugador
    escribirEnArchivo(nombreJugador, cantidadDeMovimientosActual)
    resetearJuego(zona)

definirMapa()

while not salirJuego:

    segundosTranscurridos=(pygame.time.get_ticks()-ticksAlComenzar)/1000
    segundosRestantes=tiempoParaSolucionarElNivel-round((pygame.time.get_ticks()-ticksAlComenzar)/1000)

    dibujarFondo()
    
    actualizarTiempoDeJuegoActual() 
    actualizarTiempoRestante()
    

    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            salirJuego = True

        if event.type == pygame.MOUSEBUTTONDOWN:
           if miraRect.colliderect(virusQueSeMueveRect):
                virusQueSeMueveRect.left = cantPixelesPorLadoCasilla * cantidadDeCasillasPorLado
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r: 
                print(cantidadDeMovimientosRestantes)

            elif event.key == pygame.K_e:
                match personajeActual:
                    case "UAIBOT":          
                        imgAvatar=pygame.transform.scale(pygame.image.load("assets/img/UAIBOTA.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
                        personajeActual="UAIBOTA"
                    case "UAIBOTA":
                        imgAvatar=pygame.transform.scale(pygame.image.load("assets/img/UAIBOTINA.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
                        personajeActual="UAIBOTINA"
                    case "UAIBOTINA":
                        imgAvatar=pygame.transform.scale(pygame.image.load("assets/img/UAIBOTINO.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
                        personajeActual="UAIBOTINO"
                    case "UAIBOTINO":
                        imgAvatar=pygame.transform.scale(pygame.image.load("assets/img/UAIBOT.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
                        personajeActual="UAIBOT"

            personaje.mover(bool = habitacionActual.salidas, robot = personajeActual, lista = habitacionActual.posBloques) 
              
        virusQueSeMueveRect.left = virusQueSeMueveRect.left - 1
        
        x = pygame.time.get_ticks() / 40  % 400
        y = int(math.sin(x/25.0) * 50 + 160)

        virusSinusoidalRect.left=x+cantPixelesPorLadoCasilla
        virusSinusoidalRect.top=y

        miraRect.center=(pygame.mouse.get_pos())
        rectanguloDeZonaDeTransporte=pygame.Rect(cantPixelesPorLadoCasilla*2,cantPixelesPorLadoCasilla*2,cantPixelesPorLadoCasilla * (cantidadDeCasillasPorLado-2),cantPixelesPorLadoCasilla * (cantidadDeCasillasPorLado-2))
        
        if miraRect.colliderect(rectanguloDeZonaDeTransporte):
            pantalla.blit(imgMira, (miraRect.left, miraRect.top))    
                     
    pantalla.blit(imgVirusQueSeMueve, (virusQueSeMueveRect.left, virusQueSeMueveRect.top))   
    pantalla.blit(imgVirusSinusoidal, (virusSinusoidalRect.left, virusSinusoidalRect.top)) 

    habitacionActual.colocarZonaSegura()
    habitacionActual.posBloques[personaje.y][personaje.x] = 3
    dibujarZonaDeTransporte(habitacionActual.posBloques)
    
    dt = reloj.tick() / 1000

    # Bool que busca si quedaron virus en el mapa, por defecto esta en True (Diciendo que no hay)
    boolNoHayVirus = True

    # Son muchos for... Despues veo como reducirlos, pasa que son muchos arrays.
    # Busca en el mapa, y en este, cada habitacion que tiene para buscar virus.
    # Si encuentra alguno: La bool anterior se corrije, impidiendo que se gane el juego
    for capaz in crearMapa.salas:
        for habitaciones in capaz:
            for listaY in habitaciones.posBloques:
                if 4 in listaY: # Se encontro un virus en le mapa, lo que quiere decir que el juego no termino
                    boolNoHayVirus = False

    # Si no se encontro un virus y la bool se mantuvo en True: El jugador gano.
    if boolNoHayVirus == True:
        definirMapa()
        estaSolucionado(habitacionActual.posBloques)

    if segundosRestantes <= 0 or virusQueSeMueveRect.colliderect(avatarRect) or virusSinusoidalRect.colliderect(avatarRect) or cantidadDeMovimientosRestantes <= 1:
        habitacionActual = definirMapa()
        resetearJuego()

    if boolCambioSala == True:

        for numy, y in enumerate(habitacionActual.posBloques):
            for numx, x in enumerate(y):
                if habitacionActual.posBloques[numy][numx] == 3:
                    habitacionActual.posBloques[numy][numx] = 1

        habitacionActual.salaActual = False
        habitacionActual = crearMapa.SeleccionarSala(indexY, indexX)
        habitacionActual.salaActual = True

        boolCambioSala = False
        
    if (virusQueSeMueveRect.left < cantPixelesPorLadoCasilla):
        virusQueSeMueveRect.left = cantPixelesPorLadoCasilla * cantidadDeCasillasPorLado

    pygame.display.flip()
         
pygame.quit()