import pygame
import random
import time

pygame.init()  # 기본 초기화
pygame.mixer.init()
pygame.display.set_caption('MAZE')  # 화면 title 설정

f_font = pygame.font.SysFont('Courier', 37, True)
s_font = pygame.font.SysFont('Courier', 30, True)
b_font = pygame.font.SysFont('Courier', 100, True)

win_x, win_y, fps = 1300, 950, 60

Screen = pygame.display.set_mode((win_x, win_y))
clock = pygame.time.Clock()

MAP_SIZE = 7
MAPSIZEX, MAPSIZEY = MAP_SIZE, MAP_SIZE
map = [[0 for i in range(50)] for j in range(50)]
start = 50
player_x, player_y = 1, 1
stage = 12
timer = 0
hint_start = 3 #힌트의 개수 위치
hint_end = 6 #힌트의 개수, 위치

way = 1
is_find = 0
is_clicked = 0
flag = 0
point = 50

MAIN_BG = pygame.image.load('img/bg.png')
MAIN_TL = pygame.image.load('img/title.png')
MAIN_TL_C = pygame.image.load('img/title_c.png')
PLAY_BG = pygame.image.load('img/play_bg.png')

PLAY = pygame.image.load('img/play.png')
PLAY_C = pygame.image.load('img/play_c.png')
EXIT = pygame.image.load('img/exit.png')
EXIT_C = pygame.image.load('img/exit_c.png')

EXIT2 = pygame.image.load('img/exit2.png')
EXIT2_C = pygame.image.load('img/exit2_c.png')

WALL = pygame.image.load('img/wall.png')
ROAD = pygame.image.load('img/road.png')
GOAL = pygame.image.load('img/goal.png')
HURDLE = pygame.image.load('img/hurdle.png')

HINT1 = pygame.image.load('img/hint_01.png')
HINT2 = pygame.image.load('img/hint_02.png')
HINT3 = pygame.image.load('img/hint_03.png')
HINT4 = pygame.image.load('img/hint_04.png')
HINT9 = pygame.image.load('img/hint_09.png')
HINT = [HINT1, HINT2, HINT3, HINT4]

CHA1 = pygame.image.load('img/cha01.png')
CHA2 = pygame.image.load('img/cha02.png')
CHA3 = pygame.image.load('img/cha03.png')
CHA4 = pygame.image.load('img/cha04.png')

MAIN_BGM = pygame.mixer.Sound("mp3/Follow Me.mp3")
CLICKS = pygame.mixer.Sound("mp3/click.mp3")
MOVES = pygame.mixer.Sound("mp3/move.mp3")
CLEAR = pygame.mixer.Sound("mp3/clear.mp3")
BREAK = pygame.mixer.Sound("mp3/break.mp3")

pygame.mixer.music.load("mp3/Follow Me.mp3")
pygame.mixer.music.play(-1)

class Button:  # 버튼 클래스 생성
    def __init__(self, img_in, x, y, width, height, img_act, x_act, y_act, action=None):
        mouse = pygame.mouse.get_pos()  # 마우스 좌표
        click = pygame.mouse.get_pressed()  # 마우스 클릭
        if x + width > mouse[0] > x and y + height > mouse[1] > y:  # 커서가 범위 안에 있으면
            Screen.blit(img_act, (x_act, y_act))  # img_act 호출
            if click[0] and action is not None:  # 클릭 했으면
                CLICKS.play()
                time.sleep(1)  # 1초동안 지연
                action()  # action 호출
        else:  # 커서가 범위 밖에 있으면
            Screen.blit(img_in, (x, y))  # img_in 호출

def main_menu():
    global player_x, player_y, stage, timer, hint_start, hint_end, way, is_find, is_clicked, flag
    player_x, player_y = 1, 1
    stage = 12
    timer = 0
    hint_start = 3 #힌트의 개수 위치
    hint_end = 6 #힌트의 개수, 위치
    way = 1
    is_find = 0
    is_clicked = 0
    flag = 0

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        Screen.blit(MAIN_BG, (0, 0))
        Button(MAIN_TL, ((win_x / 2) - 130), ((win_y / 2) - 230), 249, 90,
               MAIN_TL_C, ((win_x / 2) - 130), ((win_y / 2) - 225), game_main)
        Button(PLAY, ((win_x / 2) - 450), ((win_y / 2) - 20), 184, 200,
               PLAY_C, ((win_x / 2) - 445), ((win_y / 2) - 15), game_main)
        Button(EXIT, ((win_x / 2) + 300), ((win_y / 2) - 20), 194, 200,
               EXIT_C, ((win_x / 2) + 305), ((win_y / 2) - 15), quit)

        pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(0.1)
        # MAIN_BGM.play(-1)
        pygame.display.flip()  # 화면 갱신
        clock.tick(fps)  # FPS


