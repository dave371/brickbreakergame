import pygame
from random import randint

WIDTH = 800
HEIGHT = 600
PADDLE_WIDTH = 130
PADDLE_HEIGHT = 20
BALL_WIDTH = 10
BALL_HEIGHT = 10
BRICK_WIDTH = 83.5
BRICK_HEIGHT = 30
FLAG = 0
FLAG2 = 0
font_name = pygame.font.match_font("arial")
lives = 0
BUTTON_WIDTH = 130
BUTTON_HEIGHT = 40
choice_of_level = 0
max_score = 0
center_button_offset = 11.5

# defining colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


# Classes
# Paddle class
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = paddle_image
        self.rect = self.image.get_rect()
        self.rect.centerx = int(WIDTH / 2)
        self.rect.bottom = int(HEIGHT - 30)
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        # Left movement for the paddle
        if keystate[pygame.K_LEFT]:
            self.speedx = -10
        # Right movement for the paddle
        if keystate[pygame.K_RIGHT]:
            self.speedx = 10
        self.rect.x += self.speedx
        # Right boundary for the paddle
        if self.rect.right > WIDTH - 5:
            self.rect.right = WIDTH - 5
        # Left boundary for the paddle
        if self.rect.left < 0 + 5:
            self.rect.left = 0 + 5


# Ball Class
class Ball(pygame.sprite.Sprite):
    global FLAG

    def __init__(self, paddle_object):
        pygame.sprite.Sprite.__init__(self)
        self.obj = paddle_object
        self.image = ball_image
        self.rect = self.image.get_rect()
        self.rect.centerx = self.obj.rect.centerx
        self.rect.bottom = int(HEIGHT - 55)
        self.speedx = 0
        self.speedy = 0

    def move_set_ball(self):
        keystate = pygame.key.get_pressed()
        # Movement to the left
        if keystate[pygame.K_LEFT]:
            self.speedx = -10
            self.rect.centerx = self.obj.rect.centerx
        # Movement to the right
        if keystate[pygame.K_RIGHT]:
            self.speedx = 10
            self.rect.centerx = self.obj.rect.centerx
        # Sets movement to zero when there are no keys being pressed
        if (keystate[pygame.K_LEFT] == False) and (keystate[pygame.K_RIGHT] == False):
            self.speedx = 0
        # Right boundary
        if self.rect.right > (WIDTH - 65.5):
            self.rect.centerx = self.obj.rect.centerx
            self.rect.bottom = int(HEIGHT - 55)
            self.speedx = 0
        # Left boundary
        if self.rect.left < (WIDTH - 730.5):
            self.rect.centerx = self.obj.rect.centerx
            self.rect.bottom = int(HEIGHT - 55)
            self.speedx = 0

    def launch_ball(self):
        self.speedx = 4
        self.speedy = -4

    def redirect(self):
        self.speedy *= -1

    def update(self):
        global FLAG
        global lives
        keystate = pygame.key.get_pressed()
        # Launches the ball
        if keystate[pygame.K_SPACE] and FLAG == 0:
            self.launch_ball()
            FLAG = 1
        # Right boundary for moving ball
        if self.rect.right > WIDTH:
            self.speedx *= -1
        # Left boundary for moving ball
        if self.rect.left < 0:
            self.speedx *= -1
        # Top boundary for moving ball
        if self.rect.top < 0:
            self.speedy *= -1
        # Bottom boundary for moving ball
        if self.rect.bottom > HEIGHT - 40:
            self.rect.centerx = self.obj.rect.centerx
            self.rect.bottom = int(HEIGHT - 55)
            self.speedx = 0
            self.speedy = 0
            FLAG = 0
            lives -= 1
        # Updates values
        self.rect.x += self.speedx
        self.rect.y += self.speedy


# Brick Class
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        brick_type = randint(0, 6)
        pygame.sprite.Sprite.__init__(self)
        if brick_type == 1:
            self.image = blue_block
        elif brick_type == 2:
            self.image = red_block
        elif brick_type == 3:
            self.image = purple_block
        elif brick_type == 4:
            self.image = orange_block
        elif brick_type == 5:
            self.image = lblue_block
        else:
            self.image = green_block
        self.rect = self.image.get_rect()
        self.rect.x = int(x)
        self.rect.y = int(y)


