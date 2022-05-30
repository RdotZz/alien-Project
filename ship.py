import pygame

class Ship:
    """管理飞船的类"""

    def __init__(self,ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #加载飞船图像
        self.image = pygame.image.load('image/ship.bmp')
        self.rect = self.image.get_rect()

        #对于每艘新飞船都将他放到屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        #在飞船的属性X中存储小数值
        self.x = float(self.rect.x)

        #标志移动
        self.moving_right = False
        self.moving_left = False
        # self.moving_up = False
        # self.moving_down = False
    
    def update(self):
        """根据移动标志调整飞船的位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # if self.moving_up:
        #     self.rect.y += 1
        # if self.moving_down:
        #     self.rect.y -= 1

        
        self.rect.x = self.x
        
    
    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)
    
    
