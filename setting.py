import pygame
import time
import random

pygame.init()  # Pygame 초기화
pygame.mixer.init()  # Mixer 초기화
pygame.display.set_caption('TURNER')  # Caption Title 설정
clock = pygame.time.Clock()

# Default Setting
WINx, WINy, FPS = 1280, 720, 60  # Display Size, Fps 설정
box_sp = clock.tick(FPS) / 500  # Box sprite ani speed 설정
BGN, volume, DL_control = 1, 0.5, 1  # Setting : Background 설정, Volume 설정, Difficulty 설정
Stage_Level, DL_check_time, DL_win_cnt, DL_box_chg = 1, 10, 7, 540  # STAGE 1 기준 난이도
first_in = 1
time_c = 0

pygame.mixer.music.load("sound/PING PONG.mp3")
pygame.mixer.music.set_volume(volume - 0.4)
pygame.mixer.music.play(-1)
Display = pygame.display.set_mode((WINx, WINy))  # Display 설정
# Font
a_font = pygame.font.SysFont('Agency FB', 150)  # Font_1
ab_font = pygame.font.SysFont('Agency FB', 150, True)  # Font_Bold_1
b_font = pygame.font.SysFont('Agency FB', 50)  # Font_2
bb_font = pygame.font.SysFont('Agency FB', 50, True)  # Font_Bold_2
m_font = pygame.font.SysFont('Agency FB', 30)  # Font_3
mb_font = pygame.font.SysFont('Agency FB', 30, True)  # Font_Bold_3
s_font = pygame.font.SysFont('Agency FB', 20)  # Font_4
sb_font = pygame.font.SysFont('Agency FB', 20, True)  # Font_Bold_4
l_font = pygame.font.SysFont('Agency FB', 15)  # Font_5
lb_font = pygame.font.SysFont('Agency FB', 15, True)  # Font_Bold_5
# Box
BOX00 = pygame.image.load('images/box/box_0.png')  # RedBox 정지
BOX01 = pygame.image.load('images/box/box_1.png')  # RedBox 회전
B0X02 = pygame.image.load('images/box/box_2.png')  # RedBox 회전
BOX03 = pygame.image.load('images/box/box_3.png')  # RedBox 회전
BOX04 = pygame.image.load('images/box/box_4.png')  # RedBox 회전
BOX05 = pygame.image.load('images/box/box_5.png')  # BlueBox 회전
BOX06 = pygame.image.load('images/box/box_6.png')  # BlueBox 회전
BOX07 = pygame.image.load('images/box/box_7.png')  # BlueBox 회전
B0X08 = pygame.image.load('images/box/box_8.png')  # BlueBox 회전
BOX09 = pygame.image.load('images/box/box_9.png')  # BlueBox 정지
# Background
MAIN_BG = pygame.image.load("images/background/main_bg.png")  # Main 배경 이미지
BG_Sand = pygame.image.load("images/background/game_bg_1.png")  # Game Sand 배경 이미지
BG_Concrete = pygame.image.load("images/background/game_bg_2.png")  # Game Concrete 배경 이미지
BG_Paint = pygame.image.load("images/background/game_bg_3.png")  # Game Paint 배경 이미지
BG_Wood = pygame.image.load("images/background/game_bg_4.png")  # Game Wood 배경 이미지
BG_Stone = pygame.image.load("images/background/game_bg_5.png")  # Game Stone 배경 이미지
BGL = [BG_Sand, BG_Sand, BG_Concrete, BG_Paint, BG_Wood, BG_Stone]  # Game Background List
# Main Menu Button
TITLE = pygame.image.load("images/title.png")  # Title 이미지
PLAY_GAME_MM = pygame.image.load("images/btm_play1.png")  # Play Game 버튼 이미지
PLAY_GAME_MM_CL = pygame.image.load("images/btm_play2.png")  # Play Game 클릭 이미지
SETTING_MM = pygame.image.load("images/btm_set1.png")  # Setting 버튼 이미지
SETTING_MM_CL = pygame.image.load("images/btm_set2.png")  # Setting 클릭 이미지
EXIT_MM = pygame.image.load("images/btm_exit1.png")  # Exit 버튼 이미지
EXIT_MM_CL = pygame.image.load("images/btm_exit2.png")  # Exit 클릭 이미지
# Button
PLAY_BTN = pygame.image.load("images/btn/play_1.png")  # Play 버튼 이미지
PLAY_BTN_CL = pygame.image.load("images/btn/play_2.png")  # Play 클릭 이미지
BACK_BTN = pygame.image.load("images/btn/back_1.png")  # Back 버튼 이미지
BACK_BTN_CL = pygame.image.load("images/btn/back_2.png")  # Back 클릭 이미지
RESET_BTN = pygame.image.load("images/btn/reset_1.png")  # Reset 버튼 이미지
RESET_BTN_CL = pygame.image.load("images/btn/reset_2.png")  # Reset 클릭 이미지
MENU_BTN = pygame.image.load("images/btn/menu_1.png")  # Menu 버튼 이미지
MENU_BTN_CL = pygame.image.load("images/btn/menu_2.png")  # Menu 클릭 이미지
MENU_L_BTN = pygame.image.load("images/btn/menu_long_1.png")  # 긴 Menu 버튼 이미지
MENU_L_BTN_CL = pygame.image.load("images/btn/menu_long_2.png")  # 긴 Menu 클릭 이미지
# Setting Background Button
BG1_BTN = pygame.image.load("images/btn/bg_1_1.png")  # Sand 배경 설정 버튼 이미지
BG1_BTN_CL = pygame.image.load("images/btn/bg_1_2.png")  # Sand 배경 클릭 버튼 이미지
BG2_BTN = pygame.image.load("images/btn/bg_2_1.png")  # Concrete 배경 설정 버튼 이미지
BG2_BTN_CL = pygame.image.load("images/btn/bg_2_2.png")  # Concrete 배경 클릭 버튼 이미지
BG3_BTN = pygame.image.load("images/btn/bg_3_1.png")  # Paint 배경 설정 버튼 이미지
BG3_BTN_CL = pygame.image.load("images/btn/bg_3_2.png")  # Paint 배경 클릭 버튼 이미지
BG4_BTN = pygame.image.load("images/btn/bg_4_1.png")  # Wood 배경 설정 버튼 이미지
BG4_BTN_CL = pygame.image.load("images/btn/bg_4_2.png")  # Wood 배경 설정 클릭 이미지
BG5_BTN = pygame.image.load("images/btn/bg_5_1.png")  # Stone 배경 설정 버튼 이미지
BG5_BTN_CL = pygame.image.load("images/btn/bg_5_2.png")  # Stone 배경 설정 클릭 이미지
# Setting Sound Button
VOL_UP = pygame.image.load("images/btn/sfx_up_1.png")  # Volume Up 버튼 이미지
VOL_UP_CL = pygame.image.load("images/btn/sfx_up_2.png")  # Volume Up 클릭 이미지
VOL_DOWN = pygame.image.load("images/btn/sfx_down_1.png")  # Volume Down 버튼 이미지
VOL_DOWN_CL = pygame.image.load("images/btn/sfx_down_2.png")  # Volume Down 클릭 이미지
VOL_MUTE = pygame.image.load("images/btn/sfx_mute_1.png")  # Volume Mute 버튼 이미지
VOL_MUTE_CL = pygame.image.load("images/btn/sfx_mute_2.png")  # Volume Mute 클릭 이미지
VOL_RESET = pygame.image.load("images/btn/sfx_reset_1.png")  # Volume Reset 버튼 이미지
VOL_RESET_CL = pygame.image.load("images/btn/sfx_reset_2.png")  # Volume Reset 클릭 이미지
ALL_MUTE = pygame.image.load("images/btn/all_mute_1.png")  # All Mute 버튼 이미지
ALL_MUTE_CL = pygame.image.load("images/btn/all_mute_2.png")  # All Mute 클릭 이미지
ALL_RESET = pygame.image.load("images/btn/all_reset_1.png")  # All Reset 버튼 이미지
ALL_RESET_CL = pygame.image.load("images/btn/all_reset_2.png")  # All Reset 클릭 이미지
BGM_ON = pygame.image.load("images/btn/bgm_on_1.png")  # Bgm On 버튼 이미지
BGM_ON_CL = pygame.image.load("images/btn/bgm_on_2.png")  # Bgm On 클릭 이미지
BGM_OFF = pygame.image.load("images/btn/bgm_off_1.png")  # Bgm Off 버튼 이미지
BGM_OFF_CL = pygame.image.load("images/btn/bgm_off_2.png")  # Bgm Off 클릭 이미지
# Setting Difficulty Level Button
DL_UP = pygame.image.load("images/btn/dl_up_1.png")  # Difficulty Level Up 버튼 이미지
DL_UP_CL = pygame.image.load("images/btn/dl_up_2.png")  # Difficulty Level Up 클릭 이미지
DL_DOWN = pygame.image.load("images/btn/dl_down_1.png")  # Difficulty Level Down 버튼 이미지
DL_DOWN_CL = pygame.image.load("images/btn/dl_down_2.png")  # Difficulty Level Down 클릭 이미지
# UI
PlayTime = pygame.image.load("images/time.png")  # Time UI
PlayUser = pygame.image.load("images/user.png")  # User UI
PlayEnemy = pygame.image.load("images/enemy.png")  # Enemy UI
# Sound
BtnClickSound = pygame.mixer.Sound("sound/btn_click.mp3")  # Button Click Sound
CountDownSound = pygame.mixer.Sound("sound/countdown.mp3")  # CountDown Sound
ClearSound = pygame.mixer.Sound("sound/clear.mp3")  # Clear Sound
Game_OverSound = pygame.mixer.Sound("sound/game over.mp3")  # Game Over Sound
BoxSound = pygame.mixer.Sound("sound/box_suc.mp3")  # Box Reverse Sound
