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

reloj = pygame.time.Clock()
movArriba, movAbajo, movDerecha, movIzquierda = False, False, False, False
jugando = False

spawnSinosuidal = 0
cantSinosuidalAsesinado = 0


posXjugador = 2
posYjugador = 5

legacy = False

# -----> Declaraciones de botones <-----#

#Instancia imagen (y reescalado) de boton inicio
button_surface = pygame.image.load("assets/img/classic/boton.png")
button_surface = pygame.transform.scale(button_surface, (150, 50))

button_surface_classic = pygame.image.load("assets/img/legacy/legacy-mode.png")
button_surface_classic = pygame.transform.scale(button_surface_classic, (150, 50))

button_surface_legacy = pygame.image.load("assets/img/classic/classic-mode.png")
button_surface_legacy = pygame.transform.scale(button_surface_legacy, (150, 50))

# -----> Declaraciones de sonidos <-----#
sonidoExplosion = pygame.mixer.Sound("assets/sounds/explosion.wav")
sonidoInicio = pygame.mixer.Sound("assets/sounds/startUp.wav")
sonidoCaptura = pygame.mixer.Sound("assets/sounds/success.wav")
sonidoBoton = pygame.mixer.Sound("assets/sounds/boton.wav")
sonidoMover = pygame.mixer.Sound("assets/sounds/movimiento.wav")
sonidoSalto = pygame.mixer.Sound("assets/sounds/salto.wav")
sonidoMuerte = pygame.mixer.Sound("assets/sounds/muerte.wav")
sonidoMovVirus = pygame.mixer.Sound("assets/sounds/moverVirus.wav")
sonidoActualizar = pygame.mixer.Sound("assets/sounds/Actualizar.wav")
sonidoElimVirus = pygame.mixer.Sound("assets/sounds/EliminarVirus.wav")
sonidoEscribir = pygame.mixer.Sound("assets/sounds/escribir.wav")

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
colorVerde,colorAzul,colorBlanco,colorNegro, colorNaranja, colorBordeaux= (11,102,35),(0,0,255),(255,255,255),(0,0,0),(239,27,126),(102,41,53)
cantidadDeCasillasPorLado=8 # Debe ser número par ya que la zona es un cuadrado
cantPixelesPorLadoCasilla=64
salirJuego = False
lstAreaProtegida=[]

