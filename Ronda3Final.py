#!/usr/bin/env python
#-*- coding: utf-8 -*-

import math
import pygame
import random

pygame.init()
pygame.font.init() 
pygame.mixer.music.load("paseNivel.wav") 
pygame.display.set_caption("OFIRCA 2023 - Resolución de todas las rondas")
pantalla= pygame.display.set_mode((1152,648))
tipografia = pygame.font.SysFont('Arial', 18)
tipografiaGrande=pygame.font.SysFont('Arial', 24)

# -----> Variables Nuestras <-----#

reloj = pygame.time.Clock()
dt = 0
movArriba, movAbajo, movDerecha, movIzquierda = False, False, False, False

posXjugador = 2
posYjugador = 5

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

ticksAlComenzar=pygame.time.get_ticks()
personajeActual='UAIBOT'
tiempoParaSolucionarElNivel=55
cantidadDeMovimientosActual=0
cantidadDeMovimientosRestantes=10
colorVerde,colorAzul,colorBlanco,colorNegro, colorNaranja, colorBordeaux= (11,102,35),(0,0,255),(255,255,255),(0,0,0),(239,27,126),(102,41,53)
cantidadDeCasillasPorLado=8 # Debe ser número par ya que la zona es un cuadrado
cantPixelesPorLadoCasilla=64
salirJuego = False
lstAreaProtegida=[]

