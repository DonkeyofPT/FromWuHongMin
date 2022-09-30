#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Wonz
# 功能：迷宫

import pygame
import sys
import time
from pygame.locals import *
from random import randint, choice
import color


# 设置迷宫的大小
global room_m, room_n, room_size
room_m = 10
room_n = 10
room_size = 30 # 每个小房间的大小


# 设置屏幕宽度和高度为全局变量
global screen_width
screen_width = room_m * room_size*1.2
global screen_height
screen_height = room_m * room_size*1.2


#迷宫墙壁判断 这个叼迷宫的上下左右碰墙不是0123 而是下面的对应。
# 上0 下2 左3 右1
ChangeList = [0, 2, 3, 1]

class room():
    def __init__(self, x, y):
        self.walls = [True, True, True, True] # 初始化地图，小房间四周都是墙
        self.visited = False # 初始化小房间都未被访问过
        self.x = x
        self.y = y

    def getx(self):
        return self.x

    def gety(self):
        return self.y

# 画迷宫
def draw_room(screen, begin_point, walls, size, r_color):
    n = 0
    # 一个小房间的四面墙
    for wall in walls:
        x = begin_point[0] # 迷宫起点的 x 坐标
        y = begin_point[1] # 迷宫起点的 y 坐标
        n += 1
        if n == 1 and wall: # x → x + size 是墙
            pygame.draw.line(screen, r_color, (x, y), (x + size, y))
        if n == 2 and wall:
            pygame.draw.line(screen, r_color, (x + size, y), (x + size, y + size))
        if n == 3 and wall:
            pygame.draw.line(screen, r_color, (x + size, y + size), (x, y + size))
        if n == 4 and wall:
            pygame.draw.line(screen, r_color, (x, y + size), (x, y))


# 生成迷宫地图， 这个数学迷宫，True也就是1 表示有墙
def creat_map(m, n):
    room_list = [[0 for col in range(n)] for row in range(m)] # 二维数组: m*n
    for i in range(m):
        for j in range(n):
            room_list[i][j] = room(i, j)
    return room_list


# whm add 作用在于填补四周的空缺 还有就是让相邻的上下墙都是状态为1
def check_map(room_list: list):
    for i in range(room_m):
        for j in range(room_n):
            room = room_list[i][j]
            # 上
            if i == 0:
                room.walls[3] = 1  # 左
            if i == room_m-1:
                room.walls[1] = 1  # 右
            if j == 0:
                room.walls[0] = 1  # 上
            if j == room_n-1:
                room.walls[2] = 1  # 下

            if j < room_n-1:
                if room_list[i][j].walls[2] == 1:
                    room_list[i][j+1].walls[0] = 1
                if room_list[i][j+1].walls[0] == 1:
                    room_list[i][j].walls[2] = 1


# 获取下一个房间
def get_next_room(room_list, room):
    temp_rooms = {1: None,
                  2: None,
                  3: None,
                  4: None}
    temp_room_count = 0
    # 判断上下左右四个方向的小房间有没有被访问，没有的话就加入 temp_rooms[]
    if (not room.y - 1 < 0) and (not room_list[room.x][room.y - 1].visited): # 上边没被访问
        temp_rooms[1] = room_list[room.x][room.y - 1]
        temp_room_count += 1
    if (not room.x + 1 > room_m - 1) and (not room_list[room.x + 1][room.y].visited): # 右边
        temp_rooms[2] = room_list[room.x + 1][room.y]
        temp_room_count += 1
    if (not room.y + 1 > room_n - 1) and (not room_list[room.x][room.y + 1].visited): # 下边
        temp_rooms[3] = room_list[room.x][room.y + 1]
        temp_room_count += 1
    if (not room.x - 1 < 0) and (not room_list[room.x - 1][room.y].visited): # 左边
        temp_rooms[4] = room_list[room.x - 1][room.y]
        temp_room_count += 1

    if temp_room_count > 0:
        while True:
            room_id = randint(1, 4) # 随机生成，指定某一边没有墙
            if temp_rooms[room_id]:
                next_room = temp_rooms[room_id]
                if room_id == 1:
                    room.walls[0] = 0  # # 上0 下2 左3 右1  当前房间的上边没有墙
                    next_room.walls[2] = 0  # 上面房间的下边没有墙
                if room_id == 2:
                    room.walls[1] = 0 #当前房间的右边
                    next_room.walls[3] = 0 #上面房间的左边

                    #whm add begin 就是让迷宫更复杂一点，同时创造了一个bug，相邻的正方形 需要check_map修复。
                    room.walls[2] = 0
                    next_room.walls[0] = 0
                    #whm add end

                if room_id == 3:
                    room.walls[2] = 0
                    next_room.walls[0] = 0
                if room_id == 4:
                    room.walls[3] = 0
                    next_room.walls[1] = 0
                break
        return next_room
    else:
        return None


# 创建迷宫
def creat_migong(room_list, next_room, temp_yes_rooms=[]):
    while True:
        if next_room:
            # 下一房间未被访问
            if not next_room.visited:
                next_room.visited = True
                temp_yes_rooms.append(next_room)
            next_room = get_next_room(room_list, next_room)
        else:
            next_room = temp_yes_rooms.pop()  # 否则出栈
            if len(temp_yes_rooms) == 0:
                break
    # whm add 新增修补迷宫四周。
    check_map(room_list)
