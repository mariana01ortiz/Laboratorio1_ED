import pygame

class Player:
    def __init__(self, x=100, y=300):
        # Cargar sprites de carrera
        self.run_frames = []
        for i in range(1, 9):
            img = pygame.image.load(f"assets/images/player/Run{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (120, 120))
            self.run_frames.append(img)

        # Cargar sprites de salto
        self.jump_frames = []
        for i in range(1, 4):
            img = pygame.image.load(f"assets/images/player/Jump_{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (120, 120))
            self.jump_frames.append(img)

        # Rectángulo
        self.rect = self.run_frames[0].get_rect()
        self.rect.inflate_ip(-20, -20)
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
        self.rect.bottom = y
        self.vel_y = 0
        self.on_ground = True
        self.ground_y = y
        

        # Animación
        self.current_frame = 0
        self.animation_speed = 0.2
        self.jumping = False

        # Física
        self.vel_y = 0
        self.gravity = 1
        self.jump_force = -20
        self.on_ground = True

        # Estado
        self.alive = True

    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_force
            self.on_ground = False
            self.jumping = True
            self.current_frame = 0

    def apply_gravity(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        ground_y = 300
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.vel_y = 0
            self.on_ground = True
            self.jumping = False

    def update_animation(self):
        if self.jumping:
            # Animación de salto
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.jump_frames):
                self.current_frame = len(self.jump_frames) - 1  
        else:
            # Animación de carrera
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.run_frames):
                self.current_frame = 0

    def get_current_image(self):
        if self.jumping:
            return self.jump_frames[int(self.current_frame)]
        else:
            return self.run_frames[int(self.current_frame)]

    def check_collision(self, obstacles, enemies):
        for obs in obstacles:
            if self.rect.colliderect(obs.rect):
                if obs.type == "mortal":
                    self.alive = False
        for enemy in enemies:
            if enemy.active and self.rect.colliderect(enemy.rect):
                self.alive = False

    def update(self, obstacles, enemies):
        if not self.alive:
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        self.apply_gravity()
        self.update_animation()
        self.check_collision(obstacles, enemies)

    def draw(self, screen):
        screen.blit(self.get_current_image(), self.rect)