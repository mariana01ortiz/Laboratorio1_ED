import pygame

class Obstacle:
    def __init__(self, x, ground_y, image, speed):
        """
        x: posición inicial en X
        ground_y: altura del suelo
        image: imagen del obstáculo
        speed: velocidad de movimiento
        """

        self.image = image

        # Escalado moderado automático
        self.scale = pygame.transform.scale(self.image, (80, 80))
        
        self.rect = self.scale.get_rect()
        self.rect.x = x
        self.rect.y = ground_y - self.rect.height

        self.speed = speed
        
        self.type = "mortal"

    def update(self):
        """Movimiento del obstáculo"""
        self.rect.x -= self.speed

    def draw(self, screen):
        """Dibujar en pantalla"""
        screen.blit(self.scale, self.rect)

    def collide(self, player_rect):
        """Detectar colisión"""
        return self.rect.colliderect(player_rect)

    def is_off_screen(self):
        """Eliminar cuando salga de pantalla"""
        return self.rect.right < 0