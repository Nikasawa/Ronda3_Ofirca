#!/usr/bin/env python
#-*- coding: utf-8 -*-

import math
import pygame
import random

#Importacion de clases
from clases import sinosuidal
from clases import Textos
from clases import Input
from clases import sinosuidal

pygame.init()
pygame.font.init() 
pygame.mixer.music.load("assets/sounds/paseNivel.wav") 
pygame.display.set_caption("OFIRCA 2023 - Resolución de todas las rondas")
pantalla= pygame.display.set_mode((1152,648))
tipografia = pygame.font.SysFont('Arial', 18)
tipografiaGrande=pygame.font.SysFont('Arial', 24)

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

#region tablero
def crearZonaDeTransporte():

    # ceacion del "tablero", se hizo un array que a su vez contiene 9 arrays, (solo se usan 8, evitando el primero) los cuales, se inician llenandolos de espacios vacios, despues se cambian esos 0s por valores de palabras
    zonaDeTransporte = [[0 for x in range(cantidadDeCasillasPorLado+1)] for y in range(cantidadDeCasillasPorLado+1)] 
    
    zonaDeTransporte[1][1] = 'pared'
    zonaDeTransporte[2][1] = 'pared'

    zonaDeTransporte[1][8] = 'pared'
    zonaDeTransporte[2][8] = 'pared'
    zonaDeTransporte[3][8] = 'pared'
    zonaDeTransporte[4][8] = 'pared'
    zonaDeTransporte[5][8] = 'pared'
    zonaDeTransporte[6][8] = 'pared'
    zonaDeTransporte[7][8] = 'pared'
    zonaDeTransporte[8][8] = 'pared'

    zonaDeTransporte[1][2] = 'pared'
    zonaDeTransporte[1][3] = 'pared'
    zonaDeTransporte[1][5] = 'pared'
    zonaDeTransporte[1][6] = 'pared'
    zonaDeTransporte[1][7] = 'pared'
    
    zonaDeTransporte[8][2] = 'pared'
    zonaDeTransporte[8][3] = 'pared'
    zonaDeTransporte[8][4] = 'pared'
    zonaDeTransporte[8][5] = 'pared'
    zonaDeTransporte[8][6] = 'pared'
    zonaDeTransporte[8][7] = 'pared'

    zonaDeTransporte[2][5] = 'jugador'

    zonaDeTransporte[4][4] = 'assets/img/paredAlternativa'    
       
    zonaDeTransporte[4][5] = 'virus'    
    zonaDeTransporte[5][6] = 'virus'    
    zonaDeTransporte[5][5] = 'pared' 
    zonaDeTransporte[6][3] = 'pared'       

    lstAreaProtegida.append((2,4))
    lstAreaProtegida.append((2,6))
    
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

def dibujarZonaDeTransporte():

    global zonaDeTransporte
    global avatarRect
    
    # Los For arrancan a contar desde el 1 ya que despues se multiplican con los las coordenadas
    # Si arrancaran en 0, se dibujarian pegados a los bordes de la pantalla

    for i in range(1,cantidadDeCasillasPorLado+1):
        for j in range(1,cantidadDeCasillasPorLado+1):
            
            pygame.draw.rect(pantalla, colorVerde,[cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i,cantPixelesPorLadoCasilla,cantPixelesPorLadoCasilla])

            if (hayAreaProtegidaEn(j,i)==True):
                pantalla.blit(imgAreaProtegida, (cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i)) 
            if (zonaDeTransporte[j][i]=='jugador'):

                # El jugador se compone de dos partes:
                    # El sprite y la posicion en la que se dibuja
                    # El marco de la colision
                # Esto quiere decir que puede darse el error de que se dibuje en un lado y detecte que colisiona con algo de otra parte
                pantalla.blit(imgAvatar, (cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i))     
                avatarRect=pygame.Rect(cantPixelesPorLadoCasilla * (j),cantPixelesPorLadoCasilla * (i),cantPixelesPorLadoCasilla,cantPixelesPorLadoCasilla)
            if (zonaDeTransporte[j][i]=='pared'):          
               pantalla.blit(imgPared, (cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i))

            # Pared parecida a la que esta en la consigna. Supongo que se adelantaron (?
            if (zonaDeTransporte[j][i]=='assets/img/paredAlternativa'):
               pantalla.blit(imgParedAlternativa, (cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i))

            # Aca se dibuja el virus pero la colision se define en otro lado
            if (zonaDeTransporte[j][i]=='virus'):
               pantalla.blit(imgVirus, (cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i))


    pygame.draw.rect(pantalla, colorBlanco, [cantPixelesPorLadoCasilla,cantPixelesPorLadoCasilla,cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla,cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla],1)       
    pygame.display.update()

