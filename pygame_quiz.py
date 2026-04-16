import pygame
import sys
import textwrap

pygame.init()

# ── 화면 설정 ──────────────────────────────────────────
W, H = 720, 560
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Python & pygame 퀴즈")
clock = pygame.time.Clock()

# ── 색상 ───────────────────────────────────────────────
BG        = (13,  15,  20)
CARD      = (22,  24,  31)
BORDER    = (42,  45,  58)
TEXT_PRI  = (232, 232, 240)
TEXT_SEC  = (156, 163, 175)
TEXT_DIM  = (75,  85,  99)
GREEN     = (37,  201, 161)
RED       = (247, 89,  89)
BLUE      = (79,  142, 247)
PURPLE    = (162, 89,  247)
AMBER     = (247, 168, 37)

CAT_COLOR = {
    "Python 기초":  BLUE,
    "pygame 기초":  PURPLE,
    "pygame.Rect":  AMBER,
    "게임 루프":    GREEN,
    "충돌 & 물리":  RED,
}

# ── 폰트 ───────────────────────────────────────────────
def load_font(size, bold=False):
    for name in ["malgunbd" if bold else "malgun gothic",
                 "applegothic", "nanumgothic", "nanum gothic",
                 "gulim", "dotum"]:
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except:
            pass
    return pygame.font.SysFont(None, size, bold=bold)

F_SM   = load_font(16)
F_MD   = load_font(18)
F_LG   = load_font(22, bold=True)
F_CODE = pygame.font.SysFont("consolas", 14) or pygame.font.SysFont("courier new", 14)

