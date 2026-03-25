import pygame
from Button import Button

def runLeaderboardMenu(screen, events, bg, repo):

    WIDTH, HEIGHT = screen.get_size()

    # Inicialización única
    if not hasattr(runLeaderboardMenu, "initialized"):
        runLeaderboardMenu.initialized = True

        runLeaderboardMenu.title_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 70)
        runLeaderboardMenu.text_font = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", 30)

        runLeaderboardMenu.backButton = Button(
            "Volver",
            300,
            60,
            (WIDTH//2, HEIGHT - 80),
            runLeaderboardMenu.text_font
        )

        runLeaderboardMenu.action = None

    title_font = runLeaderboardMenu.title_font
    text_font = runLeaderboardMenu.text_font
    backButton = runLeaderboardMenu.backButton

    # ----------- USAR EL MISMO REPO DEL MAIN -----------
    try:
        leaderboard = repo.get_all_profiles()
        leaderboard = sorted(leaderboard, key=lambda x: x["max_score"], reverse=True)
    except Exception as e:
        print("Error leaderboard:", e)
        return 1

    # ----------- EVENTOS -----------
    for event in events:
        if event.type == pygame.QUIT:
            return 0

        if backButton.handle_event(event):
            runLeaderboardMenu.action = "back"

    mouse_pos = pygame.mouse.get_pos()

    # ----------- RENDER -----------
    screen.blit(bg, (0, 0))

    title = title_font.render("LEADERBOARD", True, (255, 60, 200))
    title_rect = title.get_rect(center=(WIDTH//2, 100))

    for i in range(6, 0, -1):
        glow = title_font.render("LEADERBOARD", True, (255, 20, 147))
        screen.blit(glow, title_rect)

    screen.blit(title, title_rect)

    # ----------- TABLA -----------
    table_width = 600
    table_height = 700
    table_x = WIDTH//2 - table_width//2
    table_y = 160

    table_rect = pygame.Rect(table_x, table_y, table_width, table_height)

    table_surf = pygame.Surface((table_width, table_height), pygame.SRCALPHA)
    pygame.draw.rect(table_surf, (20, 20, 50, 180), table_surf.get_rect(), border_radius=15)
    screen.blit(table_surf, (table_x, table_y))

    pygame.draw.rect(screen, (160, 80, 255), table_rect, 2, border_radius=15)

    header_y = table_y + 30

    headers = ["POS", "NAME", "SCORE"]
    x_positions = [table_x + 80, table_x + 250, table_x + 480]

    for i in range(3):
        text = text_font.render(headers[i], True, (0, 255, 200))
        rect = text.get_rect(center=(x_positions[i], header_y))
        screen.blit(text, rect)

    pygame.draw.line(
        screen,
        (160, 80, 255),
        (table_x + 20, header_y + 30),
        (table_x + table_width - 20, header_y + 30),
        2
    )

    y = header_y + 70
    posicion = 1

    # ----------- TOP 10 -----------
    for player in leaderboard[:10]:

        nombre = player.get("name", "Unknown")
        puntaje = player.get("max_score", 0)

        try:
            puntaje = int(puntaje)
        except:
            puntaje = 0

        nombre = str(nombre)[:12]

        if posicion == 1:
            color = (255, 215, 0)
        elif posicion == 2:
            color = (192, 192, 192)
        elif posicion == 3:
            color = (205, 127, 50)
        else:
            color = (220, 240, 255)

        datos = [str(posicion), nombre, str(puntaje)]

        for i in range(3):
            render = text_font.render(datos[i], True, color)
            rect = render.get_rect(center=(x_positions[i], y))

            glow = text_font.render(datos[i], True, (0, 255, 200))
            screen.blit(glow, (rect.x - 1, rect.y))

            screen.blit(render, rect)

        y += 40
        posicion += 1

    # ----------- BOTÓN VOLVER -----------
    backButton.update(mouse_pos)
    backButton.draw(screen)

    if runLeaderboardMenu.action == "back" and backButton.is_ready():
        runLeaderboardMenu.action = None
        return 1

    return 3