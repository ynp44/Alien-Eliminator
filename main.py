import pygame
import random

pygame.init()  # initialize pygame
win = pygame.display.set_mode((1000, 500))

pygame.display.set_caption("Alien Elimination")
laserSound = pygame.mixer.Sound("laser1.wav")
music = pygame.mixer.music.load("spaceship.wav")
pygame.mixer.music.play(-1)

walkRight = [pygame.image.load('man_shoot_ right.png'), pygame.image.load('man_shoot_ right.png'), pygame.image.load('man_walk_right.png'),pygame.image.load('man_walk_right.png')]
walkLeft = [pygame.image.load('man_shoot_left.png'), pygame.image.load('man_shoot_left.png'),pygame.image.load('man_walk_left .png'),pygame.image.load('man_walk_left .png')]
bg = pygame.image.load('space.jpg')

bul = pygame.image.load('blue_bullet.png')
bul = pygame.transform.scale(bul,(50,50))

clock = pygame.time.Clock()

class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win): #walking calculation
        if self.walkCount + 1 >= 8:
            self.walkCount = 0

        if not (self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 2], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 2], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 13, self.y + 2, 40, 52)

    def hit(self): #collides with enemy
        self.isJump = False  # debug for reset the character
        self.jumpCount = 10
        self.x = 5  # We are resetting the player position
        self.y = 301
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('Lives -1', 1, (255, 0, 0))
        win.blit(text, (500 - (text.get_width() / 2), 220))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 101  # can't use break because it will not go to .quit() func at the bottom
                    pygame.quit()

class Projectile(object): #shooting
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.velocity = 3 * facing

    def draw(self, win):
        win.blit(bul, (self.x, self.y))

