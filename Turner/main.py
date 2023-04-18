from setting import *

class Button:  # 버튼 클래스 생성
    def __init__(self, img, x, y, width, height,
                 img_c, x_act, y_act, action=None):
        mouse = pygame.mouse.get_pos()  # 마우스 좌표
        click = pygame.mouse.get_pressed()  # 마우스 클릭
        if x + width > mouse[0] > x and y + height > mouse[1] > y:  # 커서 범위
            Display.blit(img_c, (x_act, y_act))  # img_act 호출
            if click[0] and action is not None:  # 클릭 했으면
                BtnClickSound.play()  # Click Sound 재생
                BtnClickSound.set_volume(volume)
                time.sleep(1)  # 1초동안 지연
                action()  # action 호출
        else:  # 커서가 범위 밖에 있으면
            Display.blit(img, (x, y))  # img_in 호출


class Box(pygame.sprite.Sprite):  # 박스 Sprite 클래스 생성
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        b_images = [BOX00, BOX01, B0X02, BOX03,
                    BOX04, BOX05, BOX06, BOX07, B0X08, BOX09]  # image list 저장
        self.size = 50, 50  # box size
        self.index = 0  # list index 설정
        self.images = [pygame.transform.scale(image, self.size)
                       for image in b_images]  # Rect-Image Scaling
        self.image = b_images[self.index]  # ani 인덱스

        self.ani_time = round(100 / len(self.images * 100), 2)  # 이미지 시간 계산
        self.cur_time = 0  # ani_time 계산 시간 초기화
        self.time = 0  # 다시 바뀌는 시간
        self.clicked = 0  # clicked 변수 생성

        self.position = [random.randrange(256, 896),
                         random.randrange(144, 500)]  # 생성시 random 위치
        self.rect = pygame.Rect(self.position, self.size)  # rect 생성

    def update(self, bat):  # update 변수
        global cnt_1, cnt_2, DL_box_chg
        mouse = pygame.mouse.get_pos()  # 마우스 좌표
        click = pygame.mouse.get_pressed()  # 마우스 클릭
        if self.position[0] + 50 > mouse[0] > self.position[0] \
                and self.position[1] + 50 > mouse[1] > self.position[1]:  # 커서 범위
            if click[0]:  # 클릭 했으면
                self.clicked = 1  # 클릭 변수 1
        if self.clicked == 1 and self.time < DL_box_chg:  # 다시 바뀌는 시간 조절
            self.time += 1  # 다시 바뀌는 시간 증가
            self.cur_time += bat  # loop 시간 더하기
            if self.cur_time >= self.ani_time:  # loop 시간이 ani_time 초과
                self.cur_time = 0  # cur_time 초기화
                self.image = self.images[self.index]  # New index
                self.index += 1  # index 증가
                if self.index == 1:  # index 가 1이면
                    BoxSound.play()  # Box Sound 재생
                    BoxSound.set_volume(volume)
                    self.boundary()  # boundary 함수 호출
                    self.rect = pygame.Rect(self.position, self.size)  # rect 재 생성
                    cnt_1 += 1  # 내 box count 증가
                    cnt_2 -= 1  # 적 box count 감소
                if self.index >= len(self.images):  # index 가 최대 증가 하면
                    self.index = 9  # index 를 9에 고정
        else:
            self.cur_time += bat  # loop 시간 더하기
            if self.cur_time >= self.ani_time:  # loop 시간이 ani_time 초과
                self.cur_time = 0  # cur_time 초기화
                self.image = self.images[self.index]  # New index
                self.index -= 1  # index 감소
                if self.index == 8:  # index 가 8이면
                    self.boundary()  # boundary 함수 호출
                    self.rect = pygame.Rect(self.position, self.size)  # rect 재 생성
                    cnt_1 -= 1  # 내 box count 감소
                    cnt_2 += 1  # 적 box count 증가
                if self.index <= 0:  # index 가 0까지 감소 하면
                    self.index = 0  # index 0에서 고정
            self.time = 0  # time 함수 초기화
            self.clicked = 0  # clicked 함수 초기화

    def boundary(self):  # box position 최대 범위
        self.position[0] += random.randint(-32, 32)  # 호출될 때마다 x 좌표 랜덤
        self.position[1] += random.randint(-27, 27)

        if self.position[0] < 128:  # 왼쪽 최대 범위
            self.position[0] = 128
        if self.position[1] < 144:  # 위 최대 범위
            self.position[1] = 144
        if self.position[0] > 1152:  # 오른쪽 최대 범위
            self.position[0] = 1152
        if self.position[1] > 576:  # 아래 최대 범위
            self.position[1] = 576