# ── 퀴즈 데이터 ────────────────────────────────────────
lessons = [
    {
        "category": "Python 기초",
        "title": "import 와 라이브러리",
        "explain": [
            "Python에서 외부 기능을 쓰려면 import로 불러와야 해.",
            "",
            "  import pygame     ← pygame 전체를 불러옴",
            "  import random     ← random 모듈을 불러옴",
            "",
            "pygame.init()처럼 점(.)으로 기능에 접근해.",
            "불러오지 않으면 NameError 오류가 나.",
        ],
        "q": "pygame을 올바르게 불러오는 코드는?",
        "options": ["pygame.load()", "import pygame", "include pygame", "from game import pygame"],
        "answer": 1,
        "wrong": [
            "pygame.load()는 존재하지 않아. 불러오기 전에 pygame을 쓸 수 없어.",
            None,
            "include는 C/C++ 문법이야. Python에선 import를 써야 해.",
            "pygame이라는 하위 모듈이 없어서 오류가 나.",
        ],
    },
    {
        "category": "Python 기초",
        "title": "// 정수 나눗셈",
        "explain": [
            "Python의 나눗셈 연산자는 두 가지야:",
            "",
            "  /   소수점 포함   예) 600 / 2  = 300.0",
            "  //  정수 나눗셈   예) 600 // 2 = 300",
            "",
            "좌표는 정수여야 해. 소수점 좌표를 넘기면",
            "렌더링이 이상해지거나 오류가 날 수 있어.",
            "그래서 HEIGHT // 2 처럼 // 를 써.",
        ],
        "q": "HEIGHT = 600 일 때, HEIGHT // 2 의 결과는?",
        "options": ["300.0", "300", "301", "0"],
        "answer": 1,
        "wrong": [
            "300.0은 / 연산자의 결과야. //는 정수만 반환해.",
            None,
            "// 는 내림이야. 600 // 2 = 정확히 300이야.",
            "나머지와 헷갈린 것 같아. 나머지는 % 연산자야.",
        ],
    },
    {
        "category": "Python 기초",
        "title": "random.choice()",
        "explain": [
            "random.choice(리스트)는 리스트에서 무작위로",
            "하나를 뽑아.",
            "",
            "  ball_dx = random.choice([-5, 5])",
            "",
            "→ -5 또는 5 중 하나가 선택돼.",
            "→ -5면 왼쪽, 5면 오른쪽으로 공이 출발해.",
            "게임마다 방향이 달라져서 재미있어!",
        ],
        "q": "random.choice([-5, 5]) 의 결과로 가능한 값은?",
        "options": ["-5만 나옴", "5만 나옴", "-5 또는 5 둘 중 하나", "-5~5 사이 정수"],
        "answer": 2,
        "wrong": [
            "choice()는 리스트에서 무작위로 골라. -5만 나오진 않아.",
            "choice()는 리스트에서 무작위로 골라. 5만 나오진 않아.",
            None,
            "범위에서 뽑으려면 random.randint(-5, 5)를 써야 해.",
        ],
    },
    {
        "category": "pygame 기초",
        "title": "pygame.init() 과 창 생성",
        "explain": [
            "pygame 사용 전 반드시 초기화가 필요해:",
            "",
            "  pygame.init()  ← 모든 모듈을 켜는 시작 버튼",
            "",
            "그 다음 창을 만들어:",
            "  screen = pygame.display.set_mode((800, 600))",
            "  pygame.display.set_caption('핑퐁')",
            "",
            "set_mode()는 창을 만들고 Surface를 반환해.",
        ],
        "q": "pygame.init() 을 하지 않고 실행하면?",
        "options": ["정상 동작함", "일부 기능이 오류 날 수 있음", "창이 작게 열림", "FPS가 낮아짐"],
        "answer": 1,
        "wrong": [
            "공식적으로 init() 없이 pygame 기능은 보장되지 않아.",
            None,
            "창 크기는 set_mode()의 인자로 결정해. init()과 무관해.",
            "FPS는 clock.tick()이 조절해. init()과 무관해.",
        ],
    },
    {
        "category": "pygame 기초",
        "title": "게임 루프와 clock.tick()",
        "explain": [
            "게임 루프는 게임이 실행되는 동안 계속 반복돼.",
            "",
            "  clock = pygame.time.Clock()",
            "  while running:",
            "      clock.tick(60)  ← 초당 최대 60번 실행",
            "",
            "tick(60)이 없으면 루프가 초당 수천 번 돌 수도",
            "있어. 공이 엄청 빨라져서 게임이 불가능해져.",
        ],
        "q": "clock.tick(60) 의 역할은?",
        "options": ["60초 동안 멈춤", "초당 최대 60프레임으로 제한", "60번 후 종료", "FPS를 60 고정 보장"],
        "answer": 1,
        "wrong": [
            "tick()은 멈추는 게 아니야. 루프 속도를 조절해.",
            None,
            "반복 횟수를 세지 않아. 매 프레임마다 속도를 조절해.",
            "'최대' 60FPS야. 컴퓨터가 느리면 더 낮을 수 있어.",
        ],
    },
    {
        "category": "pygame 기초",
        "title": "이벤트 처리",
        "explain": [
            "pygame은 이벤트를 큐에 쌓아둬.",
            "event.get()으로 꺼내서 처리해.",
            "",
            "  for event in pygame.event.get():",
            "      if event.type == pygame.QUIT:",
            "          running = False",
            "",
            "pygame.QUIT는 창의 X 버튼을 눌렀을 때 발생해.",
            "이게 없으면 X 버튼을 눌러도 안 꺼져!",
        ],
        "q": "pygame.QUIT 이벤트가 발생하는 시점은?",
        "options": ["ESC 키를 눌렀을 때", "창의 X 버튼을 눌렀을 때", "게임이 패배했을 때", "마우스 우클릭 시"],
        "answer": 1,
        "wrong": [
            "ESC 키는 pygame.K_ESCAPE로 감지해. QUIT와 달라.",
            None,
            "게임 패배는 pygame이 자동 감지 안 해. 직접 조건을 써야 해.",
            "마우스 우클릭은 pygame.MOUSEBUTTONDOWN 이벤트야.",
        ],
    },
    {
        "category": "pygame.Rect",
        "title": "pygame.Rect — 사각형 객체",
        "explain": [
            "Rect는 위치와 크기를 가진 사각형 객체야.",
            "",
            "  pygame.Rect(x, y, width, height)",
            "",
            "  player = pygame.Rect(30, 300, 12, 90)",
            "           x=30, y=300, 너비=12, 높이=90",
            "",
            "유용한 속성: .top .bottom .centery",
            "             .left .right .centerx",
        ],
        "q": "pygame.Rect(30, 300, 12, 90) 에서 인자 순서는?",
        "options": ["너비, 높이, x, y", "x, y, 너비, 높이", "y, x, 높이, 너비", "x, 너비, y, 높이"],
        "answer": 1,
        "wrong": [
            "Rect는 위치(x, y)를 먼저, 그 다음 크기(w, h)를 받아.",
            None,
            "y를 먼저 쓰면 위치가 뒤바뀌어. 항상 x, y 순서야.",
            "x와 y는 항상 붙어 있어야 해: x, y, width, height.",
        ],
    },
    {
        "category": "pygame.Rect",
        "title": "colliderect() — 충돌 감지",
        "explain": [
            "두 Rect가 겹치는지 확인하는 함수야.",
            "",
            "  if ball.colliderect(player):",
            "      # 공이 패들에 닿았다!",
            "",
            "겹치면 True, 안 겹치면 False를 반환해.",
            "",
            "방향 조건도 필요해:",
            "  if ball.colliderect(player) and ball_dx < 0:",
            "방향 조건 없으면 공이 패들을 뚫어버려.",
        ],
        "q": "ball.colliderect(player) 의 반환값은?",
        "options": ["겹친 면적 (숫자)", "True 또는 False", "겹친 좌표 (x, y)", "항상 None"],
        "answer": 1,
        "wrong": [
            "면적은 반환하지 않아. 겹치는지 여부만 알려줘.",
            None,
            "좌표는 반환하지 않아. 참/거짓만 반환해.",
            "None은 반환하지 않아. 항상 True나 False야.",
        ],
    },
    {
        "category": "게임 루프",
        "title": "게임 루프 구조",
        "explain": [
            "모든 게임의 기본 구조야:",
            "",
            "  while running:",
            "      # 1. 입력",
            "      for event in pygame.event.get(): ...",
            "      # 2. 업데이트",
            "      ball.x += ball_dx",
            "      # 3. 렌더링",
            "      screen.fill(BLACK)",
            "      pygame.display.flip()",
            "",
            "이 순서가 뒤바뀌면 반응이 느려지거나 잔상이 남아.",
        ],
        "q": "게임 루프의 올바른 순서는?",
        "options": ["렌더링→입력→업데이트", "업데이트→입력→렌더링", "입력→업데이트→렌더링", "입력→렌더링→업데이트"],
        "answer": 2,
        "wrong": [
            "렌더링 먼저 하면 이전 상태를 그려. 반응이 한 프레임 늦어.",
            "업데이트 먼저 하면 이전 입력으로 상태를 바꿔. 한 박자 늦어.",
            None,
            "업데이트 전에 렌더링하면 변경된 상태가 다음 프레임에야 보여.",
        ],
    },
    {
        "category": "게임 루프",
        "title": "fill() 과 display.flip()",
        "explain": [
            "렌더링 단계의 두 핵심 함수야:",
            "",
            "  screen.fill(BLACK)",
            "  → 전체 화면을 검은색으로 덮어.",
            "  → 이전 프레임 그림을 지우는 거야.",
            "  → 없으면 공 지나간 자리가 다 남아.",
            "",
            "  pygame.display.flip()",
            "  → 버퍼에 그린 내용을 화면에 표시.",
            "  → 더블 버퍼링으로 깜빡임을 방지해.",
        ],
        "q": "screen.fill(BLACK) 을 매 프레임마다 호출하는 이유는?",
        "options": ["배경 색상을 바꾸려고", "이전 프레임 그림을 지우려고", "FPS를 높이려고", "메모리를 절약하려고"],
        "answer": 1,
        "wrong": [
            "배경색 변경도 가능하지만, 주목적은 이전 그림을 지우는 거야.",
            None,
            "fill()은 FPS와 무관해. FPS 조절은 clock.tick()이 해.",
            "fill()은 메모리와 무관해. 화면 픽셀을 색으로 덮어씌울 뿐이야.",
        ],
    },
    {
        "category": "충돌 & 물리",
        "title": "공 반사 원리",
        "explain": [
            "공의 속도는 dx(수평)와 dy(수직)로 표현돼.",
            "",
            "  ball.x += ball_dx",
            "  ball.y += ball_dy",
            "",
            "벽에 닿으면 방향을 반전:",
            "  if ball.top <= 0 or ball.bottom >= HEIGHT:",
            "      ball_dy *= -1  ← 부호를 바꿔",
            "",
            "  4 → -4 (아래→위),  -4 → 4 (위→아래)",
        ],
        "q": "ball_dy = 5 일 때, ball_dy *= -1 을 하면?",
        "options": ["ball_dy = 5 (변화없음)", "ball_dy = -5", "ball_dy = 0", "ball_dy = 10"],
        "answer": 1,
        "wrong": [
            "*= -1 은 -1을 곱하는 거야. 5 × -1 = -5로 바뀌어.",
            None,
            "-1을 곱하면 0이 아니야. 부호만 바뀌고 크기는 유지돼.",
            "*= 2가 아니라 *= -1이야. 방향만 반전, 속도 크기는 그대로야.",
        ],
    },
    {
        "category": "충돌 & 물리",
        "title": "y좌표 방향",
        "explain": [
            "화면 좌표계는 수학과 반대야!",
            "",
            "  (0, 0) ← 왼쪽 위",
            "  x: 오른쪽으로 갈수록 증가",
            "  y: 아래로 갈수록 증가",
            "",
            "CPU AI 코드:",
            "  if cpu.centery < ball.centery:",
            "      cpu.y += 4  ← 아래로 이동",
            "",
            "centery가 작다 = 공보다 위에 있다 → 아래로 가야 해.",
        ],
        "q": "화면의 y좌표 방향은?",
        "options": ["위로 갈수록 증가", "아래로 갈수록 증가", "항상 0", "중앙이 0"],
        "answer": 1,
        "wrong": [
            "수학 좌표계와 반대야. 화면은 왼쪽 위가 (0,0)이야.",
            None,
            "y좌표는 위치에 따라 달라. 화면 높이(600)까지 변해.",
            "중앙이 0인 건 수학 좌표계야. pygame은 왼쪽 위가 (0,0)이야.",
        ],
    },
]

