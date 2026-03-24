import pygame
from Button import Button

def runStartMenu(screen, events, bg):

    WIDTH, HEIGHT = screen.get_size()
    is_fullscreen = screen.get_flags() & pygame.FULLSCREEN

    # Re-inicializar si cambia tamaño
    if not hasattr(runStartMenu, "last_size") or runStartMenu.last_size != (WIDTH, HEIGHT):
        runStartMenu.initialized = False
        runStartMenu.last_size = (WIDTH, HEIGHT)

    if not hasattr(runStartMenu, "initialized") or runStartMenu.initialized == False:
        runStartMenu.initialized = True

        center_x = WIDTH // 2

        # 🔥 CONFIGURACIÓN POR MODO
        if is_fullscreen:
            title_size = 80
            button_font_size = 40

            button_width = 500
            button_height = 60

            start_y = 350
            spacing = 80

        else:
            # 🔧 MÁS COMPACTO PARA VENTANA
            title_size = 60
            button_font_size = 28

            button_width = 400
            button_height = 50

            start_y = int(HEIGHT * 0.35)
            spacing = int(HEIGHT * 0.11)

        # Fuentes
        runStartMenu.title_font = pygame.font.Font(None, title_size)
        runStartMenu.button_font = pygame.font.Font(None, button_font_size)

        # Botones (centrados SIEMPRE)
        runStartMenu.startButton = Button("Nuevo Juego", button_width, button_height, (center_x, start_y), runStartMenu.button_font)

        runStartMenu.leaderboardButton = Button("Leaderboard", button_width, button_height,
                                                (center_x, start_y + spacing), runStartMenu.button_font)

        runStartMenu.settingsButton = Button("Opcion", button_width, button_height,
                                            (center_x, start_y + spacing*2), runStartMenu.button_font)

        runStartMenu.quitButton = Button("Salir", button_width, button_height,
                                        (center_x, start_y + spacing*3), runStartMenu.button_font)

        runStartMenu.action = None

    # Referencias rápidas
    startButton = runStartMenu.startButton
    leaderboardButton = runStartMenu.leaderboardButton
    settingsButton = runStartMenu.settingsButton
    quitButton = runStartMenu.quitButton

    title_font = runStartMenu.title_font

    # Eventos
    for event in events:
        if event.type == pygame.QUIT:
            return 0

        if settingsButton.handle_event(event):
            runStartMenu.action = "settings"
        
        if leaderboardButton.handle_event(event):
            runStartMenu.action = "leaderboard"

        if quitButton.handle_event(event):
            runStartMenu.action = "quit"
        
        if startButton.handle_event(event):
            runStartMenu.action = "users"    

    mouse_pos = pygame.mouse.get_pos()

    startButton.update(mouse_pos)
    leaderboardButton.update(mouse_pos)
    settingsButton.update(mouse_pos)
    quitButton.update(mouse_pos)

    # Draw
    screen.blit(bg, (0, 0))

    # Título dinámico
    title_y = int(HEIGHT * (0.2 if is_fullscreen else 0.15))
    title = title_font.render("Neon Runners", True, (255, 60, 200))
    title_rect = title.get_rect(center=(WIDTH//2, title_y))

    for i in range(6, 0, -1):
        glow = title_font.render("Neon Runners", True, (255, 20, 147))
        screen.blit(glow, title_rect)

    screen.blit(title, title_rect)

    # Botones
    startButton.draw(screen)
    leaderboardButton.draw(screen)
    settingsButton.draw(screen)
    quitButton.draw(screen)

    # Acciones
    if runStartMenu.action == "settings" and settingsButton.is_ready():
        runStartMenu.action = None
        return 2
    if runStartMenu.action == "leaderboard" and leaderboardButton.is_ready():
        runStartMenu.action = None
        return 3
    if runStartMenu.action == "users" and startButton.is_ready():
        runStartMenu.action = None
        return 4

    if runStartMenu.action == "quit" and quitButton.is_ready():
        return 0

    pygame.display.flip()
    return 1