def difficulty():
    global time_p, time_c, cnt_1, Stage_Level, \
        DL_check_time, DL_win_cnt, DL_box_chg
    if 5 <= time_p != time_c and (time_p - time_c) % DL_check_time == 0 \
            and cnt_1 >= DL_win_cnt:  # Clear 조건
        time_c = time_p  # 조건 만족할때 시간을 저장
        ClearSound.play()
        ClearSound.set_volume(volume)
        Stage_Level += 1  # Stage 증가
        if Stage_Level < 5:
            DL_check_time, DL_win_cnt, DL_box_chg = 10, 7, 480  # 난이도 1
        elif 5 <= Stage_Level < 10:
            DL_check_time, DL_win_cnt, DL_box_chg = 15, 8, 420  # 난이도 2
        elif 10 <= Stage_Level < 15:
            DL_check_time, DL_win_cnt, DL_box_chg = 20, 8, 360  # 난이도 3
        elif 15 <= Stage_Level < 20:
            DL_check_time, DL_win_cnt, DL_box_chg = 25, 9, 300  # 난이도 4
        elif Stage_Level >= 20:
            DL_check_time, DL_win_cnt, DL_box_chg = 30, 9, 240  # 난이도 5
    elif 5 <= time_p != time_c and (time_p - time_c) % DL_check_time == 0 \
            and cnt_1 < DL_win_cnt:  # Game Over 조건
        Game_OverSound.play()
        Game_OverSound.set_volume(volume)
        time.sleep(2)
        over_game()


def main_menu():  # 로비 화면
    main_run = True
    reset_game()
    while main_run:  # 메인 루프
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 종료 이벤트
                pygame.quit()  # 게임 종료
        Display.blit(MAIN_BG, (0, 0))  # 배경 생성
        Display.blit(TITLE, ((WINx / 2) - 270, (WINy / 2) - 220))  # 타이틀 생성
        Button(PLAY_GAME_MM, ((WINx / 2) - 190), ((WINy / 2) - 70), 400, 70,  # PLAY GAME 버튼 생성
               PLAY_GAME_MM_CL, ((WINx / 2) - 190), ((WINy / 2) - 70), play_game)  # PLAY GAME 클릭
        Button(SETTING_MM, ((WINx / 2) - 190), ((WINy / 2) + 20), 400, 70,  # SETTING 버튼 생성
               SETTING_MM_CL, ((WINx / 2) - 190), ((WINy / 2) + 20), setting)  # SETTING 클릭
        Button(EXIT_MM, ((WINx / 2) - 190), ((WINy / 2) + 110), 400, 70,  # EXIT 버튼 생성
               EXIT_MM_CL, ((WINx / 2) - 190), ((WINy / 2) + 110), pygame.quit)  # EXIT 클릭

        pygame.display.flip()  # 화면 갱신
        clock.tick(FPS)  # FPS