def map_init():
    for i in range(MAPSIZEY):
        for j in range(MAPSIZEX):
            if map[i][j] == 3:
                map[i][j] = 0


def make_map():
    global MAPSIZEY, MAPSIZEX
    for i in range(MAPSIZEY):
        for j in range(MAPSIZEX):
            map[i][j] = 1
    x = 1
    y = 1
    map[y][x] = 0

    for i in range(100000):
        way = random.randint(1, 4)

        if way == 1:
            if x == 1:
                continue
            if map[y][x - 2] == 1:
                x -= 1
                map[y][x] = 0
                x -= 1
                map[y][x] = 0
            else:
                x -= 2
        if way == 2:
            if y == MAPSIZEY - 2:
                continue
            if map[y + 2][x] == 1:
                y += 1
                map[y][x] = 0
                y += 1
                map[y][x] = 0
            else:
                y += 2

        if way == 3:
            if x == MAPSIZEX - 2:
                continue
            if map[y][x + 2] == 1:
                x += 1
                map[y][x] = 0
                x += 1
                map[y][x] = 0
            else:
                x += 2
        if way == 4:
            if y == 1:
                continue
            if map[y - 2][x] == 1:
                y -= 1
                map[y][x] = 0
                y -= 1
                map[y][x] = 0
            else:
                y -= 2
    for i in range(MAPSIZEY):
        for j in range(MAPSIZEX):
            num = random.randint(1, 10)
            if num < 4 and map[i][j] == 0 and i != 1 and j != 1\
                    and i != MAPSIZEY-2 and j != MAPSIZEX-2:
                map[i][j] = 5


