class Alien():
    """ A small little alien that will rekt your shit"""

    def __init__(self,x,y,group):
        """
        takes three arguements, x and y which are the starting positions
        and group which is what type of invader the alien is
        """
        screen = pygame.display.get_surface()
        pygame.draw.rect(screen,(253,220,123),[x,y,10,10])
        self.group = group

    
