from moviepy import VideoFileClip
import pygame

def run_launch(screen):
    clip = VideoFileClip('assets/video/intro.mpeg')
    space_icon = pygame.image.load('assets/img/space_icon.png').convert_alpha()
    

    for frame in clip.iter_frames(fps=30, dtype="uint8"):
        surf = pygame.surfarray.make_surface(frame.swapaxes(0,1))
        surf = pygame.transform.scale(surf, (screen.get_width(), screen.get_height()))

        screen.blit(surf, (0, 0))
        pygame.display.flip()
        
        # echap pour quitter l'intro
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE):
                clip.close()
                return "startGame"

    clip.close()
    return "startGame"