class Enemy(object):
    walkRight = [pygame.image.load('ufo_alien _left.png'), pygame.image.load('ufo_alien _left.png'), pygame.image.load('ufo_alien _left.png'),pygame.image.load('ufo_alien _left.png')]
    walkLeft = [pygame.image.load('ufo_alien_right.png'), pygame.image.load('ufo_alien_right.png') ,pygame.image.load('ufo_alien_right.png'),pygame.image.load('ufo_alien_right.png')]

    def __init__(self, x, y, end):
        self.x = x
        self.y = y
        self.path = [0, 900]
        self.walkCount = 0
        self.velocity = 6
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win): #walking
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 8:
                self.walkCount = 0

            if self.velocity > 0:
                win.blit(self.walkRight[self.walkCount // 2], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 2], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))  # Red
            pygame.draw.rect(win, (0, 128, 0),
                             (self.hitbox[0], self.hitbox[1] - 20, 5 * self.health, 10))  # Green
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)  # estimate closest value

    def move(self):
        if self.velocity > 0:
            if self.x < self.path[1] + self.velocity:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.x += self.velocity
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.velocity:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.x += self.velocity
                self.walkCount = 0

    def hit(self): #shot by player
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

# main loop
def main():
    font = pygame.font.SysFont("microsoftsansserif", 30, True)  # the third argument is for activate bold
    lost_font = pygame.font.SysFont("microsoftsansserif", 70, True)
    # win_font = pygame.font.SysFont("microsoftsansserif", 70, True)
    man = Player(5, 301, 73, 64)
    shootLoop = 0
    bullets = []
    alien = []
    lives = 3
    score = 0
    lost = False
    lost_count = 0
    winner = False
    FPS = 27
    run = True

    def redrawGameWindow(): #game window detail
        win.blit(bg, (0, 0))  # built-in func for the paste every image include background too
        score_label = font.render('Score: ' + str(score), 1, (0, 0, 0))  # 1 is for anti-aliasing, just do it

        win.blit(score_label, (850, 10))
        man.draw(win)

        lives_label = font.render(f"Lives: {lives}", 1, (0, 0, 0))  # color
        win.blit(lives_label, (10, 10))  # position

        if len(alien) >= 1 or len(bullets) >= 1:
            for i in range(4):
                alien[i].draw(win)

            for bullet in bullets:
                bullet.draw(win)

        if lost:
            lost_label1 = lost_font.render("Game Over", 1, (0, 0, 0))
            win.blit(lost_label1, (1000 / 2 - lost_label1.get_width() / 2, 220))
            lost_label2 = lost_font.render(f"Score : {score}",1,(0,0,0))
            win.blit(lost_label2,(1000/2 - lost_label2.get_width()/2,300))

        pygame.display.update()

    while run:  # pygame must run in the loop
        clock.tick(FPS)
        redrawGameWindow()
        # for Lost the game
        if lives <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        for i in range(4):
            alien.append(Enemy(random.randint(0,1000),random.randint(100,400),900))
            pygame.display.update()
            # the collision between Man and Enemy cause damage
            if alien[i].visible == True:
                if man.hitbox[1] < alien[i].hitbox[1] + alien[i].hitbox[3] and man.hitbox[1] + man.hitbox[3] > \
                        alien[i].hitbox[1]:
                    if man.hitbox[0] + man.hitbox[2] > alien[i].hitbox[0] and man.hitbox[0] < alien[i].hitbox[0] + \
                            alien[i].hitbox[2]:
                        man.hit()
                        lives -= 1

            # the collision between Bullet and Enemy
            for bullet in bullets:
                if alien[i].visible == True:
                    if bullet.y - 6 < alien[i].hitbox[1] + alien[i].hitbox[3] and \
                            bullet.y + 6 > alien[i].hitbox[1]:  # for y
                        if bullet.x + 6 > alien[i].hitbox[0] and \
                                bullet.x - 6 < alien[i].hitbox[0] + alien[i].hitbox[2]:  # for x

                            alien[i].hit()
                            bullets.pop(bullets.index(bullet))
                elif alien[i].visible == False:
                    alien.pop(i)
                    score += 1


                if bullet.x < 1000 and bullet.x > 0:
                    bullet.x += bullet.velocity  # The bullets will move plus its vel
                else:
                    bullets.pop(bullets.index(bullet))

        if shootLoop > 0:
            shootLoop += 1
        if shootLoop > 2:
            shootLoop = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # press Keys zone
        keys = pygame.key.get_pressed()  # receive the key button and you saw the bottom, it will be list
        if keys[pygame.K_SPACE] and shootLoop == 0:
            laserSound.play()
            if man.left:
                facing = -1
            else:
                facing = 1

            if len(bullets) < 5:  # max bullet in the screen
                bullets.append(
                    Projectile(round(man.x + man.width // 2.9), round(man.y + man.height // 2.9), facing)) #shoot from the gun


            shootLoop = 1


        if keys[pygame.K_LEFT] and man.x > man.velocity:
            if keys[pygame.K_UP] and man.y - man.velocity > 500 - man.height:
                man.y -= man.velocity
                man.up = True
                man.down = False
                man.standing = False
                man.x -= man.velocity
                man.left = True
                man.right = False
            elif keys[pygame.K_DOWN] and man.y + man.velocity < 500 - man.height:
                man.y += man.velocity
                man.up = False
                man.down = True
                man.standing = False
                man.x -= man.velocity
                man.left = True
                man.right = False
            else:
                man.x -= man.velocity
                man.left = True
                man.right = False
                man.standing = False

        elif keys[pygame.K_RIGHT] and man.x < 1000 - man.width - man.velocity:
            if keys[pygame.K_UP] and man.y - man.velocity > 0 - man.height:
                man.y -= man.velocity
                man.up = True
                man.down = False
                man.standing = False
                man.x += man.velocity
                man.left = False
                man.right = True
            elif keys[pygame.K_DOWN] and man.y + man.velocity < 500 - man.height:
                man.y += man.velocity
                man.up = False
                man.down = True
                man.standing = False
                man.x += man.velocity
                man.left = False
                man.right = True
            else:
                man.x += man.velocity
                man.right = True
                man.left = False
                man.standing = False

        elif keys[pygame.K_UP] and man.y - man.velocity > 0 - man.height:
            man.y -= man.velocity
            man.up = True
            man.down = False
            man.standing = False
        elif keys[pygame.K_DOWN] and man.y + man.velocity < 500 - man.height:
            man.y += man.velocity
            man.down = True
            man.up = False
            man.standing = False
        else:
            man.standing = True
            man.walkCount = 0

def main_menu():
    title_font = pygame.font.SysFont("microsoftsansserif", 80, True)
    run = True
    while run:
        win.blit(bg, (0, 0))
        title_label = title_font.render("Click to Start", 1, (0, 0, 0))
        win.blit(title_label, (1000/2 - title_label.get_width()/2, 220))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()