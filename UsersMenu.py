import pygame
import sys
from Button import Button


def runUsersMenu(screen, events, bg, repo):
    WIDTH, HEIGHT = screen.get_size()
    
    runUsersMenu.profiles = repo.get_all_profiles()
    
    if not hasattr(runUsersMenu, "userButtons"):
        runUsersMenu.userButtons = []
    
    if not hasattr(runUsersMenu, "initialized"):
        runUsersMenu.initialized = True

        # Fuentes 
        runUsersMenu.title_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 80)
        runUsersMenu.button_font = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", 40)

        # Botones
        runUsersMenu.backButton = Button("Atras", 200, 60, (WIDTH-200 , HEIGHT-150), runUsersMenu.button_font)
        runUsersMenu.newUserButton = Button("Crear Usuario", 400, 60, (WIDTH//2 , HEIGHT-350), runUsersMenu.button_font)
        runUsersMenu.startGameButton = Button("Iniciar Juego", 500, 60, (WIDTH//2, HEIGHT-200), runUsersMenu.button_font)
        
        # Estado
        runUsersMenu.action = None
        runUsersMenu.selected_user = None
        runUsersMenu.userButtons = []
        
        runUsersMenu.scroll_offset = 0
        runUsersMenu.max_visible = 5
        runUsersMenu.item_height = 80
                
        #Variable para posicion de Usuarios
        runUsersMenu.start_y = 250
        runUsersMenu.spacing = 80
        
        runUsersMenu.last_profiles = []

        
    # reconstruir botones 
    if not hasattr(runUsersMenu, "last_profiles_str") or \
    runUsersMenu.last_profiles_str != str(runUsersMenu.profiles):

        runUsersMenu.userButtons = []

        for i, profile in enumerate(runUsersMenu.profiles):
            text = f"{profile['name']}  |  {profile['max_score']} pts"

            btn = Button(
                text,
                400,
                60,
                (WIDTH // 2, runUsersMenu.start_y + i * runUsersMenu.spacing),
                runUsersMenu.button_font
            )

            runUsersMenu.userButtons.append((btn, profile))

    runUsersMenu.last_profiles_str = str(runUsersMenu.profiles)

    backButton = runUsersMenu.backButton
    newUserButton = runUsersMenu.newUserButton
    newGameButton = runUsersMenu.startGameButton
    
    total_items = len(runUsersMenu.userButtons)
    max_offset = max(0, (total_items - runUsersMenu.max_visible) * runUsersMenu.item_height)    
    
    
    
    title_font = runUsersMenu.title_font
    
    for event in events:
        if event.type == pygame.QUIT:
            return 0
        if backButton.handle_event(event):
            runUsersMenu.action = "back"  
        if newUserButton.handle_event(event):
            runUsersMenu.action = "newUser"    
        for btn, profile in runUsersMenu.userButtons:
            if btn.handle_event(event):
                runUsersMenu.selected_user = profile
                print("Usuario seleccionado:", profile)     
        if event.type == pygame.MOUSEWHEEL:
            runUsersMenu.scroll_offset -= event.y * 20  # speed
            # clamp
            runUsersMenu.scroll_offset = max(0, min(runUsersMenu.scroll_offset, max_offset))     
        if newGameButton.handle_event(event):
            if runUsersMenu.selected_user is not None:
                runUsersMenu.action = "newGame"
            
    mouse_pos = pygame.mouse.get_pos()

    # Limpa 
    screen.blit(bg, (0, 0))

    # Title
    title = title_font.render("Seleccion de Usuario", True, (255, 60, 200))
    title_rect = title.get_rect(center=(WIDTH//2, 150))
    for i in range(6, 0, -1):
        glow = title_font.render("Seleccion de Usuario", True, (255, 20, 147))
        screen.blit(glow, title_rect)
    
    backButton.update(mouse_pos)
    newUserButton.update(mouse_pos)       
    newGameButton.update(mouse_pos)
    
    #Ciclo para render de usuarios
    for i, (btn, profile) in enumerate(runUsersMenu.userButtons):
        y = runUsersMenu.start_y + i * runUsersMenu.spacing - runUsersMenu.scroll_offset
        btn.rect.center = (WIDTH // 2, y)

        # only draw visible ones
        if 200 < y < HEIGHT - 400:
            btn.update(mouse_pos)
            btn.draw(screen)
        
    #Draw botones
    backButton.draw(screen)
    newUserButton.draw(screen)
    newGameButton.draw(screen)
    
    for btn, profile in runUsersMenu.userButtons:
        if runUsersMenu.selected_user and runUsersMenu.selected_user["id"] == profile["id"]:            
            pygame.draw.rect(
                    screen,
                    (0, 255, 200),  # neon cyan highlight
                    btn.rect,
                    3,
                    border_radius=12
                )
        
            
    # Cambio de estado (para delay entre click y cambio)
    if runUsersMenu.action == "newGame" and newGameButton.is_ready():
        runUsersMenu.action = None
        return 6, runUsersMenu.selected_user
    
    if runUsersMenu.action == "newUser" and newUserButton.is_ready():
        runUsersMenu.action = None
        return 5

    if runUsersMenu.action == "back" and backButton.is_ready():
        runUsersMenu.action = None
        return 1

    runUsersMenu.last_profiles = runUsersMenu.profiles.copy()
    
    # Actualizar 
    pygame.display.flip()

    return 4    