def play_game():  # 플레이 화면
    global BGN, time_p, time_s, cnt_1, cnt_2, DL_Info_View
    playing = True
    pygame.time.set_timer(pygame.USEREVENT, 1000)  # 시간 이벤트 (밀리초)
    time_p += time_s  # 퍼즈 전 시간 반환
    box_g = pygame.sprite.Group()  # 적 sprite 그룹 생성
    countdown_game()  # 카운트 다운 호출

    for i in range(15):  # box 개수
        new_box = Box()  # box 객체 생성
        box_g.add(new_box)  # 객체를 box_g 그룹에 추가

    while playing:  # 메인 루프
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 종료 이벤트
                playing = False  # 게임 종료 (main_menu)
            if event.type == pygame.USEREVENT:  # 시간 이벤트
                time_p += 1  # 게임 타이머 1초 증가
            if event.type == pygame.KEYDOWN:  # 키가 눌러졌는지 확인
                if event.key == pygame.K_F1:
                    if DL_Info_View == 1:
                        DL_Info_View = 0
                    else:
                        DL_Info_View = 1

        time_s = 0  # 퍼즈 시간 초기화
        Display.blit(BGL[BGN], (0, 0))  # 배경 생성
        Button(MENU_L_BTN, (WINx - 270), 0, 270, 50,  # MENU 버튼 생성
               MENU_L_BTN_CL, (WINx - 270), 0, pause_game)  # MENU 클릭 (pause_game)
        Display.blit(PlayTime, (0, 0))  # 게임 타이머 UI
        Display.blit(m_font.render(str(int(time_p)), True, '#FFFF00'), (140, 7))  # 게임 타이머 TXT
        Display.blit(l_font.render('FPS', True, '#FFFFFF'), (245, 10))  # FPS 텍스트 생성
        Display.blit(l_font.render(str(int(clock.get_fps())), True, '#FFFFFF'), (245, 25))  # FPS 카운트 생성
        Display.blit(m_font.render('STAGE ' + str(Stage_Level).rjust(2, '0'),  # STAGE 텍스트 생성
                                   True, '#FFFFFF'), ((WINx - 245), 7))
        Display.blit(PlayUser, (0, WINy - 50))  # USER 정보 UI
        Display.blit(m_font.render(str(cnt_1), True, '#FFFFFF'), (150, WINy - 43))  # USER 박스 카운트 생성
        Display.blit(PlayEnemy, (WINx - 200, WINy - 50))  # ENEMY 정보 UI
        Display.blit(m_font.render(str(cnt_2), True, '#FFFFFF'),  # ENEMY 박스 카운트 생성
                     (WINx - 170, WINy - 43))

        if BGN == 2:
            info_col = '#FFFFFF'  # 배경 별 폰트 색상 WHITE
        elif BGN == 5:
            info_col = '#FFD700'  # 배경 별 폰트 색상 GOLD
        else:
            info_col = '#000000'  # 배경 별 폰트 색상 BLACK

        if DL_Info_View == 1:
            Display.blit(lb_font.render('BLUE CONDITION : ' + str(int(DL_win_cnt)).rjust(1)
                                        + 'unit', True, info_col), ((WINx - 395), 3))
            Display.blit(lb_font.render('CLEAR TIMER : ' + str(int(DL_check_time)).rjust(7)
                                        + 'sec', True, info_col), ((WINx - 395), 18))
            Display.blit(lb_font.render('RESET TERM : ' + str(int(DL_box_chg / 60)).rjust(8)
                                        + 'sec', True, info_col), ((WINx - 395), 33))
        box_g.update(box_sp)  # box_g 그룹 Sprite update
        box_g.draw(Display)  # box_g 그룹 Sprite draw

        difficulty()  # 난이도 함수 호출

        pygame.display.flip()  # 화면 갱신
        clock.tick(FPS)  # FPS


