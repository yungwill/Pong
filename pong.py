import sys
import pygame
from pygame.locals import *
from button import Button

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# Font
pygame.font.init()
scorefont = pygame.font.SysFont(None, 70)
infofont = pygame.font.SysFont(None, 40)
titlefont = pygame.font.SysFont(None, 100)

# Screen height and width
screen_h, screen_w = 700, 1000

# Net Data
nX = screen_w/2
nY = 0
nheight = 700
nwidth = 10

# Size and initial starting position of paddles
paddleV_x, paddleV_y = 980, 260

paddleH_x, paddleH_y1, paddleH_y2 = 650, 0, 680

AIpaddleV_x, AIpaddleV_y = 0, 260

AIpaddleH_x, AIpaddleH_y1, AIpaddleH_y2 = 280, 0, 680

paddleV_w, paddleV_h = 20, 140

paddleH_w, paddleH_h = 140, 20

# Ball size, loc, and velocity
b_x, b_y = screen_w/2, screen_h/2
b_width = 20
bx_vel = screen_h/60
bx_vel = -bx_vel
by_vel = 0

# Movement factor of paddle
move_factor = 10
ai_move_factor = 12

# Flags
game_active = False
AI_win = False
P_win = False

# Score of players
AI_score = 0
p_score = 0


class Ball:
    """Class that draws the ball and controls the bouncing action"""
    def __init__(self, screen, x, y, width, velx, vely):
        self.screen, self.x, self.y, self.width = screen, x, y, width
        self.velx, self.vely = velx, vely

    def update(self, aipaddlev, aipaddleh1, aipaddleh2, paddlev, paddleh1, paddleh2):
        # Checks vertical paddle collision and changes ball movement of ai
        if (self.x + self.velx < aipaddlev.x + aipaddlev.width) \
                and ((aipaddlev.y < self.y + self.vely + self.width)
                     and (self.y + self.vely - self.width < aipaddlev.y + aipaddlev.height)):
            self.velx = -self.velx
            self.vely = ((aipaddlev.y + (aipaddlev.y + aipaddlev.height)) / 2) - self.y
            self.vely = -self.vely / ((5 * self.width) / 7)
            bounce()
        # Checks top horizontal paddle collision and changes ball movement of ai
        elif(self.y + self.vely < aipaddleh1.y + aipaddleh1.height) \
                and ((aipaddleh1.x < self.x + self.velx + self.width)
                     and (self.x + self.velx - self.width < aipaddleh1.x + aipaddleh2.width)):
            self.vely = -self.vely
            bounce()
        # Checks bottom horizontal paddle collision and changes ball movement of ai
        elif (self.y + self.vely > aipaddleh2.y + aipaddleh2.height) \
                and ((aipaddleh2.x < self.x + self.velx + self.width)
                     and (self.x + self.velx - self.width < aipaddleh2.x + aipaddleh2.width)):
            self.vely = -self.vely
            bounce()

        # Checks if the ball hit the side of the screen and adds a point to the player
        elif self.x + self.velx < 0:
            increment_pscore()
            self.x = screen_w / 2
            self.velx = screen_h / 60
            self.y = screen_h / 2
            self.vely = 0
        # Checks if the ball hit top or bottom of the screen and adds a point to the AI
        elif self.y + self.vely < 0:
            increment_aiscore()
            self.x = screen_w / 2
            self.velx = screen_h / 60
            self.y = screen_h / 2
            self.vely = 0

        # Checks vertical paddle collision and changes ball movement of player
        if (self.x + self.velx > paddlev.x) and ((paddlev.y < self.y + self.vely + self.width)
                                                 and (self.y + self.vely - self.width < paddlev.y + paddlev.height)):
            self.velx = -self.velx
            self.vely = ((paddlev.y + (paddlev.y + paddlev.height)) / 2) - self.y
            self.vely = -self.vely / ((5 * self.width) / 7)
            bounce()
        # Checks horizontal top paddle collision and changes ball movement of player
        elif (self.y + self.vely < paddleh1.y + paddleh1.height) \
            and ((paddleh1.x < self.x + self.velx + self.width)
                 and (self.x + self.velx - self.width < paddleh1.x + paddleh2.width)):
            self.vely = -self.vely
            bounce()
        # Checks horizontal bottom paddle collision and changes ball movement of player
        elif (self.y + self.vely > paddleh2.y + paddleh2.height) \
            and ((paddleh2.x < self.x + self.velx + self.width)
                 and (self.x + self.velx - self.width < paddleh2.x + paddleh2.width)):
            self.vely = -self.vely
            bounce()

        # Checks if the ball hit side of the screen and adds a point to the AI
        elif self.x + self.velx > screen_w:
            increment_aiscore()
            self.x = screen_w / 2
            self.velx = -screen_h / 60
            self.y = screen_h / 2
            self.vely = 0
        # Checks if the ball hit top or bottom of the screen and adds a point to the player
        elif self.y + self.vely > screen_h:
            increment_pscore()
            self.x = screen_w / 2
            self.velx = screen_h / 60
            self.y = screen_h / 2
            self.vely = 0

        if self.y + self.vely > screen_h or self.y + self.vely < 0:
            self.vely = -self.vely

        self.x += self.velx
        self.y += self.vely

    def draw(self):
        # draws the ball in the middle of the screen
        pygame.draw.circle(self.screen, red, (int(self.x), int(self.y)), int(self.width))


