# made it by Samael

import pygame
import time
import random

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_W, SCREEN_H = 500, 400
wn = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Race for Math")

bg = pygame.image.load("assest/track.png")
carImg = pygame.image.load("assest/player.png")
questionImg = pygame.image.load("assest/question-mark.png")
hearthImg = pygame.image.load("assest/hearth.png")

questionImg = pygame.transform.scale(questionImg, (40, 40))
hearthImg = pygame.transform.scale(hearthImg, (20, 20))

west_b = 157
east_b = 359

MAX_LIFE = 3
life = MAX_LIFE


questions = [
    ("3x + 5 = 20 denklemini çöz.", "5"),
    ("f(x) = 2x^2 - 3x + 1, f(2) kaçtır?", "3"),
    ("f(x) = 2x^3 - 6x + 2, f(4) kaçtır?", "4"),
    ("sin30° + cos60° kaçtır?", "1"),
    ("√169+8^2?", "77"),
    ("(2^3 * 2^4) / 2^5 sonucu?", "4"),
    ("asgeri ücret ne kadar", "28.075,50"),
    ("√49 + √36 kaçtır?", "13"),
    ("x - 5 < 10 x=?", "15"),
    ("babanla ananın yaşının toplamı", f"{random.randint(50,90),}")

]
question_index = 0

class Block:
    def __init__(self, y):
        self.y = y
        self.height = 25
        self.speedy = 4
        self.gap_width = 80
        self.gap_x = 0
        self.reset()

    def reset(self):
        self.y = -self.height
        self.gap_x = random.randint(west_b + 10, east_b - self.gap_width - 10)

    def update(self):
        self.y += self.speedy
        if self.y > SCREEN_H:
            self.reset()

    def draw(self):
        pygame.draw.rect(wn, (255, 0, 0), (west_b, self.y, self.gap_x - west_b, self.height))
        right_x = self.gap_x + self.gap_width
        pygame.draw.rect(wn, (255, 0, 0), (right_x, self.y, east_b - right_x, self.height))
        q_x = self.gap_x + self.gap_width // 2 - 20
        wn.blit(questionImg, (q_x, self.y - 40))

    def get_rects(self):
        left = pygame.Rect(west_b, self.y, self.gap_x - west_b, self.height)
        right_x = self.gap_x + self.gap_width
        right = pygame.Rect(right_x, self.y, east_b - right_x, self.height)
        q_rect = pygame.Rect(self.gap_x + self.gap_width//2 - 20, self.y - 40, 40, 40)
        return left, right, q_rect

class Heart:
    def __init__(self):
        self.image = hearthImg
        self.rect = self.image.get_rect()
        self.speedy = 3
        self.reset()

    def reset(self):
        self.rect.x = random.randint(west_b + 10, east_b - 30)
        self.rect.y = random.randint(-400, -50)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_H:
            self.reset()

    def draw(self):
        wn.blit(self.image, self.rect)

class Player:
    def __init__(self):
        self.image = carImg
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_W // 2, SCREEN_H - 80)
        self.speedx = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -5
        elif keys[pygame.K_RIGHT]:
            self.speedx = 5
        else:
            self.speedx = 0
        self.rect.x += self.speedx
        if self.rect.left < west_b:
            self.rect.left = west_b
        if self.rect.right > east_b:
            self.rect.right = east_b

def draw_text(text, size, x, y):
    font = pygame.font.Font(None, size)
    render = font.render(text, True, (0, 0, 0))
    rect = render.get_rect(center=(x, y))
    wn.blit(render, rect)

def start_screen():
    while True:
        wn.fill((200, 200, 200))
        draw_text("RACE FOR MATH", 50, SCREEN_W//2, 120)
        draw_text("ENTER bas başla", 30, SCREEN_W//2, 200)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def game_over_screen():
    while True:
        wn.fill((255, 150, 150))
        draw_text("OYUN BİTTİ", 60, SCREEN_W//2, 150)
        draw_text("ENTER bas ve bidaha oyna", 30, SCREEN_W//2, 220)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def win_screen():
    while True:
        wn.fill((150, 255, 150))
        draw_text("SEN KAZANDIN!", 60, SCREEN_W//2, 150)
        draw_text("ENTER bas ve bidaha oyna", 30, SCREEN_W//2, 220)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def question_screen():
    global question_index, life
    question, answer = questions[question_index]
    user_text = ""
    while True:
        wn.fill((200, 200, 200))
        font = pygame.font.Font(None, 40)
        wn.blit(font.render(question, True, (0, 0, 0)), (100, 120))
        wn.blit(font.render(user_text, True, (0, 0, 255)), (100, 180))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_text == answer:
                        question_index += 1
                    else:
                        life -= 1
                    return
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

def game_loop():
    global life, question_index
    life = MAX_LIFE
    question_index = 0
    block = Block(-100)
    player = Player()
    heart = Heart()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        player.update()
        block.update()
        heart.update()
        wn.blit(bg, (0, 0))
        wn.blit(player.image, player.rect)
        block.draw()
        heart.draw()
        for i in range(life):
            wn.blit(hearthImg, (10 + i * 25, 10))
        font = pygame.font.Font(None, 30)
        wn.blit(font.render(f"Soru: {question_index}/10", True, (0, 0, 0)), (350, 10))
        left_rect, right_rect, q_rect = block.get_rects()
        if player.rect.colliderect(left_rect) or player.rect.colliderect(right_rect):
            life -= 1
            block.reset()
            time.sleep(0.2)
        if player.rect.colliderect(q_rect):
            question_screen()
            block.reset()
            if question_index >= len(questions): 
                return "kazandı"
        if player.rect.colliderect(heart.rect):
            if life < MAX_LIFE:
                life += 1
            heart.reset()
        if life <= 0:
            return "oyunbitti"
        pygame.display.update()

while True:
    start_screen()
    result = game_loop()
    if result == "oyunbitti":
        game_over_screen()
    elif result == "kazandı":
        win_screen()