#endregion
    
def dibujarReglas():

    textoReglas = tipografia.render('Mueve a tu avatar con las flechas para que lleve los virus a las zonas protegidas.', False, colorBlanco)
    
    ancho=650
    alto=25
    x=64
    y=3
    pygame.draw.rect(pantalla,colorBordeaux,(x,y,ancho,alto))
    pantalla.blit(textoReglas,(x+5,y,ancho,alto))
    
    pygame.display.update()

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

    pygame.display.update()

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
    pygame.display.update()

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


    pygame.display.update()

def dibujarCartelIndicadorRonda():
    textoFelicitacion = tipografiaGrande.render('Ronda final', False, colorBlanco)
    ancho=160
    alto=50
    x=350+(cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla)
    y=5
    pygame.draw.rect(pantalla,colorBordeaux,(x,y,ancho,alto))
    pantalla.blit(textoFelicitacion,(x+5,y,ancho,alto))
    pygame.display.update()

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
       
    pygame.display.update()
    
def dibujarPorcentajeDeMovimientos():
    global cantidadDeMovimientosActual

    ancho=220
    alto=40
    x=850
    y=25

    if (cantidadDeMovimientosActual>0):
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



    pygame.display.update()




def dibujarTodo():
    dibujarFondo()
    dibujarZonaDeTransporte()
    dibujarCartelIndicadorRonda()
    dibujarReglas()
    dibujarRanking()
    
    pygame.display.update()

dibujarTodo()

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
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/paseNivel.wav"))
        
    else:
        nivelCompletado=False

    dibujarCartelIndicadorRonda()
    dibujarReglas()
    escribirMovimientosEnArchivo()
    dibujarPorcentajeDeMovimientos()
 
#region Movimientos jugador
# Ver como lo desechamos todo a la mierda.
def irALaDerechaConUAIBOT():
    global zonaDeTransporte
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if (zonaDeTransporte[j+1][i]==0):
                    posicionarElemento('jugador',j+1,i)
                    actualizarContadorDeMovimientos(1)
                    actualizarContadorMovUAIBOT()  
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break                
                if(zonaDeTransporte[j+1][i]=='virus') and not ((zonaDeTransporte[j+2][i]=='pared') or (zonaDeTransporte[j+2][i]=='virus') or (zonaDeTransporte[j+2][i]=='assets/img/paredAlternativa')):                  
                    posicionarElemento('virus',j+2,i)
                    posicionarElemento('jugador',j+1,i)
                    actualizarContadorDeMovimientos(1)
                    actualizarContadorMovUAIBOT()  
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break
                if(zonaDeTransporte[j+1][i]=='assets/img/paredAlternativa') and (zonaDeTransporte[j+2][i]==0):
                    posicionarElemento('jugador',j+1,i)
                    posicionarElemento('assets/img/paredAlternativa',j+2,i)
                    actualizarContadorDeMovimientos(1)
                    actualizarContadorMovUAIBOT()  
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break