# Button Class
class Button():
    def __init__(self, x, y, width, height, text=''):
        self.image = button
        self.rect = self.image.get_rect()
        self.rect.x = int(x)
        self.rect.y = int(y)
        self.x = int(x)
        self.y = int(y)
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win):
        # Call this method to draw the button on the screen
        win.blit(self.image, (self.x, self.y))

        if self.text != '':
            font = pygame.font.Font('font/ARCADECLASSIC.TTF', 23)
            text = font.render(self.text, 1, (255, 255, 255))
            win.blit(text, (
                int(self.x + (self.width / 2 - text.get_width() / 2)),
                int(self.y + (self.height / 2 - text.get_height() / 2))))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


# initializing pygame and creating a window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker V3")
clock = pygame.time.Clock()

# Images
blue_block = pygame.image.load("images/blue brick.png")
purple_block = pygame.image.load("images/purple brick.png")
red_block = pygame.image.load("images/red brick.png")
orange_block = pygame.image.load("images/orange brick.png")
lblue_block = pygame.image.load("images/light blue brick.png")
green_block = pygame.image.load("images/green brick.png")
ball_image = pygame.image.load("images/ball.png")
paddle_image = pygame.image.load("images/paddle.png")
button = pygame.image.load("images/button.png")
button_hover = pygame.image.load("images/button hover.png")

# Sound
block_hit = pygame.mixer.Sound("music/brick hit.wav")
paddle_hit = pygame.mixer.Sound("music/paddle sound.wav")
button_click = pygame.mixer.Sound("music/button press.wav")
background_music = pygame.mixer_music.load("music/background.mp3")
block_hit.set_volume(.1)
paddle_hit.set_volume(.1)
button_click.set_volume(.1)

# Background music
pygame.mixer_music.load("music/background.mp3")
pygame.mixer_music.set_volume(.03)
pygame.mixer_music.play(-1)