def setting():  # 설정 화면
    global BGN, volume, Stage_Level, DL_control
    while True:
        for event in pygame.event.get():  # 종료 이벤트
            if event.type == pygame.QUIT:  # 게임 종료
                pygame.quit()

        def bgn1():  # 게임 배경 변경 함수 1
            global BGN
            BGN = 1

        def bgn2():  # 게임 배경 변경 함수 2
            global BGN
            BGN = 2

        def bgn3():  # 게임 배경 변경 함수 3
            global BGN
            BGN = 3

        def bgn4():  # 게임 배경 변경 함수 4
            global BGN
            BGN = 4

        def bgn5():  # 게임 배경 변경 함수 5
            global BGN
            BGN = 5

        def all_mute():
            global volume
            volume = 0
            pygame.mixer.music.stop()

        def bgm_on():
            pygame.mixer.music.load("sound/PING PONG.mp3")
            pygame.mixer.music.set_volume(volume - 0.4)
            pygame.mixer.music.play(-1)

        def bgm_off():
            pygame.mixer.music.stop()

        def all_reset():
            global volume
            volume = 0.5
            pygame.mixer.music.load("sound/PING PONG.mp3")
            pygame.mixer.music.set_volume(volume - 0.4)
            pygame.mixer.music.play(-1)

        def vol_mute():
            global volume
            volume = 0

        def vol_reset():
            global volume
            volume = 0.5

        def vol_up():
            global volume
            if volume <= 1:
                volume += 0.1

        def vol_down():
            global volume
            if volume > 0.1:
                volume -= 0.1

        def dl_up():
            global DL_control, Stage_Level, DL_check_time, DL_win_cnt, DL_box_chg
            DL_control += 1
            if DL_control == 1:
                Stage_Level, DL_check_time, DL_win_cnt, DL_box_chg = 1, 10, 7, 480
            elif DL_control == 2:
                Stage_Level, DL_check_time, DL_win_cnt, DL_box_chg = 5, 15, 8, 420
            elif DL_control == 3:
                Stage_Level, DL_check_time, DL_win_cnt, DL_box_chg = 10, 20, 8, 360
            elif DL_control == 4:
                Stage_Level, DL_check_time, DL_win_cnt, DL_box_chg = 15, 25, 9, 300
            elif DL_control == 5:
                Stage_Level, DL_check_time, DL_win_cnt, DL_box_chg = 20, 30, 9, 240
            else:
                DL_control = 5

        def dl_down():
            global DL_control, Stage_Level, DL_check_time, DL_win_cnt, DL_box_chg
            DL_control -= 1
            if DL_control == 1:
                Stage_Level, DL_check_time, DL_win_cnt, DL_box_chg = 1, 10, 7, 480
            elif DL_control == 2:
                Stage_Level, DL_check_time, DL_win_cnt, DL_box_chg = 5, 15, 8, 420
            elif DL_control == 3:
                Stage_Level, DL_check_time, DL_win_cnt, DL_box_chg = 10, 20, 8, 360
            elif DL_control == 4:
                Stage_Level, DL_check_time, DL_win_cnt, DL_box_chg = 15, 25, 9, 300
            elif DL_control == 5:
                Stage_Level, DL_check_time, DL_win_cnt, DL_box_chg = 20, 30, 9, 240
            else:
                DL_control = 1

        Display.blit(MAIN_BG, (0, 0))  # 배경 생성
        Button(MENU_BTN, (WINx - 120), 0, 120, 50,  # MENU 버튼 생성
               MENU_BTN_CL, (WINx - 120), 0, main_menu)  # MENU 클릭 (main_menu)

        Display.blit(bb_font.render('SET BACKGROUND', True, '#000000'), (150, 100))
        Display.blit(mb_font.render('NOW [' + str(int(BGN)) + ']', True, '#000000'), (470, 120))
        Button(BG1_BTN, 150, 170, 120, 50,  # BG1 버튼 생성
               BG1_BTN_CL, 155, 170, bgn1)  # BG1 클릭
        Button(BG2_BTN, 300, 170, 120, 50,  # BG2 버튼 생성
               BG2_BTN_CL, 305, 170, bgn2)  # BG2 클릭
        Button(BG3_BTN, 450, 170, 120, 50,  # BG3 버튼 생성
               BG3_BTN_CL, 455, 170, bgn3)  # BG3 클릭
        Button(BG4_BTN, 600, 170, 120, 50,  # BG4 버튼 생성
               BG4_BTN_CL, 605, 170, bgn4)  # BG4 클릭
        Button(BG5_BTN, 750, 170, 120, 50,  # BG5 버튼 생성
               BG5_BTN_CL, 755, 170, bgn5)  # BG5 클릭

        volume_i = (volume * 10)
        Display.blit(bb_font.render('SET SOUND', True, '#000000'), (150, 270))
        Display.blit(mb_font.render('NOW SFX [' + str(int(volume_i)) + ']',
                                    True, '#000000'), (470, 290))
        Button(ALL_MUTE, 150, 340, 50, 50,  # ALL_MUTE 버튼 생성
               ALL_MUTE_CL, 155, 340, all_mute)  # ALL_MUTE 클릭
        Button(ALL_RESET, 250, 340, 50, 50,  # ALL_RESET 버튼 생성
               ALL_RESET_CL, 255, 340, all_reset)  # ALL_RESET 클릭
        Button(BGM_OFF, 150, 410, 50, 15,  # BGM_OFF 버튼 생성
               BGM_OFF_CL, 155, 410, bgm_off)  # BGM_OFF 클릭
        Button(BGM_ON, 250, 410, 50, 15,  # BGM_ON 버튼 생성
               BGM_ON_CL, 255, 410, bgm_on)  # BGM_ON 클릭
        Button(VOL_MUTE, 350, 340, 50, 50,  # VOL_MUTE 버튼 생성
               VOL_MUTE_CL, 355, 340, vol_mute)  # VOL_MUTE 클릭
        Button(VOL_RESET, 450, 340, 50, 50,  # VOL_RESET 버튼 생성
               VOL_RESET_CL, 455, 340, vol_reset)  # VOL_RESET 클릭
        Button(VOL_UP, 550, 340, 50, 50,  # VOL_UP 버튼 생성
               VOL_UP_CL, 555, 340, vol_up)  # VOL_UP 클릭
        Button(VOL_DOWN, 650, 340, 50, 50,  # VOL_DOWN 버튼 생성
               VOL_DOWN_CL, 655, 340, vol_down)  # VOL_DOWN 클릭

        Display.blit(bb_font.render('SET DIFFICULTY', True, '#000000'), (150, 440))
        Display.blit(mb_font.render('NOW [' + str(DL_control) + ']',
                                    True, '#000000'), (470, 460))
        Button(DL_DOWN, 150, 510, 50, 50,  # DL_DOWN 버튼 생성
               DL_DOWN_CL, 155, 510, dl_down)  # DL_DOWN 클릭
        Button(DL_UP, 250, 510, 50, 50,  # DL_UP 버튼 생성
               DL_UP_CL, 255, 510, dl_up)  # DL_UP 클릭

        Display.blit(mb_font.render('In Game Press [F1] :', True, '#000000'), (800, 290))
        Display.blit(mb_font.render('Show Difficulty INFO', True, '#000000'), (850, 330))

        Display.blit(mb_font.render('Develop by Smart Media', True, '#000000'), (800, 460))
        Display.blit(mb_font.render('201762024 LEE SEO JUN', True, '#000000'), (850, 500))

        pygame.display.flip()  # 화면 갱신
        clock.tick(FPS)  # FPS