imgAvatar=pygame.transform.scale(pygame.image.load("assets/img/classic/UAIBOT.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
avatarRect=imgAvatar.get_rect()   
imgMira=pygame.transform.scale(pygame.image.load("assets/img/classic/mira.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
imgPared=pygame.transform.scale(pygame.image.load("assets/img/classic/pared.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
imgParedAlternativa=pygame.transform.scale(pygame.image.load("assets/img/classic/paredAlternativa.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
imgParedAlternativa=pygame.transform.scale(pygame.image.load("assets/img/classic/paredAlternativa.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  

imgAreaProtegida=pygame.transform.scale(pygame.image.load("assets/img/classic/areaprotegida.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
listaVirus  = ["assets/img/classic/virus1.png","assets/img/classic/virus2.png","assets/img/classic/virus3.png","assets/img/classic/virus4.png","assets/img/classic/virus5.png","assets/img/classic/virus6.png"]
listaVirus2  = ["assets/img/legacy/virus1.png","assets/img/legacy/virus2.png","assets/img/legacy/virus3.png","assets/img/legacy/virus4.png","assets/img/legacy/virus5.png","assets/img/legacy/virus6.png"]
listaVirus3  = ["assets/img/classic/virus1.png","assets/img/classic/virus2.png","assets/img/classic/virus3.png","assets/img/classic/virus4.png","assets/img/classic/virus5.png","assets/img/classic/virus6.png"]
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
    fondo = pygame.image.load("assets/img/classic/fondo.png")
    pantalla.blit(fondo, (0, 0))

#region tablero
def crearZonaDeTransporte():

    # ceacion del "tablero", se hizo un array que a su vez contiene 9 arrays, (solo se usan 8, evitando el primero) los cuales, se inician llenandolos de espacios vacios, despues se cambian esos 0s por valores de palabras

    zonaDeTransporte = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 0, 0, 0, 0, 0, 0, 1],
                        [1, 1, 0, 0, 0, 0, 0, 0, 1],
                        [1, 1, 6, 0, 5, 0, 0, 0, 1],
                        [1, 1, 3, 0, 4, 1, 0, 0, 1],
                        [1, 1, 6, 0, 0, 4, 0, 0, 1],
                        [1, 1, 0, 0, 0, 0, 0, 0, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1]]
    
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
    
def dibujarContadorMov():
        
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
        global contMovUAIBOTA
        
        if lista[eval(str(self.y) + simbolo + '1')][self.x] in [0, 6]:

            contMovUAIBOTA += 1
            actualizarContadorDeMovimientos(1)

            if lista[eval(str(self.y) + opuesto + '1')][self.x] == 4:

                pygame.mixer.Sound.play(sonidoMovVirus)
                lista[eval(str(self.y) + opuesto + '1')][self.x] = 0
                lista[self.y][self.x] = 4
                
            else:
                
                pygame.mixer.Sound.play(sonidoMover)
                lista[self.y][self.x] = 0

            self.y = eval(str(self.y) + simbolo + '1')
        
    def ArrastrarHorizontal(self, simbolo, opuesto, lista):
        global contMovUAIBOTA
            
        if lista[self.y][eval(str(self.x) + simbolo + '1')] in [0, 6]:

            contMovUAIBOTA += 1
            actualizarContadorDeMovimientos(1)
            
            if lista[self.y][eval(str(self.x) + opuesto + '1')] == 4:

                pygame.mixer.Sound.play(sonidoMovVirus)
                lista[self.y][eval(str(self.x) + opuesto + '1')] = 0
                lista[self.y][self.x] = 4

            else:
                
                pygame.mixer.Sound.play(sonidoMover)
                lista[self.y][self.x] = 0

            self.x = eval(str(self.x) + simbolo + '1')

    #------------>Personaje: 2. Saltar Bloques<-------------#

    def SaltarVertical(self, simbolo, lista):
        global contMovUAIBOTINA

        if lista[eval(str(self.y) + simbolo + '1')][self.x] in [1, 4, 5] and lista[eval(str(self.y) + simbolo + '2')][self.x] in [0, 6]:
            
            contMovUAIBOTINA += 1
            pygame.mixer.Sound.play(sonidoSalto)
            actualizarContadorDeMovimientos(1)

            lista[self.y][self.x] = 0
            self.y = eval(str(self.y) + simbolo + '2')

        elif lista[eval(str(self.y) + simbolo + '1')][self.x] in [0, 6]:

            contMovUAIBOTINA += 1
            pygame.mixer.Sound.play(sonidoMover)
            actualizarContadorDeMovimientos(1)
            
            lista[self.y][self.x] = 0
            self.y = eval(str(self.y) + simbolo + '1')  
    
    def SaltarHorizontal(self, simbolo, lista):
        global contMovUAIBOTINA

        if lista[self.y][eval(str(self.x) + simbolo + '1')] in [1, 4, 5] and lista[self.y][eval(str(self.x) + simbolo + '2')] in [0, 6]:

            contMovUAIBOTINA += 1
            pygame.mixer.Sound.play(sonidoSalto)
            actualizarContadorDeMovimientos(1)

            lista[self.y][self.x] = 0
            self.x = eval(str(self.x) + simbolo + '2')

        elif lista[self.y][eval(str(self.x) + simbolo + '1')] in [0, 6]:

            contMovUAIBOTINA += 1
            pygame.mixer.Sound.play(sonidoMover)
            actualizarContadorDeMovimientos(1)
                
            lista[self.y][self.x] = 0
            self.x = eval(str(self.x) + simbolo + '1')   
                  
    def EmpujarVertical(self, simbolo, lista):
        global contMovUAIBOT

        if lista[eval(str(self.y) + simbolo + '1')][self.x] == 4 and lista[eval(str(self.y) + simbolo + '2')][self.x] in [0, 2]:

            contMovUAIBOT += 1
            pygame.mixer.Sound.play(sonidoMovVirus)
            actualizarContadorDeMovimientos(1)

            lista[self.y][self.x] = 0
            self.y = eval(str(self.y) + simbolo + '1')
            lista[eval(str(self.y) + simbolo + '1')][self.x] = 4
            
        elif lista[eval(str(self.y) + simbolo + '1')][self.x] in [0, 6]:

            contMovUAIBOT += 1
            pygame.mixer.Sound.play(sonidoMover)
            actualizarContadorDeMovimientos(1)
            
            lista[self.y][self.x] = 0
            self.y = eval(str(self.y) + simbolo + '1')
        
    def EmpujarHorizontal(self, simbolo, lista):
        global contMovUAIBOT

        if lista[self.y][eval(str(self.x) + simbolo + '1')] in [4, 5] and lista[self.y][eval(str(self.x) + simbolo + '2')] in [0, 6]:
            
            contMovUAIBOT += 1
            actualizarContadorDeMovimientos(1)
            pygame.mixer.Sound.play(sonidoMovVirus)

            lista[self.y][self.x] = 0
            lista[self.y][eval(str(self.x) + simbolo + '2')] = lista[self.y][eval(str(self.x) + simbolo + '1')] 
            self.x = eval(str(self.x) + simbolo + '1')
            
        elif lista[self.y][eval(str(self.x) + simbolo + '1')] in [0, 6]:

            contMovUAIBOT += 1
            pygame.mixer.Sound.play(sonidoMover)
            actualizarContadorDeMovimientos(1)

            lista[self.y][self.x] = 0
            self.x = eval(str(self.x) + simbolo + '1')

    def mover(self, pared, virus, robot, bool = [], lista = []):
        
        if pygame.key.get_pressed()[pygame.K_w]:
            
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
                        self.EmpujarHorizontal('+', lista)
                    case "UAIBOTA":
                        self.ArrastrarHorizontal('+', '-', lista)
                    case "UAIBOTINA":
                        self.SaltarHorizontal('+', lista)
                    case "UAIBOTINO":
                        self.SaltarHorizontal('+', lista)


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

        lista[4][2] = 6
        lista[6][2] = 6
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
    
#Quien carajo tuvo la idea de hacer este nombre tan largo?????????????????
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

###################################### Clases #######################################################
# Empiezo a programar la clase del virus sinosuidal
class Sinusoidal:

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
virusSinosuidal = Sinusoidal(random.choice(listaVirus)) 
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
                pygame.mixer.Sound.play(sonidoEscribir)
            self.mostrarTexto()
            
    def redefinir(self):
        self.text = ""
        self.mostrarTexto()

################################################ Fin clases #############################################
def resetearJuego():
    global zonaDeTransporte, cantidadDeMovimientosRestantes, cantidadDeMovimientosActual, ticksAlComenzar
    global contMovUAIBOT, contMovUAIBOTA, contMovUAIBOTINA
    global jugando

    jugando = False
    inputNombre.redefinir()
    inputMov.redefinir()

    botonInicio.presionado = False

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

    personaje.x = 2
    personaje.y = 5

    ticksAlComenzar=pygame.time.get_ticks()
    dibujarTodo()

def escribirEnArchivo(nombre, cantMovimientosUtilizados):
    file = open("ranking.txt", "a")
    file.write(str(inputNombre.text))
    file.write('\n')
    file.write(str(cantMovimientosUtilizados))
    file.write('\n')
    file.close()

def escribirMovimientosEnArchivo():
    global cantidadDeMovimientosActual, nivelCompletado, nombreJugador

    if (nivelCompletado==True):
        escribirEnArchivo(nombreJugador, cantidadDeMovimientosActual)
        resetearJuego()


def estaSolucionado():

    global nivelCompletado
    global zonaDeTransporte 

    cantVirusSobreAreasProtegidas=0

    nivelCompletado = True

    for y in zonaDeTransporte:
        if 6 in y:
            cantVirusSobreAreasProtegidas=cantVirusSobreAreasProtegidas+1       

    if cantVirusSobreAreasProtegidas > 0:
        nivelCompletado = False
    else:
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/paseNivel.wav"))

    dibujarCartelIndicadorRonda()
    dibujarReglas()
    escribirMovimientosEnArchivo()
    dibujarPorcentajeDeMovimientos()

def estaSinMovimientos():
    global cantidadDeMovimientosRestantes

    if (nivelCompletado==False) and (cantidadDeMovimientosRestantes<=0):
        resetearJuego()

######################## Declaraciones de objetos ##################################

virusSinosuidal = Sinusoidal(random.choice(listaVirus)) 
#Declaraciones botones
botonInicio = Button(button_surface, 790, 265, "Iniciar juego", False)
#Boton de cambio sprite
botonLegacy = Button(button_surface, 1060, 610, "Classic", False)
#Inputs para nombre y movimientos
inputNombre = Input(600, 120, 400, tipografia,colorNegro)
inputMov = Input(600, 200, 400, tipografia,colorNegro)
#Grupos que permiten cargar los inputs
grupo = pygame.sprite.Group(inputNombre)
grupo2 = pygame.sprite.Group(inputMov)
#Texto descriptivo de inputs
txtInputNombre = Textos()
txtInputMov = Textos()

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


######################################################################################

while not salirJuego:

    segundosTranscurridos=(pygame.time.get_ticks()-ticksAlComenzar)/1000
    segundosRestantes=tiempoParaSolucionarElNivel-round((pygame.time.get_ticks()-ticksAlComenzar)/1000)

    if (segundosRestantes<=0):
       resetearJuego()

    dibujarFondo()
    virusSinosuidal.establecerMov()

    posXmouse = pygame.mouse.get_pos()[0]
    posYmouse = pygame.mouse.get_pos()[1]


    movArriba, movAbajo, movDerecha, movIzquierda = False, False, False, False
    

    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            salirJuego = True

        if event.type == pygame.MOUSEBUTTONDOWN:
           if miraRect.colliderect(virusQueSeMueveRect):
                virusQueSeMueveRect.left = cantPixelesPorLadoCasilla * cantidadDeCasillasPorLado

    #=================================================================================#
    #                         Deteccion de acciones propias                           #

        #Deteccion de eventos de inputs
        if(jugando == False):
            grupo.update()
        if(inputNombre.text != "" and jugando == False):
            grupo2.update()

        #Evita la escritura el ambos inputs a la vez
        if event.type == pygame.MOUSEBUTTONDOWN and inputNombre.rect.collidepoint(event.pos) == False:
            inputNombre.activo = False
        if event.type == pygame.MOUSEBUTTONDOWN and inputMov.rect.collidepoint(event.pos) == False:
            inputMov.activo = False

        if(botonInicio.presionado == False):
            #Deteccion de boton Inicio
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(botonInicio.DetectarInput(pygame.mouse.get_pos())):
                    botonInicio.presionado = not(botonInicio.presionado)

                    pygame.mixer.Sound.play(sonidoBoton)

                    #Variables para trackear estado de juego
                    jugando = True

                    if(legacy == False):
                        listaVirus = listaVirus3
                        imgAreaProtegida=pygame.transform.scale(pygame.image.load("assets/img/classic/areaprotegida.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
                        imgAvatar=pygame.transform.scale(pygame.image.load("assets/img/classic/UAIBOTA.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
                        imgPared=pygame.transform.scale(pygame.image.load("assets/img/classic/pared.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla)) 
                         
                    if(legacy == True):
                        listaVirus = listaVirus2
                        imgAreaProtegida=pygame.transform.scale(pygame.image.load("assets/img/legacy/zonaSegura.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
                        imgAvatar=pygame.transform.scale(pygame.image.load("assets/img/legacy/robot2.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
                        imgPared=pygame.transform.scale(pygame.image.load("assets/img/legacy/Block1.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
                    personajeActual="UAIBOTA"

                    #Redefine sprites de virus al inicar juego
                    virusSinosuidal.sprite = random.choice(listaVirus)
                    imgVirus=pygame.transform.scale(pygame.image.load(str(random.choice(listaVirus))), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
                    imgVirusQueSeMueve=pygame.transform.scale(pygame.image.load(str(random.choice(listaVirus))), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))

        #Deteccion de boton Legacy
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(botonLegacy.DetectarInput(pygame.mouse.get_pos())):
                botonLegacy.presionado = not(botonLegacy.presionado)

                pygame.mixer.Sound.play(sonidoBoton)

                legacy = not(legacy) 

                if(legacy == False):
                    botonLegacy.CambiarContenido("Classic")
                    botonLegacy.imagen = button_surface_classic
                if(legacy == True):
                    botonLegacy.CambiarContenido("Legacy")
                    botonLegacy.imagen = button_surface_legacy
        
        #Deteccion de click sobre virus
        if event.type == pygame.MOUSEBUTTONDOWN:

            if posXmouse >= virusSinosuidal.marca.left and posXmouse <= virusSinosuidal.marca.right and posYmouse >= virusSinosuidal.marca.top and posYmouse <= virusSinosuidal.marca.bottom:
                virusSinosuidal.spawnBool = False
                virusSinosuidal.virusBool = True
                virusDestruido = True
                cantSinosuidalAsesinado += 1
            
            if posXmouse >= virusQueSeMueveRect.left and posXmouse <= virusQueSeMueveRect.right and posYmouse >= virusQueSeMueveRect.top and posYmouse <= virusQueSeMueveRect.bottom:
                virusQueSeMueveRect.left =cantPixelesPorLadoCasilla * cantidadDeCasillasPorLado
                virusQueSeMueveRect.top = cantPixelesPorLadoCasilla * (cantidadDeCasillasPorLado - 2)
                virusDestruido = True
                cantSinosuidalAsesinado += 1
    #=================================================================================#

        if event.type == pygame.KEYDOWN and jugando == True:

            if event.key == pygame.K_r: 
                resetearJuego()

            elif event.key == pygame.K_e:
                match personajeActual:
                    case "UAIBOT":          
                        if(legacy == False):
                            imgAvatar=pygame.transform.scale(pygame.image.load("assets/img/classic/UAIBOTA.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
                        if(legacy == True):
                            imgAvatar=pygame.transform.scale(pygame.image.load("assets/img/legacy/robot2.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
                        personajeActual="UAIBOTA"
                    case "UAIBOTA":
                        if(legacy == False):    
                            imgAvatar=pygame.transform.scale(pygame.image.load("assets/img/classic/UAIBOTINA.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla)) 
                        if(legacy == True):
                            imgAvatar=pygame.transform.scale(pygame.image.load("assets/img/legacy/robot3.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla)) 
                        personajeActual="UAIBOTINA"
                    case "UAIBOTINA":
                        if(legacy == False):
                            imgAvatar=pygame.transform.scale(pygame.image.load("assets/img/classic/UAIBOTINO.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
                        if(legacy == True):
                            imgAvatar=pygame.transform.scale(pygame.image.load("assets/img/legacy/robot4.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
                        personajeActual="UAIBOTINO"
                    case "UAIBOTINO":
                        if(legacy == False):
                            imgAvatar=pygame.transform.scale(pygame.image.load("assets/img/classic/UAIBOT.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
                        if(legacy == True):
                            imgAvatar=pygame.transform.scale(pygame.image.load("assets/img/legacy/robot1.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
                        personajeActual="UAIBOT"

            personaje.mover(pared = paredGrupo, virus = virusGrupo, robot = personajeActual, lista = zonaDeTransporte)
                                 
              
        virusQueSeMueveRect.left = virusQueSeMueveRect.left - 1
        
        x = pygame.time.get_ticks() / 40  % 400
        y = int(math.sin(x/25.0) * 50 + 160)

        virusSinusoidalRect.left=x+cantPixelesPorLadoCasilla
        virusSinusoidalRect.top=y

        estaSolucionado()
        estaSinMovimientos()
    #=================================================================================#
    #                                Codigo propio                                    #
                     
    if(jugando == True):
        pantalla.blit(imgVirusQueSeMueve, (virusQueSeMueveRect.left, virusQueSeMueveRect.top))   
        pantalla.blit(imgVirusSinusoidal, (virusSinusoidalRect.left, virusSinusoidalRect.top)) 
    
        actualizarTiempoDeJuegoActual() 
        actualizarTiempoRestante()

        dibujarContadorMov()
        dibujarZonaDeTransporte(zonaDeTransporte)
        dibujarPorcentajeDeMovimientos()
        dibujarRanking()
        
        virusSinosuidal.movVirus()    
        virusSinosuidal.dibujarVirus(spawnSinosuidal)

    #Dibuja boton "Iniciar Juego"
    if(botonInicio.presionado == False and inputNombre.text != "" and inputMov.text != ""):
        botonInicio.Actualizar()
        botonInicio.CambiarColorBoton(pygame.mouse.get_pos(),"black","black")

    #Dibuja Input Nombre
    if (jugando == False):
        txtInputNombre.mostrar("Nombre",800,100,colorNegro,"white")
        grupo.draw(pantalla)
    
    #Dibuja Input Movimientos
    if(inputNombre.text != "" and jugando == False):
        txtInputMov.mostrar("Movimientos",800,170,colorNegro,"white")
        grupo2.draw(pantalla)

    #Dibuja boton "legacy" 
    if(botonInicio.presionado == False):
        botonLegacy.Actualizar()
        if(legacy == False):
            botonLegacy.CambiarColorBoton(pygame.mouse.get_pos(),"blue","black")
        if(legacy == True):
            botonLegacy.CambiarColorBoton(pygame.mouse.get_pos(),"yellow","white")
            
    #                              Fin codigo propio                                  #
    #=================================================================================#

    miraRect.center=(pygame.mouse.get_pos())
    rectanguloDeZonaDeTransporte=pygame.Rect(cantPixelesPorLadoCasilla*2,cantPixelesPorLadoCasilla*2,cantPixelesPorLadoCasilla * (cantidadDeCasillasPorLado-2),cantPixelesPorLadoCasilla * (cantidadDeCasillasPorLado-2))
    
    if miraRect.colliderect(rectanguloDeZonaDeTransporte) and jugando == True:
        pantalla.blit(imgMira, (miraRect.left, miraRect.top))    
        
    #Reloj interno
    reloj.tick(60)
    dt = reloj.tick(60) / 1000
    
    virusGrupo.update(personaje.rect)
    paredGrupo.update()

    pygame.display.update()

    if virusQueSeMueveRect.colliderect(avatarRect) or virusSinusoidalRect.colliderect(avatarRect):
        resetearJuego()
        
    if (virusQueSeMueveRect.left < cantPixelesPorLadoCasilla):
        virusQueSeMueveRect.left = cantPixelesPorLadoCasilla * cantidadDeCasillasPorLado
         
pygame.quit()