# ── 유틸: 텍스트 그리기 ────────────────────────────────
def draw_text(surface, text, font, color, x, y, max_width=None, align="left"):
    rendered = font.render(text, True, color)
    if align == "center":
        x = x - rendered.get_width() // 2
    elif align == "right":
        x = x - rendered.get_width()
    surface.blit(rendered, (x, y))
    return rendered.get_height()

def draw_multiline(surface, lines, font, color, x, y, line_h=22):
    cy = y
    for line in lines:
        font.render(line, True, color)
        surf = font.render(line, True, color)
        surface.blit(surf, (x, cy))
        cy += line_h
    return cy

def draw_rect_border(surface, rect, color, radius=8, width=1, fill=None):
    if fill:
        pygame.draw.rect(surface, fill, rect, border_radius=radius)
    pygame.draw.rect(surface, color, rect, width=width, border_radius=radius)

def alpha_rect(surface, color, rect, alpha, radius=8):
    s = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    r, g, b = color
    pygame.draw.rect(s, (r, g, b, alpha), (0, 0, rect[2], rect[3]), border_radius=radius)
    surface.blit(s, (rect[0], rect[1]))

def progress_bar(surface, x, y, w, h, pct, color):
    pygame.draw.rect(surface, (30, 33, 45), (x, y, w, h), border_radius=h)
    filled = int(w * pct)
    if filled > 0:
        pygame.draw.rect(surface, color, (x, y, filled, h), border_radius=h)