class PaddleBase:
    """Basis class for all paddles"""
    def __init__(self, screen, x, y, width, height):
        # Flags to check if keys are being pressed
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

        self.x = x
        self.y = y

        self.width = width
        self.height = height
        self.screen = screen

    def __str__(self): pass

    def update(self, ball): pass

    def draw(self):
        # Draws the paddle at loc of provided information
        pygame.draw.rect(self.screen, white, (self.x, self.y, self.width, self.height))


class AIHPaddle(PaddleBase):
    """Paddle class for Horizontal AI Paddle"""
    def __init__(self, screen, x, y, width, height):
        super().__init__(screen, x, y, width, height)
        self.screen, self.x, self.y, self.width, self.height = screen, x, y, width, height

    def __str__(self): pass

    def update(self, ball):
        # Calculates where to move
        # Checks ball x loc and moves towards it while not going beyond the screen
        if self.x > ball.x and self.x + ai_move_factor + self.width > 0:
            self.x -= ai_move_factor
        elif self.x < ball.x and self.x + ai_move_factor + self.width <= 500:
            self.x += ai_move_factor
        # Calls draw method from the base class
        super().draw()


class AIVPaddle(PaddleBase):
    """Paddle class for Vertical AI Paddle"""
    def __init__(self, screen, x, y, width, height):
        super().__init__(screen, x, y, width, height)
        self.screen, self.x, self.y, self.width, self.height = screen, x, y, width, height

    def __str__(self): pass

    def update(self, ball):
        # Calculates where to move
        # Checks ball y loc and moves towards it while not going beyond the screen
        if self.y > ball.y and self.y - ai_move_factor > 0:
            self.y -= ai_move_factor
        elif self.y < ball.y and self.y + ai_move_factor + self.height < screen_h:
            self.y += ai_move_factor
        # Calls draw method from the base class
        super().draw()


class HPaddle(PaddleBase):
    """Horizontal Player Paddle allowing player to control the paddle"""
    def __init__(self, screen, x, y, width, height):
        super().__init__(screen, x, y, width, height)
        self.screen, self.x, self.y, self.width, self.height = screen, x, y, width, height

    def __str__(self): pass

    def update(self, ball):
        # Checks flags to see if certain keys are being pressed and if they are move them there
        # while staying inside screen
        if self.moving_left:
            if self.x <= 500:
                self.x = 500
            else:
                self.x -= move_factor
        elif self.moving_right:
            if self.x + move_factor + self.width >= screen_w:
                self.x = screen_w - self.width
            else:
                self.x += move_factor
        # Calls draw method from the base class
        super().draw()


class VPaddle(PaddleBase):
    def __init__(self, screen, x, y, width, height):
        super().__init__(screen, x, y, width, height)
        self.screen, self.x, self.y, self.width, self.height = screen, x, y, width, height

    def __str__(self): pass

    def update(self, ball):
        # Checks flags to see if certain keys are being pressed and if they are move them there
        # while staying inside screen
        if self.moving_up:
            if self.y - move_factor < 0:
                self.y = 0
            else:
                self.y -= move_factor
        elif self.moving_down:
            if self.y + move_factor + self.height > screen_h:
                self.y = screen_h - self.height
            else:
                self.y += move_factor
        # Calls draw method from the base class
        super().draw()


def reset_paddles():
    """Resets paddles to original locations"""
    global paddleV_x, paddleV_y, paddleH_x, paddleH_y1, paddleH_y2
    global AIpaddleV_x, AIpaddleV_y, AIpaddleH_x, AIpaddleH_y1, AIpaddleH_y2

    paddleV_x, paddleV_y = 980, 260
    paddleH_x, paddleH_y1, paddleH_y2 = 650, 0, 680
    AIpaddleV_x, AIpaddleV_y = 0, 260
    AIpaddleH_x, AIpaddleH_y1, AIpaddleH_y2 = 280, 0, 680


def bounce():
    """Bouncing sound to be used when ball hits paddle"""
    # Stores sound inside var and plays it
    ballbounce = pygame.mixer.Sound('sounds/bounce.wav')
    ballbounce.play()


