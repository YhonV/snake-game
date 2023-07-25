import pygame
import random

pygame.init()   #Inicializamos pygame, siempre debe ir

white = (255,255,255)
black = (0,0,0)      #Colores RGBA   
red = (255,0,0)      #pygame solo acepta RGBA
yellow = (255,255,102)
orange = (255, 165, 0)
color_light = (170,170,170)
color_dark = (100,100,100)

dis_width = 600     #Definimos la pantalla
dis_height = 400
dis=pygame.display.set_mode((dis_width,dis_height)) 
pygame.display.set_caption("Snake Game by Cactu")

background = pygame.image.load('snake/imagenes/grass.png')
background = pygame.transform.scale(background, (dis_width, dis_height))

#Creamos un objeto Clock para controlar la velocidad de FPS
clock = pygame.time.Clock()

#Definimos la velocidad de la serpiente y su tamaño inicial
snake_speed = 15
snake_block = 10
orange_body = True

#Definimos los mensajes
font_style = pygame.font.SysFont("bahnschrift",25)
score_font = pygame.font.SysFont("comicsansms",35)

def draw_buttons():
    pygame.draw.rect(dis, color_dark, [dis_width // 6, dis_height // 1.8, 200, 50])
    pygame.draw.rect(dis, color_dark, [dis_width // 6, dis_height // 1.8 + 70, 200, 50])

    font = pygame.font.SysFont("comicsansms", 35)
    text_surface = font.render("Jugar de nuevo", True, white)
    dis.blit(text_surface, (dis_width // 6, dis_height // 1.9 + 10))

    text_surface = font.render("Salir", True, white)
    dis.blit(text_surface, (dis_width // 6 + 70, dis_height // 1.8 + 80))

def boton_clickeado(mouse_x, mouse_y):
    if dis_width // 6 <= mouse_x <= dis_width // 6 + 200 and dis_height // 1.8 <= mouse_y <= dis_height // 1.8 + 50:
        return True, False
    elif dis_width // 6 <= mouse_x <= dis_width // 6 + 200 and dis_height // 1.8 + 70 <= mouse_y <= dis_height // 1.8 + 120:
        return False, True
    else:
        return False, False

def mostrar_botones():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                jugar_de_nuevo, salir_del_juego = boton_clickeado(mouse_x, mouse_y)
                if jugar_de_nuevo:
                    return True
                elif salir_del_juego:
                    pygame.quit()
                    quit()

        dis.blit(background, [0, 0])
        draw_buttons()
        pygame.display.update()
    
def your_score(score):
    value = score_font.render(f"Tu puntaje: {score}",True,yellow)
    dis.blit(value,[0,0])

def our_snake(snake_block, snake_list, orange_body):
    for i, x in enumerate(snake_list):
        color = orange if i % 2 == (0 if orange_body else 1) else black
        pygame.draw.rect(dis, color, [x[0], x[1], snake_block, snake_block])

def message(msg,color):
    mesg=font_style.render(msg,True,color)
    dis.blit(mesg,[dis_width/6,dis_height/3])

#Bucle del juego
def gameLoop():
    global orange_body
    while True:
        game_over = False
        game_close = False

        x1 = dis_width / 2
        y1 = dis_height / 2
        x1_change = 0
        y1_change = 0
        snake_List = []
        lenght_of_snake = 1
        foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

        while not game_over:
            while game_close:
                dis.blit(background, [0, 0])
                draw_buttons()
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        jugar_de_nuevo, salir_del_juego = boton_clickeado(mouse_x, mouse_y)
                        if jugar_de_nuevo:
                            game_over = False
                            game_close = False
                            x1 = dis_width / 2  # Reiniciar la posición de la serpiente
                            y1 = dis_height / 2
                            x1_change = 0  # Reiniciar la dirección de la serpiente
                            y1_change = 0
                            snake_List.clear()  # Limpiar la lista de la serpiente
                            lenght_of_snake = 1  # Reiniciar la longitud de la serpiente
                            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0  # Nueva posición de la comida
                            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                        elif salir_del_juego:
                            pygame.quit()
                            quit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = snake_block
                        x1_change = 0

            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                game_close = True

            x1 += x1_change
            y1 += y1_change
            dis.blit(background, [0, 0])

            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > lenght_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True

            pygame.draw.circle(dis, red, (int(foodx + snake_block / 2), int(foody + snake_block / 2)), int(snake_block / 2))
            our_snake(snake_block, snake_List, orange_body)
            your_score(lenght_of_snake - 1)

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                lenght_of_snake += 1
                orange_body = not orange_body

            clock.tick(snake_speed)

        if not mostrar_botones():
            break

gameLoop()