def countdown_game():  # 게임 시작전 countdown
    global BGN, countdown, cnt_txt, first_in
    pygame.time.set_timer(pygame.USEREVENT, 1000)  # 시간 이벤트 (밀리초)
    CountDownSound.play()
    CountDownSound.set_volume(volume)
    while True:  # 메인 루프
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 종료 이벤트
                pygame.quit()  # 게임 종료
            if event.type == pygame.USEREVENT:  # 시간 이벤트
                countdown -= 1  # 1초 감소
                cnt_txt = str(countdown).rjust(3)
                if countdown == 0:
                    cnt_txt = 'PLAY'  # 카운트 출력 0초
                    pygame.time.delay(100)
                    CountDownSound.stop()
                elif countdown < 0:  # 'PLAY' 출력 후
                    break
        if countdown < 0:
            break
        Display.blit(BGL[BGN], (0, 0))  # 배경 생성
        Display.blit(a_font.render(cnt_txt, True, '#000000'),  # 카운트 다운 텍스트 생성
                     ((WINx / 2) - 100, (WINy / 2) - 100))

        pygame.display.flip()  # 화면 갱신
        clock.tick(FPS)  # FPS
    first_in = 0
    return


def reset_game():  # 게임 변수 초기화
    global time_p, time_s, cnt_1, cnt_2, countdown, cnt_txt
    global DL_Info_View, Stage_Level, DL_check_time, DL_win_cnt, DL_box_chg
    time_p, time_s = 0, 0  # Play time, Pause time 설정
    cnt_1, cnt_2 = 0, 15  # Box color count 설정
    DL_Info_View = 0  # 난이도 정보 표시 (0, 1)
    if first_in == 0:
        countdown, cnt_txt = 4, '3'.rjust(3)
    else:
        countdown, cnt_txt = 3, '3'.rjust(3)  # 3초 카운트 다운


