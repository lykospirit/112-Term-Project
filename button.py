import pygame, os, sys
from pygame.locals import *

class Button(pygame.sprite.Sprite):

    def __init__(self, path, bkgrnd, size, row, col, passes=1, main=False, color=None):
        pygame.sprite.Sprite.__init__(self)
        self.inactiveImg = pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)
        if not main:
            activePath = path.replace('.png','active.png')
            self.activeImg = pygame.transform.scale(pygame.image.load(activePath).convert_alpha(), size)
        else: self.activeImg = self.inactiveImg
        self.img = self.inactiveImg
        self.rect = self.img.get_rect()
        self.img.set_colorkey(None)
        self.angle, self.isRotating = 0, False
        self.hasRotated, self.rotateReset = 0, False
        self.passes, self.main, self.color, self.row, self.col = passes, main, color, row, col
        self.active, self.lastColor = 0, None

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