imgAvatar=pygame.transform.scale(pygame.image.load("UAIBOT.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
avatarRect=imgAvatar.get_rect()   
imgMira=pygame.transform.scale(pygame.image.load("mira.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
imgPared=pygame.transform.scale(pygame.image.load("pared.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
imgParedAlternativa=pygame.transform.scale(pygame.image.load("paredAlternativa.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
imgParedAlternativa=pygame.transform.scale(pygame.image.load("paredAlternativa.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  

imgAreaProtegida=pygame.transform.scale(pygame.image.load("areaprotegida.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
listaVirus  = ["virus1.png","virus2.png","virus3.png","virus4.png","virus5.png","virus6.png"]

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
    fondo = pygame.image.load("fondo.png")
    pantalla.blit(fondo, (0, 0))

#region tablero
def crearZonaDeTransporte():

    # ceacion del "tablero", se hizo un array que a su vez contiene 9 arrays, (solo se usan 8, evitando el primero) los cuales, se inician llenandolos de espacios vacios, despues se cambian esos 0s por valores de palabras

    zonaDeTransporte = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 1, 1, 1, 1, 1, 1, 1, 1],
                        [0, 1, 0, 0, 0, 0, 0, 0, 1],
                        [0, 1, 0, 0, 0, 0, 0, 0, 1],
                        [0, 1, 6, 0, 5, 0, 0, 0, 1],
                        [0, 1, 3, 0, 4, 1, 0, 0, 1],
                        [0, 1, 6, 0, 0, 4, 0, 0, 1],
                        [0, 1, 0, 0, 0, 0, 0, 0, 1],
                        [0, 1, 1, 1, 1, 1, 1, 1, 1]]
    
    zonaDeTransporte[posYjugador][posXjugador] = 3
    
    return zonaDeTransporte

zonaDeTransporte=crearZonaDeTransporte()

def hayAreaProtegidaEn(x,y):
    punto=(x,y)
    return lstAreaProtegida.__contains__(punto)

def posicionarElemento(elemento,x,y): 
    global zonaDeTransporte
    global avatarRect
    zonaDeTransporte[x][y]=elemento
    if (elemento=='jugador'):
        r=pygame.Rect(cantPixelesPorLadoCasilla * (x),cantPixelesPorLadoCasilla * (y),cantPixelesPorLadoCasilla,cantPixelesPorLadoCasilla)
        avatarRect=r

def borrarElemento(x,y):
    global zonaDeTransporte
    zonaDeTransporte[x][y]=0

#endregion

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
        
        self.cambioSala = False
        """
        # Esto es para probar el cambio de 'salas', ahora solo cambia de color la pantalla

        # si llega a uno de los dos extremos de la pantalla y tiene una habitacion al costado, pasa a esa sala (el mapa cambia de color y se posiciona al otro extremo de la pantalla), 
        # si no, 
        # choca contra la pared (su posicion se establece al mayor rango que tiene, para dar la ilusion de un limite)

        if self.rect.right >= pantalla.get_width():

            if signo == '+' and 'derecha' in bool:
                self.rect.left = 0
                self.cambioSala = True
                indexHorizontal += 1
            else:
                self.rect.right = pantalla.get_width()

        if  self.rect.left <= 0:

            if signo == '-' and 'izquierda' in bool:
                self.rect.right = pantalla.get_width()
                self.cambioSala = True
                indexHorizontal -= 1
            else:
                self.rect.left = 0"""
        
     #------------>Personaje: 1. Arrastrar Bloques<-------------#
    # Utilidad de las siguientes 4 funciones:  
    # Revisa si en la direccion contraria a la que se va a mover (Ej: Si se mueve para arriba, mira la casilla de abajo), tiene un virus para mover
    # Si es cierto, arrastra al virus hacia la posicion del jugador y se limpia (regresa a 0) la posicion del virus
    # Si NO lo es, limpia solo la posicion que tenia el jugador antes de moverse

    def ArrastrarVertical(self, simbolo, opuesto, lista):
        
        if lista[eval(str(self.y) + simbolo + '1')][self.x] == 0:

            self.pasosRealizados += 1
                
            if lista[eval(str(self.y) + opuesto + '1')][self.x] == 4:


                lista[eval(str(self.y) + opuesto + '1')][self.x] = 0
                lista[self.y][self.x] = 4
                
            else:
                
                lista[self.y][self.x] = 0

            self.y = eval(str(self.y) + simbolo + '1')
        
    def ArrastrarHorizontal(self, simbolo, opuesto, lista):
            
        if lista[self.y][eval(str(self.x) + simbolo + '1')] == 0:

            self.pasosRealizados += 1

            if lista[self.y][eval(str(self.x) + opuesto + '1')] == 4:

                    
                lista[self.y][eval(str(self.x) + opuesto + '1')] = 0
                lista[self.y][self.x] = 4

            else:

                lista[self.y][self.x] = 0
                juego.boolVirus = True

            self.x = eval(str(self.x) + simbolo + '1')

    #------------>Personaje: 2. Saltar Bloques<-------------#

    def SaltarVertical(self, simbolo, lista):

        if lista[eval(str(self.y) + simbolo + '1')][self.x] == 4 and lista[eval(str(self.y) + simbolo + '2')][self.x] in [0, 2]:


            self.pasosRealizados += 1

            lista[self.y][self.x] = 0
            self.y = eval(str(self.y) + simbolo + '2')

        elif lista[eval(str(self.y) + simbolo + '1')][self.x] == 0:

            self.pasosRealizados += 1
            
            lista[self.y][self.x] = 0
            self.y = eval(str(self.y) + simbolo + '1')  
    
    def SaltarHorizontal(self, simbolo, lista):

        if lista[self.y][eval(str(self.x) + simbolo + '1')] == 4 and lista[self.y][eval(str(self.x) + simbolo + '2')] in [0, 2]:

            self.pasosRealizados += 1

            lista[self.y][self.x] = 0
            self.x = eval(str(self.x) + simbolo + '2')

        elif lista[self.y][eval(str(self.x) + simbolo + '1')] in [0, 2]:

            self.pasosRealizados += 1
                
            lista[self.y][self.x] = 0
            self.x = eval(str(self.x) + simbolo + '1')   
                  
    def EmpujarVertical(self, simbolo, lista):

        if lista[eval(str(self.y) + simbolo + '1')][self.x] == 4 and lista[eval(str(self.y) + simbolo + '2')][self.x] in [0, 2]:


            lista[self.y][self.x] = 0
            self.y = eval(str(self.y) + simbolo + '1')
            lista[eval(str(self.y) + simbolo + '1')][self.x] = 4
            
        elif lista[eval(str(self.y) + simbolo + '1')][self.x] == 0:


            lista[self.y][self.x] = 0
            self.y = eval(str(self.y) + simbolo + '1')
        
    def EmpujarHorizontal(self, simbolo, lista):

        if lista[self.y][eval(str(self.x) + simbolo + '1')] in [4, 5] and lista[self.y][eval(str(self.x) + simbolo + '2')] in [0, 6]:
            
            lista[self.y][self.x] = 0
            lista[self.y][eval(str(self.x) + simbolo + '2')] = lista[self.y][eval(str(self.x) + simbolo + '1')] 
            self.x = eval(str(self.x) + simbolo + '1')
            
        elif lista[self.y][eval(str(self.x) + simbolo + '1')] == 0:

            lista[self.y][self.x] = 0
            self.x = eval(str(self.x) + simbolo + '1')

    def mover(self, pared, virus, robot, bool = [], lista = []):
        
        if pygame.key.get_pressed()[pygame.K_w]:
            
            match robot:
                    case "UAIBOT":
                        self.EmpujarHorizontal('-', lista)
                    case "UAIBOTA":
                        self.ArrastrarHorizontal('-', '+', lista)
                    case "UAIBOTINA":
                        self.SaltarHorizontal('-', lista)
                    case "UAIBOTINO":
                        self.SaltarHorizontal('-', lista)
                

        if pygame.key.get_pressed()[pygame.K_s]:
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
             match personajeActual:
                    case "UAIBOT":
                        self.EmpujarVertical('+', lista)
                    case "UAIBOTA":
                        self.ArrastrarVertical('+', '-', lista)
                    case "UAIBOTINA":
                        self.SaltarVertical('+', lista)
                    case "UAIBOTINO":
                        self.SaltarVertical('+', lista)


        if pygame.key.get_pressed()[pygame.K_a]:
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
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
        lista[self.y][self.x] = 3


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

        pantalla.blit(imgVirus, (self.rect.left, self.rect.top))

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

        pantalla.blit(imgPared, (self.rect.left, self.rect.top)) 

# Aca defino el objeto de personaje, pero lo ideal seria que si agregamos mas clases las definamos en un espacio apropiado
# Añadir clase de paredes para collide y que no se empujen dos cosas a la vez
virusGrupo = pygame.sprite.Group()
paredGrupo = pygame.sprite.Group()

for numY, y in enumerate(zonaDeTransporte):
    for numX, x in enumerate(y): 

        if y[numX] == 3:
            personaje = jugador(numX * 64, numY * 64, 64, 64)
        #if y[numX] == 2:
        #    virusGrupo.add(virus(numX * 64, numY * 64))
        #if y[numX] == 1:
        #   paredGrupo.add(pared(numX * 64, numY * 64))


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

    global zonaDeTransporte
    global avatarRect
    
    # Los For arrancan a contar desde el 1 ya que despues se multiplican con los las coordenadas
    # Si arrancaran en 0, se dibujarian pegados a los bordes de la pantalla

    for y in range(1,cantidadDeCasillasPorLado+1):
        for x in range(1,cantidadDeCasillasPorLado+1):
            
            pygame.draw.rect(pantalla, colorVerde,[cantPixelesPorLadoCasilla*x,cantPixelesPorLadoCasilla*y,cantPixelesPorLadoCasilla,cantPixelesPorLadoCasilla])
            
            if zona[y][x] in [1, 3, 4, 5, 6]:

                totalImagenes = [0, imgPared, 0, imgAvatar, imgVirus, imgParedAlternativa, imgAreaProtegida]
                pantalla.blit(totalImagenes[zonaDeTransporte[y][x]], (cantPixelesPorLadoCasilla*x,cantPixelesPorLadoCasilla*y))
           

                # El jugador se compone de dos partes:
                    # El sprite y la posicion en la que se dibuja
                    # El marco de la colision
                # Esto quiere decir que puede darse el error de que se dibuje en un lado y detecte que colisiona con algo de otra parte

    pygame.draw.rect(pantalla, colorBlanco, [cantPixelesPorLadoCasilla,cantPixelesPorLadoCasilla,cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla,cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla],1)       
    

def dibujarTodo():
    dibujarFondo()
    dibujarZonaDeTransporte(zonaDeTransporte)
    dibujarCartelIndicadorRonda()
    dibujarReglas()
    dibujarRanking()


#dibujarTodo()

def estaSolucionado():

    global nivelCompletado
    global zonaDeTransporte

    cantVirusSobreAreasProtegidas=0

    for punto in lstAreaProtegida:
        x=punto[0]
        y=punto[1]
        if zonaDeTransporte[x][y]=='virus':
            cantVirusSobreAreasProtegidas=cantVirusSobreAreasProtegidas+1       

    if (cantVirusSobreAreasProtegidas==len(lstAreaProtegida)):
        nivelCompletado=True
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("paseNivel.wav"))
        
    else:
        nivelCompletado=False

    dibujarCartelIndicadorRonda()
    dibujarReglas()
    escribirMovimientosEnArchivo()
    dibujarPorcentajeDeMovimientos()

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

    zonaDeTransporte=crearZonaDeTransporte()
    cantidadDeMovimientosActual=0

    cantidadDeMovimientosRestantes=cantidadDeMovimientosDeterminada

    ticksAlComenzar=pygame.time.get_ticks()
    dibujarTodo()

def escribirEnArchivo(nombre, cantMovimientosUtilizados):
    file = open("ranking.txt", "a")
    file.write(nombre)
    file.write('\n')
    file.write(str(cantMovimientosUtilizados))
    file.write('\n')
    file.close()

def escribirMovimientosEnArchivo():
    global cantidadDeMovimientosActual, nivelCompletado, nombreJugador

    if (nivelCompletado==True):
        escribirEnArchivo(nombreJugador, cantidadDeMovimientosActual)
        resetearJuego()

def estaSinMovimientos():

    global cantidadDeMovimientosRestantes
    if (nivelCompletado==False) and (cantidadDeMovimientosRestantes<=0):
        resetearJuego()



while not salirJuego:

    segundosTranscurridos=(pygame.time.get_ticks()-ticksAlComenzar)/1000
    segundosRestantes=tiempoParaSolucionarElNivel-round((pygame.time.get_ticks()-ticksAlComenzar)/1000)

    if (segundosRestantes<=0):
       resetearJuego()

    dibujarFondo()
    
    actualizarTiempoDeJuegoActual() 
    actualizarTiempoRestante()

    movArriba, movAbajo, movDerecha, movIzquierda = False, False, False, False
    

    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            salirJuego = True

        if event.type == pygame.MOUSEBUTTONDOWN:
           if miraRect.colliderect(virusQueSeMueveRect):
                virusQueSeMueveRect.left = cantPixelesPorLadoCasilla * cantidadDeCasillasPorLado
        if event.type == pygame.KEYDOWN:

            

            #estaSolucionado()
            #estaSinMovimientos()

            if event.key == pygame.K_r: 
                print(zonaDeTransporte)

            elif event.key == pygame.K_e:
                match personajeActual:
                    case "UAIBOT":          
                        imgAvatar=pygame.transform.scale(pygame.image.load("UAIBOTA.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
                        personajeActual="UAIBOTA"
                    case "UAIBOTA":
                        imgAvatar=pygame.transform.scale(pygame.image.load("UAIBOTINA.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
                        personajeActual="UAIBOTINA"
                    case "UAIBOTINA":
                        imgAvatar=pygame.transform.scale(pygame.image.load("UAIBOTINO.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
                        personajeActual="UAIBOTINO"
                    case "UAIBOTINO":
                        imgAvatar=pygame.transform.scale(pygame.image.load("UAIBOT.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
                        personajeActual="UAIBOT"

            personaje.mover(pared = paredGrupo, virus = virusGrupo, robot = personajeActual, lista = zonaDeTransporte)
                                 
              
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

    dibujarZonaDeTransporte(zonaDeTransporte)
    
    dt = reloj.tick() / 1000

    
    
    virusGrupo.update(personaje.rect)
    paredGrupo.update()

    pygame.display.update()

    if virusQueSeMueveRect.colliderect(avatarRect) or virusSinusoidalRect.colliderect(avatarRect):
        resetearJuego()
        
    if (virusQueSeMueveRect.left < cantPixelesPorLadoCasilla):
        virusQueSeMueveRect.left = cantPixelesPorLadoCasilla * cantidadDeCasillasPorLado
         
pygame.quit()