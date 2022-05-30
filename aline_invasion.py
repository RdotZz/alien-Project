import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_hight))
        pygame.display.set_caption("Alien Invasion")
       
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            #监视鼠标和键盘事件
            self._check_evnets()
            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
            #更新屏幕图像
            self._update_aliens()
            self._update_screen()

            
    def _check_evnets(self):
        """响应案件和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            
                
    def _check_keydown_events(self,event):
        """响应按键"""         
        if event.key == pygame.K_RIGHT:
            #向右移动飞船
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            #向左移动飞船
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):

        self.bullets.update()

        for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0 :
                    self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self):
        #检查是否有子弹击中外星人
        #如果有，就删除对应的子弹和外星人
        collections = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        #刷新外星人
        if not self.aliens:
            #删除现有的子弹并兴建一群外星人
            self.bullets.empty()
            self._create_fleet()

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien) 

    def _create_fleet(self):
        """创建外星人群"""
        alien = Alien(self)
        alien_width, alien_height= alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_hight - 
                                    (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        
        #创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        #检查是否有外星人撞到飞船
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        
        #检查是否有外星人到达屏幕底端
        self._check_aliens_bottom()
    
    def _check_fleet_edges(self):
        """有外星人到达屏幕边缘时采取措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """将整个外星人下移动，并且改变方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip()

    

    def _ship_hit(self):
        """响应飞船被外星人撞击"""
        
        if self.stats.ships_left > 0:
            #ships_lefts -1 
            self.stats.ships_left -= 1

            #清空余下外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            #创建一群新的外星人，并将飞船放到屏幕底端中央
            self._create_fleet()
            self.ship.center_ship()

            #暂停0.5s
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕底端"""
        screen_rect = self.screen.get_rect()
        for aliens in self.aliens.sprites():
            if aliens.rect.bottom >= screen_rect.bottom:
                #像飞船被撞到一样处理
                self._ship_hit()
                break
    
        
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()