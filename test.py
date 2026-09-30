import pygame
import settings as st
import text

# Initialize pygame
pygame.init()

# Setup screen and canvas (done before the loop)
canvas = pygame.Surface((400, 600))
#realscreen = pygame.display.set_mode((800, 600), pygame.SCALED , vsync=1)
realscreen = st.Abstract().screen2
#clock = pygame.time.Clock()
running = True

# --- THE MAIN GAME LOOP ---
while running:
    
    # 1. Event Handling (Happens once per frame)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Clear canvas (Prevents smearing/flickering from past frames)
    canvas.fill((30, 30, 30))

    canvas.blit(pygame.image.load('chara_sprites/chara_placeholder.bmp'), (0,0))
    # 3. Draw your game elements onto the canvas
    # Example: pygame.draw.circle(canvas, (255, 0, 0), (400, 300), 50)
    lines = ["Game Start", "Settings", "Quit"]
    height_of_line = st.UISettings().text_margin_up

    canvas.fill(st.UISettings().bg_color)
    for line in lines:
        text.render_text(canvas, line, 
                        (st.UISettings().text_margin_left,
                        height_of_line,
                        ))
        height_of_line += st.UISettings().text_line_height
    # 4. Clear the real screen
    realscreen.fill((0, 0, 0))

    # 5. Blit your canvas onto the real screen
    realscreen.blit(canvas, (0, 0))

    # 6. FLIP THE DISPLAY (This must happen ONLY HERE, exactly once per loop)
    pygame.display.flip()

    # 7. Control frame rate (e.g., 60 FPS)
    #clock.tick(60)

pygame.quit()