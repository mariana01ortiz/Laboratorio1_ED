from UsersMenu import runUsersMenu
import pygame
import sys
from Button import Button
from InputBox import InputBox




def runNewUsersMenu(screen, events, bg):
    WIDTH, HEIGHT = screen.get_size()

    # Variables creadas solo al inicio
    if not hasattr(runNewUsersMenu, "initialized"):
        runNewUsersMenu.initialized = True

        # Fuentes 
        runNewUsersMenu.title_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 80)
        runNewUsersMenu.button_font = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", 40)

        # Botones
        runNewUsersMenu.backButton = Button("Atras", 200, 60, (WIDTH-200 , HEIGHT-150), runNewUsersMenu.button_font)
        runNewUsersMenu.saveButton = Button("Guardar", 200, 60, (WIDTH//2 , 500), runNewUsersMenu.button_font)

        #Inputs
        runNewUsersMenu.nameInputBox = InputBox(WIDTH//2-200, 400, 400, 60, runNewUsersMenu.button_font)
        
        # Estado
        runNewUsersMenu.action = None
    
    backButton = runNewUsersMenu.backButton
    nameInputBox = runNewUsersMenu.nameInputBox
    saveButton = runNewUsersMenu.saveButton
    
    title_font = runNewUsersMenu.title_font
    button_font = runNewUsersMenu.button_font
    
    #Manejo de eventos
    for event in events:
        result=nameInputBox.handle_event(event)
        if event.type == pygame.QUIT:
            return 0
        if backButton.handle_event(event):
            runNewUsersMenu.action = "back"
            

        if saveButton.handle_event(event):
            name = nameInputBox.text.strip()
            if name != "":
                newId = repo.get_next_id()
                repo.save_profile(newId, name, 0, 0)
                print(f"Created {newId} for {name}")

                nameInputBox.text = ""
                
            else:
                print("Name cannot be empty")

            
    mouse_pos = pygame.mouse.get_pos()

    # Limpa 
    screen.blit(bg, (0, 0))

    # Title
    title = title_font.render("Creacion de Usuario", True, (255, 60, 200))
    title_rect = title.get_rect(center=(WIDTH//2, 150))
    for i in range(6, 0, -1):
        glow = title_font.render("Creacion de Usuario", True, (255, 20, 147))
        screen.blit(glow, title_rect)
        
    title = button_font.render("Ingrese su nombre", True, (95, 38, 105))
    title_rect = title.get_rect(center=(WIDTH//2, 360))
    for i in range(6, 0, -1):
        glow = button_font.render("Ingrese su nombre", True, (255, 255, 255))
        screen.blit(glow, title_rect)    
    
    backButton.update(mouse_pos)       
    saveButton.update(mouse_pos)
    
    backButton.draw(screen)
    nameInputBox.draw(screen)
    saveButton.draw(screen)
    
    if runNewUsersMenu.action == "back" and backButton.is_ready():
        runNewUsersMenu.action = None
        return 4
    
    
    # Actualizar 
    pygame.display.flip()
    
    return 5