def irArribaConUAIBOT():
    global zonaDeTransporte
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if (zonaDeTransporte[j][i-1]==0):
                    posicionarElemento('jugador',j,i-1)
                    actualizarContadorDeMovimientos(1)
                    actualizarContadorMovUAIBOT()                  
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break
                if(zonaDeTransporte[j][i-1]=='virus') and not ((zonaDeTransporte[j][i-2]=='pared') or (zonaDeTransporte[j][i-2]=='virus')  or (zonaDeTransporte[j][i-2]=='assets/img/paredAlternativa')):
                    posicionarElemento('virus',j,i-2)
                    posicionarElemento('jugador',j,i-1)
                    actualizarContadorDeMovimientos(1)   
                    actualizarContadorMovUAIBOT()                
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break

def irAbajoConUAIBOT():
    global zonaDeTransporte
    for j in range(1,cantidadDeCasillasPorLado):
        for i in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if (zonaDeTransporte[j][i+1]==0):
                    posicionarElemento('jugador',j,i+1)
                    actualizarContadorDeMovimientos(1)       
                    actualizarContadorMovUAIBOT()    
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break
                if(zonaDeTransporte[j][i+1]=='virus') and not ((zonaDeTransporte[j][i+2]=='pared') or (zonaDeTransporte[j][i+2]=='virus') or (zonaDeTransporte[j][i+2]=='assets/img/paredAlternativa')):
                    posicionarElemento('virus',j,i+2)
                    posicionarElemento('jugador',j,i+1)
                    actualizarContadorDeMovimientos(1)     
                    actualizarContadorMovUAIBOT()    
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break

def irALaIzquierdaConUAIBOT():
    global zonaDeTransporte
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if (zonaDeTransporte[j-1][i]==0):
                    posicionarElemento('jugador',j-1,i)              
                    actualizarContadorDeMovimientos(1)
                    actualizarContadorMovUAIBOT()  
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break
                if(zonaDeTransporte[j-1][i]=='virus') and not ((zonaDeTransporte[j-2][i]=='pared') or (zonaDeTransporte[j-2][i]=='virus') or (zonaDeTransporte[j-2][i]=='assets/img/paredAlternativa') ):
                    posicionarElemento('virus',j-2,i)
                    posicionarElemento('jugador',j-1,i)
                    actualizarContadorDeMovimientos(1)  
                    actualizarContadorMovUAIBOT()  
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break
                if(zonaDeTransporte[j-1][i]=='assets/img/paredAlternativa') and (zonaDeTransporte[j-2][i]==0):
                    posicionarElemento('jugador',j-1,i)
                    posicionarElemento('assets/img/paredAlternativa',j-2,i)
                    actualizarContadorDeMovimientos(1)
                    actualizarContadorMovUAIBOT()  
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break