def draw_map():
    global player_y, player_x, MAPSIZEY, MAPSIZEX, way, point

    for i in range(MAPSIZEY):
        start_i = 50 + i
        for j in range(MAPSIZEX):
            start_j = 50 + j
            if i == 0:
                Screen.blit(WALL, (50 * j + point, 50 * i + point))
            if j == 0:
                Screen.blit(WALL, (50 * j + point, 50 * i + point))
            if i == MAPSIZEY - 1:
                Screen.blit(WALL, (50 * j + point, 50 * i + point))
            if j == MAPSIZEX - 1:
                Screen.blit(WALL, (50 * j + point, 50 * i + point))
            if map[i][j] == 3:
                Screen.blit(HINT[random.randint(0, 3)], (50 * j + point, 50 * i + point))
            if (map[i][j] == 5) and ((i == player_y - 1 and j == player_x) or (i == player_y + 1 and j == player_x) or (
                    i == player_y and j == player_x + 1) or (i == player_y and j == player_x - 1)):
                Screen.blit(HURDLE, (50 * j + point, 50 * i + point))
            if stage < 3:
                if map[i][j] == 1:
                    Screen.blit(WALL, (50 * j + point, 50 * i + point))
            if i == MAPSIZEY - 2 and j == MAPSIZEX - 2:
                Screen.blit(GOAL, (50 * j + point, 50 * i + point))

            if way == 1:  # 상
                if i == player_y and j == player_x:
                    Screen.blit(CHA1, (50 * player_x + point, 50 * player_y + point))
                    for k in range(1, 3):
                        if player_y - k > 0 and map[player_y - k][player_x - 1] == 1:
                            Screen.blit(WALL, (50 * (player_x - 1) + point, 50 * (player_y - k) + point))
                        elif player_y - k > 0 and map[player_y - k][player_x - 1] == 0:
                            Screen.blit(ROAD, (50 * (player_x - 1) + point, 50 * (player_y - k) + point))
                        if player_y - k > 0 and map[player_y - k][player_x + 1] == 1:
                            Screen.blit(WALL, (50 * (player_x + 1) + point, 50 * (player_y - k) + point))
                        elif player_y - k > 0 and map[player_y - k][player_x + 1] == 0:
                            Screen.blit(ROAD, (50 * (player_x + 1) + point, 50 * (player_y - k) + point))
                        if player_y - k > 0 and map[player_y - k][player_x] == 1:
                            Screen.blit(WALL, (50 * player_x + point, 50 * (player_y - k) + point))
                        elif player_y - k > 0 and map[player_y - k][player_x] == 0:
                            Screen.blit(ROAD, (50 * player_x + point, 50 * (player_y - k) + point))

            if way == 2:  # 하
                if i == player_y and j == player_x:
                    Screen.blit(CHA2, (50 * player_x + point, 50 * player_y + point))
                    for k in range(1, 3):
                        if player_y + k < MAPSIZEY and map[player_y + k][player_x - 1] == 1:
                            Screen.blit(WALL, (50 * (player_x - 1) + point, 50 * (player_y + k) + point))
                        elif player_y + k < MAPSIZEY and map[player_y + k][player_x - 1] == 0:
                            Screen.blit(ROAD, (50 * (player_x - 1) + point, 50 * (player_y + k) + point))
                        if player_y + k < MAPSIZEY and map[player_y + k][player_x + 1] == 1:
                            Screen.blit(WALL, (50 * (player_x + 1) + point, 50 * (player_y + k) + point))
                        elif player_y + k < MAPSIZEY and map[player_y + k][player_x + 1] == 0:
                            Screen.blit(ROAD, (50 * (player_x + 1) + point, 50 * (player_y + k) + point))
                        if player_y + k < MAPSIZEY and map[player_y + k][player_x] == 1:
                            Screen.blit(WALL, (50 * player_x + point, 50 * (player_y + k) + point))
                        elif player_y + k < MAPSIZEY and map[player_y + k][player_x] == 0:
                            Screen.blit(ROAD, (50 * player_x + point, 50 * (player_y + k) + point))
            if way == 3:  # 좌
                if i == player_y and j == player_x:
                    Screen.blit(CHA3, (50 * player_x + point, 50 * player_y + point))
                    for k in range(1, 3):
                        if player_x - k > 0 and map[player_y - 1][player_x - k] == 1:
                            Screen.blit(WALL, (50 * (player_x - k) + point, 50 * (player_y - 1) + point))
                        elif player_x - k > 0 and map[player_y - 1][player_x - k] == 0:
                            Screen.blit(ROAD, (50 * (player_x - k) + point, 50 * (player_y - 1) + point))
                        if player_x - k > 0 and map[player_y + 1][player_x - k] == 1:
                            Screen.blit(WALL, (50 * (player_x - k) + point, 50 * (player_y + 1) + point))
                        elif player_x - k > 0 and map[player_y + 1][player_x - k] == 0:
                            Screen.blit(ROAD, (50 * (player_x - k) + point, 50 * (player_y + 1) + point))
                        if player_x - k > 0 and map[player_y][player_x - k] == 1:
                            Screen.blit(WALL, (50 * (player_x - k) + point, 50 * player_y + point))
                        elif player_x - k > 0 and map[player_y][player_x - k] == 0:
                            Screen.blit(ROAD, (50 * (player_x - k) + point, 50 * player_y + point))

            if way == 4:  # 우
                if i == player_y and j == player_x:
                    Screen.blit(CHA4, (50 * player_x + point, 50 * player_y + point))
                    for k in range(1, 3):
                        if player_x + k < MAPSIZEX and map[player_y - 1][player_x + k] == 1:
                            Screen.blit(WALL, (50 * (player_x + k) + point, 50 * (player_y - 1) + point))
                        elif player_x + k < MAPSIZEX and map[player_y - 1][player_x + k] == 0:
                            Screen.blit(ROAD, (50 * (player_x + k) + point, 50 * (player_y - 1) + point))
                        if player_x + k < MAPSIZEX and map[player_y + 1][player_x + k] == 1:
                            Screen.blit(WALL, (50 * (player_x + k) + point, 50 * (player_y + 1) + point))
                        elif player_x + k < MAPSIZEX and map[player_y + 1][player_x + k] == 0:
                            Screen.blit(ROAD, (50 * (player_x + k) + point, 50 * (player_y + 1) + point))
                        if player_x + k < MAPSIZEX and map[player_y][player_x + k] == 1:
                            Screen.blit(WALL, (50 * (player_x + k) + point, 50 * player_y + point))
                        elif player_x + k < MAPSIZEX and map[player_y][player_x + k] == 0:
                            Screen.blit(ROAD, (50 * (player_x + k) + point, 50 * player_y + point))


def dfs(y, x):
    global is_find
    if y == MAPSIZEY - 2 and x == MAPSIZEX - 2 and map[y][x] == 0:
        is_find = 1
    elif map[y][x] == 0 or map[y][x] == 3 or map[y][x] == 5:
        map[y][x] = 1
        if is_find == 0:
            dfs(y + 1, x)
        if is_find == 0:
            dfs(y, x + 1)
        if is_find == 0:
            dfs(y, x - 1)
        if is_find == 0:
            dfs(y - 1, x)

        map[y][x] = 0
    if is_find == 1:
        map[y][x] = 3


def is_clear():
    global player_x, player_y, MAPSIZEX, MAPSIZEY, stage
    if player_x == MAPSIZEX - 2 and player_y == MAPSIZEY - 2:
        return True
    else:
        return False

