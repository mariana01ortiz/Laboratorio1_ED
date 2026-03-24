import pygame

class Enemy:
    def __init__(self, delay_ms=500, size=(120, 120)):
        # -------- SPRITES --------
        self.frames = []
        for i in range(1, 11):
            img = pygame.image.load(f"assets/images/enemy/cop{i}.png").convert_alpha()
            img = pygame.transform.scale(img, size)
            self.frames.append(img)

        self.current_frame = 0
        self.animation_speed = 0.2

        # -------- HITBOX --------
        self.rect = self.frames[0].get_rect()
        self.rect.inflate_ip(-30, -30)  # hitbox más ajustado

        # -------- MOVIMIENTO --------
        self.speed = 5
        self.delay_ms = delay_ms
        self.spawn_time = pygame.time.get_ticks()
        self.active = False

        # -------- FÍSICA --------
        self.vel_y = 0
        self.gravity = 1
        self.jump_force = -18
        self.on_ground = False

        # -------- SUELO --------
        self.ground_y = 0

    def update(self, player_rect, obstacles):
        current_time = pygame.time.get_ticks()

        # -------- SPAWN CON DELAY --------
        if not self.active:
            if current_time - self.spawn_time >= self.delay_ms:
                self.active = True

                # Aparece fuera de pantalla (izquierda)
                self.rect.midleft = (-200, player_rect.centery)

                # Alinear suelo con el jugador
                self.ground_y = player_rect.bottom
                self.rect.bottom = self.ground_y
                self.on_ground = True
            else:
                return False

        # -------- ANIMACIÓN --------
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0

        # -------- MOVIMIENTO HACIA EL JUGADOR --------
        self.rect.x += self.speed


        # -------- DETECTAR OBSTÁCULOS --------
        look_ahead = self.rect.copy()
        look_ahead.x += 80

        for obstacle in obstacles:
            if look_ahead.colliderect(obstacle.rect):
                if self.on_ground:
                    self.vel_y = self.jump_force
                    self.on_ground = False

        # -------- GRAVEDAD --------
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.vel_y = 0
            self.on_ground = True
            
        # -------- RESPAWN SI SALE DE PANTALLA --------
        screen_width = pygame.display.get_surface().get_width()

        if self.rect.left > screen_width:
            self.rect.right = -100  # reaparece por la izquierda
            self.rect.bottom = self.ground_y    

        # -------- COLISIÓN CON PLAYER --------
        if self.rect.colliderect(player_rect):
            return True

        return False

    def draw(self, screen):
        if self.active:
            frame = self.frames[int(self.current_frame)]

            # Dibujar centrado respecto al hitbox
            draw_rect = frame.get_rect(center=self.rect.center)
            screen.blit(frame, draw_rect)