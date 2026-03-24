from UsersMenu import runUsersMenu
from newUsersMenu import runNewUsersMenu
import pygame
import asyncio
from StartMenu import runStartMenu
from SettingsMenu import runSettingsMenu
from LeaderboardMenu import runLeaderboardMenu
from Game import runGame

pygame.init()

async def main():
    settings = {"fullscreen": False}
    selected_user = None

    repo = ProfileRepository()

    if settings["fullscreen"]:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((800, 600))

    clock = pygame.time.Clock()

    bg_original = pygame.image.load("assets/images/background.jpeg").convert_alpha()
    bg = pygame.transform.scale(bg_original, screen.get_size())

    bg_original2 = pygame.image.load("assets/images/background2.png").convert_alpha()
    bg2 = pygame.transform.scale(bg_original2, screen.get_size())

    state = 1

    while True:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT or state == 0:
                return  # 🔥 IMPORTANTE en pygbag

        if state == 1:
            state = runStartMenu(screen, events, bg)

        elif state == 2:
            result = runSettingsMenu(screen, events, bg, bg_original)
            if isinstance(result, tuple):
                state, screen, bg = result
            else:
                state = result

        elif state == 3:
            state = runLeaderboardMenu(screen, events, bg)

        elif state == 5:
            state = runNewUsersMenu(screen, events, bg)
            if state == 4:
                if hasattr(runUsersMenu, "initialized"):
                    del runUsersMenu.initialized

        elif state == 4:
            result = runUsersMenu(screen, events, bg, repo)

            if isinstance(result, tuple):
                state, selected_user = result
            else:
                state = result

        elif state == 6:
            if selected_user is None:
                print("ERROR: no hay usuario seleccionado")
                state = 4
            else:
                state = runGame(screen, events, bg2, selected_user, repo)

        pygame.display.flip()
        clock.tick(60)

        # 🔥 CLAVE PARA WEB
        await asyncio.sleep(0)

# 🔥 entrada principal
asyncio.run(main())