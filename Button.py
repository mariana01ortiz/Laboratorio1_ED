import pygame

class Button:
    def __init__(self, text, width, height, pos, font):
        self.text = text
        self.font = font

        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = pos

        self.baseColor  = (20, 20, 50, 160)
        self.hoverColor = (60, 20, 90)
        self.clickColor = (0, 255, 200) 
        self.textColor  = (220, 240, 255)

        self.currentColor = self.baseColor

        self.is_pressed = False
        self.press_time = 0
        self.delay = 150
        
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                self.press_time = pygame.time.get_ticks()
                self.currentColor = self.clickColor
                return False 

        if event.type == pygame.MOUSEBUTTONUP:
            if self.is_pressed:
                self.is_pressed = False
                if self.rect.collidepoint(event.pos):
                    return True
        return False

    def update(self, mouse_pos):
        if not self.is_pressed:
            if self.rect.collidepoint(mouse_pos):
                self.currentColor = self.hoverColor
            else:
                self.currentColor = self.baseColor
        else:
            if not self.rect.collidepoint(mouse_pos):
                self.currentColor = self.baseColor

    # Click termina
    def is_ready(self):
        return True 

    def draw(self, screen, selected=False):
        surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        

        pygame.draw.rect(surf, self.currentColor, surf.get_rect(), border_radius=12)
        

        if selected:
            overlay = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160)) 
            surf.blit(overlay, (0,0))

        screen.blit(surf, self.rect.topleft)


        pygame.draw.rect(screen, (160, 80, 255), self.rect, 2, border_radius=12)

    
        text = self.font.render(self.text, True, self.textColor)
        screen.blit(text, text.get_rect(center=self.rect.center))