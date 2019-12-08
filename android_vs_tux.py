# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 13:30:11 2019

@author: Azumi Mamiya
"""

import sys
import pygame
import random
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_LEFT, K_RIGHT,K_SPACE, K_r
import abc
import my_function as my_func



def dispmessage(sf, msg, h, color):
    sysfont = pygame.font.SysFont(None, 60)
    message = sysfont.render(msg, True, color)
    message_rect = message.get_rect()
    message_rect.center = (300,h)
    sf.blit(message, message_rect)

class MyObject():
    def __init__(self,x,y,wh,w,h,name):
        # player settings
        self.x = x; self.y = y #オブジェクトの座標
        self.wh = wh# オブジェクトの大きさ
        self.dx = 0; self.dy = 0 #プレイヤーの速度
        # area settings
        self.w = w; self.h = h #エリアの横と縦の大きさ
        self.t_jump=0; self.t_move = 0 # 移動からの時間を計測
        # game settings
        self.GRAVITY=0.6 # 重力
        self.Decay=0.5 # 横移動の減衰率
        self.name=name
        
    def move(self):
        self.x += self.dx; self.y += self.dy# 移動
        self.t_jump+=2; self.t_move+=1# 時間進める
        
        if self.dx > self.wh*0.2:
            self.dx -= abs(self.Decay * self.t_move)
        elif self.dx < -self.wh*0.2:
            self.dx += abs(self.Decay * self.t_move)
        else:
            self.dx=0
        self.dy += self.GRAVITY * self.t_jump
        
    def collision_area(self):
        if self.x < 0 + self.wh:
            self.dx *= 0
            self.x = 0 + self.wh*2/3
        
        if self.x > self.w -2*self.wh:
            self.dx *= 0
            self.x = self.w -self.wh-self.wh*2/3
        
        if self.y < 0 :
            self.dy *= -1
        
        if self.y > self.h-self.wh:
            self.dy *= 0
            self.y=self.h-self.wh
    
    def xy_body(self):
        return {'x1':self.x,
                'x2':self.x + self.wh,
                'y1':self.y,
                'y2':self.y + self.wh}
    
    def print_xy(self):
        print(f"x:{self.x}, y:{self.y}, dx:{self.dx}, dy:{self.dy}")

class Control(metaclass=abc.ABCMeta):# プレイヤーの操作方法の定義(抽象クラス)
    @abc.abstractmethod
    def direction(self):# 移動
        pass
    @abc.abstractmethod
    def draw(self,surface,image):# 描画メソッド
        pass

class Android(MyObject, Control):# 主人公
    def __init__(self,x,y,wh,w,h,name):
        super(Android, self).__init__(x,y,wh,w,h,name)
    
    def direction(self,d):
        if d == "LEFT":
            self.dx = -self.wh/3
        if d == "RIGHT":
            self.dx = self.wh/3
        if d == "UP" and self.y == self.h-self.wh:# jump
            self.t_jump=0
            self.dy = -self.wh*1.1
            self.t_jump=0
        if d == "DOWN":
            self.dy = self.wh
        self.t_move=0
    
    def draw(self, surface, image, mode):
        # 矩形を描画 pygame.draw.rect(Surface, color, Rect, width=0)
        if mode==0 or mode == 2:
            pygame.draw.rect(surface, (0, 0, 255), (self.x, self.y, self.wh, self.wh))
        if mode==1 or mode == 2:
            surface.blit(image, (self.x-22,self.y-10))

class Tux(MyObject, Control):# ボス
    def __init__(self,x,y,wh,w,h,name):
        super(Tux,self).__init__(x,y,wh,w,h,name)
        self.GRAVITY=0.5 # 重力
        self.t=0
    
    def make_fire(self, x):
        if self.t%20==0:
            # アップルを生成
            if self.x < x:
                return Apple(self.x+self.wh,self.y,40,self.w, self.h,'fire'+str(self.t),'R')
            else:
                return Apple(self.x,self.y,40,self.w, self.h,'fire'+str(self.t),'L')
        else:
            return []
    
    def direction(self):
        self.t+=1
        if self.t%50==0:
            if random.random()>0.5:
                self.dx = self.wh/3
            else:
                self.dx = -self.wh/3
        if self.y == self.h-self.wh and self.t%145==0:
            self.dy = -self.wh/2
            self.t_jump=0
        self.t_move=0
    
    def draw(self, surface, image, mode):
        if mode==0 or mode == 2:
            pygame.draw.rect(surface, (0, 0, 255), (self.x, self.y, self.wh, self.wh))
        if mode==1 or mode == 2:
            surface.blit(image, (self.x-40,self.y-12))

class Apple(MyObject, Control):
    def __init__(self,x,y,wh,w,h,name, direction):
        super(Apple,self).__init__(x,y,wh,w,h,name)
        self.direct=direction
        self.rand_speed = random.random()
    def move(self):
        self.x += self.dx; self.y += self.dy# 移動
    
    def collision_area(self):
        pass
    
    def direction(self):
        if self.direct=='R':
            self.dx=self.wh*self.rand_speed
        if self.direct=='L':
            self.dx=-self.wh*1.5
        
    def draw(self, surface, image, mode):
        if mode==0 or mode == 2:
            pygame.draw.rect(surface, (0, 0, 255), (self.x, self.y, self.wh, self.wh))
        if mode==1 or mode == 2:
            surface.blit(image, (self.x-22,self.y-7))

class Android2(MyObject, Control):
    def __init__(self,x,y,wh,w,h,name):
        super(Android2,self).__init__(x,y,wh,w,h,name)
    def move(self):
        self.x += self.dx; self.y += self.dy# 移動
    
    def collision_area(self):
        pass
    
    def direction(self):
        self.dx = 0; self.dy = 0
        
    def draw(self, surface, image, mode):
        if mode==0 or mode == 2:
            pygame.draw.rect(surface, (0, 0, 255), (self.x, self.y, self.wh, self.wh))
        if mode==1 or mode == 2:
            surface.blit(image, (self.x-22,self.y-10))

def main():
    my_func.create_tux(24)# 画像生成
    my_func.create_android(14)
    my_func.create_apple(14)
    
    draw_mode = 1 #描画モード
    width_stage = 600; height_stage = 400# area
    pygame.init()
    pygame.display.set_mode((width_stage, height_stage))# 画面設定
    pygame.display.set_caption("タックス vs ドロイド君")#タイトル
    surface = pygame.display.get_surface()
    
    image_android = pygame.image.load("./android1.png")
    image_apple = pygame.image.load("./apple.png")
    image_tux = pygame.image.load("./tux.png")
    image_android2 = pygame.image.load("./android2.png")
    state = 0
    
    while(True):
        pygame.time.delay(60)
        if state == 0 or state == 2 or state == 3:# state:{0:ゲームスタート}, {1:ゲーム進行中}, {2:ゲームオーバー}
            if state==0:
                dispmessage(surface, "Hit space Key", 120, (255,0,0))
                dispmessage(surface, "Doroid vs Tux", 190, (255,0,0))
            elif state==2:
                dispmessage(surface, "Game Over", 120, (255,255,255))
                dispmessage(surface, "[r]:Retry [Esc]:Quit", 190, (255,255,255))
            elif state == 3:
                dispmessage(surface, "GAME CLEAR!", 120, (218,179,0))
                dispmessage(surface, "[r]:Retry [Esc]:Quit", 190, (218,179,0))
            for event in pygame.event.get():
                if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                if event.type == KEYDOWN:
                    # スペースキーでスタート
                    if event.key == K_r or event.key == K_SPACE and state == 0:
                        state = 1
                        android = Android(450,150,40,width_stage,height_stage,'android')# player1
                        tux = Tux(100,100,70,width_stage,height_stage, 'tux')# player2
                        android2 = Android2(10,360,40,width_stage,height_stage, 'android2')
                        obgect_list = [android, tux, android2]
                    if event.key == K_ESCAPE:
                        print('quit')
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
            continue
        
        surface.fill((0,0,0))# 画面初期化
        # HELP ME 出力
        sysfont = pygame.font.SysFont(None, 20)
        message = sysfont.render('HELP ME', True, (255,255,255))
        message_rect = message.get_rect()
        message_rect.center = (33,350)
        surface.blit(message, message_rect)
        # リンゴを削除
        NewObject_list=[]
        for p in obgect_list:
            if p.name=='android' or\
                p.name=='tux' or\
                p.name=='android2' or\
                p.name[0:4]=='fire' and (p.x < width_stage and p.x > 0):
                NewObject_list.append(p)
        obgect_list=NewObject_list
        # ファイア追加
        fire = tux.make_fire(android.x)
        if fire==[]:
            pass
        else:
            obgect_list.append(fire)
        # プレイヤー描画
        for p in obgect_list[::-1]:
            if p.name=='android':
                p.draw(surface, image_android, draw_mode)
            elif p.name[0:4]=='fire':
                p.draw(surface, image_apple, draw_mode)
            elif p.name=='tux':
                p.draw(surface, image_tux, draw_mode)
            elif p.name=='android2':
                p.draw(surface, image_android2, draw_mode)
        pygame.display.update()
        # ----ボタン処理----
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
                
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key == K_SPACE:
                    android.direction("UP")
                # 矢印キーなら中心座標を矢印の方向に移動
        #ボタン長押し処理
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_LEFT]:
            android.direction("LEFT")
        if pressed_key[K_RIGHT]:
            android.direction("RIGHT")
        #-----------------
        # 他のプレイヤーの方向を決める
        for p in obgect_list[1:]:
            p.direction()
        
        # 敵と衝突判定
        xy_player = android.xy_body()
        for enemy in list(set(obgect_list)^set([android])^set([android2])):
            xy_enemy = enemy.xy_body()
            if xy_player['x2'] >= xy_enemy['x1']\
                and xy_player['x1'] <= xy_enemy['x2']\
                and xy_player['y2'] >= xy_enemy['y1']\
                and xy_player['y1'] <= xy_enemy['y2']:
                state = 2
        # クリア判定
        #if int(xy_player['x2']) <= 16 and int(xy_player['y2']) == 300:
        #    print('clear!')
        
        if xy_player['x2'] >= android2.xy_body()['x1']\
                and xy_player['x1'] <= android2.xy_body()['x2']\
                and xy_player['y2'] >= android2.xy_body()['y1']\
                and xy_player['y1'] <= android2.xy_body()['y2']:
                state = 3
        # プレイヤーの移動と衝突処理
        for p in obgect_list:
            p.move()
        for p in obgect_list:
            p.collision_area()

if __name__ == "__main__":
    main()  