# Author: Mekiyan, Mushfiq
# Username: BynumM, mushfiqmahim
#
# Assignment: P01: Final Project
#
# Purpose: Take everything from what we have learned in python to create a project
######################################################################
# Acknowledgements:

# licensed under a Creative Commons
# Attribution-Noncommercial-Share Alike 3.0 United States License.

import pygame
import random
import keyboard

class Game:
    def __init__(self): #Designing the screen
        pygame.init()
        self.size = (800, 600)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.bg_color = (255,255,255)
        self.text_color = (0, 0, 0)
        self.snake = snake(self.size)


#Created the player snake
def snake():

#The movement of the snake, when the snake eats (touches the food) it will grow, and movement:

    #use arrow keys for the movement of the snake


#Create the food and establish random places the food goes on the screen
def food():



def movement():





 def main():

    if __name__ == "__main__":
        main()