def game_main():
    global player_x, player_y, is_find, is_clicked, timer, stage, MAPSIZEY, MAPSIZEX, way, flag, hint_end, hint_start
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    make_map()

    run = True
    while run:  # 메인 루프
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT and stage < 13:
                timer += 1
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:  # 키가 눌러졌는지 확인
                if player_x == 0:
                    player_x += 1
                if map[player_y][player_x - 1] != 1 and map[player_y][player_x - 1] != 5 \
                        and event.key == pygame.K_LEFT:  # 캐릭터를 왼쪽으로
                    way = 3
                    player_x -= 1  # -5만큼:
                    MOVES.play(0, 400)
                if player_x >= MAPSIZEX - 1:
                    player_x -= 1
                    MOVES.play(0, 400)
                if map[player_y][player_x + 1] != 1 and map[player_y][player_x + 1] != 5 \
                        and event.key == pygame.K_RIGHT:  # 캐릭터를 오른쪽으로
                    way = 4
                    player_x += 1
                    MOVES.play(0, 400)
                if player_y >= MAPSIZEY - 1:
                    player_y -= 1
                    MOVES.play(0, 400)
                if map[player_y - 1][player_x] != 1 and map[player_y - 1][player_x] != 5 \
                        and event.key == pygame.K_UP:  # 캐릭터를 위로
                    way = 1
                    player_y -= 1
                    MOVES.play(0, 400)
                if player_y == 0:
                    player_y += 1
                    MOVES.play(0, 400)
                if map[player_y + 1][player_x] != 1 and map[player_y + 1][player_x] != 5 \
                        and event.key == pygame.K_DOWN:  # 캐릭터를 아래로
                    way = 2
                    player_y += 1
                    MOVES.play(0, 400)
                if event.key == pygame.K_SPACE and hint_end > hint_start:
                    dfs(player_y, player_x)
                    is_find = 0
                    is_clicked = timer
                    hint_end -= 1
                    CLICKS.play()
                if event.key == pygame.K_a and map[player_y][player_x + 1] == 5:
                    map[player_y][player_x + 1] = 0
                    BREAK.play()
                if event.key == pygame.K_a and map[player_y][player_x - 1] == 5:
                    map[player_y][player_x - 1] = 0
                    BREAK.play()
                if event.key == pygame.K_a and map[player_y + 1][player_x] == 5:
                    map[player_y + 1][player_x] = 0
                    BREAK.play()
                if event.key == pygame.K_a and map[player_y - 1][player_x] == 5:
                    map[player_y - 1][player_x] = 0
                    BREAK.play()

            if is_clicked + 2 == timer:
                map_init()

        if is_clear() == True:
            CLEAR.play()
            stage += 1
            make_map()
            player_y = 1
            player_x = 1
            flag += 1
            if flag == 2:
                flag = 0
                MAPSIZEX += 2
                MAPSIZEY += 2
            make_map()
            Screen.fill("BLACK")
            draw_map()

        Screen.blit(PLAY_BG, (0, 0))
        Screen.blit(f_font.render('STAGE ' + str(stage).rjust(4), True, '#FFFFFF'), (win_x - 340, 100))
        Screen.blit(f_font.render('TIME  ' + str(int(timer)).rjust(4), True, '#FFFFFF'), (win_x - 340, 200))
        Screen.blit(f_font.render('HINT', True, '#FFFFFF'), (win_x - 340, 300))

        for i in range(hint_start, hint_end):
            Screen.blit(HINT9, (win_x - 50*i, 300))

        Screen.blit(s_font.render('↑ : UP', True, '#FFFFFF'), (win_x - 340, 485))
        Screen.blit(s_font.render('← : LEFT', True, '#FFFFFF'), (win_x - 340, 535))
        Screen.blit(s_font.render('→ : RIGHT', True, '#FFFFFF'), (win_x - 340, 585))
        Screen.blit(s_font.render('↓ : DOWN', True, '#FFFFFF'), (win_x - 340, 635))
        Screen.blit(s_font.render('SPACE: HINT', True, '#FFFFFF'), (win_x - 340, 685))
        Screen.blit(s_font.render('A: BREAK BOX', True, '#FFFFFF'), (win_x - 340, 735))
        Button(EXIT2, (win_x - 250), (win_y - 100), 150, 50, EXIT2_C, (win_x - 250), (win_y - 100), quit)
        draw_map()

        if stage == 13:
            score = timer * 3
            Screen.fill("BLACK")
            Screen.blit(b_font.render('GAME CLEAR!!!', True, '#FFFFFF'), (300, (win_y / 2) - 100))
            Screen.blit(b_font.render('Score:   ' + str(score), True, '#FFFFFF'), (300, (win_y / 2)))

        clock.tick(60)
        pygame.display.flip()

main_menu()
