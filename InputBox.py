import pygame

class InputBox:
    def __init__(self, x, y, w, h, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font

        self.text = ""
        self.active = False

        # Colores
        self.baseColor = (20, 20, 50)
        self.activeColor = (60, 20, 90)
        self.textColor = (220, 240, 255)
        self.glowColor = (0, 255, 200)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return self.text  # submit text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

        return None

    def update(self):
        pass

    def draw(self, screen):
        color = self.activeColor if self.active else self.baseColor

        # Draw 
        pygame.draw.rect(screen, color, self.rect, border_radius=10)

        # Glow 
        if self.active:
            for i in range(6, 0, -2):
                glow_rect = self.rect.inflate(i*4, i*4)
                glow_surf = pygame.Surface((glow_rect.w, glow_rect.h), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (*self.glowColor, 40), glow_surf.get_rect(), border_radius=12)
                screen.blit(glow_surf, glow_rect.topleft)

        # Borde
        pygame.draw.rect(screen, (160, 80, 255), self.rect, 2, border_radius=10)

        # Texto
        txt_surface = self.font.render(self.text, True, self.textColor)
        screen.blit(txt_surface, (self.rect.x + 10, self.rect.y + 10))