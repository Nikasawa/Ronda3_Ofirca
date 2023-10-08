import pygame
import random
import math

#placeholders para evitar que el script tire error(se definen el .py principal)
tipografia = ""
pantalla = "" 
event = "" 
listaVirus = []
dt = ""

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
                    dibujarMenu()
            else:
                self.text += event.unicode
            self.mostrarTexto()
            
    def redefinir(self):
        self.text = ""
        self.mostrarTexto()