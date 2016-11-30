import pygame, os, sys
from pygame.locals import *

class Button(pygame.sprite.Sprite):

    def __init__(self, path, bkgrnd, size):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(path).convert()
        self.img = pygame.transform.scale(img, size)
        self.rect = self.img.get_rect()
        self.img.set_colorkey(bkgrnd)
        self.angle, self.isRotating = 0, False
        self.hasRotated, self.rotateReset = 0, False

    def rotate(self):
        if self.isRotating:
            self.angle -= 2
            self.rotatedImg = pygame.transform.rotate(self.img, self.angle)
            self.rotatedRect = self.rotatedImg.get_rect()
            self.rotatedRect.center = self.rect.center
            if self.angle == -90:
                self.angle = 0
                self.isRotating = False
                self.hasRotated = 30
