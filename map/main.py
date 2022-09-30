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

#名字没取好 功能就是画迷宫
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


# 功能比较多， 就是画迷宫，画用户，画中间的大字。 如果strA传空 就不画大字
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


# 玩游戏调用这个就可以 然后里面设置了循环调用这个函数 方便重复玩
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
                time.sleep(1)
                for i in range(3):
                    PrintTotal(r_list, list_users, f"{-i+3}")
                    time.sleep(1)
                PlayGame()
            # 键盘响应，只取按“→”键作为例子，“↑”、“↓”、“←”类似，只要改改参数即可
            elif event.type == pygame.KEYDOWN:

                # 瞎输continue 否则下面溢出
                if (((-event.key + 1073741906) > 3) or ((-event.key + 1073741906) < 0)):
                    continue

                # 因为上下左右是一定的数值 所以先取到0 1 2 3 再根据ChangeList 转为迷宫识别的上下左右下标
                wallPos = maze.ChangeList[-event.key + 1073741906]

                # 无墙 才可以移动
                if (r_list[FirstUser.GetMathX()][FirstUser.GetMathY()].walls[wallPos] == False):
                    # 重新刷屏 主要是清理所有头像画面
                    PrintTotal(r_list, [], "")
                    screen.blit(FirstUser.GetUser(), FirstUser.move(event.key))

                # 有墙 不能移动 但是没有移动的话 也要给这个用户增加步数，也可以不加就是了
                elif (r_list[FirstUser.GetMathX()][FirstUser.GetMathY()].walls[wallPos] == True):
                    FirstUser.AddStep()
                    # 重新刷屏 主要是清理之前的字体
                    PrintTotal(r_list, list_users, "")
                    print_text(font2, 300, 0, "This is a wall!", color.Red, False)

                print_text(font1, 25, 0, f"Steps:{FirstUser.GetSteps()}", color.Black, False)

        #这个不能删 否则会黑屏
        pygame.display.flip()



# 游戏开始
if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode([screen_width, screen_height])
    pygame.display.set_caption('迷宫') # 游戏标题
    global font1, font2, font3 # 文字
    PlayGame()
