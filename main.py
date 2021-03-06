import pygame, sys, random, math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invasion")
icon = pygame.image.load("rocket.png")
pygame.display.set_icon(icon)


background = pygame.image.load("bg.jpg")

mixer.music.load('moonlight.wav')
mixer.music.play(-1)

playerImg = pygame.image.load("spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(0, num_of_enemies):
	enemyImg.append(pygame.image.load("alien.png"))
	enemyX.append(random.randint(0, 736))
	enemyY.append(random.randint(50,150))
	enemyX_change.append(3)
	enemyY_change.append(40)

bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 8
bullet_state = "ready"

score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)
overX = 200
overY = 250

def player(playerX, playerY):
	screen.blit(playerImg, (playerX, playerY))

def enemy(enemyX, enemyY, i):
	screen.blit(enemyImg[i], (enemyX, enemyY))

def fire_bullet(bulletX, bulletY):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bulletImg, (bulletX + 16, bulletY + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
	distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
	if distance < 27:
		return True
	return False

def showScore(textX, textY):
	showscore = font.render("Score : " + str(score), True, (250, 150, 150))
	screen.blit(showscore, (textX, textY))

def game_over_text(textX, textY):
	showover = over_font.render("GAME OVER!", True, (250,150,150))
	screen.blit(showover, (overX, overY))

while True:
	screen.fill((7,11,22))
	screen.blit(background, (0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				playerX_change = 3.0
			if event.key == pygame.K_LEFT:
				playerX_change = -3.0
			if event.key == pygame.K_SPACE:
				if bullet_state is "ready":
					bullet_sound = mixer.Sound('shoot.wav')
					bullet_sound.play()
					bulletX = playerX
					fire_bullet(bulletX, bulletY)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change = 0

	playerX += playerX_change

	if playerX <= 0:
		playerX = 0
	elif playerX >= 736:
		playerX = 736

	for i in range(0, num_of_enemies):
		if enemyY[i] > 450:
			for i in range(0, num_of_enemies):
				enemyY[i] = 2000
			game_over_text(overX, overY)
			break
		enemyX[i] += enemyX_change[i]
		if enemyX[i] <= 0:
			enemyX_change[i] = 2.0
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= 736:
			enemyX_change[i] = -2.0
			enemyY[i] += enemyY_change[i]

		collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
		if collision:
			explosion_sound = mixer.Sound('explode.wav')
			explosion_sound.play()
			bulletY = 480
			bullet_state = "ready"
			score += 1
			print(score)
			enemyX[i] = random.randint(0,800)
			enemyY[i] = random.randint(50,150)

		enemy(enemyX[i], enemyY[i], i)

	if bulletY <= 0:
		bulletY = 480
		bullet_state = "ready"

	if bullet_state is "fire":
		fire_bullet(bulletX, bulletY)
		bulletY -= bulletY_change

	player(playerX, playerY)
	showScore(textX, textY)
	pygame.display.update()