# Functions
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font("font/ARCADECLASSIC.TTF", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (int(x), int(y))
    surf.blit(text_surface, text_rect)


def build_level():
    global choice_of_level
    global max_score
    brick_sprites = pygame.sprite.Group()

    if choice_of_level == 1:
        max_score = 0
        start = 9
        top = 80
        brick_sprites = pygame.sprite.Group()
        for row in range(5):
            for col in range(start):
                brick = Brick((col * (BRICK_WIDTH + 5) + 4.5), top)
                brick_sprites.add(brick)
                max_score += 1
            top += BRICK_HEIGHT + 5

    if choice_of_level == 2:
        max_score = 0
        start = 9
        top = 220
        offset = 0
        for col in range(6):
            for row in range(start):
                brick = Brick((row * (BRICK_WIDTH + 5) + 4.5) + offset, top)
                brick_sprites.add(brick)
                max_score += 1
            start -= 1
            top -= BRICK_HEIGHT + 5
            offset += 44.5

    if choice_of_level == 3:
        max_score = 0
        start = 9
        top = 40
        offset = 0
        for col in range(9):
            for row in range(start):
                brick = Brick((row * (BRICK_WIDTH + 5) + 4.5) + offset, top)
                brick_sprites.add(brick)
                max_score += 1
            start -= 1
            top += BRICK_HEIGHT + 5
            offset += 45

    return brick_sprites


def menu_call():
    FPS = 60

    play = Button(350 - center_button_offset, (HEIGHT * 1 / 2), BUTTON_WIDTH, BUTTON_HEIGHT, "Play")
    controls = Button(350 - center_button_offset, (HEIGHT * 3.5 / 6), BUTTON_WIDTH, BUTTON_HEIGHT, "Controls")
    exit_game = Button(350 - center_button_offset, (HEIGHT * 4 / 6), BUTTON_WIDTH, BUTTON_HEIGHT, "Exit")

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play.is_over(pos):
                    button_click.play()
                    pygame.time.delay(200)
                    running = False
                    level_select()
                if exit_game.is_over(pos):
                    button_click.play()
                    pygame.time.delay(200)
                    pygame.quit()
                    quit()
                if controls.is_over(pos):
                    button_click.play()
                    pygame.time.delay(200)
                    controls_menu()
            if event.type == pygame.MOUSEMOTION:
                if play.is_over(pos):
                    play.image = button_hover
                else:
                    play.image = button
                if controls.is_over(pos):
                    controls.image = button_hover
                else:
                    controls.image = button
                if exit_game.is_over(pos):
                    exit_game.image = button_hover
                else:
                    exit_game.image = button

        screen.fill(BLACK)
        draw_text(screen, "Brick Breaker", 60, 400, 150)
        play.draw(screen)
        controls.draw(screen)
        exit_game.draw(screen)
        pygame.display.update()

    pygame.quit()
    quit()


def main_game():
    # Making paddle objects
    paddle_sprite = pygame.sprite.Group()
    paddle = Paddle()
    paddle_sprite.add(paddle)

    # Making ball objects
    ball_sprite = pygame.sprite.Group()
    ball = Ball(paddle)
    ball_sprite.add(ball)

    brick_sprites = build_level()
    # All sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(brick_sprites)
    all_sprites.add(ball_sprite)
    all_sprites.add(paddle_sprite)

    # Variables
    global lives
    lives = 3
    score = 0
    FPS = 60

    # Main game loop
    running = True

    while running:
        # Determines the speed at which the program runs
        clock.tick(FPS)

        # Checking all events
        for event in pygame.event.get():
            # Making sure that we can quit
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pause_menu()

        # Moving the ball at the set position (starting point)
        if FLAG == 0:
            ball.move_set_ball()

        # Ball collision with the paddle
        if pygame.sprite.spritecollide(ball, paddle_sprite, False):
            ball.redirect()
            paddle_hit.play()

        # Brick collision and point taking
        brick_collisions = pygame.sprite.spritecollide(ball, brick_sprites, True)

        if brick_collisions:
            block_hit.play()
            ball.redirect()

        for bricks in brick_collisions:
            score += 1

        # Out of lives
        if lives == 0:
            game_over_screen()

        # Checking if you won
        if score == max_score:
            level_cleared_screen()

        # Update
        all_sprites.update()

        # Draw / render
        screen.fill(BLACK)
        all_sprites.draw(screen)
        draw_text(screen, "Score   " + str(score), 18, 200, 10)
        draw_text(screen, "Lives   " + str(lives), 18, 600, 10)

        # Flipping the display
        pygame.display.update()


def game_over_screen():
    FPS = 60

    menu = Button(150, (HEIGHT * 3 / 4), BUTTON_WIDTH, BUTTON_HEIGHT, "Menu")
    retry = Button(350, (HEIGHT * 3 / 4), BUTTON_WIDTH, BUTTON_HEIGHT, "Retry")
    exit_level = Button(550, (HEIGHT * 3 / 4), BUTTON_WIDTH, BUTTON_HEIGHT, "Exit")

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu.is_over(pos):
                    button_click.play()
                    pygame.time.delay(200)
                    menu_call()
                if retry.is_over(pos):
                    running = False
                    button_click.play()
                    pygame.time.delay(200)
                    main_game()
                if exit_level.is_over(pos):
                    running = False
                    button_click.play()
                    pygame.time.delay(400)
                    pygame.quit()
                    quit()

            if event.type == pygame.MOUSEMOTION:
                if menu.is_over(pos):
                    menu.image = button_hover
                else:
                    menu.image = button
                if retry.is_over(pos):
                    retry.image = button_hover
                else:
                    retry.image = button
                if exit_level.is_over(pos):
                    exit_level.image = button_hover
                else:
                    exit_level.image = button
            # new end

        screen.fill(BLACK)
        # new
        draw_text(screen, "GAME OVER!", 60, (WIDTH / 2), 150)
        menu.draw(screen)
        retry.draw(screen)
        exit_level.draw(screen)
        # new end
        pygame.display.update()


def level_select():
    global choice_of_level
    FPS = 60

    level_1 = Button(150, (HEIGHT * 3 / 4), BUTTON_WIDTH, BUTTON_HEIGHT, "Level 1")
    level_2 = Button(350, (HEIGHT * 3 / 4), BUTTON_WIDTH, BUTTON_HEIGHT, "Level 2")
    level_3 = Button(550, (HEIGHT * 3 / 4), BUTTON_WIDTH, BUTTON_HEIGHT, "Level 3")

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if level_1.is_over(pos):
                    choice_of_level = 1
                    button_click.play()
                    pygame.time.delay(200)
                    main_game()
                if level_2.is_over(pos):
                    choice_of_level = 2
                    button_click.play()
                    pygame.time.delay(200)
                    main_game()
                if level_3.is_over(pos):
                    choice_of_level = 3
                    button_click.play()
                    pygame.time.delay(200)
                    main_game()

            if event.type == pygame.MOUSEMOTION:
                if level_1.is_over(pos):
                    level_1.image = button_hover
                else:
                    level_1.image = button
                if level_2.is_over(pos):
                    level_2.image = button_hover
                else:
                    level_2.image = button
                if level_3.is_over(pos):
                    level_3.image = button_hover
                else:
                    level_3.image = button

        screen.fill(BLACK)
        # new
        draw_text(screen, "Level Select", 60, (WIDTH / 2), 150)
        level_1.draw(screen)
        level_2.draw(screen)
        level_3.draw(screen)
        # new end
        pygame.display.update()

    pygame.quit()
    quit()


def level_cleared_screen():
    FPS = 60

    menu = Button(150, (HEIGHT * 3 / 4), BUTTON_WIDTH, BUTTON_HEIGHT, "Menu")
    retry = Button(350, (HEIGHT * 3 / 4), BUTTON_WIDTH, BUTTON_HEIGHT, "Retry")
    exit_level = Button(550, (HEIGHT * 3 / 4), BUTTON_WIDTH, BUTTON_HEIGHT, "Exit")

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu.is_over(pos):
                    button_click.play()
                    pygame.time.delay(200)
                    menu_call()
                if retry.is_over(pos):
                    running = False
                    button_click.play()
                    pygame.time.delay(200)
                    main_game()
                if exit_level.is_over(pos):
                    button_click.play()
                    pygame.time.delay(400)
                    running = False
                    pygame.quit()
                    quit()

            if event.type == pygame.MOUSEMOTION:
                if menu.is_over(pos):
                    menu.image = button_hover
                else:
                    menu.image = button
                if retry.is_over(pos):
                    retry.image = button_hover
                else:
                    retry.image = button
                if exit_level.is_over(pos):
                    exit_level.image = button_hover
                else:
                    exit_level.image = button

        screen.fill(BLACK)
        # new
        draw_text(screen, "Level Cleared!", 60, (WIDTH / 2), 150)
        draw_text(screen, "Your score   " + str(max_score), 40, (WIDTH / 2), 250)
        menu.draw(screen)
        retry.draw(screen)
        exit_level.draw(screen)
        # new end
        pygame.display.update()


def pause_menu():
    FPS = 60

    back_gameplay = Button(350 - center_button_offset, (HEIGHT * 1 / 2), BUTTON_WIDTH, BUTTON_HEIGHT, "Return")
    controls = Button(350 - center_button_offset, (HEIGHT * 3.5 / 6), BUTTON_WIDTH, BUTTON_HEIGHT, "Controls")
    exit_game = Button(350 - center_button_offset, (HEIGHT * 4 / 6), BUTTON_WIDTH, BUTTON_HEIGHT, "Exit")

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_gameplay.is_over(pos):
                    running = False
                    button_click.play()
                    pygame.time.delay(200)
                if exit_game.is_over(pos):
                    button_click.play()
                    pygame.time.delay(400)
                    pygame.quit()
                    quit()
                if controls.is_over(pos):
                    button_click.play()
                    pygame.time.delay(200)
                    controls_menu()

            if event.type == pygame.MOUSEMOTION:
                if back_gameplay.is_over(pos):
                    back_gameplay.image = button_hover
                else:
                    back_gameplay.image = button
                if controls.is_over(pos):
                    controls.image = button_hover
                else:
                    controls.image = button
                if exit_game.is_over(pos):
                    exit_game.image = button_hover
                else:
                    exit_game.image = button

        screen.fill(BLACK)
        draw_text(screen, "Paused", 60, (WIDTH / 2), 150)
        back_gameplay.draw(screen)
        exit_game.draw(screen)
        controls.draw(screen)
        pygame.display.update()


def controls_menu():
    back_button = Button(10, 500, BUTTON_WIDTH, BUTTON_HEIGHT, "Back")

    FPS = 60
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_over(pos):
                    running = False
                    button_click.play()
                    pygame.time.delay(200)

            if event.type == pygame.MOUSEMOTION:
                if back_button.is_over(pos):
                    back_button.image = button_hover
                else:
                    back_button.image = button

        screen.fill(BLACK)
        draw_text(screen, "Controls", 40, (WIDTH / 2), 20)
        draw_text(screen, "Use the left and right arrows keys to move the paddle", 30, (WIDTH / 2), 100)
        draw_text(screen, "Use space to launch the ball", 30, (WIDTH / 2), 150)
        draw_text(screen, "Use escape to pause the game", 30, (WIDTH / 2), 200)
        back_button.draw(screen)

        pygame.display.update()


# Calls
menu_call()

# Ending program
pygame.quit()
quit()