# ── 버튼 클래스 ────────────────────────────────────────
class Button:
    def __init__(self, rect, text, font, color):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.color = color
        self.hovered = False

    def draw(self, surface):
        c = tuple(min(255, v + 30) for v in self.color) if self.hovered else self.color
        pygame.draw.rect(surface, c, self.rect, border_radius=8)
        surf = self.font.render(self.text, True, (0, 0, 0))
        rx = self.rect.x + (self.rect.w - surf.get_width()) // 2
        ry = self.rect.y + (self.rect.h - surf.get_height()) // 2
        surface.blit(surf, (rx, ry))

    def update(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

# ── 게임 상태 ──────────────────────────────────────────
state = {
    "phase": "learn",   # learn | quiz | result
    "idx": 0,
    "selected": None,
    "score": 0,
    "wrongs": [],
    "scroll": 0,
}

def current():
    return lessons[state["idx"]]

def reset():
    state.update({"phase": "learn", "idx": 0, "selected": None,
                  "score": 0, "wrongs": [], "scroll": 0})

btn_next    = Button((40, H - 64, W - 80, 44), "문제 풀기 →", F_MD, BLUE)
btn_quiz    = Button((40, H - 64, W - 80, 44), "다음 →",      F_MD, GREEN)
btn_restart = Button((W//2 - 130, H - 72, 260, 44), "처음부터 다시", F_MD, BLUE)
btn_back    = Button((40, H - 64, W - 80, 44), "← 설명 다시 보기", F_SM, BORDER)

option_btns = []
for i in range(4):
    option_btns.append(Button((40, 260 + i * 58, W - 80, 48), "", F_SM, CARD))

# ── 그리기 함수 ────────────────────────────────────────
def draw_learn():
    lesson = current()
    color  = CAT_COLOR.get(lesson["category"], BLUE)
    total  = len(lessons)
    pct    = state["idx"] / total

    screen.fill(BG)

    # 진행 바
    draw_text(screen, f"LESSON {state['idx']+1} / {total}", F_SM, TEXT_DIM, 40, 20)
    badge = F_SM.render(lesson["category"], True, color)
    screen.blit(badge, (W - 40 - badge.get_width(), 20))
    progress_bar(screen, 40, 44, W - 80, 3, pct, color)

    # 카드 배경
    pygame.draw.rect(screen, CARD, (20, 58, W - 40, H - 130), border_radius=12)
    pygame.draw.rect(screen, BORDER, (20, 58, W - 40, H - 130), width=1, border_radius=12)

    # 제목
    t = F_LG.render(lesson["title"], True, TEXT_PRI)
    screen.blit(t, (40, 74))

    # 설명 (코드 스타일)
    y = 112
    for line in lesson["explain"]:
        is_code = line.startswith("  ")
        font = F_CODE if is_code else F_SM
        clr  = (180, 210, 255) if is_code else TEXT_SEC
        surf = font.render(line, True, clr)
        screen.blit(surf, (40, y))
        y += 21

    # 버튼
    btn_next.color = color
    btn_next.update(pygame.mouse.get_pos())
    btn_next.draw(screen)

def draw_quiz():
    lesson = current()
    color  = CAT_COLOR.get(lesson["category"], BLUE)
    total  = len(lessons)
    pct    = (state["idx"] + 0.5) / total
    sel    = state["selected"]

    screen.fill(BG)

    # 진행 바
    draw_text(screen, f"QUIZ {state['idx']+1} / {total}", F_SM, TEXT_DIM, 40, 20)
    badge = F_SM.render(lesson["category"], True, color)
    screen.blit(badge, (W - 40 - badge.get_width(), 20))
    progress_bar(screen, 40, 44, W - 80, 3, pct, color)

    # 문제 박스
    pygame.draw.rect(screen, CARD, (20, 56, W - 40, 68), border_radius=10)
    pygame.draw.rect(screen, BORDER, (20, 56, W - 40, 68), width=1, border_radius=10)

    # 문제 텍스트 (줄 바꿈 처리)
    q_text = lesson["q"]
    wrapped = textwrap.wrap(q_text, width=46)
    for wi, wline in enumerate(wrapped):
        surf = F_MD.render(wline, True, TEXT_PRI)
        screen.blit(surf, (36, 68 + wi * 24))

    # 보기 버튼들
    mouse = pygame.mouse.get_pos()
    for i, btn in enumerate(option_btns):
        opt = lesson["options"][i]
        is_ans = (i == lesson["answer"])
        is_sel = (i == sel)

        if sel is not None:
            if is_ans:
                bg = (37, 201, 161, 40)
                border_c = GREEN
                tc = GREEN
            elif is_sel:
                bg = (247, 89, 89, 40)
                border_c = RED
                tc = RED
            else:
                bg = None
                border_c = BORDER
                tc = TEXT_DIM
        else:
            bg = None
            border_c = BORDER
            tc = TEXT_SEC
            if btn.rect.collidepoint(mouse):
                border_c = color
                tc = TEXT_PRI

        # 배경
        if sel is not None and is_ans:
            alpha_rect(screen, GREEN, (btn.rect.x, btn.rect.y, btn.rect.w, btn.rect.h), 35)
        elif sel is not None and is_sel and not is_ans:
            alpha_rect(screen, RED, (btn.rect.x, btn.rect.y, btn.rect.w, btn.rect.h), 35)
        else:
            pygame.draw.rect(screen, CARD, btn.rect, border_radius=8)

        pygame.draw.rect(screen, border_c, btn.rect, width=1, border_radius=8)

        # 알파벳 원
        cx, cy = btn.rect.x + 22, btn.rect.centery
        pygame.draw.circle(screen, border_c, (cx, cy), 11, 1)
        lbl = F_SM.render(chr(65 + i), True, tc)
        screen.blit(lbl, (cx - lbl.get_width()//2, cy - lbl.get_height()//2))

        # 텍스트
        t = F_SM.render(opt, True, tc)
        screen.blit(t, (btn.rect.x + 42, btn.rect.centery - t.get_height()//2))

    # 피드백
    if sel is not None:
        is_correct = (sel == lesson["answer"])
        fy = 260 + 4 * 58 + 8
        fh = 70

        if is_correct:
            alpha_rect(screen, GREEN, (20, fy, W - 40, fh), 20, radius=8)
            pygame.draw.rect(screen, GREEN, (20, fy, W - 40, fh), width=1, border_radius=8)
            t = F_SM.render("✓ 정답! 완벽해.", True, GREEN)
            screen.blit(t, (36, fy + 12))
        else:
            alpha_rect(screen, RED, (20, fy, W - 40, fh), 20, radius=8)
            pygame.draw.rect(screen, RED, (20, fy, W - 40, fh), width=1, border_radius=8)
            t = F_SM.render("✗ 오답 — 이 보기를 고른 이유가 있겠지만:", True, RED)
            screen.blit(t, (36, fy + 8))
            reason = lesson["wrong"][sel]
            wrapped_r = textwrap.wrap(reason, width=52)
            for ri, rl in enumerate(wrapped_r):
                rt = F_SM.render(rl, True, TEXT_SEC)
                screen.blit(rt, (36, fy + 28 + ri * 19))
            ans_t = F_SM.render(f"✓ 정답: {lesson['options'][lesson['answer']]}", True, GREEN)
            screen.blit(ans_t, (36, fy + fh - 4))

        btn_quiz.color = color
        btn_quiz.update(mouse)
        btn_quiz.draw(screen)
    else:
        btn_back.update(mouse)
        btn_back.draw(screen)

def draw_result():
    total   = len(lessons)
    score   = state["score"]
    pct     = score / total
    color   = GREEN if pct >= 0.8 else AMBER if pct >= 0.6 else RED

    screen.fill(BG)

    # 타이틀
    emoji = "🏆" if pct >= 0.8 else "💪" if pct >= 0.6 else "📚"
    draw_text(screen, "RESULT", F_SM, TEXT_DIM, W//2, 30, align="center")

    score_surf = F_LG.render(f"{score} / {total}", True, color)
    screen.blit(score_surf, (W//2 - score_surf.get_width()//2, 56))

    pct_surf = F_MD.render(f"정답률  {int(pct*100)}%", True, TEXT_SEC)
    screen.blit(pct_surf, (W//2 - pct_surf.get_width()//2, 90))

    progress_bar(screen, 60, 118, W - 120, 8, pct, color)

    # 틀린 문제 목록
    wrongs = state["wrongs"]
    if wrongs:
        t = F_SM.render("틀린 문제 다시 보기", True, TEXT_DIM)
        screen.blit(t, (40, 142))
        y = 164
        for wi in wrongs:
            wl = lessons[wi]
            wc = CAT_COLOR.get(wl["category"], BLUE)
            pygame.draw.rect(screen, CARD, (20, y, W - 40, 64), border_radius=8)
            pygame.draw.rect(screen, BORDER, (20, W - 40, W - 40, 64), width=1, border_radius=8)
            cat_t = F_SM.render(f"{wl['category']} · {wl['title']}", True, wc)
            screen.blit(cat_t, (36, y + 8))
            q_t = F_SM.render(wl["q"][:52] + ("…" if len(wl["q"]) > 52 else ""), True, TEXT_SEC)
            screen.blit(q_t, (36, y + 27))
            ans_t = F_SM.render(f"✓ {wl['options'][wl['answer']]}", True, GREEN)
            screen.blit(ans_t, (36, y + 44))
            y += 72
            if y > H - 90:
                break

    btn_restart.update(pygame.mouse.get_pos())
    btn_restart.draw(screen)

# ── 메인 루프 ──────────────────────────────────────────
running = True
while running:
    clock.tick(60)
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            if state["phase"] == "learn":
                if btn_next.clicked(pos):
                    state["phase"] = "quiz"
                    state["selected"] = None

            elif state["phase"] == "quiz":
                if state["selected"] is None:
                    for i, btn in enumerate(option_btns):
                        if btn.rect.collidepoint(pos):
                            state["selected"] = i
                            if i == current()["answer"]:
                                state["score"] += 1
                            else:
                                state["wrongs"].append(state["idx"])
                    if btn_back.clicked(pos):
                        state["phase"] = "learn"
                else:
                    if btn_quiz.clicked(pos):
                        if state["idx"] + 1 >= len(lessons):
                            state["phase"] = "result"
                        else:
                            state["idx"] += 1
                            state["phase"] = "learn"
                            state["selected"] = None

            elif state["phase"] == "result":
                if btn_restart.clicked(pos):
                    reset()

    # 옵션 버튼 y 위치 업데이트
    for i, btn in enumerate(option_btns):
        btn.rect.y = 140 + i * 56

    if state["phase"] == "learn":
        draw_learn()
    elif state["phase"] == "quiz":
        draw_quiz()
    else:
        draw_result()

    pygame.display.flip()

pygame.quit()
sys.exit()
