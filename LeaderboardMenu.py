import pygame
from Button import Button

def runLeaderboardMenu(screen, events, bg):

    # Obtiene el ancho y alto de la ventana actual
    WIDTH, HEIGHT = screen.get_size()

    # Inicialización única (se ejecuta solo la primera vez)
    if not hasattr(runLeaderboardMenu, "initialized"):
        runLeaderboardMenu.initialized = True

        # Carga de fuentes para el título y el texto
        runLeaderboardMenu.title_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 70)
        runLeaderboardMenu.text_font = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", 30)

        # Creación del botón "Volver"
        runLeaderboardMenu.backButton = Button(
            "Volver",
            300,
            60,
            (WIDTH//2, HEIGHT - 80),
            runLeaderboardMenu.text_font
        )

        # Variable para controlar acciones del menú
        runLeaderboardMenu.action = None

    # Referencias locales para facilitar el uso
    title_font = runLeaderboardMenu.title_font
    text_font = runLeaderboardMenu.text_font
    backButton = runLeaderboardMenu.backButton

    # Instancia del repositorio de perfiles
    repo = ProfileRepository()

    try:
        # Obtiene todos los perfiles
        leaderboard = repo.get_all_profiles()
        # Ordena los perfiles por puntaje (de mayor a menor)
        leaderboard = sorted(leaderboard, key=lambda x: x["max_score"], reverse=True)
    except Exception as e:
        # Manejo de errores en caso de fallo al obtener datos
        print("Error leaderboard:", e)
        return 1

    # Manejo de eventos del usuario
    for event in events:
        if event.type == pygame.QUIT:
            return 0  # Cerrar el juego

        # Detecta interacción con el botón "Volver"
        if backButton.handle_event(event):
            runLeaderboardMenu.action = "back"

    # Actualiza el estado del botón según la posición del mouse
    mouse_pos = pygame.mouse.get_pos()

    # Dibuja el fondo
    screen.blit(bg, (0, 0))

    # Renderiza el título principal
    title = title_font.render("LEADERBOARD", True, (255, 60, 200))
    title_rect = title.get_rect(center=(WIDTH//2, 100))

    # Efecto de brillo del título
    for i in range(6, 0, -1):
        glow = title_font.render("LEADERBOARD", True, (255, 20, 147))
        screen.blit(glow, title_rect)

    # Dibuja el título principal
    screen.blit(title, title_rect)

    # Dimensiones y posición de la tabla
    table_width = 600
    table_height = 700
    table_x = WIDTH//2 - table_width//2
    table_y = 160

    # Rectángulo base de la tabla
    table_rect = pygame.Rect(table_x, table_y, table_width, table_height)

    # Superficie semi-transparente para el fondo de la tabla
    table_surf = pygame.Surface((table_width, table_height), pygame.SRCALPHA)
    pygame.draw.rect(table_surf, (20, 20, 50, 180), table_surf.get_rect(), border_radius=15)
    screen.blit(table_surf, (table_x, table_y))

    # Borde de la tabla
    pygame.draw.rect(screen, (160, 80, 255), table_rect, 2, border_radius=15)

    # Posición del encabezado
    header_y = table_y + 30

    # Títulos de las columnas
    headers = ["POS", "NAME", "SCORE"]

    # Posiciones horizontales de cada columna
    x_positions = [
        table_x + 80,
        table_x + 250,
        table_x + 480
    ]

    # Renderizado de los encabezados
    for i in range(3):
        text = text_font.render(headers[i], True, (0, 255, 200))
        rect = text.get_rect(center=(x_positions[i], header_y))
        screen.blit(text, rect)

    # Línea separadora entre encabezado y datos
    pygame.draw.line(
        screen,
        (160, 80, 255),
        (table_x + 20, header_y + 30),
        (table_x + table_width - 20, header_y + 30),
        2
    )

    # Posición inicial de las filas
    y = header_y + 70
    posicion = 1

    # Itera sobre los 10 mejores jugadores
    for player in leaderboard[:10]:

        # Obtiene nombre y puntaje
        nombre = player.get("name", "Unknown")
        puntaje = player.get("max_score", 0)

        # Asegura que el puntaje sea numérico
        try:
            puntaje = int(puntaje)
        except:
            puntaje = 0

        # Limita el nombre a 12 caracteres
        nombre = str(nombre)[:12]

        # Define color según posición
        if posicion == 1:
            color = (255, 215, 0)  # Oro
        elif posicion == 2:
            color = (192, 192, 192)  # Plata
        elif posicion == 3:
            color = (205, 127, 50)  # Bronce
        else:
            color = (220, 240, 255)  # Normal

        # Datos a mostrar en la fila
        datos = [str(posicion), nombre, str(puntaje)]

        # Renderiza cada columna
        for i in range(3):
            render = text_font.render(datos[i], True, color)
            rect = render.get_rect(center=(x_positions[i], y))

            # Efecto de brillo en el texto
            glow = text_font.render(datos[i], True, (0, 255, 200))
            screen.blit(glow, (rect.x - 1, rect.y))

            screen.blit(render, rect)

        # Avanza a la siguiente fila
        y += 40
        posicion += 1

    backButton.update(mouse_pos)

    # Dibuja el botón "Volver"
    backButton.draw(screen)

    # Control de acción del botón
    if runLeaderboardMenu.action == "back" and backButton.is_ready():
        runLeaderboardMenu.action = None
        return 1

    # Actualiza la pantalla
    pygame.display.flip()

    return 3