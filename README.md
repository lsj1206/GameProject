# Turner

한국 전통놀이인 **딱지치기**를 Pygame 기반 미니게임으로 구현한 프로젝트입니다.

화면에 등장하는 딱지를 클릭해 뒤집고, 제한 시간 안에 목표 개수 이상을 달성하면 다음 스테이지로 진행합니다. 스테이지가 올라갈수록 목표 조건과 유지 시간이 달라지는 방식으로 난이도가 조정됩니다.

## Project Info

- Language: Python
- Library: Pygame
- Type: 2D Mini Game
- Development: lsj1206
- 2022.03 - 2022.05

## How to Run

```powershell
pip install pygame
python main.py
```

## Controls

- Mouse Click: 딱지 뒤집기
- F1: 게임 중 난이도 정보 표시/숨김
- Menu Button: 일시정지 메뉴

## Structure

```text
.
├── main.py
├── setting.py
├── images/
│   ├── background/
│   ├── box/
│   └── btn/
└── sound/
```

## Features

- 딱지 뒤집기 애니메이션
- 스테이지 기반 난이도 증가
- 배경, 사운드, 난이도 설정 화면
- 카운트다운, 일시정지, 게임오버 화면