def pause_game():  # 일시 정지 화면
    global time_s
    pause_run = True
    CountDownSound.stop()
    time_s = time_p  # 플레이 타임 저장
    back_p = 0

    def back():
        global back_p
        back_p = 1

    while pause_run:  # 메인 루프
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 종료 이벤트
                pygame.quit()  # 게임 종료
        c_display = Display.convert_alpha()  # 투명 처리 가능한 화면 생성
        c_display.fill((155, 155, 155, 5))  # RGB + 투명도 설정
        Display.blit(c_display, (0, 0))  # 배경 생성
        Display.blit(bb_font.render('Pause Game', True, '#000000'),  # Pause Game 생성
                     ((WINx / 2.35), (WINy / 2) - 150))
        Button(PLAY_BTN, ((WINx / 2) - 60), ((WINy / 2) - 60), 120, 50,  # PLAY 버튼 생성
               PLAY_BTN_CL, ((WINx / 2) - 60), ((WINy / 2) - 60), back)  # PLAY 클릭 (play_game)
        Button(MENU_BTN, ((WINx / 2) - 60), ((WINy / 2) + 30), 120, 50,  # MENU 버튼 생성
               MENU_BTN_CL, ((WINx / 2) - 60), ((WINy / 2) + 30), main_menu)  # MENU 클릭 (main_menu))

        if back_p == 1:
            return

        pygame.display.flip()  # 화면 갱신
        clock.tick(FPS)  # FPS


def over_game():  # 일시 정지 화면
    global time_p, time_s, cnt_1
    pause_run = True
    score = (time_p * Stage_Level) + cnt_1
    time_s = time_p  # 플레이 타임 저장
    while pause_run:  # 메인 루프
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 종료 이벤트
                pygame.quit()  # 게임 종료
        c_display = Display.convert_alpha()  # 투명 처리 가능한 화면 생성
        c_display.fill((155, 155, 155, 5))  # RGB + 투명도 설정
        Display.blit(c_display, (0, 0))  # 배경 생성
        Display.blit(bb_font.render('Game Over', True, '#000000'),  # Pause Game 생성
                     ((WINx / 2.35), (WINy / 2) - 150))
        Button(MENU_BTN, ((WINx / 2) - 60), ((WINy / 2) - 60), 120, 50,  # MENU 버튼 생성
               MENU_BTN_CL, ((WINx / 2) - 60), ((WINy / 2) - 60), main_menu)  # MENU 클릭
        Display.blit(b_font.render('STAGE : ' + str(Stage_Level).rjust(2, '0'),  # Stage 표시
                                   True, '#000000'), ((WINx / 2.75), (WINy / 2) + 30))
        Display.blit(b_font.render('SCORE : ' + str(score).ljust(9),  # Score 표시
                                   True, '#000000'), ((WINx / 2.75), (WINy / 2) + 80))
        pygame.display.flip()  # 화면 갱신
        clock.tick(FPS)  # FPS


main_menu()