def check_play_button(play_button, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    global game_active
    # Checks if there is a collision between the mouse and rect
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        # Makes mouse cursor invisible
        pygame.mouse.set_visible(False)
        reset_score()
        game_active = True


def draw_score(screen):
    """Draws the score to the top middle of the screen"""
    # Sets the image to game_score
    points_needed = infofont.render("7 Points to Win", False, white)
    game_score = scorefont.render(str(AI_score) + "          " + str(p_score), False, white)
    # Draws the score
    screen.blit(game_score, (screen_w/2.4, 70))
    screen.blit(points_needed, (screen_w/8, 45))


def increment_aiscore():
    """Adds to AI's score when called"""
    global AI_score
    AI_score += 1


def increment_pscore():
    """Adds to player's score when called"""
    global p_score
    p_score += 1


def reset_score():
    """Resets the score to 0"""
    global AI_score
    global p_score
    AI_score, p_score = 0, 0


def win():
    """Checks if there is a winner based on score"""
    global AI_score
    global p_score
    global game_active
    global AI_win
    global P_win
    # Checks if score is 7 or above and ends the game if it is
    if AI_score >= 7:
        AI_win = True
        game_active = False
        pygame.mouse.set_visible(True)
    elif p_score >= 7:
        P_win = True
        game_active = False
        pygame.mouse.set_visible(True)


def run_game():
    # Initializes pygame
    global P_win
    global AI_win
    pygame.init()

    # Sets the background color, creates the screen, and its caption
    bg_color = black
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("Pong")
    play_button = Button(screen, "Play")

    # Initializes obj of player, ai paddles, ball classes
    paddleh1 = HPaddle(screen, paddleH_x, paddleH_y1, paddleH_w, paddleH_h)
    paddleh2 = HPaddle(screen, paddleH_x, paddleH_y2, paddleH_w, paddleH_h)
    paddlev = VPaddle(screen, paddleV_x, paddleV_y, paddleV_w, paddleV_h)

    aipaddleh1 = AIHPaddle(screen, AIpaddleH_x, AIpaddleH_y1, paddleH_w, paddleH_h)
    aipaddleh2 = AIHPaddle(screen, AIpaddleH_x, AIpaddleH_y2, paddleH_w, paddleH_h)
    aipaddlev = AIVPaddle(screen, AIpaddleV_x, AIpaddleV_y, paddleV_w, paddleV_h)

    ball = Ball(screen, b_x, b_y, b_width, bx_vel, by_vel)

    # Starts main loop for the game
    while True:
        # Checks if there are any events
        for event in pygame.event.get():
            # Quits the game if player presses the exit button on the screen
            if event.type == pygame.QUIT:
                sys.exit()
            # Checks if mouse is being pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(play_button, mouse_x, mouse_y)

            # Checks if any keys are being pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    paddlev.moving_up = True
                elif event.key == pygame.K_DOWN:
                    paddlev.moving_down = True

                if event.key == pygame.K_LEFT:
                    paddleh1.moving_left = True
                    paddleh2.moving_left = True
                elif event.key == pygame.K_RIGHT:
                    paddleh1.moving_right = True
                    paddleh2.moving_right = True

                if event.key == K_ESCAPE:
                    sys.exit()

            # Checks if any keys are released
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    paddlev.moving_up = False
                elif event.key == pygame.K_DOWN:
                    paddlev.moving_down = False

                if event.key == pygame.K_LEFT:
                    paddleh1.moving_left = False
                    paddleh2.moving_left = False
                elif event.key == pygame.K_RIGHT:
                    paddleh1.moving_right = False
                    paddleh2.moving_right = False

        screen.fill(bg_color)
        # Draws the startup screen only when game isn't playing
        if not game_active:
            title = titlefont.render("   PONG", False, white)
            title2 = titlefont.render("AI -- NO WALLS", False, green)
            screen.blit(title, (screen_w/3, 150))
            screen.blit(title2, (screen_w/4, 250))
            play_button.draw_button()

            # Prints winner of previous round in startup screen of next game
            if AI_win:
                screen.blit(scorefont.render("Player 1 is Winner!", False, green), (screen_w / 3.5, 400))
            if P_win:
                screen.blit(scorefont.render("Player 2 is Winner!", False, green), (screen_w / 3.5, 400))
            reset_paddles()
        # Only runs when game is playing
        if game_active:
            P_win = False
            AI_win = False
            # Draws the score, palyer and ai paddles, ball, and net to the screen
            draw_score(screen)

            paddleh1.draw()
            paddlev.draw()
            paddleh2.draw()

            aipaddleh1.draw()
            aipaddleh2.draw()
            aipaddlev.draw()
            ball.draw()

            pygame.draw.rect(screen, white, (nX, nY, nwidth, nheight))

            win()

            # update methods to update paddle, ball loc and movements
            paddlev.update(ball)
            paddleh1.update(ball)
            paddleh2.update(ball)

            aipaddlev.update(ball)
            aipaddleh1.update(ball)
            aipaddleh2.update(ball)
            ball.update(aipaddlev, aipaddleh1, aipaddleh2, paddlev, paddleh1, paddleh2)

        pygame.display.flip()
        # Slows down the time
        pygame.time.wait(10)


run_game()
