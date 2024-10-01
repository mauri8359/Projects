import tkinter
from tkinter import simpledialog
import turtle
import time
import random
import pygame


pygame.init()
pygame.mixer.init()


def exit():
    global program, player_score
    program = False

    # Actualizo archivo Ranking.txt con el nuevo contenido
    with open("Ranking.txt", "w", encoding="utf-8") as file:
        #print(file.readlines())
        # Num de lineas
        lineas = len(player_score["name"])
        for i in range(lineas):
            lista_cadenas = list(map(int, player_score["score"]))
            maxi = max(lista_cadenas)
            pos_max = lista_cadenas.index(maxi)
            max_name = player_score["name"].pop(pos_max)
            max_score = player_score["score"].pop(pos_max)
            file.write(f"{max_name} {max_score}\n")


def resetmarcador():
    global snake_body, contador, increase, sum_vel, player_score, lista_cadenas

    # Consigo el valor minimo y maximo de la lista, no la posición
    lista_cadenas = list(map(int, player_score["score"]))
    print(f"{lista_cadenas} lista_cadenas")
    for i in snake_body:
        i.hideturtle()
    snake_body = []

    if len(lista_cadenas) <= 4:
        player_score["name"].append(player_name)
        player_score["score"].append(contador)
    else:
        minimo = min(lista_cadenas)
        print(f"{minimo} valor minimo lista")
        pos_min = lista_cadenas.index(minimo)

        if int(minimo) <= contador:
            #Encuentro la posición del val_min y la sustituyo por la mía
            player_score["name"][int(pos_min)] = player_name
            player_score["score"][int(pos_min)] = contador
            print(player_score)
            # player_score["name"][last_name] = player_name
            # player_score["score"][last_score] = contador
    #print(f"{player_score} player_score luego de reset")

    contador = 0
    increase = 0
    sum_vel = 0
    comida.goto(0, 100)
    text.clear()
    texto()
    

def pos_comida():
    global comidas
    # Reducimos el numero a la mitad del cuadraro y lo multiplicamos para que sea múltiple del rango de movimiento del snake
    x = random.randint(-13, 13) * 20
    y = random.randint(-12, 9) * 20
    comida.goto(x, y)


def name():
    root = tkinter.Tk()
    root.withdraw()  
    player_name = simpledialog.askstring("Nombre Jugador", "Por favor, introduce tu nombre: ")
    while len(player_name) >= 11 or len(player_name) < 1:
        player_name = simpledialog.askstring("Nombre Jugador", "Introduce un nombre valido porfavor: ")
    return player_name


def texto():
    global contador, best_score, player_name
    text.write(f"Score: {contador}   Top score: {best_score}    Player: {player_name}",
            align="center", font=("Courier", 15, "normal"))
    

def up():
    cabeza.direction = "up"


def down():
    cabeza.direction = "down"


def left():
    cabeza.direction = "left"


def right():
    cabeza.direction = "right"


def mov():
    if cabeza.direction == "up":
        y = cabeza.ycor()
        cabeza.sety(y + 20)

    if cabeza.direction == "down":
        y = cabeza.ycor()
        cabeza.sety(y - 20)

    if cabeza.direction == "left":
        x = cabeza.xcor()
        cabeza.setx(x - 20)

    if cabeza.direction == "right":
        x = cabeza.xcor()
        cabeza.setx(x + 20)


# Extracción datos Ranking.txt
player_score = {"name": [], "score": []}

with open("Ranking.txt", "r+", encoding="utf-8") as file:
    data = file.readlines()
    if len(data) == 0:
        # Si archivo no tiene datos, no se añaden datos al diccionario
        pass
    else:
        # extraemos el texto de cada linea del archivo y lo añadimos al diccionario
        for line in data:
            #print(line)
            append = line.split()
            #print(append)
            player_score["name"].append(append[0].rstrip())
            player_score["score"].append(append[1].rstrip())


# Creo una lista con valores int() para tener el score dentro de una lista con valores int()
lista_cadenas = list(map(int, player_score["score"]))

# Selecciono el valor de best_score
if len(lista_cadenas) <= 4:
    best_score = 0
else:
    #print(f"LISTA CON LOS SCORES: {lista_cadenas}")
    maximo = max(lista_cadenas)
    #minimo = min(lista_cadenas)
    # print(f"ESTE ES EL VALOR MINIMO: {minimo}")
    # print(f"ESTE ES EL VALOR MINIMO: {maximo}")


    # Con esto consigo la posición del valor mas alto de la lista
    pos_max = lista_cadenas.index(maximo)
    #pos_min = lista_cadenas.index(minimo)

    best_score = int(lista_cadenas[lista_cadenas.index(maximo)])


