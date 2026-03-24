import pygame
from Button import Button

repo = SettingsRepository()

def runSettingsMenu(screen, events, bg, bg_original):
    WIDTH, HEIGHT = screen.get_size()

    # Detectar cambio de tamaño
    if not hasattr(runSettingsMenu, "last_size") or runSettingsMenu.last_size != (WIDTH, HEIGHT):
        runSettingsMenu.initialized = False
        runSettingsMenu.last_size = (WIDTH, HEIGHT)

    # ----------- INICIALIZACIÓN -----------
    if not hasattr(runSettingsMenu, "initialized") or not runSettingsMenu.initialized:

        is_fullscreen = screen.get_flags() & pygame.FULLSCREEN
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        scale = 1.0 if is_fullscreen else 0.8

        # Fuentes
        title_size = int(HEIGHT * 0.08 * scale)
        label_size = int(HEIGHT * 0.025 * scale)
        button_font_size = int(HEIGHT * 0.03 * scale)

        runSettingsMenu.title_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", title_size)
        runSettingsMenu.label_font = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", label_size)
        runSettingsMenu.button_font = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", button_font_size)

        # Layout
        row_height = int(95 * scale) if is_fullscreen else int(80 * scale)
        start_y = center_y - (row_height * 2.0)

        btn_w, btn_h = int(140 * scale), int(50 * scale)
        gap = int(80 * scale) if is_fullscreen else int(25 * scale)

        # Slider
        runSettingsMenu.slider_width = int(WIDTH * 0.4)
        runSettingsMenu.slider_x = center_x - runSettingsMenu.slider_width // 2
        runSettingsMenu.slider_y = start_y + 20
        runSettingsMenu.slider_hitbox = pygame.Rect(
            runSettingsMenu.slider_x,
            runSettingsMenu.slider_y - 20,
            runSettingsMenu.slider_width,
            40
        )

        # Datos
        data = repo.get_settings("game_settings")
        if data:
            runSettingsMenu.volume = data["data"]["volume"]
            runSettingsMenu.difficulty = data["data"]["difficulty"]
            runSettingsMenu.fullscreen = data["data"].get("fullscreen", False)
        else:
            runSettingsMenu.volume = 50
            runSettingsMenu.difficulty = "Easy"
            runSettingsMenu.fullscreen = False

        # Botones
        diff_y = runSettingsMenu.slider_y + row_height
        runSettingsMenu.easyBtn = Button("Easy", btn_w, btn_h,
            (center_x - (btn_w // 2) - (gap // 2), diff_y),
            runSettingsMenu.button_font)
        runSettingsMenu.hardBtn = Button("Hard", btn_w, btn_h,
            (center_x + (btn_w // 2) + (gap // 2), diff_y),
            runSettingsMenu.button_font)

        # Botones ON/OFF con ajuste solo en fullscreen
        fs_y = diff_y + row_height
        offset_fs = 30 if is_fullscreen else 0  
        runSettingsMenu.onBtn = Button("ON", btn_w, btn_h,
            (center_x - (btn_w // 2) - (gap // 2), fs_y + offset_fs),
            runSettingsMenu.button_font)
        runSettingsMenu.offBtn = Button("OFF", btn_w, btn_h,
            (center_x + (btn_w // 2) + (gap // 2), fs_y + offset_fs),
            runSettingsMenu.button_font)

        action_y = fs_y + row_height + int(35 * scale)
        runSettingsMenu.saveButton = Button("Guardar", btn_w, btn_h,
            (center_x - (btn_w // 2) - (gap // 4), action_y),
            runSettingsMenu.button_font)
        runSettingsMenu.backButton = Button("Atras", btn_w, btn_h,
            (center_x + (btn_w // 2) + (gap // 4), action_y),
            runSettingsMenu.button_font)

        # Panel
        panel_w = int(runSettingsMenu.slider_width + (180 if is_fullscreen else 120))
        runSettingsMenu.panel_rect = pygame.Rect(0, 0, panel_w, int(HEIGHT * 0.75))
        runSettingsMenu.panel_rect.center = (center_x, center_y)

        runSettingsMenu.action = None
        runSettingsMenu.initialized = True

    # ----------- EVENTOS -----------
    for event in events:
        if event.type == pygame.QUIT:
            return 0

        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            if pygame.mouse.get_pressed()[0]:
                mx, my = event.pos
                if runSettingsMenu.slider_hitbox.collidepoint(mx, my):
                    rel_x = mx - runSettingsMenu.slider_x
                    runSettingsMenu.volume = max(0, min(100,
                        int((rel_x / runSettingsMenu.slider_width) * 100)))

        if runSettingsMenu.easyBtn.handle_event(event):
            runSettingsMenu.difficulty = "Easy"
        if runSettingsMenu.hardBtn.handle_event(event):
            runSettingsMenu.difficulty = "Hard"
        if runSettingsMenu.onBtn.handle_event(event):
            runSettingsMenu.fullscreen = True
        if runSettingsMenu.offBtn.handle_event(event):
            runSettingsMenu.fullscreen = False
        if runSettingsMenu.saveButton.handle_event(event):
            runSettingsMenu.action = "save"
        if runSettingsMenu.backButton.handle_event(event):
            runSettingsMenu.action = "back"

    # ----------- RENDER -----------
    screen.blit(bg, (0, 0))
    center_x = WIDTH // 2

    # Panel
    panel_surf = pygame.Surface((runSettingsMenu.panel_rect.width, runSettingsMenu.panel_rect.height))
    panel_surf.set_alpha(195)
    panel_surf.fill((10, 5, 25))
    screen.blit(panel_surf, runSettingsMenu.panel_rect)

    # Título
    title_rect = runSettingsMenu.title_font.render("Opciones", True, (255, 60, 200)).get_rect(
        center=(center_x, runSettingsMenu.panel_rect.top + 50)
    )
    for i in range(6, 0, -1):
        glow = runSettingsMenu.title_font.render("Opciones", True, (255, 20, 147))
        screen.blit(glow, title_rect)
    title = runSettingsMenu.title_font.render("Opciones", True, (255, 60, 200))
    screen.blit(title, title_rect)

    # Slider
    pygame.draw.rect(screen, (60, 60, 80),
        (runSettingsMenu.slider_x, runSettingsMenu.slider_y,
         runSettingsMenu.slider_width, 8), border_radius=4)
    vol_w = (runSettingsMenu.volume / 100) * runSettingsMenu.slider_width
    pygame.draw.rect(screen, (0, 255, 200),
        (runSettingsMenu.slider_x, runSettingsMenu.slider_y,
         vol_w, 8), border_radius=4)
    pygame.draw.circle(screen, (255, 255, 255),
        (int(runSettingsMenu.slider_x + vol_w),
         runSettingsMenu.slider_y + 4), 10)

    # Texto Volumen
    vol_lbl = runSettingsMenu.label_font.render(
        f"Volumen: {runSettingsMenu.volume}", True, (200, 200, 200))
    screen.blit(vol_lbl, (runSettingsMenu.slider_x, runSettingsMenu.slider_y - 30))

    # Etiqueta "Dificultad"
    diff_label = runSettingsMenu.label_font.render("Dificultad", True, (200, 200, 200))
    diff_label_rect = diff_label.get_rect(center=(
        WIDTH // 2,
        runSettingsMenu.easyBtn.rect.top - 20
    ))
    screen.blit(diff_label, diff_label_rect)

    # Etiqueta "Fullscreen"
    is_fullscreen = screen.get_flags() & pygame.FULLSCREEN
    fs_offset = -15 if is_fullscreen else 0
    fs_label = runSettingsMenu.label_font.render("Fullscreen", True, (200, 200, 200))
    fs_label_rect = fs_label.get_rect(center=(
        WIDTH // 2,
        runSettingsMenu.onBtn.rect.top - 10 + fs_offset
    ))
    screen.blit(fs_label, fs_label_rect)

    # Botones
    buttons = [
        runSettingsMenu.easyBtn, runSettingsMenu.hardBtn,
        runSettingsMenu.onBtn, runSettingsMenu.offBtn,
        runSettingsMenu.saveButton, runSettingsMenu.backButton
    ]
    mouse_pos = pygame.mouse.get_pos()
    for btn in buttons:
        btn.update(mouse_pos)
    runSettingsMenu.easyBtn.draw(screen, selected=(runSettingsMenu.difficulty == "Easy"))
    runSettingsMenu.hardBtn.draw(screen, selected=(runSettingsMenu.difficulty == "Hard"))
    runSettingsMenu.onBtn.draw(screen, selected=(runSettingsMenu.fullscreen))
    runSettingsMenu.offBtn.draw(screen, selected=(not runSettingsMenu.fullscreen))
    runSettingsMenu.saveButton.draw(screen)
    runSettingsMenu.backButton.draw(screen)

    pygame.display.flip()

    # ----------- ACCIONES -----------
    if runSettingsMenu.action == "save":
        repo.save_settings(
            "game_settings",
            runSettingsMenu.volume,
            runSettingsMenu.difficulty,
            runSettingsMenu.fullscreen
        )
        if runSettingsMenu.fullscreen:
            screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((800,600))
        bg = pygame.transform.scale(bg_original, screen.get_size())
        runSettingsMenu.initialized = False
        runSettingsMenu.action = None
        return 2, screen, bg

    if runSettingsMenu.action == "back":
        runSettingsMenu.action = None
        return 1

    return 2