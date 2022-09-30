#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Wonz
# 功能：主程序
import time

import pygame
import sys
import random
import maze
import color
import mapp


# 设置屏幕宽度和高度为全局变量
global screen_width
screen_width = maze.screen_width
global screen_height
screen_height = maze.screen_height


# 输出文本信息
def print_text(font, x, y, text, color, shadow=True):
    if shadow:
        imgText = font.render(text, True, (0, 0, 0))
        screen.blit(imgText, (x-2,y-2))
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x,y))

#重画迷宫
def PrintAll(r_list):
    # 画出去起点和终点的其他点
    begin_point = [0, 0]
    for i in range(maze.room_m):
        for j in range(maze.room_n):
            begin_point[0] = 25 + i * maze.room_size
            begin_point[1] = 25 + j * maze.room_size
            r_color = color.Black
            maze.draw_room(screen, begin_point, r_list[i][j].walls, maze.room_size, r_color)
    # 画起点
    maze.draw_room(screen, [25, 25], [0, 0, 0, 1], maze.room_size, color.White)
    # 画终点
    maze.draw_room(screen, [25 + (maze.room_m - 1) * maze.room_size, 25 + (maze.room_n - 1) * maze.room_size],
                        [0, 1, 0, 0], maze.room_size, color.White)
    pygame.draw.circle(screen, color.Red, [25 + (maze.room_m ) * maze.room_size, 25 + (maze.room_n- 0.5) * maze.room_size], maze.room_size/3, 0)


def PrintTotal(list_migong, list_user: list, strA: str):
    font3 = pygame.font.Font(None, 99)
    screen.fill(color.White)
    PrintAll(list_migong)
    for user in list_user:
        screen.blit(user.GetUser(), user.GetPosTuple())

    if len(strA) > 0:
        print_text(font3, (25 + (maze.room_m - 1) * maze.room_size) / 2,
                   (25 + (maze.room_n - 1) * maze.room_size) / 2, strA, color.Red, False)
    pygame.display.flip()


def PlayGame():
    succflag = False
    # 字体
    font1 = pygame.font.Font(None, 25)
    font2 = pygame.font.Font(None, 25)

    # 清屏
    screen.fill(color.White)

    # 创建随机迷宫
    r_list = maze.creat_map(maze.room_m, maze.room_n)
    begin_room = r_list[0][0]
    maze.creat_migong(r_list, begin_room)

    # 画迷宫
    PrintAll(r_list)

    # 加载角色照片，并画角色
    FirstUser = mapp.User("user.png")
    list_users =[]
    list_users.append(FirstUser)
    screen.blit(FirstUser.GetUser(), FirstUser.GetPosTuple())

    # 键盘控制角色移动
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()
            # 走到终点
            elif (FirstUser.GetMathX() == maze.room_m - 1 and FirstUser.GetMathY() == maze.room_n - 1):
                PrintTotal(r_list, list_users, "win")
                succflag = True
                for i in range(3):
                    time.sleep(1)
                    PrintTotal(r_list, list_users, f"{-i+3}")
            # 键盘响应，只取按“→”键作为例子，“↑”、“↓”、“←”类似，只要改改参数即可
            elif event.type == pygame.KEYDOWN:

                # 瞎输continue 否则下面溢出
                if (((-event.key + 1073741906) > 3) or ((-event.key + 1073741906) < 0)):
                    continue

                # 重新刷屏
                PrintTotal(r_list, [], "")

                print_text(font1, 25, 0, f"Steps:{FirstUser.GetSteps()}", color.Black, False)

                wallPos = maze.ChangeList[-event.key + 1073741906]

                # 无墙
                if (r_list[FirstUser.GetMathX()][FirstUser.GetMathY()].walls[wallPos] == False):
                    screen.blit(FirstUser.GetUser(), FirstUser.move(event.key))

                # 有墙
                elif (r_list[FirstUser.GetMathX()][FirstUser.GetMathY()].walls[wallPos] == True):
                    FirstUser.AddStep()
                    screen.blit(FirstUser.GetUser(), FirstUser.GetPosTuple())
                    print_text(font2, 300, 0, "This is a wall!", color.Red, False)

        pygame.display.flip()
        if succflag:

            succflag = False
            PlayGame()

# 游戏开始
if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode([screen_width, screen_height])
    pygame.display.set_caption('迷宫') # 游戏标题
    global font1, font2, font3 # 文字
    PlayGame()