program = True
# Contador puntos 
contador = 0
increase = 0
# Contador aumentar velocidad serpiente
sum_vel = 0

# Llamada funcion conseguir nombre
player_name = name()


# Definición de la ventana con sus caracteristicas
ventana = turtle.Screen()
ventana.title("Snake")
ventana.bgcolor("green")
# Midas ventana
ventana.setup(width=600, height=600)
# bloqueo aumento ventana
ventana.cv._rootwindow.resizable(False, False)
# Para mejorar las animaciones
ventana.tracer(0)


# Cabeza de la serpiente
cabeza = turtle.Turtle()
cabeza.speed(10)
# Cambiar forma figura
cabeza.shape("square")
# Para que no deje rastro de lo que va haciendo
cabeza.penup()
# Definir la posición inicial del punto
cabeza.goto(0, 0)
# Para que espera a la siguiente orden
cabeza.direction = "stop"


# Linea limitadora horizontal
linea = turtle.Turtle()
linea.speed(0)
linea.hideturtle()
linea.pensize(3)
linea.penup()
linea.goto(-300, 230)
linea.pendown()
linea.forward(ventana.window_width())


# Comida
comida = turtle.Turtle()
comida.speed(0)
comida.color("red")
comida.shape("square")
comida.penup()

pos_comida()


# Snake Body
snake_body = []


# Texto
text = turtle.Turtle()
text.speed(1)
text.color("white")
text.penup()
text.hideturtle()
text.goto(0, 255)
texto()


# Config Teclado
ventana.listen()
ventana.onkeypress(up, "w")
ventana.onkeypress(down, "s")
ventana.onkeypress(right, "d")
ventana.onkeypress(left, "a")
ventana.onkeypress(exit, "q")


while program:
    ventana.update()

    # Colisiones
    # Colision fuera límite
    if cabeza.xcor() > 260 or cabeza.xcor() < -260 or cabeza.ycor() > 200 or\
       cabeza.ycor() < -260:
        limit_sound = pygame.mixer.Sound("./sonido/boing-2-44164.wav")
        limit_sound.set_volume(0.4)
        limit_sound.play()
        pygame.time.wait(int(limit_sound.get_length() * 500))
        cabeza.goto(0, 0)
        cabeza.direction = "stop"
        # Ocultar todo el cuerpo del snake
        resetmarcador()


    # Colision con el cuerpo
    for segments in snake_body:
        if segments.distance(cabeza) < 20:
            cabeza.goto(0, 0)
            cabeza.direction = "stop"
            body_sound = pygame.mixer.Sound("./sonido/hit_cuerpo.wav")
            body_sound.set_volume(0.4)
            body_sound.play()
            pygame.time.wait(int(body_sound.get_length() * 500))
            resetmarcador()
            

    # Colision comida (por default 20px)
    if cabeza.distance(comida) < 20:   
        pos_comida()
        #print(player_score)
        # Añadir cuerpo a la serpiente
        new_snake_body = turtle.Turtle()
        new_snake_body.speed(10)
        new_snake_body.color("grey")
        new_snake_body.shape("square")
        new_snake_body.penup()
        snake_body.append(new_snake_body)

        # Aumentar puntos
        contador += 1
        if contador > best_score:
            best_score = contador
        sum_vel +=1
        

        # Sonido al comer
        if sum_vel < 5:
            eat_sound = pygame.mixer.Sound("./sonido/a.wav")
            eat_sound.set_volume(0.4)
            eat_sound.play()
        # https://desarrollaria.com/desarrollar-ia/sonido-y-voz/como-generar-sonido-con-python-y-crear-una-mini-aplicacion-interactiva
        else:
            increase += 0.01
            sum_vel = 0
            speedup_sound = pygame.mixer.Sound("./sonido/vol.wav")
            speedup_sound.set_volume(1)
            speedup_sound.play()

        # Actualizamos texto con los nuevos datos
        text.clear()
        texto()

    total_snake_body = len(snake_body)
    # Range de la lista, -1 para que empiece del valor añadido más reciente al más antiguo
    # 0 Para que vaya hasta el valor 0
    # -1 Para que cada vez se reste -1 al range (si tengo 4 valores hará: 4,3,2,1)
    for index in range(total_snake_body - 1, 0, - 1):
        # Con esto obtenemos la posición del snake_body de delante
        x = snake_body[index - 1].xcor()
        y = snake_body[index - 1].ycor()
        # Con este le decimos que siga el snake_body que tiene delante
        snake_body[index].goto(x, y)

    if total_snake_body > 0:
        x = cabeza.xcor()
        y = cabeza.ycor()
        snake_body[0].goto(x, y)
    
    mov()
    # Para que vaya más lento
    time.sleep(0.1 - increase)

# ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana)
pygame.mixer.quit()
pygame.quit()
ventana.bye()