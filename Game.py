import pygame
import random
from Enemy import Enemy
from Player import Player
from Obstacle import Obstacle

def runGame(screen, events, bg, player_data, repo):

    # 🔥 Inicialización SOLO UNA VEZ
    if not hasattr(runGame, "initialized"):
        runGame.initialized = True

        runGame.clock = pygame.time.Clock()
        runGame.WIDTH, runGame.HEIGHT = screen.get_size()

        runGame.ground_y = runGame.HEIGHT - 300
        runGame.player = Player(100, runGame.ground_y)
        runGame.enemy = Enemy()
        runGame.obstacles = []

        runGame.obstacle_images = []
        for i in range(1, 4):
            img = pygame.image.load(
                f"assets/images/obstacle/obstaculo{i}.png"
            ).convert_alpha()
            runGame.obstacle_images.append(img)

        runGame.spawn_timer = 0
        runGame.spawn_delay = random.randint(800, 1800)

        runGame.score = 0
        runGame.score_timer = 0

        runGame.font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 40)
        runGame.pause_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 55)

        runGame.paused = False

    # 🔥 FRAME UPDATE
    dt = runGame.clock.tick(60)
    runGame.score_timer += dt

    if runGame.score_timer >= 500:
        runGame.score += 10
        runGame.score_timer = 0

    # -------- EVENTS --------
    for event in events:
        if event.type == pygame.QUIT:
            return 0

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_SPACE):
                runGame.player.jump()

            if event.key == pygame.K_ESCAPE:
                runGame.paused = not runGame.paused

            if runGame.paused and event.key == pygame.K_q:
                del runGame.initialized
                return 1

    # -------- PAUSE --------
    if runGame.paused:
        pause_text = runGame.pause_font.render(
            "Juego pausado - ESC continuar | Q salir",
            True,
            (255, 255, 255)
        )

        rect = pause_text.get_rect(
            center=(runGame.WIDTH // 2, runGame.HEIGHT // 2)
        )

        screen.blit(bg, (0, 0))
        screen.blit(pause_text, rect)
        return 6  # 🔥 seguimos en estado juego

    # -------- SPAWN --------
    runGame.spawn_timer += dt
    if runGame.spawn_timer >= runGame.spawn_delay:
        runGame.spawn_timer = 0
        runGame.spawn_delay = random.randint(800, 1800)

        img = random.choice(runGame.obstacle_images)
        obstacle = Obstacle(runGame.WIDTH, runGame.ground_y, img, speed=6)
        runGame.obstacles.append(obstacle)

    # -------- UPDATE --------
    runGame.player.update(runGame.obstacles, [runGame.enemy])

    dead = runGame.enemy.update(runGame.player.rect, runGame.obstacles)
    if dead:
        runGame.player.alive = False

    for obs in runGame.obstacles:
        obs.update()

    runGame.obstacles = [
        obs for obs in runGame.obstacles if not obs.is_off_screen()
    ]

    # -------- GAME OVER --------
    if not runGame.player.alive:
        print("Guardando score:", player_data["id"], runGame.score)
        repo.update_max_score(player_data["id"], runGame.score)

        del runGame.initialized  # 🔥 reinicia el juego
        return 1

    # -------- DRAW --------
    screen.blit(bg, (0, 0))

    score_text = runGame.font.render(
        f"Puntos: {runGame.score}", True, (255, 255, 255)
    )
    screen.blit(score_text, (runGame.WIDTH - 300, 20))

    runGame.player.draw(screen)
    runGame.enemy.draw(screen)

    for obs in runGame.obstacles:
        obs.draw(screen)

    return 6  # 🔥 seguimos en juego