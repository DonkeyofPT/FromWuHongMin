#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pygame
import maze


class User:
    # 数学位置
    roomx = 0
    roomy = 0
    # 角色开局位置
    __PosX = 26+maze.room_size/10
    __posY = 25+maze.room_size/10
    __user = 0

    #用户耗费步数
    __steps = 0

    #角色图形调用方法screen.blit(FirstUser.GetUser(), FirstUser.GetPosTuple())
    def __init__(self, strA: str):
        self.__user = pygame.image.load(strA).convert_alpha()
        self.__user = pygame.transform.smoothscale(self.__user, (maze.room_size / 1.5, maze.room_size / 1.5))

    def move(self, direct: int):
        self.__steps += 1
        # 上
        if direct == 1073741906:
            self.__posY -= maze.room_size
            self.roomy -= 1
        # 下
        elif direct == 1073741905:
            self.__posY += maze.room_size
            self.roomy += 1
        # 左
        elif direct == 1073741904:
            self.__PosX -= maze.room_size
            self.roomx -= 1
        # 右
        elif direct == 1073741903:
            self.__PosX += maze.room_size
            self.roomx += 1

        return (self.__PosX, self.__posY)

    def GetUser(self):
        return self.__user

    def GetSteps(self):
        return self.__steps

    def GetPosTuple(self):
        return (self.__PosX, self.__posY)

    def GetMathX(self):
        return self.roomx

    def GetMathY(self):
        return self.roomy

    def AddStep(self):
        self.__steps += 1
