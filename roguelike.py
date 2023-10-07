import time
import pygame
import random

pygame.init()
pantalla = pygame.display.set_mode((600, 600))

reloj = pygame.time.Clock()
dt = 0

indexHorizontal = 0
indexVertical = 1
mapa = 'cyan'
eliminarse = False

# Bool para el while
gameOver = False

# Clase del jugador
class jugador(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.surface = pygame.Surface((x, y))
        self.surface.fill('red')
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.x = x
        self.y = y

        self.rect = self.surface.get_rect()
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        self.rect.width = self.x
        self.rect.height = self.y 
        
        self.cambioSala = False

    def movVertical(self, signo, bool, block):

        # signo: Direccion a la que se va a mover (logica para reducir codigo)
        # bool: Condicion al llegar al limite del mapa. Pregunta si hay una sala al costado para moverse a ella o chocar contra la pared

        global indexVertical

        moverse = True

        for x in block:
            if x.rect.colliderect(self.rect.left, eval(str(self.rect.y) + signo + str(dt * 350)), self.rect.width, self.rect.height):
                moverse = False
        
        if moverse:
            self.rect.top = eval(str(self.rect.top) + signo + str(dt * 350))

        if self.rect.top <= 0:

            if signo == '-' and 'arriba' in bool:
                self.rect.bottom = pantalla.get_height()
                self.cambioSala = True
                indexVertical -= 1
            else:
                self.rect.top = 0

        if self.rect.bottom >= pantalla.get_height():

            if signo == '+' and 'abajo' in bool:
                self.rect.top = 0
                self.cambioSala = True
                indexVertical += 1
            else:
                self.rect.bottom = pantalla.get_height()

    # Movimiento del jugador, misma logica que en el juego de ofirca. Se usa un eval para tener la ecuacion: la posicion acutal, signo ingresado (que puede ser + o -), y los frames por segundo aumentados un poquito
    def movHorizontal(self, signo, bool, block):

        moverse = True

        for x in block:
            if x.rect.colliderect(eval(str(self.rect.x) + signo + str(dt * 350)), self.rect.top, self.rect.width, self.rect.height):
                moverse = False

        if moverse:
            self.rect.x = eval(str(self.rect.left) + signo + str(dt * 350))

        global indexHorizontal

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
                self.rect.left = 0

    def mover(self, bool, block):
        
        if pygame.key.get_pressed()[pygame.K_w]:
            self.movVertical('-', bool, block)

        if pygame.key.get_pressed()[pygame.K_s]:
            self.movVertical('+', bool, block)

        if pygame.key.get_pressed()[pygame.K_d]:
            self.movHorizontal('+', bool, block)

        if pygame.key.get_pressed()[pygame.K_a]:
            self.movHorizontal('-', bool, block)

    def dibujar(self):

        # dibujo del jugador, con el sprite (por ahora es un color), y la rect (es una tupla con el tamaño y la posicion)
        pygame.draw.rect(pantalla, 'red', self.rect)

    def update(self, bool, block):
        self.mover(bool, block)
        self.dibujar()
        
# Clase para los bloques (cuadrados blancos)
# Es una clase hija de 'pygame.sprite.Sprite'
class bloques(pygame.sprite.Sprite):

    def __init__(self, posX, posY):

        # Aca se heredan las propiedades
        pygame.sprite.Sprite.__init__(self) 
        self.posX = posX
        self.posY = posY
        self.surface = pygame.Surface((50, 50))
        self.surface.fill('white')
        self.rect = self.surface.get_rect()
        self.rect.width = 50
        self.rect.height = 50
        self.rect.topleft = (self.posX, self.posY)
    
    def update(self):
        pygame.draw.rect(pantalla, 'white', self.rect) 

# clase de mapa, para generar la estructura
class mapa:

    def __init__(self, totalSalas, totalCapas, salas = []):
        self.totalSalas = totalSalas # Cantidad de salas totales que se tienen que procesar (mayor cantidad a medida que se pasan niveles)
        self.totalCapas = totalCapas
        self.salas = salas
        
        self.cantCapas = 3 # Elige la cantidad de capas (Valor de Y en index de lista) Por ahora lo hago en un valor fijo
        self.salas = [[] for filas in range(totalSalas) for columnas in range(totalCapas)]

    def agregar(self, sala, indexY):
        self.salas[indexY].append(sala)

    def SeleccionarSala(self, indexY, indexX):
        return self.salas[indexY][indexX]

class habitacion:

    def __init__(self, colorFondo, posBloques = [], salaActual = False, salidas = []):

        self.colorFondo = colorFondo
        self.colorFondo = colorFondo
        self.posBloques = posBloques
        self.salaActual = salaActual
        self.salidas = salidas

    def get_Salidas(self):
        return self.salidas


class proyectil(pygame.sprite.Sprite):

    def __init__(self, posX, posY, direccion1, direccion2):
        pygame.sprite.Sprite.__init__(self)

        # variable para que sepa a donde ir (derecha o izquierda, arriba o abajo)
        self.direccion1 = direccion1
        self.direccion2 = direccion2

        # posicones iniciales (El centro del jugador)
        self.posX = posX
        self.posY = posY

        # Superficie y collider
        self.surface = pygame.Surface((10, 10))
        self.surface.fill('red')
        self.rect = self.surface.get_rect()
        self.rect.center = (self.posX, self.posY)

    def update(self):

        # Se mueve constantemente para la direccion que se le asigne
        if self.direccion1 == 'vertical':
            self.rect.move_ip(0, eval(self.direccion2 + str(5)))
        else:
            self.rect.move_ip(eval(self.direccion2 + str(5)), 0)

        # Si toca un borde, desaparece (mejor optimizacion)
        if self.rect.top <= 0 or self.rect.left <= 0 or self.rect.bottom >= pantalla.get_height() or self.rect.right >= pantalla.get_width():
            self.kill()

        pygame.draw.circle(pantalla, 'red', self.rect.center, 10)

# Definir las variables con las clases
personaje = jugador(pantalla.get_width() / 2, pantalla.get_height() / 2, 50, 50)

mapas = mapa(2, 2)


sala0 = habitacion('cyan',
                [bloques(0, 100),
                bloques(0, 200),
                bloques(0, 300),
                bloques(0, 400)],
                True,
                ['derecha', 'arriba'])

sala1 = habitacion('cyan',
                [bloques(250, 200),
                bloques(350, 200),
                bloques(250, 400),
                bloques(350, 400)],
                False,
                ['izquierda'])

# Nueva sala de prueba para probar los cambios de sala verticales
sala2 = habitacion('cyan',
                   [bloques(100, 100),
                    bloques(200, 100),
                    bloques(300, 100),
                    bloques(400, 100),
                    bloques(500, 100)],
                    False,
                    ['abajo'])

mapas.agregar(sala2, 0)
mapas.agregar(sala0, 1)
mapas.agregar(sala1, 1)

bloque = pygame.sprite.Group()
proyectiles = pygame.sprite.Group()

# - ################### INICIO Funciones Globales ################### - #

def limpiarGrupo(self, var):
    self.empty()
    for j in var:
        self.add(j)

# - ################### FIN Funciones Globales ################### - #

# 'Intentar' hacer que el mapa tenga varias 'capas'

x = mapas.SeleccionarSala(indexVertical, indexHorizontal)

limpiarGrupo(bloque, x.posBloques)

# While Maestro
while not gameOver:

    pantalla.fill('cyan')

    # For para capturar eventos
    for event in pygame.event.get():

        # Si uno de los eventos capturados es que se apreto la equis de la ventana, esta se cierre (Corta el while)
        if event.type == pygame.QUIT:
            gameOver = True

        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_UP]:
                proyectiles.add(proyectil(personaje.rect.left + 25, personaje.rect.top + 25, 'vertical', '-'))
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                proyectiles.add(proyectil(personaje.rect.left + 25, personaje.rect.top + 25, 'vertical', '+'))
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                proyectiles.add(proyectil(personaje.rect.left + 25, personaje.rect.top + 25, 'Horizontal', '+'))
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                proyectiles.add(proyectil(personaje.rect.left + 25, personaje.rect.top + 25, 'Horizontal', '-'))   

    bloque.update()
    eliminarse = False

    mapas.SeleccionarSala(indexVertical, indexHorizontal).posBloques = bloque.copy()

    personaje.update(x.get_Salidas(), bloque)    

    if personaje.cambioSala:
        x.salaActual = False
        x = mapas.SeleccionarSala(indexVertical, indexHorizontal)
        x.salaActual = True
        proyectiles.empty()
        personaje.cambioSala = False
        limpiarGrupo(bloque, x.posBloques)

    proyectiles.update()
    if pygame.sprite.groupcollide(bloque, proyectiles, True, True):
        eliminarse = True

    personaje.dibujar()

    dt = reloj.tick() / 100
    reloj.tick(60)

    pygame.display.flip()
        