def irALaDerechaConUAIBOTA():
    global zonaDeTransporte
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if(zonaDeTransporte[j-1][i]=='virus') and (zonaDeTransporte[j+1][i]==0):                                     
                    posicionarElemento('jugador',j+1,i)
                    posicionarElemento('virus',j,i)
                    actualizarContadorDeMovimientos(1) 
                    actualizarContadorMovUAIBOTA()
                    borrarElemento(j-1,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break
                elif (zonaDeTransporte[j+1][i]==0):
                    posicionarElemento('jugador',j+1,i)
                    actualizarContadorDeMovimientos(1)  
                    actualizarContadorMovUAIBOTA()        
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break

def irArribaConUAIBOTA():
    global zonaDeTransporte
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if(zonaDeTransporte[j][i+1]=='virus') and (zonaDeTransporte[j][i-1]==0):                                     
                    posicionarElemento('jugador',j,i-1)
                    posicionarElemento('virus',j,i)
                    actualizarContadorMovUAIBOTA()
                    borrarElemento(j,i+1)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break
                elif (zonaDeTransporte[j][i-1]==0):
                    posicionarElemento('jugador',j,i-1)
                    actualizarContadorDeMovimientos(1)
                    actualizarContadorMovUAIBOTA()
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break

def irAbajoConUAIBOTA():
    global zonaDeTransporte
    for j in range(1,cantidadDeCasillasPorLado):
        for i in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if(zonaDeTransporte[j][i-1]=='virus') and (zonaDeTransporte[j][i+1]==0):                                     
                    posicionarElemento('jugador',j,i+1)
                    posicionarElemento('virus',j,i)
                    actualizarContadorDeMovimientos(1)       
                    actualizarContadorMovUAIBOTA()     
                    borrarElemento(j,i-1)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break
                elif (zonaDeTransporte[j][i+1]==0):
                    posicionarElemento('jugador',j,i+1)
                    actualizarContadorDeMovimientos(1)    
                    actualizarContadorMovUAIBOTA()       
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break

def irALaIzquierdaConUAIBOTA():
    global zonaDeTransporte
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if(zonaDeTransporte[j+1][i]=='virus') and (zonaDeTransporte[j-1][i]==0):                                     
                    posicionarElemento('jugador',j-1,i)
                    posicionarElemento('virus',j,i)
                    actualizarContadorDeMovimientos(1)  
                    actualizarContadorMovUAIBOTA()
                    borrarElemento(j+1,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break
                elif (zonaDeTransporte[j-1][i]==0):
                    posicionarElemento('jugador',j-1,i)
                    actualizarContadorDeMovimientos(1)
                    actualizarContadorMovUAIBOTA()
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break

def irALaDerechaConUAIBOTIN():
    global zonaDeTransporte
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if (zonaDeTransporte[j+1][i]==0):
                    posicionarElemento('jugador',j+1,i)
                    actualizarContadorDeMovimientos(1)
                    actualizarContadorMovUAIBOTINA()   
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break
                elif j+2<(len(zonaDeTransporte[j])):
                    if(zonaDeTransporte[j+2][i]==0) and (zonaDeTransporte[j+1][i]=='virus'):
                        posicionarElemento('jugador',j+2,i)
                        actualizarContadorDeMovimientos(1)    
                        actualizarContadorMovUAIBOTINA()           
                        borrarElemento(j,i)
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                        break 

def irArribaConUAIBOTIN():
    global zonaDeTransporte
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if (zonaDeTransporte[j][i-1]==0):
                    posicionarElemento('jugador',j,i-1)
                    actualizarContadorDeMovimientos(1)
                    actualizarContadorMovUAIBOTINA()   
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break
                elif i-2<(len(zonaDeTransporte[i])):
                     if((zonaDeTransporte[j][i-2]==0) and (zonaDeTransporte[j][i-1]=='virus')):
                        posicionarElemento('jugador',j,i-2)
                        actualizarContadorDeMovimientos(1)      
                        actualizarContadorMovUAIBOTINA()   
                        borrarElemento(j,i)
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                        break 

def irAbajoConUAIBOTIN():
    global zonaDeTransporte
    for j in range(1,cantidadDeCasillasPorLado):
        for i in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):              
                if (zonaDeTransporte[j][i+1]==0):
                    posicionarElemento('jugador',j,i+1)
                    actualizarContadorDeMovimientos(1)     
                    actualizarContadorMovUAIBOTINA()    
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break
                elif i+2<(len(zonaDeTransporte[i])):
                    if((zonaDeTransporte[j][i+2]==0) and (zonaDeTransporte[j][i+1]=='virus')):
                        posicionarElemento('jugador',j,i+2)
                        actualizarContadorDeMovimientos(1)         
                        actualizarContadorMovUAIBOTINA()           
                        borrarElemento(j,i)
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                        break 

def irALaIzquierdaConUAIBOTIN():
    global zonaDeTransporte
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if (zonaDeTransporte[j-1][i]==0):
                    posicionarElemento('jugador',j-1,i)
                    actualizarContadorDeMovimientos(1)     
                    actualizarContadorMovUAIBOTINA()         
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                    break
                elif j-2<(len(zonaDeTransporte[j])):
                    if(zonaDeTransporte[j-2][i]==0 and zonaDeTransporte[j-1][i]=='virus'):
                        posicionarElemento('jugador',j-2,i)
                        actualizarContadorDeMovimientos(1)
                        actualizarContadorMovUAIBOTINA()   
                        borrarElemento(j,i)
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/sounds/mover.wav"))
                        break 
#endregion

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
    
    actualizarTiempoDeJuegoActual() 
    actualizarTiempoRestante()

    if (segundosRestantes<=0):
       resetearJuego()

    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            salirJuego = True
        if event.type == pygame.MOUSEBUTTONDOWN:
           if miraRect.colliderect(virusQueSeMueveRect):
                virusQueSeMueveRect.left = cantPixelesPorLadoCasilla * cantidadDeCasillasPorLado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                match personajeActual:
                    case "UAIBOT":    
                        irALaDerechaConUAIBOT()
                    case "UAIBOTA":
                         irALaDerechaConUAIBOTA()
                    case "UAIBOTINA":
                         irALaDerechaConUAIBOTIN()        
                    case "UAIBOTINO":
                         irALaDerechaConUAIBOTIN()                    
            elif event.key == pygame.K_LEFT:
                match personajeActual:
                    case "UAIBOT":    
                        irALaIzquierdaConUAIBOT()
                    case "UAIBOTA":
                         irALaIzquierdaConUAIBOTA()  
                    case "UAIBOTINA":
                         irALaIzquierdaConUAIBOTIN() 
                    case "UAIBOTINO":
                         irALaIzquierdaConUAIBOTIN()    
            elif event.key == pygame.K_UP:
                match personajeActual:
                    case "UAIBOT":    
                        irArribaConUAIBOT()
                    case "UAIBOTA":
                         irArribaConUAIBOTA() 
                    case "UAIBOTINA":
                         irArribaConUAIBOTIN() 
                    case "UAIBOTINO":
                         irArribaConUAIBOTIN() 
            elif event.key == pygame.K_DOWN:
                match personajeActual:
                    case "UAIBOT":    
                        irAbajoConUAIBOT()
                    case "UAIBOTA":
                         irAbajoConUAIBOTA() 
                    case "UAIBOTINA":
                         irAbajoConUAIBOTIN()  
                    case "UAIBOTINO":
                         irAbajoConUAIBOTIN()  
            elif event.key == pygame.K_r: 
                resetearJuego()
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
                                 
        dibujarZonaDeTransporte()       
        virusQueSeMueveRect.left = virusQueSeMueveRect.left - 1
        
        x = pygame.time.get_ticks() / 40  % 400
        y = int(math.sin(x/25.0) * 50 + 160)
        
        virusSinusoidalRect.left=x+cantPixelesPorLadoCasilla
        virusSinusoidalRect.top=y

        pantalla.blit(imgVirusQueSeMueve, (virusQueSeMueveRect.left, virusQueSeMueveRect.top))   
        pantalla.blit(imgVirusSinusoidal, (virusSinusoidalRect.left, virusSinusoidalRect.top))   

        miraRect.center=(pygame.mouse.get_pos())
        rectanguloDeZonaDeTransporte=pygame.Rect(cantPixelesPorLadoCasilla*2,cantPixelesPorLadoCasilla*2,cantPixelesPorLadoCasilla * (cantidadDeCasillasPorLado-2),cantPixelesPorLadoCasilla * (cantidadDeCasillasPorLado-2))
        
        if miraRect.colliderect(rectanguloDeZonaDeTransporte):
            pantalla.blit(imgMira, (miraRect.left, miraRect.top))    
                     
        estaSolucionado()
        estaSinMovimientos()
        pygame.display.flip      

    if virusQueSeMueveRect.colliderect(avatarRect) or virusSinusoidalRect.colliderect(avatarRect):
        resetearJuego()
        
    if (virusQueSeMueveRect.left < cantPixelesPorLadoCasilla):
        virusQueSeMueveRect.left = cantPixelesPorLadoCasilla * cantidadDeCasillasPorLado
         
pygame.quit()